# MAKE SURE TO ADD TO README THAT THEY NEED TO RUN THIS!!!!

from django.core.management.base import BaseCommand
from myRoom import webscraper, models
from myRoom.models import Building, Room


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("This will take 5 minutes. Wait until you receive an 'all done!' message. Thank you for your patience.")

        #delete current building and room objects to avoid repeats
        Building.objects.all().delete()
        Room.objects.all().delete()

        #populate building database
        building_list = webscraper.get_buildings()
        for list_item in building_list:
            Building.objects.create(title = list_item)

        #populate rooms database
        room_list = webscraper.get_rooms()
        for room in room_list:
            seperator = room.find("?") # the ? separates building name and room number
            building_name = room[:seperator]
            room_number = room[seperator+1:]
            building_obj = Building.objects.get(title=building_name)
            room_title = building_name + " " + room_number
            Room.objects.create(title = room_title, building = building_obj, roomNum = room_number)

        print("All done!")