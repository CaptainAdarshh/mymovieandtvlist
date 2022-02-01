from django.conf.urls import url
from . import views

app_name = 'categories'

urlpatterns = [
    url(r'of/(?P<username>[-\w]+)', views.ListCategory.as_view(),name='all'),
    url(r'movies/in/(?P<slug>[-\w]+)/$',views.SingleCategory.as_view(),name='single'),
]