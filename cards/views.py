from django.shortcuts import render
from django.core.paginator import Paginator
import json
from pathlib import Path


def index(request):
    with open(Path("jobs.json"), encoding="utf-8") as f:
        jobs = json.load(f)

    paginator = Paginator(jobs, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "cards/index.html", {
        "jobs": page_obj.object_list,
        "page_obj": page_obj
    })