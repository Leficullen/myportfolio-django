from django.urls import path

from main.views import show_main, show_experiences, show_projects, github_contributions_api, create_project, get_projects_json, delete_project, create_experience, delete_experience, edit_experience, login_user, logout_user, register, toggle_star_project, toggle_star_experience, get_experiences_json, edit_project

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experiences/", show_experiences, name="show_experiences"),
    path("projects/", show_projects , name="show_projects"),

    path("api/github-contributions/", github_contributions_api, name="github_contributions_api"),

    path('projects/add/', create_project, name="create_project"),
    path('api/projects/', get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("projects/<uuid:project_id>/edit/", edit_project, name="edit_project"),

    path('experiences/add/', create_experience, name="create_experience"),
    path('api/experiences/', get_experiences_json, name="get_experiences_json"),
    path('experiences/<uuid:experience_id>/delete/', delete_experience, name="delete_experience"),
    path('experiences/<uuid:experience_id>/edit/', edit_experience, name="edit_experience"),

    path('login/', login_user, name="login_user"),
    path('register/', register, name="register"),
    path('logout/', logout_user, name="logout_user"),
    path("projects/<uuid:id>/star", toggle_star_project, name="toggle_star_project"),
    path("experiences/<uuid:id>/star", toggle_star_experience, name="toggle_star_experience")


]
