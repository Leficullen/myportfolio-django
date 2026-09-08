# Individual Assignment 1 — Portfolio Website

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
| Individual Assignment |    ✅   |
| Tutorial 2            |    ✅   |

---

# 📑 Track Report — Individual Assignment 1

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

# 💭 Reflective Questions

## 1. Penggunaan Semantic HTML5

Secara garis besar, sebenarnya saya tidak membutuhkan elemen **Semantic HTML5** dalam mengerjakan portofolio saya, karena pembagian struktur HTML dapat dilakukan hanya dengan mengandalkan `div`.

Namun, menurut saya kode yang baik adalah kode yang memiliki readability yang baik. Penggunaan elemen Semantic HTML5 akan lebih readable karena memiliki arti khusus di setiap pembagiannya, sehingga kode akan lebih rapi dan mudah dibaca oleh saya sendiri dalam melakukan debugging dan maintenance.

Selain itu, programmer lain yang baru membaca kode tersebut juga dapat langsung mengerti maksud dari struktur kode yang saya buat.

---

## 2. Responsive Design

Tantangan terbesarnya adalah saat menyesuaikan **layout dan spacing antar ukuran layar**.

Saya mulai menyusun web dari tampilan desktop, sehingga tampilan yang saya coba buat lebih cocok di desktop. Saat berpindah ke layar yang lebih kecil, saya harus berpikir lagi mengenai layout yang cocok untuk layar HP dan tablet.

Spacing juga menjadi tantangan yang cukup berat bagi saya. Biasanya saya tidak kesulitan dalam mengatur spacing karena menggunakan **TailwindCSS**, tetapi saat menggunakan vanilla CSS, saya merasa bahwa untuk mengatur spacing saja sudah lumayan ribet.

Hal yang paling cepat saya pikirkan ketika berpindah ke layar yang lebih kecil adalah mulai dari mengatur **ukuran teks terlebih dahulu**, karena dengan mengatur teks saya menjadi lebih memiliki gambaran mengenai layout lainnya sebaiknya dibuat seperti apa.

---

## 3. Redundancy dan Implementasi MVT

Saya merasa banyak kode di struktur HTML saya yang redundan, contohnya pada saat ingin menampilkan beberapa project saya.

Secara umum, struktur HTML tiap project menggunakan struktur yang sama. Perbedaannya hanya pada **konten dan image**-nya saja.

Kemudian, saya juga berpikir bahwa akan lebih baik jika project dapat saya tambahkan tanpa perlu susah payah membuka source code dan menambahkannya secara manual.

Oleh karena itu, saya berpikir akan menerapkan **MVT (Model-View-Template)** pada iterasi proyek selanjutnya, dengan mendefinisikan class model untuk project dan menghubungkannya dengan view.

Data tersebut kemudian dapat ditampilkan menggunakan beberapa logic Python seperti **loop** dan **filter** di template. Saya pikir dengan pendekatan tersebut, masalah redundansi pada kode saya dapat teratasi.

---

# 🤖 AI Disclosure

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

<p align="center">
  <strong>Individual Assignment 1 — PBP F</strong><br/>
  Muh. Alfi Rizqy · 2506550721
</p>
