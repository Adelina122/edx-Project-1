from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from . import util
from markdown2 import markdown

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
    return render(request, "encyclopedia/newpage.html")