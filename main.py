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
        print(f"{Color.RESET}{Color.BOLD}PENCARIAN, PENGURUTAN & FILTER ANTRIAN{Color.RESET}".center(60))
        print(f"{Color.RESET}Fitur Analisis dan Filtrasi Data Pasien{Color.RESET}".center(60))
        print(f"{Color.CYAN}{'=' * 60}{Color.RESET}")
        
        print(f"  {Color.CYAN}── Opsi Pengurutan (Sorting) ──{Color.RESET}")
        print(f"  [{Color.GREEN}1{Color.RESET}] Urut Alfabetis     (A-Z)")
        print(f"  [{Color.GREEN}2{Color.RESET}] Urut Urgensi       (Darurat → Normal)")
        print(f"  [{Color.GREEN}3{Color.RESET}] Urut Gabungan      (Darurat A-Z → Normal A-Z)")
        print()
        print(f"  {Color.CYAN}── Opsi Pencarian (Searching) ──{Color.RESET}")
        print(f"  [{Color.GREEN}4{Color.RESET}] Cari Pasien        (Nama / ID / Tanggal)")
        print()
        print(f"  {Color.CYAN}── Opsi Penyaringan (Filtering) ──{Color.RESET}")
        print(f"  [{Color.GREEN}5{Color.RESET}] Tampilkan Khusus Pasien Darurat")
        print(f"  [{Color.GREEN}6{Color.RESET}] Tampilkan Khusus Pasien Normal")
        print()
        print(f"  [{Color.RED}0{Color.RESET}] Kembali ke Menu Utama")
        print(f"{Color.CYAN}{'-' * 60}{Color.RESET}")
        
        pilihan = input(f"  Pilih menu [0-6]: {Color.BOLD}").strip()
        print(Color.RESET, end="")
        
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
            
        # ─── FITUR BARU: FILTER KATEGORI ───
        elif pilihan == '5':
            clear_screen()
            antrian.display_by_kategori("Darurat")
            input(f"\n{Color.CYAN}Tekan Enter untuk kembali...{Color.RESET}")
        elif pilihan == '6':
            clear_screen()
            antrian.display_by_kategori("Normal")
            input(f"\n{Color.CYAN}Tekan Enter untuk kembali...{Color.RESET}")
        # ────────────────────────────────────
        else:
            print(f"\n{Color.RED}❌ Pilihan tidak valid! Masukkan angka antara 0 sampai 6.{Color.RESET}")
            input(f"{Color.YELLOW}  Tekan [Enter] untuk mencoba lagi...{Color.RESET}")

# ─────────────────────────────────────────────────────────
# ALUR UTAMA PROGRAM
# ─────────────────────────────────────────────────────────
def main():
    antrian = PriorityQueue()
    
    # Load data lama dari CSV jika ada
    load_data(antrian)

    #Load fungsi login
    from interface import login_admin
    while True:
        clear_screen()
        # Jika fungsi login mengembalikan True, keluar dari loop login dan masuk ke aplikasi
        if login_admin():
            break

    
    while True:
        clear_screen()
        header_klinik()
        
        # Dashboard Statistik Terstandarisasi Warna
        print(f" STATS: [Menunggu: {Color.RED}{antrian.size()}{Color.RESET}] | [Pasien dilayani]: {Color.GREEN}{antrian.get_log_count()}{Color.RESET}]")
        print(f"{Color.CYAN}{'-' * 60}{Color.RESET}")
        
        display_menu()
        pilihan = input(f"Pilih menu [0-4]: {Color.BOLD}").strip()
        print(Color.RESET, end="") # Reset warna input utama
        
        if pilihan == '1':
            # ─── LOOPING MULTI-INPUT REGISTRASI PASIEN ───
            while True:
                clear_screen()
                print(f"\n{Color.CYAN}=== REGISTRASI PASIEN BARU ==={Color.RESET}\n")
                nama = input(f"  Nama Pasien : {Color.BOLD}").strip()
                print(Color.RESET, end="")
                if not nama:
                    print(f"\n{Color.RED}❌ Nama tidak boleh kosong!{Color.RESET}")
                    input(f"\n{Color.CYAN}  Tekan Enter untuk mencoba lagi...{Color.RESET}")
                    continue
                
                # 🛡️ BUG HANDLING: VERIFIKASI LOCK Y/N
                print(f"\n  {Color.YELLOW}[VERIFIKASI ADMIN]{Color.RESET}")
                print(f"  Apakah nama {Color.BOLD}'{nama}'{Color.RESET} sudah benar dan sesuai KTP/BPJS?")
                
                while True:
                    verif = input(f"  Konfirmasi [Y/N]: {Color.BOLD}").strip().lower()
                    print(Color.RESET, end="")
                    if verif in ['y', 'n']:
                        break
                    print(f"  {Color.RED}❌ Masukan salah. Ketik Y jika benar, atau N untuk membatalkan.{Color.RESET}")
                
                if verif == 'n':
                    print(f"\n{Color.RED}❌ Pendaftaran dibatalkan. Data tidak dimasukkan ke antrian.{Color.RESET}")
                    input(f"{Color.CYAN}  Tekan Enter untuk mengulang...{Color.RESET}")
                    continue # Mengulang loop registrasi dari awal (input nama lagi)
                    
                print(f"\n  {Color.YELLOW}Kategori Kondisi Pasien:{Color.RESET}")
                print(f"  [{Color.GREEN}1{Color.RESET}] Normal")
                print(f"  [{Color.GREEN}2{Color.RESET}] Darurat (Prioritas)")
                
                while True:
                    kat_input = input(f"  Pilih [1/2] : {Color.BOLD}").strip()
                    print(Color.RESET, end="")
                    if kat_input in ['1', '2']:
                        break
                    print(f"  {Color.RED}❌ Pilihan salah. Ketik 1 untuk Normal atau 2 untuk Darurat.{Color.RESET}")
                    
                kategori = "Darurat" if kat_input == '2' else "Normal"
                new_id = antrian.enqueue(nama, kategori)
                print(f"\n{Color.GREEN}✅ Pasien {Color.BOLD}{new_id}{Color.RESET}{Color.GREEN} berhasil terdaftar!{Color.RESET}")
                
                # ─── 🔁 PERTANYAAN INPUT ULANG (MULTI-INPUT LOCK) ───
                print(f"\n{Color.CYAN}{'-' * 45}{Color.RESET}")
                print("  Apakah ingin mendaftarkan pasien lain?")
                while True:
                    ulang = input(f"  Input lagi? [Y/N]: {Color.BOLD}").strip().lower()
                    print(Color.RESET, end="")
                    if ulang in ['y', 'n']:
                        break
                    print(f"  {Color.RED}❌ Masukan salah. Ketik Y untuk input lagi, atau N untuk kembali ke menu utama.{Color.RESET}")
                
                if ulang == 'n':
                    break # Keluar dari loop registrasi dan kembali ke Menu Utama
            # ───────────────────────────────────────────────────

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
            print(f"\n{Color.GREEN}Sampai jumpa kembali!{Color.RESET}\n")
            break

        else:
            # Bug Handling Utama: Menghentikan layar untuk memberikan feedback error
            print(f"\n{Color.RED}❌ Pilihan menu tidak tersedia! Masukkan angka antara 0 sampai 4.{Color.RESET}")
            input(f"{Color.YELLOW}  Tekan [Enter] untuk kembali ke menu utama...{Color.RESET}")

if __name__ == "__main__":
    main()