from django.conf.urls import url
from . import views

app_name = 'movies'

urlpatterns = [
    url(r'^$', views.MovieList.as_view(), name='all'),
    url(r'new/$',views.CreateMovie.as_view(), name='create'),
    url(r'by/(?P<username>[-\w]+)/$', views.UserMovies.as_view(), name='for_user'),
    url(r'by/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.MovieDetail.as_view(), name='single'),
    url(r'delete/(?P<pk>\d+)/$', views.DeleteMovie.as_view(), name='delete'),
]
