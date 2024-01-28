from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse

class searchForm(forms.Form):
    text_field = forms.CharField(label='', widget = forms.TextInput(attrs={
    'placeholder': 'Search Wiki', 
    'style': 'width 100%'
    }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": searchForm()
    })

def entry(request, title):
    entry_md = util.get_entry(title)
    entry_HTML = Markdown().convert(entry_md)
    return render(request, "encyclopedia/entry.html", {
        "entries": util.list_entries(),
        'entry': entry_HTML,
        'title': title,
        'form': searchForm()
    })

def search(request):
    if request.method == 'POST':
        entries_found = []
        entries_all = util.list_entries()
        form = searchForm(request.POST)
        if form.is_valid():
            text_field = form.cleaned_data['text_field']
            for entry in entries_all:
                if text_field.lower() == entry.lower():
                    title = entry
                    entry = util.get_entry(title)
                    return HttpResponseRedirect(reverse('entry', args=[title]))
                if text_field.lower() in entry.lower():
                    entries_found.append(entry)
            return render(request, 'encyclopedia/search.html', {
                'results': entries_found,
                'text_field': text_field,
                'form': searchForm()
            })
    return render(request, 'encyclopedia/search.html', {
        'text_field': '',
        "form": SearchForm()
    })
