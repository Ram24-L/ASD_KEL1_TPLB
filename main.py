# main.py
# Proyek Akhir Algoritma & Struktur Data - Kelompok 1
# Ketua: Muhammad Ramdhan Maulana

import os
from engine import PriorityQueue
from storage import load_data, save_data 
from interface import header_klinik, display_menu, animasi_panggil, Color

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Inisialisasi struktur data utama (Linked List Based Priority Queue)
    antrian = PriorityQueue()
    
    # Load data dari CSV saat program dimulai (Tugas Anggota 1)
    load_data(antrian)
    
    while True:
        clear_screen()
        header_klinik() # Menampilkan banner "Klinik Dokter"
        
        # Pemanis: Statistik Ringkas
        wait_count = antrian.size()
        log_count = antrian.get_log_count()
        print(f"  \033[94mANTREAN AKTIF: {wait_count}\033[0m | \033[92mTOTAL DILAYANI: {log_count}\033[0m") # Sudah ada warna
        print("\033[96m" + "─" * 60 + "\033[0m")
        
        display_menu()
        pilihan = input("\nPilih menu [0-5]: ")

        if pilihan == '1':
            # Registrasi Pasien
            nama = input("Nama Pasien: ")
            print("Kategori: 1. Normal | 2. Darurat (Prioritas)")
            kat_input = input("Pilih [1/2]: ")
            kategori = "Darurat" if kat_input == '2' else "Normal"
            
            # Memasukkan ke Queue 
            new_id = antrian.enqueue(nama, kategori)
            input(f"\n{Color.GREEN}✅ Pasien {Color.BOLD}{new_id}{Color.RESET}{Color.GREEN} berhasil terdaftar! Tekan Enter...{Color.RESET}")

        elif pilihan == '2':
            # Panggil Pasien (Dequeue)
            pasien_dipanggil = antrian.dequeue()
            if pasien_dipanggil:
                animasi_panggil(pasien_dipanggil)
            else:
                print("\nAntrian kosong!")
                input("Tekan Enter...")

        elif pilihan == '3':
            # Lihat Antrian (Display & Sorting)
            antrian.display_all()
            input("\nTekan Enter untuk kembali...")

        elif pilihan == '4':
            # Cari Pasien (Searching)
            keyword = input("Masukkan Nama/ID yang dicari: ")
            antrian.search_pasien(keyword)
            input("\nTekan Enter...")

        elif pilihan == '5':
            # Riwayat Pelayanan (Log Stack)
            antrian.show_logs()
            input("\nTekan Enter...")

        elif pilihan == '0':
            # Simpan data sebelum keluar (Tugas Anggota 1)
            save_data(antrian)
            print(f"\n{Color.GREEN}💾 Data berhasil disimpan. Sampai jumpa!{Color.RESET}")
            break
        else:
            print(f"\n{Color.RED}❌ Pilihan tidak valid!{Color.RESET}")
            input(f"{Color.YELLOW}Tekan Enter untuk melanjutkan...{Color.RESET}")

if __name__ == "__main__":
    main()