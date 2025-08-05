from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect  # If we can't find the object in db queries the system should automaticly response with 404 error.
from . models import  Topic, Entry, User
from . forms import EntryForm, TopicAndEntryForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count


# Create your views here.
def home(request):
    # View function for homepage.
    # It fetches all topics and sends them to template.

    #Order topics by creation date in descending order.
    topics = Topic.objects.annotate(entry_count=Count('entry')).order_by('-created_at')
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


def user_profile(request, user_id):
    """
    View function for displaying a user's profile and their entries.
    """
    target_user = get_object_or_404(User, id=user_id)
    user_entries = Entry.objects.filter(author=target_user).order_by('-created_at')

    context = {
        'target_user': target_user,
        'user_entries': user_entries,
    }
    return render(request, 'main/user_profile.html', context)


@login_required
def edit_entry(request, entry_id):
    """
    View function for editing an existing entry.
    """
    entry = get_object_or_404(Entry, id=entry_id)

    # Ensure that only the author of the entry can edit it
    if entry.author != request.user:
        return redirect('topic_detail', topic_id=entry.topic.id)

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', topic_id=entry.topic.id)
    else:
        form = EntryForm(instance=entry)

    context = {'form': form, 'entry': entry}
    return render(request, 'main/edit_entry.html', context)


@login_required
def delete_entry(request, entry_id):

    # View function for deleting an entry.

    entry = get_object_or_404(Entry, id=entry_id)

    # Ensure that only the author of the entry can delete it
    if entry.author == request.user:
        topic_id = entry.topic.id
        entry.delete()
        return redirect('topic_detail', topic_id=topic_id)

    # Redirect back to the topic if the user is not the author
    return redirect('topic_detail', topic_id=entry.topic.id)
