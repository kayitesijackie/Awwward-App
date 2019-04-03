from rest_framework import serializers
from .models import UserProfile,Project


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user','bio','profile_pic','projects')

