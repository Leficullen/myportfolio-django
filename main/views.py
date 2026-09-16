from django.shortcuts import render

import os
import requests
from datetime import datetime, timedelta, timezone
from django.http import JsonResponse, HttpResponse

from main.models import Experience
from main.models import Project
from main.static_datas import ICON_PATHS, TECH_STACKS

from django.contrib import messages
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import ProjectForm

from django.conf import settings
from django.contrib import messages
from hmac import compare_digest

def show_main(request):
    github_username = os.getenv("GITHUB_USERNAME", "Leficullen")

    context = {
        "name": "Muh. Alfi Rizqy",
        "npm": "2506550721",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "tech_stacks": TECH_STACKS,
        "github_username": github_username,
        "github_calendar": None,
        "icons": ICON_PATHS,
    }

    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name": "Muh. Alfi Rizqy",
        "experience_list": Experience.objects.all(),
    }

    return render(request, "experience.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    # context = {
    #     "name": "Muh. Alfi Rizqy",
    #     "project_list": Project.objects.all(),
    # }
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Lefi",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def get_github_contributions(username):
    token = os.getenv("GITHUB_TOKEN")
    if not token or not username:
        return None

    query = """query($username: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $username) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            colors
            months {
              name
              year
              firstDay
              totalWeeks
            }
            weeks {
              firstDay
              contributionDays {
                date
                weekday
                contributionCount
                color
                contributionLevel
              }
            }
          }
        }
      }
    }"""

    now = datetime.now(timezone.utc)
    one_year_ago = now - timedelta(days=365)

    try:
        response = requests.post(
            "https://api.github.com/graphql",
            json={
                "query": query,
                "variables": {
                    "username": username,
                    "from": one_year_ago.isoformat(),
                    "to": now.isoformat(),
                },
            },
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    except (KeyError, TypeError, requests.RequestException):
        return None

def github_contributions_api(request):
    github_username= os.getenv("GITHUB_USERNAME", "Leficullen")
    github_calendar = get_github_contributions(github_username)

    if not github_calendar:
        return JsonResponse({"error": "Github Contribution data is unavailable"}, status=503)
    return JsonResponse(github_calendar)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if (request.method == "POST"):
        if not has_edit_secret(request):
            messages.error(request, "Kode rahasia salah!")
            return render(request, "projects_form.html", {
                "name": "Lefi",
                "form": form,
            })

        if form.is_valid():
            form.save()
            messages.success(request, "Proyek baru berhasil ditambahkan!")
            return redirect("main:show_projects")

    context = {
        "name": "Lefi",
        "form": form
    }

    return render(request, "projects_form.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        if not has_edit_secret(request):
            messages.error(request, "Kode rahasia salah!")
            return redirect("main:show_projects")

        project.delete()
        messages.success(request, "Project berhasil dihapus")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def has_edit_secret(request):
    expected_secret = settings.PORTFOLIO_EDIT_SECRET

    header_secret = request.headers.get("X-Portfolio-Secret", "")
    form_secret = request.POST.get("edit_secret", "")

    return (
        expected_secret
        and (
            compare_digest(header_secret, expected_secret)
            or compare_digest(form_secret, expected_secret)
        )
    )

# Create your views here.
