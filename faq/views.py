from django.shortcuts import render
from .models import Faq
# Create your views here.


def faq(request):
    """
    View function to render the FAQ page.
    """
    faqs = Faq.objects.all()
    context = {
        'faqs': faqs,
    }
    return render(request, 'faq/faq.html', context)
