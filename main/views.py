from django.shortcuts import render

import os
import requests
from datetime import datetime, timedelta, timezone
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden

from main.models import Experience
from main.models import Project
from main.static_datas import ICON_PATHS, TECH_STACKS

from django.contrib import messages
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import ProjectForm, ExperienceForm

from django.conf import settings
from django.contrib import messages
from hmac import compare_digest

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

import datetime

from django.views.decorators.http import require_POST


def show_main(request):
    github_username = os.getenv("GITHUB_USERNAME", "Leficullen")
    last_login = request.COOKIES.get("last_login", "Belum ada sesi login / Cookie tidak ditemukan")
    user = request.user

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
        "last_login": last_login,
        "user": user
    }

    return render(request, "index.html", context)

def show_experiences(request):
    title_query = request.GET.get("title", "").strip()
    context = {
        "name": "Muh. Alfi Rizqy",
        "title_query": title_query,
        "is_can_edit" : is_can_edit(request),
        "form": ExperienceForm(),
    }

    return render(request, "experience.html", context)

def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Lefi",
        "title_query": title_query,
        "is_can_edit": is_can_edit(request),
        "form": ProjectForm(),
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


# PROJECTS
def create_project(request):
    if not is_super_user(request):
        return HttpResponseForbidden("Anda tidak berhak membuat project baru!")

    form = ProjectForm(request.POST or None)
    if (request.method == "POST"):
        if not has_edit_secret(request):
            messages.error(request, "Kode rahasia salah!")
            return render(request, "projects_form.html", {
                "name": "Lefi",
                "form": form,
            })

        if form.is_valid() and request.user.is_superuser:
            form.save()
            messages.success(request, "Proyek baru berhasil ditambahkan!")
            return redirect("main:show_projects")

    context = {
        "name": "Lefi",
        "form": form,
        "is_can_edit": True
    }

    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else  False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "image": project.image,
                "url_link": project.url_link,
                "tech_stack": project.tech_stack,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })
    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not is_super_user(request):
        return HttpResponseForbidden("Anda tidak berhak menghapus proyek!")
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        if not has_edit_secret(request):
            messages.error(request, "Kode rahasia salah!")
            return redirect("main:show_projects")

        project.delete()
        messages.success(request, "Project berhasil dihapus")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not is_can_edit(request):
        return HttpResponseForbidden("Anda tidak berhak mengedit proyek!")

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if not has_edit_secret(request):
            messages.error(request, "Kode sandi salah!")
        elif form.is_valid():
            form.save()
            messages.success(request,"Project berhasil diperbaharui!")
            return redirect("main:show_projects")
    else:
        form = ProjectForm(instance=project)

    context = {
        "name": "Lefi",
        "form": form,
        "project": project,
        "is_edit": True,
    }
    return render(request, "projects_form.html" ,context)

# EXPERIENCE
@login_required(login_url="/login/")
def create_experience(request):
    if not is_super_user(request):
        return HttpResponseForbidden("Anda tidak berhak membuat experience!")

    form = ExperienceForm(request.POST or None)
    context = {
            "name" : "Lefi",
            "form": form,
            "is_edit": False
        }
    if (request.method == "POST"):
        if not has_edit_secret(request):
            messages.error(request, "Kode rahasia salah!")
            return render(request, 'experiences_form.html', context)

        elif form.is_valid():
            form.save()
            return redirect("main:show_experiences")

    return render(request, 'experiences_form.html', context)

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []

    for experience in experiences:
        starred_users =experience.starred_by.all()

        is_starred = (
            request.user in starred_users if request.user.is_authenticated else False
        )

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category": experience.category,
                "category_display": experience.get_category_display(),
                "is_ongoing": experience.is_ongoing,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": ", ".join([u.username for u in starred_users])
            }
        })

    return JsonResponse(data, safe=False)


@login_required(login_url="/login")
def delete_experience(request, experience_id):
    if not is_super_user(request):
        return HttpResponseForbidden("Anda tidak berhak menghapus experience!")
    experience = get_object_or_404(Experience, pk=experience_id)


    if request.method == "POST":
        if not has_edit_secret(request):
            messages.error(request,"Kata sandi salah!")
            return redirect("main:show_experiences")

        experience.delete()
        messages.success(request,"Experience berhasil dihapus!")
        return redirect("main:show_experiences")

    return redirect("main:show_experiences")

@login_required(login_url="/login")
def edit_experience(request, experience_id):

    experience = get_object_or_404(Experience, pk=experience_id)

    if not is_can_edit(request):
        return HttpResponseForbidden("Anda tidak berhak mengedit experience!")

    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)

        if not has_edit_secret(request):
            messages.error(request,"Kata sandi salah!")
        elif form.is_valid():
            form.save()
            messages.success(request, "Experience berhasil diperbarui")
            return redirect("main:show_experiences")
    else:
        form = ExperienceForm(instance=experience)

    context = {
        "name": "Lefi",
        "form": form,
        "experience": experience,
        "is_edit": True
    }
    return render(request, "experiences_form.html", context)

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

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil terdaftar!")
        return redirect("main:login_user")
    context = {"form" : form}

    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_main")
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d ( %H:%M:%S )"))
        return response

    context = {"form": form}
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    messages.success(request, "Logout")

    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response

@login_required(login_url="/login/")
def toggle_star_project(request, id):
    project = get_object_or_404(Project, pk=id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def toggle_star_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experiences")

def is_super_user(request):
    return request.user.is_superuser

def is_can_edit(request):
    return request.user.is_superuser or request.user.groups.filter(name="Editor").exists()


@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
# Create your views here.
