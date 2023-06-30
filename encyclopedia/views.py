from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from . import util
from random import randint
from markdown2 import markdown

class NewPageForm(forms.Form):
    pageName = forms.CharField(
        label='Title',
        widget=forms.TextInput(
            attrs={
                'name': 'title', 
                'id':'pageTitle',
                'placeholder': 'Enter a title for the page',
                'class': 'form-field'}))
    
    pageContent = forms.CharField(
        label='Content',
        widget=forms.Textarea(
            attrs={
                'name': 'content', 
                'placeholder': 'Enter a content for the page', 
                'class': 'form-field',
                'rows': '3', 
                'cols': '5'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    content = util.get_entry(title)
    if content is None:
        content = "##Entry not found"

    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title" : title, "content" : content
    })

def search(request):
    q = request.POST.get('q')
    if q in util.list_entries():
        return redirect("encyclopedia:title", title=q)
    return render(request, "encyclopedia/search.html", {"results": util.search(q), "q": q})

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            pageName = form.cleaned_data['pageName']
            pageContent = form.cleaned_data['pageContent']
            if pageName in util.list_entries():
                pageContent = "##Title already exist. Try another one"
                pageContent = markdown(pageContent)
                return render(request, "encyclopedia/entry.html", {"title": pageName, "content": pageContent})
            util.save_entry(pageName, pageContent)
            return redirect("encyclopedia:title", title=pageName)
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form" : form
            })
        
    return render(request, "encyclopedia/newpage.html", {
        "form" : NewPageForm()
    })

def editpage(request, entry):
    content = util.get_entry(entry)
    if content:
        return render(request, "encyclopedia/editpage.html",{
        "title": entry,
        "content" : util.get_entry(entry)
    })
    else:
        return HttpResponseRedirect(reverse('encyclopedia:index'))
    
def savepage(request, entry):
    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(entry, new_content)
        return redirect("encyclopedia:title", entry)


def random(request):
    entries = util.list_entries()
    entry = entries[randint(0, len(entries)-1)]
    return redirect("encyclopedia:title", title=entry)


