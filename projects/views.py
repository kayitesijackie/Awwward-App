from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Max,F
from .models import UserProfile,Project
from .forms import NewProjectForm,VoteForm,ProfileEditForm
from django.urls import reverse
from django.http  import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectSerializer



# Create your views here.
def index(request):
    projects = Project.objects.all()
    return render(request,'index.html',{'projects':projects})


@login_required(login_url='/accounts/login/')
def profile(request):
    profile = UserProfile.objects.filter(user = request.user).first()
    projects = Project.objects.filter(user=profile.user).all()

    if request.method == 'POST':
        form = ProfileEditForm(request.POST,instance=profile,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))
    else:
        form = ProfileEditForm(instance=profile)

    context = {
        'profile':profile,
        'projects':projects,
        'form':form,
    }
    return render(request,'profile.html',context)



