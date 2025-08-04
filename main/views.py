from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect  # If we can't find the object in db queries the system should automaticly response with 404 error.
from django.http import HttpResponse
from . models import  Topic, Entry, User
from . forms import EntryForm, TopicAndEntryForm
from django.contrib.auth.forms import UserCreationForm



# Create your views here.
def home(request):
    # View function for homepage.
    # It fetches all topics and sends them to template.

    #Order topics by creation date in descending order.
    topics = Topic.objects.order_by('-created_at')
    context = {'topics': topics}
    return render(request, 'main/home.html', context)

@login_required
def topic_detail(request, topic_id):
    # View function for a specific topic's detail page.
    # It fetches the topic and all associated entries.

    # Use get_object_or_404 to handle non-existent topics
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            #Get user or create a new one if not exists
            user = request.user # Use the logged-in user

            #Create the new entry
            Entry.objects.create(
                topic = topic,
                author = user,
                content = form.cleaned_data['content'],
            )
            # Redirect to the same page to show the new entry
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = EntryForm() # An empty form for GET requests

    entries = topic.entry_set.order_by('-created_at')
    context = {'topic': topic, 'entries': entries, 'form': form}
    return render(request, 'main/topic_detail.html', context)

    #Get all entries for the specific topic, ordered by creation date
    entries = topic.entries.order_by('-created_at')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'main/topic_detail.html', context)

@login_required # Protects this view, user must be logged in to access.
def create_topic_with_entry(request):
    #View function to create a new topic and entry
    if request.method == 'POST':
        form = TopicAndEntryForm(request.POST)
        if form.is_valid():
            #Get the logged-in user directly from the request.
            user = request.user

            #Create a new topic
            topic = Topic.objects.create(
                title = form.cleaned_data['title'],
                created_by = user
            )

            #Create the first entry for the new topic
            Entry.objects.create(
                topic = topic,
                author = user,
                content = form.cleaned_data['content'],
            )

            #Redirect to the new topic's detail page.
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = TopicAndEntryForm()
    return render(request, 'main/create_topic.html', {'form': form})

def register(request):
    # View function for user registration
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') # Redirect to the home page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

