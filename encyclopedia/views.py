from django.shortcuts import render
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

