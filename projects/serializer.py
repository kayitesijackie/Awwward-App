from rest_framework import serializers
from .models import UserProfile,Project


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user','bio','profile_pic','projects')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('project_title','project_description','landing_page','live_site','design','usability','content')
