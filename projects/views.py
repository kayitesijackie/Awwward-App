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



@login_required(login_url='/accounts/login/')
def submit_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST,request.FILES)

        if form.is_valid():
            project = Project(project_title=request.POST['project_title'],landing_page=request.FILES['landing_page'],project_description=request.POST['project_description'],live_site=request.POST['live_site'],user=request.user)
            project.save()
            return redirect(reverse('index'))
    else:
        form = NewProjectForm()

    return render(request,'submit_project.html',{'form':form})


def search_project(request):
    try:
        if 'project' in request.GET and request.GET['project']:
            searched_term = (request.GET.get('project')).title()
            searched_project = Project.objects.get(project_title__icontains = searched_term.title())
            return render(request,'search.html',{'project':searched_project})
    except (ValueError,Project.DoesNotExist):
        raise Http404()

    return render(request,'search.html')


@login_required(login_url='/accounts/login/')
def project(request,project_id):
    project = Project.objects.get(id=project_id)
    rating = round(((project.design + project.usability + project.content)/3),2)
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid:
            project.vote_submissions += 1
            if project.design == 0:
                project.design = int(request.POST['design'])
            else:
                project.design = (project.design + int(request.POST['design']))/2
            if project.usability == 0:
                project.usability = int(request.POST['usability'])
            else:
                project.usability = (project.design + int(request.POST['usability']))/2
            if project.content == 0:
                project.content = int(request.POST['content'])
            else:
                project.content = (project.design + int(request.POST['content']))/2
            project.save()
            return redirect(reverse('project',args=[project.id]))
    else:
        form = VoteForm()
    return render(request,'project.html',{'form':form,'project':project,'rating':rating})

class ProfileList(APIView):
    def get(self,request,format=None):
        all_users = UserProfile.objects.all()
        serializers = ProfileSerializer(all_users,many=True)
        return Response(serializers.data)

class ProjectList(APIView):
    def get(self,request,format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects,many=True)
        return Response(serializers.data)
