
# PBP - Portfolio Website

### 👤 Student Information

| Information    | Details                                                                               |
| -------------- | ------------------------------------------------------------------------------------- |
| **Name**       | Muh. Alfi Rizqy                                                                       |
| **NPM**        | 2506550721                                                                            |
| **Class**      | PBP F                                                                                 |
| **Deployment** | [muh-alfi-myportfolio.pws.cs.ui.ac.id](https://muh-alfi-myportfolio.pws.cs.ui.ac.id/) |

---

## 📌 Progress Status

| Task                  | Status |
| --------------------- | :----: |
| Tutorial 0            |    ✅   |
| Tutorial 1            |    ✅   |
| Assignment 1          |    ✅   |
| Tutorial 2            |    ✅   |
| Assignment 2          |    ✅   |

---

# 📑 Individual Assignment 1

## 1. Track Report

Untuk Tugas 1 ini, saya memutuskan membuat **Project Section** yang menampilkan project-project yang telah saya kerjakan. Dalam mengerjakannya, saya melalui tiga progress utama.

### 📍 Progress 1 — Initial Project Section

**2 September 2026**

Pada commit pertama di tanggal 2 September 2026, saya mencoba untuk membuat layout utama dari **Project Section**. Hal tersebut cukup menantang bagi saya karena saya perlu memahami struktur HTML dan behaviour CSS yang dibuatkan ASDOS dalam template.

Setelah beberapa menit, saya telah berhasil membuat layout utama dan beberapa card project, namun masih sangat datar dan dalam bentuk placeholder. Oleh karena itu, saya berencana untuk menyempurnakannya sambil memikirkan ide yang cocok.

---

### 📍 Progress 2 — Hero Section Redesign

**7 September 2026**

Lima hari kemudian, pada tanggal 7 September 2026, saya mencoba melanjutkan tugas ini. Namun, saya merasa ada yang janggal di website saya. Saya merasa website saya kurang menarik karena **Hero Section**-nya terlihat biasa saja, padahal Hero Section yang baik seharusnya dapat membuat pengunjung tertarik dengan website saya.

Oleh karena itu, sebelum melanjutkan Project Section, saya mencoba membuat Hero Section terlebih dahulu, dan Hero Section yang lama saya jadikan **Profile Section**.

Setelah beberapa jam, akhirnya saya berhasil membuat Hero Section yang lebih menarik.

<p align="center">
  <img
    width="1280"
    alt="Hero Section"
    src="https://github.com/user-attachments/assets/d56323a4-9cbd-4a1e-8fea-47f06c015e76"
  />
</p>

---

### 📍 Progress 3 — Project Section Enhancement

**7 September 2026**

Setelah Hero Section beres, saya kemudian melanjutkan progress Project Section saya. Card buatan saya sebelumnya terasa sangat datar dan kurang menarik, jadi saya berencana merombak beberapa bagian sehingga terlihat lebih menarik.

Kemudian, saya juga menambahkan animasi ringan yang ditrigger melalui **hover** untuk melihat deskripsi dari tiap project saya.

<p align="center">
  <img
    width="1280"
    alt="Project Section"
    src="https://github.com/user-attachments/assets/59878d6b-8485-4626-829f-2527f43628e4"
  />
</p>

---

### 🔧 Final Adjustments

Terakhir, saya juga melakukan beberapa penyesuaian seperti memperbaiki bug kecil, melakukan perubahan desain minor, dan beberapa penyempurnaan lainnya pada website.

---

## 💭 Reflective Questions

### 1. Penggunaan Semantic HTML5

Secara garis besar, sebenarnya saya tidak membutuhkan elemen **Semantic HTML5** dalam mengerjakan portofolio saya, karena pembagian struktur HTML dapat dilakukan hanya dengan mengandalkan `div`.

Namun, menurut saya kode yang baik adalah kode yang memiliki readability yang baik. Penggunaan elemen Semantic HTML5 akan lebih readable karena memiliki arti khusus di setiap pembagiannya, sehingga kode akan lebih rapi dan mudah dibaca oleh saya sendiri dalam melakukan debugging dan maintenance.

Selain itu, programmer lain yang baru membaca kode tersebut juga dapat langsung mengerti maksud dari struktur kode yang saya buat.

---

### 2. Responsive Design

Tantangan terbesarnya adalah saat menyesuaikan **layout dan spacing antar ukuran layar**.

Saya mulai menyusun web dari tampilan desktop, sehingga tampilan yang saya coba buat lebih cocok di desktop. Saat berpindah ke layar yang lebih kecil, saya harus berpikir lagi mengenai layout yang cocok untuk layar HP dan tablet.

Spacing juga menjadi tantangan yang cukup berat bagi saya. Biasanya saya tidak kesulitan dalam mengatur spacing karena menggunakan **TailwindCSS**, tetapi saat menggunakan vanilla CSS, saya merasa bahwa untuk mengatur spacing saja sudah lumayan ribet.

Hal yang paling cepat saya pikirkan ketika berpindah ke layar yang lebih kecil adalah mulai dari mengatur **ukuran teks terlebih dahulu**, karena dengan mengatur teks saya menjadi lebih memiliki gambaran mengenai layout lainnya sebaiknya dibuat seperti apa.

---

### 3. Redundancy dan Implementasi MVT

Saya merasa banyak kode di struktur HTML saya yang redundan, contohnya pada saat ingin menampilkan beberapa project saya.

Secara umum, struktur HTML tiap project menggunakan struktur yang sama. Perbedaannya hanya pada **konten dan image**-nya saja.

Kemudian, saya juga berpikir bahwa akan lebih baik jika project dapat saya tambahkan tanpa perlu susah payah membuka source code dan menambahkannya secara manual.

Oleh karena itu, saya berpikir akan menerapkan **MVT (Model-View-Template)** pada iterasi proyek selanjutnya, dengan mendefinisikan class model untuk project dan menghubungkannya dengan view.

Data tersebut kemudian dapat ditampilkan menggunakan beberapa logic Python seperti **loop** dan **filter** di template. Saya pikir dengan pendekatan tersebut, masalah redundansi pada kode saya dapat teratasi.

---

## 🤖 AI Disclosure

Dalam mengembangkan website ini, saya memanfaatkan dua model AI yang berbeda, yaitu **AI Overview dari Google** dan **Generative AI ChatGPT**.

### Google AI Overview

Saya memanfaatkan AI Overview dalam mencari syntax tertentu dalam CSS, karena terlalu lama menggunakan TailwindCSS membuat saya lupa syntax-syntax dasar dalam vanilla CSS.

Jadi, saya bertanya kepada AI Overview dengan membandingkan syntax di Tailwind, contohnya:

> "Dalam Vanilla CSS, bagaimana membuat `flex-col` seperti pada TailwindCSS?"

Dengan cara tersebut, saya dapat lebih terbiasa kembali dengan syntax dan behaviour vanilla CSS tanpa kehilangan esensi dari proses pembelajarannya.

Saya memilih AI Overview Google karena merasa kebutuhan tersebut sudah cukup ditangani dengan model yang lebih rendah.

### ChatGPT

Kemudian, saya menggunakan Generative AI ChatGPT saat melakukan **debugging**, karena proses tersebut membutuhkan pemikiran yang lebih tajam sehingga saya memilih model yang lebih tinggi.

Pada saat mendapati jalan buntu dan tidak mengerti letak kesalahannya, saya akan bertanya terlebih dahulu kepada ChatGPT mengenai permasalahan yang saya alami dan ekspektasi dari hasil yang sebenarnya saya inginkan.

Jika konteks tersebut masih kurang, saya akan menyalin beberapa bagian kode yang berkaitan dengan masalah tersebut agar ChatGPT mendapatkan konteks yang lebih jelas.

Namun, saya **tidak langsung meminta kode final yang sudah benar**. Sebaliknya, saya meminta ChatGPT untuk memahami masalah saya dan menjelaskan kesalahan yang terjadi. Setelah itu, saya sendiri yang menerjemahkan penjelasan tersebut menjadi kode yang sesuai.

---

# 📑 Individual Assignment 2

## Track Report

Untuk tugas 2, saya memutuskan mengubah Project Section yang telah saya buat di tugas sebelumnnya dari static menjadi dynamic. Pada minggu pertama, saya mulai dengan menambahkan model untuk Projecy dengan atribut: 
  - id: Berfungsi sebagai identitas unik setiap project, menggunakan UUIDField untuk mengenerate kode unik setiap project.
  - title: Berfungsi untuk menyimpan judul setiap project, menggunakan CharField dengan maksimal character 225.
  - description: Berfungsi untuk menyimpan deskripsi singkat mengenai project, menggunakan TextField tanpa ada batasan.
  - image: Berfungsi untuk menyimpan string path image yang disimpan dalam lokal, menggunakan CharField dengan maksimal character 225, Nullable, dan bisa saja kosong.
  - url_link: Berfungsi untuk menyimpan link url tiap project yang redirect langsung ke project saya, menggunakan URLField.
Selain itu, saya juga menambahkan properti "is_live" yang bergantung pada eksistensi nilai di url_link, bertipe data boolean.
Setelah model nya jadi, saya kemudian menambahkan views dan template baru khusus untuk menampilkan project. Akhirnya, Project Section yang dulunya Dinamis sekarang telah menjadi statis. Untuk memasukkan data, saya mencoba menambahkan Django Admin sehingga saya bisa me-manage data dengan lebih mudah.

Sebenarnya, untuk tugas 2 sebagian requirement telah terpenuhi, yang sekarang tersisa adalah membuat unit test, karena saya merasa waktunya masih lama, jadi saya menghabiskan beberapa hari untuk menyempurnakan desain website saya di halaman utama, saya mulai dengan menambahkan section baru, yaitu Tech Stack Section yang menampilkan Tools dan Tech Stack yang pernah saya gunakan, saya menambahkan animasi marquee untuk membuat section tersebut lebih menarik. Disini saya juga memanfaatkan penggunaaan Views-Template agar kode saya tidak menumpuk semua di file `index.html`.
<img width="2934" height="1616" alt="image" src="https://github.com/user-attachments/assets/e70f7276-c0ac-4e8b-bad0-bac1c423e685" />


Kemudian saya juga menambahkan Github Section di halaman utama yang menampilkan Github Contributions saya dalam setahun terakhir. Disini saya fectch dari graphQL API Github. Untuk function fetchernya saya definisikan di views.py. Perubahan lainnya saya lakukan dengan menyempurnakan desain di bagian yang kurang dan menyempurnakan desain lainnya di Profile Section, 

<img width="2940" height="1626" alt="image" src="https://github.com/user-attachments/assets/a9cafbcd-64a2-46f8-87c1-babbed39e5d4" />
<img width="2946" height="1622" alt="image" src="https://github.com/user-attachments/assets/e881e16d-fd0e-4535-a277-037864b15af6" />

Selain itu, saya juga mengubah Navbar sehingga menjadi lebih menarik dan interaktif. Saat di-hover, navbar akan menampilkan versi lenkgapnya.
<img width="1560" height="212" alt="image" src="https://github.com/user-attachments/assets/1cf78c3f-0f4e-4a38-84fb-93ccdd2d9cfa" />

Terakhir, saya menambahkan unit test untuk menguji Projects Section saya dengan meliputi 3 tes utama:
1. URL Projects dapat diakses dan menggunakan template yang tepat
2. Data model muncul di halaman HTML ketika ada data
3. Halaman HTML menampilkan pesan kondisi kosong ketika belum ada data

Sejujurnya, saya masih ingin menyempurnakan bagian halaman Projects dan Experiences, tapi karena waktu yang tidak cukup, seshingga saya akan melanjutkannya di lain kesempatan.

## 💭 Reflective Questions

### 1. Flow ketika user membuka Halaman Baru
Pada saat user membuka halaman baru dengan menuliskan `https://muh-alfi-myportfolio.pws.cs.ui.ac.id/projects/`, maka request akan masuk ke `urls.py` lalu kemudian diteruskan langsung ke `main.urls.py`, di dalam  `main.urls.py` akan dicocokkan path nya, karena user mengakses path `/projects`, maka views yang akan menangani request tersebut adalah `show_projects` seperti yang telah didefinisikan dalam kode. View tersebut kemudian akan mengambil data dari model `Project` melalui  `Project.objects.all()` lalu menyimpannya ke context sebagai `project_list` lalu kemudian akan dirender ke template  `projects.html`. Di dalam template tersebut, data dari  `project_list` ditampilkan ke browser dengan menggunakan loop, kemudian untuk mengakses judul, deskripsi, image, dan url_link itu berdasarkan item pada `project_list`.

### 2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model
Data pada Projects Section lebih baik disimpan dalam model sehingga bersifat dinamis, dibandingkan langsung ditulis dalam template yang masih bersifat statis. Dengan mengubah project section menggunakan data dinamis, data dari projects dapat saya ubah seiring waktu tanpa membuka kembali codebase yang telah saya tulis, jadi jika ada tambahan projek atau mungkin data projek yang bisa saja berubah seiring waktu, saya tinggal mengubah datanya lewat Django Admin tanpa membuka codebase. Dalam konteks pemeliharaan aplikasi, ini juga lebih sehat karena template hanya fokus menampilkan data sedangkan penyimpanan data akan dihandle oleh Model berdasarkan struktur datanya. Untuk pengembangan kedepannya juga akan lebih fleksibel karena data sudah bersifat dinamis.

### 3. Perbedaan `makemigrations` dan `migrate`
Kedua perintah tersebut merupakan perintah bawaan python yang berbeda, `makemigrations` berfungsi untuk membuat migrasi berdasarkan perubahan pada Model yang telah terdefinsikan di `main.models.py`, jadi setiap saya ingin menambahkan, mengubah, atau bahkan menghapus seuatu di Model, saya akan menjalankan  `makemigrations`. Namun, untuk menerapkan perubahan tersebut di database kita, kita perlu menjalankan `migrate` juga, jadi kedua command tersebut saling berkaitan. Pada project ini sendiri saya menggunakan perintah `makemigrations` ketika saya telah mendefinisikan model untuk Projects, kemudain saya menjalankan `migrate` agar perubahan tersebut terimplementasikan dalam database.


## 🤖 AI Disclosure

Untuk penggunaan AI di tugas ini lebih berkurang dibandingkan sebelumnya, karena saya telah terbiasa dengan syntax-syntax di vanilla CSS, saya menggunakan AI ChatGPT hanya untuk meminta informasi mengenai suatu Library yang biasa saya pakai di Framework Javascript untuk diimplementasikan di Django:
https://chatgpt.com/share/6aa81ec5-4510-83ec-8ca4-7c09717cb7c6

Selain itu, saya juga sempat bertanya kepada Google AI Overview mengenai Github Section apakah dapat diimplementasikan di Django atau tidak, walaupun dari jawabannya tidak jadi saya gunakan dan memilih menggunakan pendekatan berbeda setelah membaca beberapa dokumentasi mengenai Github API
https://share.google/aimode/cIrIaPZvOPPyW9ge5


<p align="center">
  <strong>Individual Assignment 1 — PBP F</strong><br/>
  Muh. Alfi Rizqy · 2506550721
</p>
