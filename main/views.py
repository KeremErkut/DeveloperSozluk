from django.shortcuts import render, get_object_or_404, \
    redirect  # If we can't find the object in db queries the system should automaticly response with 404 error.
from django.http import HttpResponse
from . models import  Topic, Entry, User
from . forms import EntryForm


# Create your views here.
def home(request):
    # View function for homepage.
    # It fetches all topics and sends them to template.

    #Order topics by creation date in descending order.
    topics = Topic.objects.order_by('-created_at')
    context = {'topics': topics}
    return render(request, 'main/home.html', context)

def topic_detail(request, topic_id):
    # View function for a specific topic's detail page.
    # It fetches the topic and all associated entries.

    # Use get_object_or_404 to handle non-existent topics
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            #Get user or create a new one if not exists
            user, created = User.objects.get_or_create(username=form.cleaned_data['username'])

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

