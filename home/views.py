from django.shortcuts import render


def index(request):
    """View function for the home page of the site."""
    return render(request, 'home/index.html')


def about(request):
    """View function for the about page of the site."""
    return render(request, 'home/about.html')
