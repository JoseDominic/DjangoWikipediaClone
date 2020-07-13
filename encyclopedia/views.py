from django.shortcuts import render
from django.http import HttpResponseNotFound,HttpResponseRedirect
from django import forms
from django.urls import reverse

from . import util

from markdown2 import markdown
import re
import random as rn

class EntryForm(forms.Form):
    title = forms.CharField(label='Title')
    entry = forms.CharField(widget=forms.Textarea)

class EditForm(forms.Form):
    entry = forms.CharField(widget=forms.Textarea)

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

def new(request):
    if request.method=='POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data['entry']
            title = form.cleaned_data['title']
            entries = util.list_entries()
            if title in entries:
                return render(request,'encyclopedia/new.html',{
                    "form":form,
                    "error":'Title already exists!Please give another title!'
                })
            util.save_entry(title,entry)
            return HttpResponseRedirect(reverse('show_wiki',kwargs={"title":title}))
        else:
            return render(request,'encyclopedia/new.html',{
                'form':form
            })
    return render(request,'encyclopedia/new.html',{
        "form":EntryForm()
    })

def edit(request,title):
    if request.method =='POST':
        form = EditForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data['entry']
            util.save_entry(title,entry)
            return HttpResponseRedirect(reverse('show_wiki',kwargs={'title':title}))
        else:
            return render(request,'encyclopedia/edit.html',{
                'title':title,
                'form':form
            })
    entry = util.get_entry(title)
    form = EditForm({"entry":entry})
    return render(request,'encyclopedia/edit.html',{
        'title':title,
        'form':form
    })

#view that returns a random wiki page
def random(request):
    entries = util.list_entries()
    n = rn.randint(0,len(entries)-1)
    title = entries[n]
    return HttpResponseRedirect(reverse('show_wiki',kwargs={'title':title}))
    