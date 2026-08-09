⚡ Dashboard Monitoring Material Gudang - PLN UP3 Padang
Dashboard monitoring real-time untuk arus material gudang PLN UP3, dibangun dengan Streamlit dan Plotly. Menampilkan tiga modul dalam satu halaman: Material Masuk (SP2B), Material Return, dan Material Keluar.

🖥️ Fitur
Material Masuk (SP2B) — frekuensi pasokan, total volume masuk, dan Top 10 vendor/pengantar material paling dominan.
Material Return — frekuensi pengembalian, total volume return, dan Top 10 material yang paling sering di-return.
Material Keluar — frekuensi pengeluaran, total volume keluar, dan Top 10 material yang paling sering dikeluarkan.
Data ditarik otomatis (real-time) dari Google Sheets, dengan cache 10 menit agar tidak membebani request.

📁 Struktur Project
.
├── dashboard.py         # Aplikasi utama Streamlit
├── requirements.txt     # Daftar dependency Python
└── README.md            # Dokumentasi project

⚙️ Cara Menjalankan Secara Lokal
Clone repo ini:
bash
   git clone <url-repo-kamu>
   cd <nama-folder-repo>
(Opsional) Buat virtual environment:
bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
Install dependency:
bash
   pip install -r requirements.txt
   
Jalankan dashboard:
bash

   streamlit run dashboard.py
Buka browser ke http://localhost:8501.

URL publik yang dihasilkan: https://dashboard-monitoring-material-pln-up3-padang.streamlit.app/

📊 Sumber Data
Data diambil langsung dari Google Sheets (format CSV export), dengan tiga sheet terpisah berdasarkan GID:

Material Masuk (SP2B)
Material Return
Material Keluar

🛠️ Tech Stack
Streamlit — framework web app
Plotly — visualisasi chart interaktif
Pandas & NumPy — pengolahan data
