# main.py
# Proyek Akhir Algoritma & Struktur Data - Kelompok 1
# Ketua: Muhammad Ramdhan Maulana

import os
from engine import PriorityQueue
from storage import load_data, save_data 
from interface import header_klinik, display_menu, animasi_panggil, Color

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ─────────────────────────────────────────────────────────
# SUBMENU: Lihat Antrian (sort + search terintegrasi)
# ─────────────────────────────────────────────────────────
def menu_lihat_antrian(antrian):
    while True:
        clear_screen()
        print("\n" + "=" * 50)
        print("  LIHAT ANTRIAN".center(50))
        print("=" * 50)
        print("  ── Tampilan ──")
        print("  [1] Urutan Asli        (Prioritas Aktif)")
        print("  [2] Urut Alfabetis     (A-Z)")
        print("  [3] Urut Urgensi       (Darurat → Normal)")
        print("  [4] Gabungan           (Darurat A-Z → Normal A-Z)")
        print()
        print("  ── Pencarian ──")
        print("  [5] Cari Pasien        (Nama / ID / Tanggal)")
        print()
        print("  [0] Kembali ke Menu Utama")
        print("-" * 50)
        pilihan = input("  Pilih [0-5]: ").strip()

        if pilihan == '1':
            antrian.display_all()
            input("\nTekan Enter untuk kembali ke submenu...")
        elif pilihan == '2':
            antrian.display_sorted('alpha')
            input("\nTekan Enter untuk kembali ke submenu...")
        elif pilihan == '3':
            antrian.display_sorted('urgency')
            input("\nTekan Enter untuk kembali ke submenu...")
        elif pilihan == '4':
            antrian.display_sorted('combined')
            input("\nTekan Enter untuk kembali ke submenu...")
        elif pilihan == '5':
            _cari_pasien_inline(antrian)
        elif pilihan == '0':
            break
        else:
            print("\n  Pilihan tidak valid!")
            input("  Tekan Enter...")

def _cari_pasien_inline(antrian):
    """Fitur search yang muncul di dalam submenu Lihat Antrian."""
    print("\n" + "-" * 50)
    print("  CARI PASIEN")
    print("  Bisa cari berdasarkan:")
    print("    • Nama (sebagian) → 'michael' → Michael Flow & Michael Bart")
    print("    • ID pasien       → 'P007'")
    print("    • Tanggal/Waktu   → '2026-05-19'")
    print("-" * 50)
    keyword = input("  Kata kunci: ").strip()
    if keyword:
        antrian.search_pasien(keyword)
    else:
        print("\n  Kata kunci tidak boleh kosong.")
    input("\nTekan Enter untuk kembali ke submenu...")

# ─────────────────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────────────────
def main():
    # Inisialisasi struktur data utama (Linked List Based Priority Queue)
    antrian = PriorityQueue()

    # Load data dari CSV saat program dimulai
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
        pilihan = input("\nPilih menu [0-4]: ").strip()

        if pilihan == '1':
            # Registrasi Pasien
            clear_screen()
            print("\n" + "=" * 50)
            print("  REGISTRASI PASIEN BARU".center(50))
            print("=" * 50)
            nama = input("  Nama Pasien : ").strip()
            if not nama:
                print("\n  Nama tidak boleh kosong!")
                input("  Tekan Enter...")
                continue
            print("  Kategori    : 1. Normal  |  2. Darurat (Prioritas)")
            kat_input = input("  Pilih [1/2] : ").strip()
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
                print("\n  Antrian kosong! Tidak ada pasien yang perlu dipanggil.")
                input("  Tekan Enter...")

        elif pilihan == '3':
            # Lihat Antrian → submenu sort + search terintegrasi
            menu_lihat_antrian(antrian)

        elif pilihan == '4':
            # Riwayat Pelayanan (Log Stack)
            clear_screen()
            antrian.show_logs()
            input("\nTekan Enter untuk kembali...")

        elif pilihan == '0':
            # Simpan data sebelum keluar
            save_data(antrian)
            print(f"\n{Color.GREEN}💾 Data berhasil disimpan. Sampai jumpa!{Color.RESET}")
            break

        else:
            print(f"\n{Color.RED}❌ Pilihan tidak valid!{Color.RESET}")
            input(f"{Color.YELLOW}Tekan Enter untuk melanjutkan...{Color.RESET}")

if __name__ == "__main__":
    main()
