Notifikasi 
Demonstrasi Event Driven Architecture (EDA) dengan Python & RabbitMQ

# Apa Ini
Aplikasi ini merupakan contoh penerapan Event Driven Architecture (EDA) menggunakan ekosistem Python. Setiap aksi pengguna menghasilkan sebuah event yang dikirim ke antrian, kemudian diproses secara asinkron oleh worker, dan hasilnya dikirimkan melalui Email maupun Telegram.

# Arsitektur
## 1 Flask UI
Antarmuka web berbasis Flask. Pengguna berinteraksi di sini, lalu event dipublikasikan ke RabbitMQ.

## 2 RabbitMQ
Message broker yang mengelola antrian (queue). Menjamin event tidak hilang dan terkirim ke worker.

## 3 Worker / Agent
Proses Python yang berjalan di latar belakang. Mengonsumsi event dari antrian dan mengeksekusi tugas.

## 4 Notifikasi
Hasil dikirim ke pengguna melalui Email dan Telegram.