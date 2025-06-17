from rest_framework import serializers
from .models import Room, Review, Building, Tag, Photo


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    building = BuildingSerializer()

    class Meta:
        model = Room
        fields = '__all__'
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id','image']
class ReviewSerializer(serializers.ModelSerializer):
    building = BuildingSerializer()
    room = RoomSerializer()
    tags = TagsSerializer(many=True)
    user = serializers.CharField(source='user.username')
    photos = PhotoSerializer(many=True)
    class Meta:
        model = Review
        fields = '__all__'


class SearchBuildingSearializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['id', 'title']
class SearchRoomSearializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'title']


