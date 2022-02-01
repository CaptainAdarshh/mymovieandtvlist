from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404
from django.contrib import messages

from braces.views import SelectRelatedMixin

from . import models
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class MovieList(SelectRelatedMixin,generic.ListView):
    model = models.Movie
    select_related = ('user', 'category')

class UserMovies(generic.ListView):
    model = models.Movie
    template_name = 'movies/user_movie_list.html'

    def get_queryset(self):
        try:
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

        except User.DoesNotExist:
            raise Http404
        else:
            return self.movie_user.movies.all()
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_user'] = self.movie_user
        return context

class MovieDetail(SelectRelatedMixin ,generic.DetailView):
    model = models.Movie
    select_related = ('user','category')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreateMovie(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ('name','category','release')
    model = models.Movie

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeleteMovie(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Movie
    select_related = ('user', 'category')
    success_url = reverse_lazy('movies:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)
    
    def delete(self, *args, **kwargs):
        messages.success(self.request,'Movie Deleted')
        return super().delete(*args, **kwargs)