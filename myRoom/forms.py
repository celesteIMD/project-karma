from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Building, Room, Photo, Review, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['building', 'room', 'userReview', 'rating', 'tags']
        labels = {
            'userReview': 'Review',
            'building': 'Building',
            'room': 'Room',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.none()

        if 'building' in self.data:
            try:
                building_id = int(self.data.get('building'))
                self.fields['room'].queryset = Room.objects.filter(building__id=building_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['room'].queryset = self.instance.building.room_set.order_by('building')

    """def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].validators.append(MinValueValidator(1))

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['rating'].validators.append(MaxValueValidator(5))"""

class ImageForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
          
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        """
        If you want to customize the labels I found this online.
        labels = {
            'username': 'Custom Username Label',
            'password1': 'Custom Password Label',
            'password2': 'Confirm Password',
        }
        help_texts = {
            'username': 'Enter your desired username (letters, numbers, and @/./+/-/_ only).',
            'password1': 'Choose a strong password with at least 8 characters.',
            'password2': 'Re-enter your password for verification.',
        }
        error_messages = {
            'username': {
                'unique': "This username is already taken. Please choose another.",
            },
            'password1': {
                'password_too_common': "Your password is too common. Choose something stronger.",
            },
        }
        """