from django.shortcuts import render
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.db.models import Count
from categories.models import Category
from movies.models import Movie
from . import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

class SingleCategory(generic.DetailView):
    model = Category


class ListCategory(generic.ListView):
    model = Category
    template_name = 'categories/category_list.html'

    def index(self):
        # self.movie_user = (1,2,3)
        self.movie_user = User.objects.prefetch_related('movies').get(username__iexact=self.kwargs.get('username'))
        self.movie_watched = models.Category.objects.prefetch_related('movies').get(slug__iexact='watched')
        self.movie_watching = models.Category.objects.prefetch_related('movies').get(slug__iexact='watching')
        self.movie_planned = models.Category.objects.prefetch_related('movies').get(slug__iexact='plan-to-watch')
        
        self.watched=0
        for element in self.movie_user.movies.all():
            if element in self.movie_watched.movies.all():
                self.watched+=1
        print(self.watched)
        self.watching=0
        for element in self.movie_user.movies.all():
            if element in self.movie_watching.movies.all():
                self.watching+=1
        print(self.watching)
        self.planned=0
        for element in self.movie_user.movies.all():
            if element in self.movie_planned.movies.all():
                self.planned+=1
        print(self.planned)
        self.all=0
        for element in self.movie_user.movies.all():
            self.all+=1
        print(self.all)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        self.index()
        list2 = [self.watched, self.watching, self.planned,self.all]
        list1 = [0,1,2]
        self.main = list2
        context['movie_user'] = self.main
        return context


