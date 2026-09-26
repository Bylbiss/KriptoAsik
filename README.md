# 🔐 Aplikasi Kriptografi

Aplikasi web interaktif untuk belajar dan menerapkan berbagai algoritma kriptografi klasik dan modern.

## 📋 Fitur Utama

### 🔢 Algoritma Tersedia

1. **Caesar Cipher** - Substitusi sederhana dengan pergeseran karakter
2. **Rail Fence Cipher** - Transposisi dengan pola zigzag
3. **Vernam Cipher (OTP)** - One-Time Pad dengan operasi XOR
4. **Blowfish Cipher** - Block cipher modern yang aman
5. **Super Enkripsi** - Kombinasi 4 algoritma dengan urutan yang dapat dikonfigurasi

### ✨ Fitur Tambahan

- **Visualisasi Proses** - Langkah demi langkah detail algoritma
- **Konfigurasi Fleksibel** - Atur urutan algoritma di Super Enkripsi
- **Master Key System** - Satu kunci untuk semua algoritma di Super Enkripsi

## 🚀 Cara Menjalankan

### Prerequisites

- Python 3.8 atau lebih baru
- pip (package manager)

### Instalasi

1. Clone atau download project ini
2. Buka terminal/command prompt di folder project
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Menjalankan Aplikasi

```bash
streamlit run Kriptografi/app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

## 📁 Struktur Project

```
KriptoAsik/
├── Kriptografi/
│   ├── app.py                 # Main aplikasi Streamlit
│   ├── caesar.py             # Implementasi Caesar Cipher
│   ├── rail_fence.py         # Implementasi Rail Fence Cipher
│   ├── vernam.py             # Implementasi Vernam Cipher (OTP)
│   ├── blowfish.py           # Implementasi Blowfish Cipher
│   ├── super_enkripsi.py     # Implementasi Super Enkripsi
│   └── session_manager.py    # Modul lama, tidak digunakan oleh aplikasi
├── requirements.txt          # Dependencies Python
└── README.md                # Dokumentasi ini
```

## 🎯 Cara Penggunaan

### Mode Individual

1. Pilih algoritma dari sidebar
2. Pilih mode: Enkripsi atau Dekripsi
3. Input teks secara manual
4. Masukkan kunci yang sesuai
5. Klik tombol proses untuk melihat hasil dan visualisasi

### Super Enkripsi

1. Pilih "Super Enkripsi" dari menu
2. Input teks secara manual
3. Masukkan Master Key
4. Atur urutan 4 algoritma sesuai keinginan
5. Lihat preview kunci turunan dan urutan proses
6. Proses untuk melihat hasil langkah demi langkah

## 🔧 Konfigurasi Super Enkripsi

Super Enkripsi menggunakan sistem **derivasi kunci** dari satu Master Key:

- **Caesar**: `sum(ASCII) mod 26`
- **Rail Fence**: `len(key) mod 5 + 2` (2-6 rails)
- **Vernam**: Key asli (diulang sesuai panjang teks)
- **Blowfish**: `MD5(key)[:16]`

## 👥 Tim Pengembang

- **Bylbiss El Haqqie** (123240003)
- **Muhammad Restu Firmansyah** (123240050)
- **Alifah Chairul Munawar** (123240234)

## 📚 Dependencies

- `streamlit` - Framework web app
- `pandas` - Manipulasi data dan visualisasi grid
- `pycryptodome` - Library kriptografi untuk Blowfish

## 🛠️ Troubleshooting

### Error Import Module

Pastikan semua dependencies sudah terinstall:

```bash
pip install -r requirements.txt
```

### Error Blowfish

Jika ada error dengan Blowfish, pastikan `pycryptodome` terinstall:

```bash
pip install pycryptodome
```

### Port Already in Use

Jika port 8501 sudah digunakan, gunakan port lain:

```bash
streamlit run Kriptografi/app.py --server.port 8502
```

## 📝 Catatan

- Aplikasi tidak menyimpan riwayat proses.
- Blowfish menggunakan mode ECB untuk kesederhanaan (tidak direkomendasikan untuk data sensitif real)
