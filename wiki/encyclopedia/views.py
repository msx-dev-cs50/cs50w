from django.shortcuts import render
from django import forms

from . import util

class NewSearchForm(forms.Form):
    searchTitle = forms.CharField(label="Search ...")


allTitles = util.list_entries()

def index(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        
        if form.is_valid():
            similarResults=[]
            searchEntry = form.cleaned_data["searchTitle"]

            titles = [title.lower() for title in allTitles]
            searchEntry = searchEntry.lower()
            

            if searchEntry in titles:
                requested_page = util.get_entry(searchEntry)
                print(requested_page)
                return render(request, "encyclopedia/entry.html", {
                    "page": requested_page,
                    "form": NewSearchForm()
                })
            else:
                for title in titles:
                    title = title.lower()
                    if searchEntry in title:
                        similarResults.append(title)
                    
                
                if not similarResults:
                    return render(request, "encyclopedia/oops.html", {
                        "message": "Oops, looks like no entries match!",
                        "form": NewSearchForm()
                    })
                else:
                    return render(request, "encyclopedia/searchResults.html", {
                        "results": similarResults,
                        "form": NewSearchForm()
                    })


    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": NewSearchForm()
        })

def entry(request, entry):
    requested_page = util.get_entry(entry)

    if requested_page != None:
        return render(request, "encyclopedia/entry.html", {
            "page": requested_page, 
            "form": NewSearchForm()
        })
    else:
        return render(request, "encyclopedia/oops.html", {
            "message": "Oops, this entry does not exist!",
            "form": NewSearchForm()
        })