from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Project

class ProjectForm(ModelForm):
     class Meta:
          model = Project
          fields = [
               "title",
               "description",
               "tech_stack",
               "url_link",
               "image"
          ]

          labels = {
               "title": "Nama Proyek",
               "description": "Deskripsi Proyek",
               "tech_stack": "Teknologi yang digunakan",
               "url_link": "URL Proyek",
               "image": "URL Gambar Proyek",
          }

          widgets = {
               "title": TextInput(
                    attrs={
                         "placeholder": "Masukkan Judul Proyek disini...",
                         "maxlength" : 255,
                    }
               ),
               "description": Textarea(
                    attrs={
                         "placeholder": "Masukkan Deskripsi Proyek disini...",
                         "rows" : 3,
                    }
               ),
               "tech_stack": TextInput(
                    attrs={
                         "placeholder": "Masukkan Tech Stack Proyek disini...",
                    }
               ),
               "url_link": URLInput(
                    attrs={
                         "placeholder": "https://...",
                    }
               ),
               "image": TextInput(
                    attrs={
                         "placeholder": "/static/img/...",
                    }
               ),



          }
