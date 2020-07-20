from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.shortcuts import redirect
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def search(request):
    data = request.POST.copy()
    search = data.get('q')
    entry_list = util.list_entries()
    answer = ""
    matching_list = []
    for li in entry_list:
        if li.casefold() == search.casefold():
            answer = li
            return redirect("/wiki/" + answer)
            break
        if search.casefold() in li.casefold():
            matching_list.append(li)
    return render(request, "encyclopedia/search.html", {
        "entries": matching_list
    })


def entry(request, entry):
    entry_list = util.list_entries()
    found = False
    for li in entry_list:
        if li.casefold() == entry.casefold():
            answer = li
            found = True
            break
    if found is False:
        message = "Sorry, Page not found."
        return render(request, "encyclopedia/error.html", {
            "message": message
        })
    return render(request, "encyclopedia/entry.html", {
        "title": answer,
        "entry": Markdown().convert(util.get_entry(answer))
    })


def newpage(request):
    if request.method == "POST":
        data = request.POST.copy()
        title = data.get('title')
        body = data.get('body')
        entry_list = util.list_entries()
        body = title + "\n" + body
        title = title.replace("#", "")
        title = title.strip()
        title = title.replace(" ", "_")
        for li in entry_list:
            if title.casefold() == li.casefold():
                message = "Sorry, Title already taken."
                return render(request, "encyclopedia/error.html", {
                    "message": message
                })
        util.save_entry(title, body)
        return redirect("/wiki/" + title)
    return render(request, "encyclopedia/newpage.html")


def edit(request, title):
    if request.method == "POST":
        data = request.POST.copy()
        body = data.get('body')
        entry_list = util.list_entries()
        util.save_entry(title, body)
        return redirect("/wiki/" + title)
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "entry": util.get_entry(title)
        })


def randomize(request):
    entries = util.list_entries()
    choice = random.choice(entries)
    return redirect("/wiki/" + choice)


def error(request):
    return render(request, "encyclopedia/error.html")
