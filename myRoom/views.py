from contextlib import nullcontext

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse

from .forms import RegistrationForm, ReviewForm, ImageForm, ProfilePictureForm
from .models import Review, Room, Photo, Building, Profile, Tag
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializer import ReviewSerializer, RoomSerializer, BuildingSerializer, SearchBuildingSearializer, SearchRoomSearializer
from django.http import JsonResponse
import json

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            profile = Profile.objects.create(user=user)
            login(request, user)
            return redirect("/")
    else:
        form = RegistrationForm()

    return render(request, 'users/signup.html', {'form': form})
def myLogin(request):
    if(request.user.is_authenticated):
        return redirect("/")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def index(request):
    review_form = ReviewForm
    return render(request, 'index.html', {'review_form': review_form})


@login_required
def userLogout(request):
    logout(request)
    return redirect('/')

def rooms(request, id):
    review_form = ReviewForm
    room = get_object_or_404(Room, id=id)
    reviews = room.reviews.all()
    #photos = Photo.objects.all()
    tags = Tag.objects.all()
    average = room.average_rating()
    return render(request, 'rooms.html', {'room' : room, 'reviews': reviews, 'tags': tags,
                                          'average' : average, 'review_form': review_form})

def buildings(request, id):
    review_form = ReviewForm
    building = get_object_or_404(Building, id=id)
    reviews = building.reviews.all()
    tags = Tag.objects.all()
    average = building.average_rating()
    rooms = Room.objects.filter(building=building)
    return render(request, 'building.html', {'building' : building, 'reviews': reviews,
                                             'tags': tags, 'average' : average, 'rooms' : rooms, 'review_form': review_form})

def results(request):
    review_form = ReviewForm
    if request.method == "POST":
        searched = request.POST['searched']
        room_results = Room.objects.filter(title__icontains=searched)
        for room in room_results:
            room.type = 'room'

        building_results = Building.objects.filter(title__icontains=searched)
        for building in building_results:
            building.type = 'building'

        search_results = list(room_results) + list(building_results)
        return render(request, 'results.html', {'searched': searched,
                                                'search_results': search_results,'review_form': review_form})
    else:
        return render(request, 'results.html')

@login_required
def profile(request):
    form = ProfilePictureForm()
    return render(request, 'profile.html', {
        'PFPform': form
    })
@login_required
def changePFP(request):
    profile = get_object_or_404(Profile, user=request.user)

    form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('profile')

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    # Custom action to retrieve reviews for a specific room
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        room = self.get_object()
        reviews = room.reviews.all() # Get all reviews linked to this room
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    # Custom action to retrieve reviews for a specific building
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        building = self.get_object()
        reviews = building.reviews.all()  # Get all reviews linked to rooms in this building
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class AllBuildingAndRooms(viewsets.ViewSet):
    def list(self, request):
        Rooms = Room.objects.all()
        Buildings = Building.objects.all()

        Rooms_Serialized = SearchRoomSearializer(Rooms, many=True).data
        Buildings_Serialized = SearchBuildingSearializer(Buildings, many=True).data

        return Response({
            'Rooms': Rooms_Serialized,
            'Buildings': Buildings_Serialized
        })
class UserReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Review.objects.filter(user = self.request.user)

"""def review_page(request):
    review_form = ReviewForm
    image_form = ImageForm
    reviews = Review.objects.all()
    photos = Photo.objects.all()
    return render(request, 'reviews.html',
                  {'review_form': review_form, 'reviews': reviews,
                   'image_form': image_form, 'photos': photos})"""
def add_review(request):

    if request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        photos = request.FILES.getlist('photos')

        if review_form.is_valid():

            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            review_form.save_m2m()

            if request.POST.get('room'):
                room_id = review.room.id
            for photo in photos:
                Photo.objects.create(image=photo, report=review)
            return redirect('room', room_id)
 
            review.save()
            room_id = review.room.id
            for photo in photos:
                Photo.objects.create(image=photo, report=review)


            return redirect('room', room_id)

    else:
        return redirect('login')

def get_rooms(request):
    data = json.loads(request.body)
    building_id = data["id"]
    roomlist = Room.objects.filter(building__id=building_id)
    return JsonResponse(list(roomlist.values("id", "roomNum")), safe=False)
