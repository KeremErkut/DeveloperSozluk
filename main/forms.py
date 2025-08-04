from django import forms

from main.models import Topic


class EntryForm(forms.Form):
    # A form for creating a new entry.

    content = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), label='Content')

class TopicAndEntryForm(forms.Form):
    # A form for creating a new topic along with its first entry.

    title = forms.CharField(max_length=50, label='Title')
    content = forms.CharField(widget=forms.Textarea(), label='Content')