from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    # View function for homepage.
    # It will diplay a list of all topics
    return render(request, 'main/home.html')

def topic_detail(request, topic_id):
    # View function for a specific topic's detail page.
    # It will display all entries under that topic
    return render(request, 'main/topic_detail.html') # For now, we will just render the template without any context.

