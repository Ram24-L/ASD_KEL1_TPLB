# main.py
# Proyek Akhir Algoritma & Struktur Data - Kelompok 1
# Ketua: Muhammad Ramdhan Maulana

import os
import time
from engine import PriorityQueue
from storage import load_data, save_data 
from interface import header_klinik, display_menu, animasi_panggil, Color

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ─────────────────────────────────────────────────────────
# SUBMENU: Fitur Pencarian & Pengurutan Pasien (Menu 4)
# ─────────────────────────────────────────────────────────
def menu_filter_search(antrian):
    while True:
        clear_screen()
        print(f"{Color.CYAN}{'=' * 60}")
        print(f"{Color.RESET}{Color.BOLD}PENCARIAN & PENGURUTAN ANTRIAN{Color.RESET}".center(60))
        print(f"{Color.RESET}{Color.CYAN}Fitur Analisis dan Filtrasi Data Pasien{Color.RESET}".center(60))
        print(f"{Color.CYAN}{'=' * 60}{Color.RESET}")
        
        print(f"  {Color.CYAN}── Opsi Pengurutan (Sorting) ──{Color.RESET}")
        print(f"  [{Color.GREEN}1{Color.RESET}] Urut Alfabetis     (A-Z)")
        print(f"  [{Color.GREEN}2{Color.RESET}] Urut Urgensi       (Darurat → Normal)")
        print(f"  [{Color.GREEN}3{Color.RESET}] Urut Gabungan      (Darurat A-Z → Normal A-Z)")
        print()
        print(f"  {Color.CYAN}── Opsi Pencarian (Searching) ──{Color.RESET}")
        print(f"  [{Color.GREEN}4{Color.RESET}] Cari Pasien        (Nama / ID / Tanggal)")
        print()
        print(f"  [{Color.RED}0{Color.RESET}] Kembali ke Menu Utama")
        print(f"{Color.CYAN}{'-' * 60}{Color.RESET}")
        
        pilihan = input(f"  Pilih menu [0-4]: {Color.BOLD}").strip()
        print(Color.RESET, end="") # Reset warna setelah user mengetik
        
        if pilihan == '0':
            break
        elif pilihan == '1':
            clear_screen()
            print(f"\n{Color.YELLOW}=== ANTRIAN ALFABETIS (A-Z) ==={Color.RESET}")
            antrian.display_sorted("nama")
            input(f"\n{Color.CYAN}Tekan Enter untuk kembali...{Color.RESET}")
        elif pilihan == '2':
            clear_screen()
            print(f"\n{Color.YELLOW}=== ANTRIAN BERDASARKAN URGENSI ==={Color.RESET}")
            antrian.display_sorted("kategori")
            input(f"\n{Color.CYAN}Tekan Enter untuk kembali...{Color.RESET}")
        elif pilihan == '3':
            clear_screen()
            print(f"\n{Color.YELLOW}=== ANTRIAN GABUNGAN (PRIORITAS & A-Z) ==={Color.RESET}")
            antrian.display_sorted("gabungan")
            input(f"\n{Color.CYAN}Tekan Enter untuk kembali...{Color.RESET}")
        elif pilihan == '4':
            clear_screen()
            print(f"\n{Color.CYAN}=== PENCARIAN DATA PASIEN ==={Color.RESET}\n")
            keyword = input(f"  Masukkan Nama / ID / Tanggal Pasien: {Color.BOLD}").strip()
            print(Color.RESET, end="")
            if keyword:
                antrian.search_pasien(keyword)
            else:
                print(f"\n{Color.RED}❌ Keyword pencarian tidak boleh kosong!{Color.RESET}")
            input(f"\n{Color.CYAN}Tekan Enter untuk kembali...{Color.RESET}")
        else:
            # Bug Handling: Input selain 0-4 terkunci di sini sebelum layar dibersihkan
            print(f"\n{Color.RED}❌ Pilihan tidak valid! Masukkan angka antara 0 sampai 4.{Color.RESET}")
            input(f"{Color.YELLOW}  Tekan [Enter] untuk mencoba lagi...{Color.RESET}")

# ─────────────────────────────────────────────────────────
# ALUR UTAMA PROGRAM
# ─────────────────────────────────────────────────────────
def main():
    antrian = PriorityQueue()
    
    # Load data lama dari CSV jika ada
    load_data(antrian)
    
    while True:
        clear_screen()
        header_klinik()
        
        # Dashboard Statistik Terstandarisasi Warna
        print(f" STATS: [Menunggu: {Color.RED}{antrian.size()}{Color.RESET}] | [Total Riwayat Hari Ini: {Color.GREEN}{antrian.get_log_count()}{Color.RESET}]")
        print(f"{Color.CYAN}{'-' * 60}{Color.RESET}")
        
        display_menu()
        pilihan = input(f"Pilih menu [0-4]: {Color.BOLD}").strip()
        print(Color.RESET, end="") # Reset warna input utama
        
        if pilihan == '1':
            clear_screen()
            print(f"\n{Color.CYAN}=== REGISTRASI PASIEN BARU ==={Color.RESET}\n")
            nama = input(f"  Nama Pasien : {Color.BOLD}").strip()
            print(Color.RESET, end="")
            if not nama:
                print(f"\n{Color.RED}❌ Nama tidak boleh kosong!{Color.RESET}")
                input(f"\n{Color.CYAN}  Tekan Enter untuk kembali...{Color.RESET}")
                continue
            
            # ─── 🛡️ BUG HANDLING: VERIFIKASI LOCK Y/N ───
            print(f"\n  {Color.YELLOW}[VERIFIKASI ADMIN]{Color.RESET}")
            print(f"  Apakah nama {Color.BOLD}'{nama}'{Color.RESET} sudah benar dan sesuai?")
            
            while True:
                verif = input(f"  Konfirmasi [Y/N]: {Color.BOLD}").strip().lower()
                print(Color.RESET, end="")
                if verif in ['y', 'n']:
                    break
                print(f"  {Color.RED}❌ Masukan salah. Ketik Y jika benar, atau N untuk membatalkan.{Color.RESET}")
            
            if verif == 'n':
                print(f"\n{Color.RED}❌ Pendaftaran dibatalkan. Data tidak dimasukkan ke antrian.{Color.RESET}")
                input(f"{Color.CYAN}  Tekan Enter untuk kembali...{Color.RESET}")
                continue # Menggagalkan alur dan kembali ke menu utama
            # ─────────────────────────────────────────────
                
            print(f"\n  {Color.YELLOW}Kategori Kondisi Pasien:{Color.RESET}")
            print(f"  [{Color.GREEN}1{Color.RESET}] Normal")
            print(f"  [{Color.GREEN}2{Color.RESET}] Darurat (Prioritas)")
            
            while True:
                kat_input = input(f"  Pilih [1/2] : {Color.BOLD}").strip()
                print(Color.RESET, end="")
                if kat_input in ['1', '2']:
                    break
                print(f"  {Color.RED}❌ Pilihan salah. Ketik 1 untuk Normal or 2 untuk Darurat.{Color.RESET}")
                
            kategori = "Darurat" if kat_input == '2' else "Normal"
            new_id = antrian.enqueue(nama, kategori)
            input(f"\n{Color.GREEN}✅ Pasien {Color.BOLD}{new_id}{Color.RESET}{Color.GREEN} berhasil terdaftar! Tekan Enter...{Color.RESET}")

        elif pilihan == '2':
            clear_screen()
            pasien_dipanggil = antrian.dequeue()
            if pasien_dipanggil:
                animasi_panggil(pasien_dipanggil)
            else:
                print(f"\n  {Color.RED}Antrian kosong! Tidak ada pasien di ruang tunggu.{Color.RESET}")
                input(f"\n{Color.CYAN}  Tekan Enter...{Color.RESET}")

        elif pilihan == '3':
            clear_screen()
            print(f"\n{Color.CYAN}DAFTAR ANTRIAN AKTIF{Color.RESET}".center(52))
            antrian.display_all()
            input(f"\n{Color.CYAN}Tekan Enter untuk kembali...{Color.RESET}")

        elif pilihan == '4':
            menu_filter_search(antrian)

        elif pilihan == '0':
            save_data(antrian)
            print(f"\n{Color.GREEN}💾 Data berhasil disimpan secara permanen ke database CSV. Sampai jumpa!{Color.RESET}\n")
            break

        else:
            # Bug Handling Utama: Menghentikan layar untuk memberikan feedback error
            print(f"\n{Color.RED}❌ Pilihan menu tidak tersedia! Masukkan angka antara 0 sampai 4.{Color.RESET}")
            input(f"{Color.YELLOW}  Tekan [Enter] untuk kembali ke menu utama...{Color.RESET}")

if __name__ == "__main__":
    main()