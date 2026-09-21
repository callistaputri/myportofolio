Nama : Callista Putri Anjola

NPM : 2506603740

Kelas : PBP A

Prodi: Sistem Informasi

## Tugas 1

1. Ya, saya saat merancang struktur HTML, saya menggunakan elemen semantik HTML5 yaitu < section >. Elemen tersebut membantu saya dalam pembuatan tugas dengan cara menjadi pembagi konten About Me dan Experiences dengan terstruktur. Penggunaan elemen ini membantu saya dalam membagi setiap informasi berdasarkan bagiannya masing-masing sehingga website menjadi lebih rapi dan lebih mudah dikembangkan. Selain itu, saya juga menggunakan elemen < div > yang membantu saya untuk mengatur layout konten yang ada. Saya juga menggunakan elemen < ul > dan < li > untuk membuat daftar pengalaman menjadi lebih tertata.


2. Tantangan yanvg saya temukan adalah bagaimana cara menjaga posisi garis dan titik yang terdapat pada bagian kiri experiences saya agar tetap sejajar dengan daftar pengalaman saat website dibuka dengan ukuran layar yang berbeda. Saya menggunakan garis dan titik untuk memisahkan satu pengalaman dengan yang lainnya. Saya juga menggunakan hover pada titik tersebut, di mana dot akan berubah menjadi penuh ketika kursor diarahkan ke salah satu pengalaman sehingga membuat tanda kepada user mengenai bagian apa yang sedang dipilih/dilihat. 


3.  Keterbatasan yang saya rasakan dari static web adalah saya masih harus mengubah kode HTML secara manual setiap ingin memperbarui atau menambahkan informasi yang terdapat pada website portofolio. Selain itu, informasi yang ditampilkan juga masih terbatas dan belum dapat memberikan detail yang interaktif. Untuk iterasi selanjutnya, saya ingin menambah fitur dimana user dapat menekan suatu pengalaman untuk melihat informasi tambahan, seperti sertifikat, foto dokumentasi, atau detail lain dari kegiatan tersebut. Saya juga ingin menerapkan fitur tersebut jika nantinya saya akan membuat section projects, skills, dan lain sebagainya agar informasi menjadi lebih lengkap namun tampilan website tetap rapi.


AI Disclosure

Dalam proses pengembangan website portofolio ini, saya menggunakan beberapa AI tools yaitu ChatGPT dan Claude sebagai alat bantu pembelajaran dan pemecahan masalah. Saya menggunakannya terutama ketika saya mengalami kesulitan memahami konsep atau menemukan solusi terhadap permasalahan yang muncul selama proses pengembangan website.

AI membantu saya memahami berbagai fitur dan elemen HTML5 serta CSS ketika terdapat konsep yang belum saya pahami, termasuk fungsi elemen semantik, pengaturan layout, responsive design, dan stylingnya. Selain itu, saya juga menggunakan AI untuk meminta arahan ketika ingin menambahkan fitur atau tampilan tertentu pada website, seperti menyusun garis timeline dan dots pada bagian Experiences agar terlihat rapi.

Biasanya, saya menjelaskan permasalahan yanhg terjadi secara spesifik dengan menyertakan potongan kode atau menjelaskan masalah yang terjadi pada halaman website. Contohnya, ketika terdapat elemen CSS yang sulit dirapikan, saya mendeskripsikan bentuk hasil yang saya inginkan kemudian meminta penjelasan mengenai penyebab dan cara memperbaikinya. Dengan cara tersebut, AI memberikan arahan yang lebih baik dibandingkan hanya meminta kode secara langsung.

Saat saya menemukan error yang sudah sulit saya selesaikan sendiri, saya menggunakan AI untuk membantu mengidentifikasi sumber masalah berdasarkan kode dan tampilan yang saya kirimkan. Setelah mendapatkan penjelasan, saya mempelajari kembali letak kesalahan dan memahami alasan mengapa solusi tersebut bsia bekerja. Proses ini membantu saya melanjutkan pengembangan website dan juga meningkatkan pemahaman saya terhadap struktur HTML dan CSS yang digunakan.

## Tugas 2

1. Ketika pengguna membuka halaman education pada portofolio saya melalui /education/, request pertama akan masuk pada urls.py pada proyek. Request akan diarahkan ke main.urls karena saya memakai include("main.urls"). Setelah itu, main/urls.py menentukan bahwa url /education/ akan menjalankan show_education yang terdapat di views.py. Dalam views.py, saya mengambil data education dari model menggunakan Education.objects.all(). Lalu, data tersebut dikirimkan kepada templates/education.html. Di sana, data education ditampilkan denbgan menggunakan {% for %}. Jadi, setiap data yang berada di database akan ditampilkan di halaman. Lalu, hasilnya dikirinmkan ke browser dan ditampilkan sebagai halaman education.


2. Menurut pendapat saya, data lebih baik disimpan di dalam model daripada ditulis manual langsung pada template agar lebih mudah jika ada perubahan atau penambahan data. Jika ditulis manual dalam template, setiap kali saya ingin menambahkan atau mengganti data, saya harus mengganti kode HTML nya. Sedangkan jika disimpan dalam model, saya dapat cukup menambahkan atau mengubah data di database dan template dapat menampilkannya secara otomatis. Selain itu, kode juga menjadi lebih rapi.


3. makemigrations digunakan untuk membuat file yang berisi perubahan model yang saya buat, kalau migrate digunakan untuk menerapkan perubahan tersebut kepada database. contoh saat saya menambah model education, saya menjalankan python manage.py makemigrations dan perintah tersebut membuat file migration untuk model education. Setelah itu, saya akan menjalankan python manage.py migrate agar perubahannya benar-benar diterapkan pada database dan tabel education dibuat.


AI Disclosure

Dalam proses pengembangan website portofolio ini, saya menggunakan beberapa AI tools yaitu ChatGPT dan Gemini AI sebagai alat bantu pembelajaran dan pemecahan masalah. Saya menggunakannya terutama ketika mengalami kesulitan memahami konsep Django atau menemukan solusi dari masalah yang muncul selama proses pengembangan website.

Pada tugas ini, saya menggunakan AI untuk membantu memahami cara membuat model baru, melakukan migration, mengambil data dari model melalui view, serta menampilkan data menggunakan Django Template Language (DTL). Selain itu, saya menggunakan AI untuk membantu menyesuaikan styling Education dan Experience agar sesuai dengan tema website.

Ketika menemukan error, saya memberikan kode atau pesan error kepada AI untuk membantu mencari sumber masalah. Setelah mendapatkan penjelasan, saya mempelajari kembali penyebab error tersebut dan melakukan perbaikan pada kode saya sendiri. Dengan begitu, AI membantu saya menyelesaikan masalah sekaligus memahami proses pengembangan fitur baru pada Django.

## Tugas 3

1. Menurut saya, ModelForm digunakan agar pembuatan form menjadi lebih mudah karena form dapat langsung terhubung dengan model yang telah dibuat. Jadi, field yang ada pada model dapat digunakan pada form tanpa mengharuskan saya membuat perubahan pada HTML secara manual. Setelah data diisi dan valid, data juga dapat langsung disimpan ke dalam database dengan menggunakan form.save(). Selain itu, {% csrf_token %} digunakan untuk keamanan pada form yang menggunakan method POST. Token tersebut membantu django memastikan bahwa request yang dikirim berasal dari form yang terpercaya, sehingga request yang tidak memiliki token sesuai akan ditolak. Jadi, setiap form yang terdapat pada website saya perlu menggunakan {% csrf_token %} agar dapat diproses dengan aman.


2. Menurut saya, JSON lebih sering digunakan dalam pengembangan aplikasi web modern karena bentuk datanya lebih sederhana dan lebih mudah dibaca dibanding dengan XML. JSON juga menggunakan struktur seperti key dan value sehingga lebih mudah digunakan untuk menyimpan dan juga mengirim data. Selain itu, JSON juga memiliki struktur yang cukup mirip dengan struktur data yang digunakan dalam pemrograman sehingga lebih mudah prosesnya.


3. Dalam portofolio saya, saat data education ingin direturn dalam bentuk JSON, request akan masuk ke fungsi get_education_json yang terdapat pada file views.py. Di dalam fungsi tersebut, saya mengambil data education dari database menggunakan Education.objects.all(). Setelahnya, data tersebut diubah mnejadi JSON dengan serializers.serialize("json", education). Hasil JSON tersebut kemudian direturn menggunakan HTTPResponse dengan content_type="application/json". Pada halaman education, saya memanggil fungsi tersebut dan mengambil hasil JSON nya. Setelah itu, diproses menggunakan serializers.deserialize() sehingga data yang pada awalnya berbentuk JSON bisa kembali menjadi object django dan ditampilkan pada template education.html. Serialization diperlukan karena data yang saya ambil dari database masih berupa object atau QuerySet django, sehingga perlu diubah ke format JSON terlebih dahulu agar dapat dikirim dan digunakan sebagai data JSON.


AI Disclosure

Dalam proses mengerjakan tugas 3, saya menggunakan AI tools seperti ChatGPT dan Claude sebagai alat bantu ketika saya mengalami kesulitan dalam memahami materi atau menemukan error pada portofolio saya.

Saya menggunakan AI untuk membantu memahami cara membuat dan menggunakan ModelForm, membuat fitur seperti create, update, dan delete pada section education, serta memahami proses pengambilan data dalam bentuk JSON dan melakukan serialization dan deserialization. Saya juga menggunakan AI untuk membantu menyesuaikan beberapa bagian styling pada website portofolio sayaa.

Saat aya mengalami error, biasanya saya memberikan beberapa kode atau pesan error yang muncul kepada AI untuk membantu saya memahami penyebab error. Setelah itu saya mencoba menerapkan solusi yang diberi pada project saya dan mengecek kembali apakah hasilnya sesuai. Jadi, AI membantu saya dalam belajar dan memahami bagian yang belum saya mengerti selama mengerjakan tugas, bukan untuk membuat keseluruhan project secara langsung.