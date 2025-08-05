from django import forms
from .models import Entry

from main.models import Topic


class EntryForm(forms.ModelForm): # Changed to forms.ModelForm

    # A form for creating and editing an entry.

    class Meta:
        model = Entry
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class TopicAndEntryForm(forms.Form):
    # A form for creating a new topic along with its first entry.

    title = forms.CharField(max_length=50, label='Title')
    content = forms.CharField(widget=forms.Textarea(), label='Content')