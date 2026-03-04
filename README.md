# CleanerC - Modern Disk Optimizer

CleanerC adalah aplikasi desktop berbasis Python yang dirancang untuk membantu pengguna mengoptimalkan penggunaan ruang penyimpanan pada sistem operasi Windows. Aplikasi ini menyediakan antarmuka modern untuk memindahkan file sementara (temporary files) dan sampah sistem ke Recycle Bin secara aman tanpa menghapus data secara permanen.

## Fitur Utama

1.  **Pemindaian Cepat**: Menganalisis direktori temporer, update cache, dan file hibernasi untuk mengidentifikasi sampah sistem.
2.  **Manajer Hibernasi**: Mematikan hibernasi (`powercfg -h off`) untuk menghemat hingga 10GB+ ruang disk.
3.  **Flush DNS**: Reset cache resolver jaringan untuk mengatasi masalah koneksi.
4.  **Pembersihan Aman**: Menggunakan metode pemindahan ke Recycle Bin untuk menjaga keamanan data.
5.  **Monitor Kapasitas**: Menampilkan informasi penggunaan disk, CPU, dan GPU secara real-time.
6.  **Alat Sistem**: Termasuk Process Optimizer, Startup Manager, dan Pencari File Besar.
7.  **Antarmuka Responsif**: UI modern dengan CustomTkinter dan dukungan multithreading.
8.  **Indikator Kemajuan**: Progress bar dan status visual yang transparan.

## Spesifikasi Teknis

- Bahasa Pemrograman: Python 3.10+
- Library UI: CustomTkinter
- Library Sistem: psutil, send2trash

## Panduan Instalasi

Langkah-langkah untuk menyiapkan lingkungan pengembangan:

1. Pastikan Python sudah terinstal di sistem Anda.
2. Clone repositori ini atau unduh file sumber.
3. Buka terminal di direktori proyek dan buat lingkungan virtual (opsional):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Untuk Windows: .venv\Scripts\activate
   ```
4. Instal dependensi yang diperlukan melalui pip:
   ```bash
   pip install -r requirements.txt
   ```

## Cara Menjalankan Aplikasi

Jalankan skrip utama menggunakan interpreter Python:
```bash
python main.py
```

## Prosedur Build ke Executable (.exe)

Aplikasi ini siap dikompilasi menjadi satu file eksekutabel menggunakan PyInstaller. Ikuti petunjuk berikut:

1. Instal PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Jalankan perintah build berikut:
   ```bash
   pyinstaller --noconsole --onefile --name CleanerC main.py
   ```
3. File eksekutabel akan tersedia di folder `dist`.

Catatan: Flag `--noconsole` digunakan untuk menyembunyikan jendela terminal saat aplikasi dijalankan, dan `--onefile` menggabungkan semua dependensi ke dalam satu file .exe tunggal.
