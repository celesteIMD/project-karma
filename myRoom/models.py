from email.policy import default

from django.db import models
from django.contrib.auth.models import User
from django.db.models import IntegerField, Model, Avg, Count
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  image = models.ImageField(default='default.jpg', upload_to='profile_pics', null='true', blank=True)

class Tag(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

class Building(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=100)
  tags = models.ManyToManyField(Tag, blank=True, related_name='building_tags')
  #average of every review from the building
  def __str__(self):
    return self.title
  def average_rating(self):
    rooms = self.rooms.all()  # Get all rooms in this building
    total_rating = 0
    total_count = 0
    for room in rooms:
      room_rating = room.average_rating() or 0
      total_rating += room_rating * room.reviews.count()
      total_count += room.reviews.count()
    return round(total_rating / total_count, 2) if total_count > 0 else 0

class Room(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=100)
  building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
  tags = models.ManyToManyField(Tag, blank=True, related_name='room_tags')
  roomNum = models.CharField(max_length=100)

  def __str__(self):
    return self.title

  # average of every review from the room
  def average_rating(self):
    if self.reviews.count() > 0:
      return round(self.reviews.aggregate(Avg('rating'))['rating__avg'], 2) or 0

RATING_OPTIONS = (
  (1, "1"),
  (2, "2"),
  (3, "3"),
  (4, "4"),
  (5, "5")
)
class Review(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=100)
  userReview = models.TextField()  # user complaint text
  #rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) # 1-5 star
  rating = models.IntegerField(choices=RATING_OPTIONS, default=1)
  building = models.ForeignKey(Building, on_delete=models.CASCADE,null=True, blank=True, related_name="reviews")
  room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
  tags = models.ManyToManyField(Tag, blank=True, related_name = 'review_tags')
  date = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  #A review can be made on a building or a room
  def clean(self):
    if not self.building and not self.room:
      raise ValidationError('You must select a room or a building before reviewing')

#since we want to have multiple photos per reveiw, it's a seperate class with
#many-to-one relationship to report
class Photo(models.Model):
  id = models.AutoField(primary_key=True)
  image = models.ImageField(null=True, blank= True, upload_to='review_photos')
  report = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='photos')

#functions to update Tags:
def update_room_tags(room):
  top_tags = (
    Tag.objects.filter(review_tags__room=room)
    .annotate(tag_count=Count('review_tags'))
    .order_by('-tag_count')[:5]
  )
  room.tags.set(top_tags)

def update_building_tags(building):
  top_tags = (
    Tag.objects.filter(room_tags__building=building)
    .annotate(tag_count=Count('room_tags'))
    .order_by('-tag_count')[:5]
  )
  building.tags.set(top_tags)

#This function triggers after a review is created, updated or deleted.
@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
#Sender : class that triggered the signal
#Instance: Specific Review object that was saved/deleted
#**kwargs: additional arguments
def update_tags_on_review_change(sender, instance, **kwargs):
    # Update Room Tags if the review is for a room
    if instance.room:
        update_room_tags(instance.room)
        update_building_tags(instance.room.building)

    # Update Building Tags if the review is for a building
    elif instance.building:
        update_building_tags(instance.building)