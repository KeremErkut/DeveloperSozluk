from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect  # If we can't find the object in db queries the system should automaticly response with 404 error.
from . models import  Topic, Entry, User
from . forms import EntryForm, TopicAndEntryForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator


# Create your views here.
def home(request):

    # View function for the homepage, displaying all topics with search and pagination.

    search_query = request.GET.get('q')

    if search_query:
        topics = Topic.objects.filter(title__icontains=search_query).annotate(entry_count=Count('entry')).order_by('-created_at')
    else:
        topics = Topic.objects.annotate(entry_count=Count('entry')).order_by('-created_at')

    # Pagination logic
    paginator = Paginator(topics, 5)  # Show 5 topics per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'search_query': search_query}
    return render(request, 'main/home.html', context)

@login_required
def topic_detail(request, topic_id):
    """
    View function for displaying a topic's entries with pagination.
    """
    topic = get_object_or_404(Topic, id=topic_id)
    all_entries = topic.entry_set.all().order_by('created_at')

    # Pagination logic
    paginator = Paginator(all_entries, 10)  # Show 10 entries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.author = request.user
            new_entry.topic = topic
            new_entry.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = EntryForm()

    context = {
        'topic': topic,
        'page_obj': page_obj,  # Pass the paginated object to the template
        'form': form
    }
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
    user = get_object_or_404(User, id=user_id)
    user_entries = Entry.objects.filter(author=user).order_by('-created_at')[:10]

    # Check if the currently logged-in user is the profile owner
    is_owner = request.user == user

    context = {
        'profile_user': user,
        'user_entries': user_entries,
        'is_owner': is_owner,  # Pass this boolean to the template
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
