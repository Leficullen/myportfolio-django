from django.shortcuts import render

import os
import requests
from datetime import datetime, timedelta, timezone
from django.http import JsonResponse

from main.models import Experience
from main.models import Project
from main.static_datas import ICON_PATHS, TECH_STACKS

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
    context = {
        "name": "Muh. Alfi Rizqy",
        "project_list": Project.objects.all(),
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

# Create your views here.
