from django.shortcuts import render
from django.http import HttpResponseNotFound

from . import util

from markdown2 import markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show_wiki(request,title):
    entry = util.get_entry(title)
    if(entry):
        return render(request,"encyclopedia/entry.html",{
            "entry":markdown(entry),
            "title":title
            })
    return HttpResponseNotFound('<h1>Page Not Found </h1>')