from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    content = util.get_entry(entry)

    if not content:
        return render(request, "encyclopedia/error404.html", {
            "title": entry
        })
    
    content = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "content": content
    })


def search(request):
    if request.method == "POST":
        entry = request.POST["q"]
    
        if entry == '':
            HttpResponseRedirect(reverse("index"))

        entries = util.list_entries()

        #finds the exact pages
        for item in entries:
            if entry.lower() == item.lower():
                return HttpResponseRedirect(reverse("entry", args=(item,)))

        #finds possible pages to show
        possible_entries = []
        for item in entries:
            if entry.lower() in item.lower():
                possible_entries.append(item)

        if len(possible_entries) != 0:
            return render(request, "encyclopedia/search.html", {
                "entries": possible_entries
            })
        return HttpResponseRedirect(reverse("entry", args=(entry,)))
        
    else:
        entry = "search"
        return HttpResponseRedirect(reverse("entry", args=(entry,)))    


class AddEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Markdown content of the page")


def add(request):
    if request.method == "POST":
        form = AddEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            entries = util.list_entries()
            # check if title is not in entries
            for entry in entries:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/add.html", {
                        "form": form,
                        "error": "This entry already exists!"
                    })
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=(title,)))

    return render(request, "encyclopedia/add.html", {
        "form": AddEntryForm(),
        "error": ""
    })

from random import choice

def random(request):
    entry = choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", args=(entry,)))


class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Markdown content of the page")


def edit(request, entry):
    if request.method == "POST":
        form = EditEntryForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("entry", args=(entry,)))

        else:
            return render(request, "encyclopedia/edit", {
                "entry": entry,
                "form": form
            })

    form = EditEntryForm()
    form.fields["content"].initial = util.get_entry(entry)

    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "form": form
    })