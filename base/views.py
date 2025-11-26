from django.shortcuts import render



def home(request):
    """
    Home page view - renders the base template with default content
    """
    return render(request, 'base.html')