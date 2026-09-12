from django.shortcuts import render

import os
import requests
from datetime import datetime, timedelta, timezone

from main.models import Experience
from main.models import Project

def show_main(request):
    github_username = os.getenv("GITHUB_USERNAME", "Leficullen")
    tech_stacks = {
        "right": [
            {"name": "HTML", "img": "/static/logos/html-logo.svg"},
            {"name": "CSS", "img": "/static/logos/css-logo.svg"},
            {"name": "JavaScript", "img": "/static/logos/nodejs-logo.svg"},
            {"name": "TypeScript", "img": "/static/logos/typescript-logo.svg"},
            {"name": "React", "img": "/static/logos/react-logo.svg"},
            {"name": "Next.js", "img": "/static/logos/next-logo.svg"},
            {"name": "Vite", "img": "/static/logos/vite-logo.svg"},
            {"name": "Vue.js", "img": "/static/logos/vuejs-logo.svg"},
            {"name": "Tailwind CSS", "img": "/static/logos/tailwind-logo.svg"},
            {"name": "Figma", "img": "/static/logos/figma-logo.svg"},
            {"name": "Prettier", "img": "/static/logos/prettier-logo.svg"},
            {"name": "VS Code", "img": "/static/logos/vscode-logo.svg"},
            {"name": "GitHub", "img": "/static/logos/github-logo.svg"},
        ],
        "left": [
            {"name": "Git", "img": "/static/logos/git-logo.svg"},
            {"name": "Docker", "img": "/static/logos/docker-logo.svg"},
            {"name": "Ubuntu", "img": "/static/logos/ubuntu-logo.svg"},
            {"name": "Python", "img": "/static/logos/python-logo.svg"},
            {"name": "Java", "img": "/static/logos/java-logo.svg"},
            {"name": "PHP", "img": "/static/logos/php-logo.svg"},
            {"name": "Laravel", "img": "/static/logos/laravel-logo.svg"},
            {"name": "WordPress", "img": "/static/logos/wordpress-logo.svg"},
            {"name": "PostgreSQL", "img": "/static/logos/postgresql-logo.svg"},
            {"name": "MySQL", "img": "/static/logos/myswl-logo.svg"},
            {"name": "Postman", "img": "/static/logos/postman-logo.svg"},
            {"name": "npm", "img": "/static/logos/npm-logo.svg"},
        ],
    }

    context = {
        "name": "Muh. Alfi Rizqy",
        "npm": "2506550721",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "tech_stacks": tech_stacks,
        "github_username": github_username,
        "github_calendar": get_github_contributions(github_username),
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




# Create your views here.
