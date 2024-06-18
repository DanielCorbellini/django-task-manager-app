from django.shortcuts import render
from django.views.generic import TemplateView

def login(TemplateView):
    template_name = 'login.html'
    
def index(request):
    context = {
        'index_text':"Welcome Index Page.",
        }
    return render(request, 'index.html', context)