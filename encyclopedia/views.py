from django.shortcuts import render
from django.http import HttpResponseNotFound,HttpResponseRedirect
from django import forms
from django.urls import reverse

from . import util

from markdown2 import markdown
import re

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title":'Encyclopedia'
    })

def show_wiki(request,title):
    entry = util.get_entry(title)
    if(entry):
        return render(request,"encyclopedia/entry.html",{
            "entry":markdown(entry),
            "title":title
            })
    return HttpResponseNotFound('<h1>Page Not Found </h1>')

def search(request):
    query = request.GET['q']
    entries = util.list_entries()
    #query = query.lower()
    results = []
    for e in entries:
        if (re.search(query,e,re.IGNORECASE)):
            results.append(e)
    if len(results)==1 and results[0]==query:
        return HttpResponseRedirect(reverse('show_wiki',kwargs={'title':query}))
    else:
        return render(request,'encyclopedia/index.html',{
            "heading":'Search Results',
            "entries":results,
            "query":query,
        })

    