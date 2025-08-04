from django import forms

class EntryForm(forms.Form):
    # A form for creating a new entry.

    username = forms.CharField(max_length=50, label='Username')
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), label='Content')