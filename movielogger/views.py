
from pipes import Template
from django.views.generic import TemplateView, ListView
from movies.models import Movie

class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(ListView):
    model = Movie
    template_name = 'index.html'