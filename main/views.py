from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    # View function for homepage.
    # It will diplay a list of all topics
    return HttpResponse("This will be the home page, displaying all topics.")

def topic_detail(request, topic_id):
    # View function for a specific topic's detail page.
    # It will display all entries under that topic
    return HttpResponse(f"This will be the detail page for topic with ID: {topic_id}")

