from django.urls import path, include
from . import views
from .views import get_rooms
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from rest_framework.routers import DefaultRouter

# The router automatically creates URL endpoints for viewsets
router = DefaultRouter()
#The first argument defines the base URL path for that viewset.
#The second argument is the viewset class that handles requests.
router.register(r'rooms', views.RoomViewSet)  # Room endpoints
router.register(r'building', views.BuildingViewSet)
router.register(r'reviews', views.ReviewViewSet)  # Review endpoints
router.register(r'searchData', views.AllBuildingAndRooms, basename='searchData')
router.register(r'userReviews', views.UserReviewViewSet, basename='userReviews')


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.myLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('room/<int:id>', views.rooms, name='room'),
    path('building/<int:id>', views.buildings, name='building'),
    path('results/', views.results, name='results'),
    path('profile/', views.profile, name='profile'),
    path('changePFP/', views.changePFP, name='changePFP'),


    #path('review_page/', views.review_page, name="review_page"),
    path('add_review/', views.add_review, name="add_review"),
   # path('add_image/<int:review_id>/', views.add_image, name="add_image"),

    #API endpoints
    path('api/', include(router.urls)),

    #cascading room selection
    path('building/room/', views.get_rooms, name='get_rooms'),
    ]


