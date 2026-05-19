# interface.py
# Modul Tampilan / UI - Kelompok 1

import time
import os

# Definisi Warna ANSI
class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    BLUE = '\033[94m'

def header_klinik():
    """Menampilkan banner utama aplikasi dengan tulisan putih dan pembatas cyan."""
    print(f"{Color.CYAN}{'=' * 60}")
    print(f"{Color.RESET}SISTEM ANTRIAN KLINIK{Color.RESET}".center(60))
    print(f"{Color.RESET}Pelayanan Kesehatan Cepat & Responsif{Color.RESET}".center(60))
    print(f"{Color.CYAN}{'=' * 60}{Color.RESET}")

def display_menu():
    """Menampilkan daftar pilihan menu dengan format yang rapi."""
    menu_items = [
        "Registrasi Pasien Baru",
        "Panggil Pasien Berikutnya",
        "Lihat Antrian Aktif (Fix Order)",
        "Pencarian & Pengurutan Pasien",
        "Keluar & Simpan Data"
    ]

    '''Memberikan warna untuk nomor pada menu.'''
    for i, item in enumerate(menu_items):
        # Jika item terakhir (Keluar & Simpan Data), set nomornya menjadi 0
        if i == len(menu_items) - 1:
            num_str = f"[{Color.RED}0{Color.RESET}]"
        else:
            num_str = f"[{Color.GREEN}{i+1}{Color.RESET}]"
            
        print(f"  {num_str} {item}")
    print(f"{Color.CYAN}{'-' * 60}{Color.RESET}")

def loading_spinner(duration=1, message="Memproses"):

    """Animasi spinner sederhana."""
    symbols = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{Color.YELLOW} {symbols[i % 4]} {message}...{Color.RESET}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print("\r" + " " * (len(message) + 10) + "\r", end="")

def animasi_panggil(pasien):
    
    """Memberikan efek visual saat memanggil pasien."""
    loading_spinner(1.5, "MENGHUBUNGKAN KE SPEAKER")
    
    '''Menentukan warna berdasarkan kategori pasien'''
    border_color = Color.RED if pasien.kategori == "Darurat" else Color.GREEN
    text_style = Color.BOLD + Color.RED if pasien.kategori == "Darurat" else Color.BOLD + Color.GREEN
    inner_width = 58

    print("\n" + border_color + "╔" + "═" * inner_width + "╗")
    print("║" + "PASIEN HARAP MENUJU RUANG DOKTER".center(inner_width) + "║")
    print("╠" + "═" * inner_width + "╣" + Color.RESET)
    
    # Baris data dengan padding dinamis agar bingkai kanan (║) tetap sejajar
    line_id = f"  ID PASIEN : {pasien.id_pasien}"
    print(f"{border_color}║  {Color.BOLD}ID PASIEN :{Color.RESET} {pasien.id_pasien}" + " " * (inner_width - len(line_id)) + f"{border_color}║")
    
    line_nama = f"  NAMA      : {pasien.nama.upper()}"
    print(f"{border_color}║  {Color.BOLD}NAMA      :{Color.RESET} {pasien.nama.upper()}" + " " * (inner_width - len(line_nama)) + f"{border_color}║")
    
    line_status = f"  STATUS    : {pasien.kategori.upper()}"
    print(f"{border_color}║  {Color.BOLD}STATUS    :{Color.RESET} {text_style}{pasien.kategori.upper()}{Color.RESET}" + 
          " " * (inner_width - len(line_status)) + f"{border_color}║")
    
    if pasien.kategori == "Darurat":
        msg = "  ⚠ PERINGATAN: SEGERA BERIKAN TINDAKAN MEDIS!"
        print(f"{border_color}║{Color.RED}{msg}{Color.RESET}" + " " * (inner_width - len(msg)) + f"{border_color}║")
    else:
        msg = "  i CATATAN: Mohon menunggu giliran dengan tertib."
        print(f"{border_color}║{Color.BLUE}{msg}{Color.RESET}" + " " * (inner_width - len(msg)) + f"{border_color}║")
        
    print(border_color + "╚" + "═" * inner_width + "╝" + Color.RESET)
    
    input(f"\n{Color.YELLOW}Tekan [Enter] setelah pasien selesai dilayani...{Color.RESET}")
    print(f"\n{Color.GREEN}✅ Pasien telah selesai. Data dipindahkan ke Riwayat.{Color.RESET}")
    time.sleep(1)

def tabel_kosong():
    """Tampilan jika data tidak ditemukan."""
    print(f"\n{Color.RED}┌────────────────────────────────────────┐")
    print("│  DATA TIDAK DITEMUKAN / ANTRIAN KOSONG │")
    print(f"└────────────────────────────────────────┘{Color.RESET}")