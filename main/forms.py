from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateTimeInput

from main.models import Project, Experience

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
                         "rows" : 1,
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

class ExperienceForm(ModelForm):

     class Meta:
          model = Experience
          fields = [
               "title",
               "description",
               "category",
               "thumbnail",
               "started_at",
               "ended_at"
          ]
          labels = {
               "title" : "Judul Pengalaman",
               "description" : "Deskripsi Pengalaman",
               "category" : "Kategori",
               "thumbnail" : "Thumbnail",
               "started_at" : "Masa Mulai",
               "ended_at" : "Masa Berakhir"
          }
          widgets = {
               "title" : TextInput(
                    attrs={
                         "placeholder":"Masukkan Judul Pengalaman disini...",
                         "maxlength" : 255,
                    }
               ),
               "description" : Textarea(
                    attrs={
                         "placeholder":"Masukkan Deskripsi Pengalaman disini...",
                         "rows": 1,
                    }
               ),
               "category": Select(
                    attrs={
                         "class": "dropdown",
                    }
               ),
               "thumbnail" : TextInput(
                    attrs={
                         "placeholder" : "/static/img/...",
                    }
               ),
               "started_at": DateTimeInput(
                    attrs={"type":"date"},
                    format="%d/%m/%Y",

               ) ,
               "ended_at": DateTimeInput(
                    attrs={"type":"date"},
                    format="%d/%m/%Y",
               )

          }
