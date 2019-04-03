from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'^$',views.index, name='index'),
    url(r'^profile/',views.profile, name='profile'),
    url(r'^new_project/',views.submit_project, name='submit_project'),
    url(r'^search/',views.search_project,name='search_project'),
    url(r'^project/(\d+)',views.project,name='project'),
    url(r'^api/profiles/$',views.ProfileList.as_view(),name='profile_list'),
    url(r'^api/projects/$',views.ProjectList.as_view(),name='project_list'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
