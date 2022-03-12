from django.shortcuts import render
import random

from . import util
from django import forms
from markdown2 import Markdown


class SearchForm(forms.Form):
    searchItem = forms.CharField(label="Search Encyclopedia")

class CreatePage(forms.Form):
    newTitle = forms.CharField(label='')
    newContent = forms.CharField(widget=forms.Textarea, label='')

class EditPage(forms.Form):
    editContent = forms.CharField(widget=forms.Textarea, label='')


markdowner = Markdown()

titles = util.list_entries()


def index(request):
    searched = []
    if request.method == "GET":
        return render(request, "encyclopedia/index.html", {
        "entries": titles,
        "form": SearchForm()
        })
    else:
        form = SearchForm(request.POST)
        if form.is_valid():
            searchItem = form.cleaned_data["searchItem"]

            lowerTitles = titles.copy()
            lowerTitles = [i.lower() for i in lowerTitles]

            if searchItem.lower() in lowerTitles:
                return render(request, "encyclopedia/entry.html", {
                "entryTitle": searchItem,
                "pageContent": markdowner.convert(util.get_entry(searchItem)),
                "form": SearchForm()
                })
            else:
                for i in titles:
                    if searchItem.lower() in i.lower(): 
                    # if i.lower().startswith(searchItem.lower()):
                        searched.append(i)
                if len(searched) == 0:
                    return render(request, "encyclopedia/nonExist.html", {
                        "entryTitle": searchItem,
                        "form": SearchForm()
                        })
            return render(request, "encyclopedia/search.html", {
                "entries": searched,
                "entryTitle": searchItem,
                "form": SearchForm()
                })
        else:
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": SearchForm()
            })

def entry(request, title): 
    entryPage = util.get_entry(title)

    if entryPage is None:
        return render(request, "encyclopedia/nonExist.html", {
            "entryTitle": title,
            "form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entryTitle": title,
            "pageContent": markdowner.convert(entryPage),
            "form": SearchForm()
        })

def newPage(request):
    if request.method == "POST":

        lowerTitles = titles.copy()
        lowerTitles = [i.lower() for i in lowerTitles]

        form = CreatePage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["newTitle"]
            content = form.cleaned_data["newContent"]
            # print(title, content)

            if title.lower() in lowerTitles:
                return render(request, "encyclopedia/error.html", {
                "form": SearchForm()
            })

            util.save_entry(title, content)

            return render(request, "encyclopedia/entry.html", {
                "entryTitle": title,
                "pageContent": markdowner.convert(util.get_entry(title)),
                "form": SearchForm()
                })
    else:

        return render(request, "encyclopedia/newPage.html", {
            "form": SearchForm(),
            "form1": CreatePage()
        })

def edit(request, title):
    entryPage = util.get_entry(title)

    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
        "entryTitle": title,
        "form": SearchForm(),
        "form2": EditPage(initial={'editContent': entryPage})
        })
    else:
        form = EditPage(request.POST)
        if form.is_valid():
            content = form.cleaned_data["editContent"]
            util.save_entry(title, content)

            return render(request, "encyclopedia/entry.html", {
                "entryTitle": title,
                "pageContent": markdowner.convert(util.get_entry(title)),
                "form": SearchForm()
                })

def randomPage(request):
    if request.method == "GET":
        num = random.randint(0, len(titles) - 1)
        page_random = titles[num]

        return render(request, "encyclopedia/entry.html", {
            'form': SearchForm(),
            'pageContent': markdowner.convert(util.get_entry(page_random)),
            'entryTitle': page_random
            })