\# MPK-AI: Internal Audit Assistant (Source Code Only)



MPK-AI adalah sistem asisten audit internal berbasis \*\*Local Large Language Model (LLM)\*\* dengan pendekatan \*\*Retrieval-Augmented Generation (RAG)\*\*. Proyek ini dikembangkan selama kegiatan magang di PT Mohairson Pawan Khatulistiwa (MPK).



Sistem ini dirancang untuk otomasi pencarian informasi, ekstraksi data dokumen, serta tanya-jawab berbasis basis data internal perusahaan secara \*\*offline\*\*, menjaga kerahasiaan data tetap berada di infrastruktur lokal.



---



\## ✨ Fitur Utama



\- \*\*Offline AI Assistant\*\*: Menggunakan Local LLM (format GGUF) untuk privasi data maksimal.

\- \*\*RAG-based QA\*\*: Menjawab pertanyaan berdasarkan konteks dokumen spesifik, bukan sekadar basis pengetahuan umum model.

\- \*\*PDF Parsing Pipeline\*\*: Integrasi ekstraksi teks otomatis dari dokumen audit.

\- \*\*Interactive Dashboard\*\*: Interface pengguna yang intuitif dibangun dengan Streamlit.

\- \*\*Audit-Ready Logging\*\*: Output jawaban yang terstruktur untuk kebutuhan dokumentasi audit.



---



\## 📁 Struktur Proyek



```bash

mpk-ai-source/

├── app.py                # Entry point aplikasi (Streamlit UI \& Logic)

├── Modelfile.txt         # Konfigurasi model lokal (Ollama)

├── requirements.txt      # Daftar dependency Python

├── README.md             # Dokumentasi proyek

├── data/                 # Placeholder (dokumen perusahaan tidak disertakan)

└── models/               # Placeholder (file model GGUF tidak disertakan)

```



---



\## 🔒 Keamanan \& Kerahasiaan Data



\*\*Penting:\*\* Repository ini hanya berisi \*source code\* inti untuk tujuan dokumentasi akademik. Sesuai dengan kebijakan kerahasiaan perusahaan (NDA), repositori ini \*\*TIDAK\*\* menyertakan:



\* Dokumen PDF internal perusahaan

\* Dataset sensitif atau arsip audit

\* File model `.gguf` berukuran besar



Folder `data/` dan `models/` hanya disediakan sebagai placeholder struktur sistem.



---



\## 🛠️ Persyaratan Sistem



\* \*\*Python\*\*: 3.9 atau lebih tinggi

\* \*\*Runtime\*\*: Ollama (untuk menjalankan LLM lokal)

\* \*\*Library Utama\*\*: `streamlit`, `llama-index`, `pypdf`



---



\## 🚀 Cara Menjalankan



1\. \*\*Clone Repository\*\*



```bash

git clone https://github.com/USERNAME/mpk-ai-source.git

cd mpk-ai-source

```



2\. \*\*Instalasi Dependency\*\*



```bash

pip install -r requirements.txt

```



3\. \*\*Persiapkan Model\*\*



Pastikan Ollama sudah terinstal dan model yang didefinisikan di `Modelfile.txt` sudah tersedia.



4\. \*\*Jalankan Aplikasi\*\*



```bash

streamlit run app.py

```



---



\## 💡 Tips Tambahan



\* Buat file `requirements.txt` dengan:



```bash

pip freeze > requirements.txt

```



\* Jika memungkinkan (tanpa melanggar NDA), tambahkan screenshot UI dengan data dummy agar repository lebih menarik.



---



\## 👤 Author



Developed by \*\*Muhammad Radhi\*\*

Internship Project – PT Mohairson Pawan Khatulistiwa (MPK)

2026

