# Student Performance Dashboard

Dashboard interaktif untuk menganalisis dan memprediksi performa akademik siswa berdasarkan berbagai faktor demografi, gaya hidup, dan akademik. Proyek ini dibangun menggunakan **Dash Framework** dan model machine learning.

## Deskripsi Proyek
Proyek ini bertujuan untuk memberikan wawasan (insight) kepada pendidik dan orang tua mengenai faktor-faktor yang mempengaruhi nilai ujian siswa. Dashboard ini mencakup visualisasi data (EDA), eksplorasi dataset, serta fitur prediksi dan klasifikasi status akademik.

<img width="1512" height="856" alt="Screenshot 2026-04-16 at 09 58 55" src="https://github.com/user-attachments/assets/e98ce0af-3c50-4d66-89bd-595bb25ca1fa" />


### Fitur Utama:
- **Home**: Ringkasan KPI performa siswa secara keseluruhan.
- **Dataset**: Eksplorasi data mentah dan ringkasan statistik.
- **EDA (Exploratory Data Analysis)**: Visualisasi distribusi kolom dan korelasi antar fitur.
- **Prediction**: Prediksi nilai ujian (Real-time) berdasarkan input pengguna menggunakan model Linear Regression.
- **Classification**: Klasifikasi status akademik (Pass/Remedial/Fail) menggunakan model Logistic Regression.

## Cara Instalasi

### 1. Prasyarat
Pastikan Anda sudah menginstal Python (disarankan versi 3.9 ke atas).

### 2. Kloning Repositori
```bash
git clone <url-repository-ini>
cd ProjectAkhir
```

### 3. Buat Virtual Environment (Opsional namun Disarankan)
```bash
python -m venv venv
# Untuk Windows:
venv\Scripts\activate
# Untuk macOS/Linux:
source venv/bin/activate
```

### 4. Instal Dependensi
```bash
pip install -r requirement.txt
```

## Cara Menjalankan Projek

Setelah semua dependensi terinstal, jalankan perintah berikut di terminal:

```bash
python app.py
```

Aplikasi akan berjalan di `http://127.0.0.1:8050/`. Buka alamat tersebut di browser Anda untuk melihat dashboard.

## Struktur Folder
- `app.py`: Titik masuk utama aplikasi.
- `pages/`: Berisi file untuk setiap halaman dashboard.
- `src/`: Berisi komponen UI, logika pemrosesan data, dan model.
- `data/`: Penyimpanan dataset CSV.
- `assets/`: File CSS untuk styling.
- `notebooks/`: Proses analisis data dan pelatihan model (Jupyter Notebook).

## Tim Pengembang : 
1. Nur Istikomah, S.Pd. dari SMKN 1 Sukorejo
2. Zahrotul Janah, S.Kom, M.M. dari SMK Muhammadiyah 8 Siliragung
3. Moh Iskandar Maulana, S.ST dar SMKN 1 Lumajang

Project ini dibuat ketika melaksanakan pelatihan Pemorgraman Data Science BBPPMPV BOE Malang Tahun 2026
