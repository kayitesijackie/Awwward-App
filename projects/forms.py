from .models import Project,UserProfile
from django.contrib.auth.models import User
from django.forms import ModelForm

class NewProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('project_title','project_description','landing_page','live_site')


