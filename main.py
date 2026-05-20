# main.py
# Proyek Akhir Algoritma & Struktur Data - Kelompok 1
# Ketua: Muhammad Ramdhan Maulana

import os
from engine import PriorityQueue
from storage import load_data, save_data
from interface import header_klinik, display_menu, animasi_panggil

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ─────────────────────────────────────────────────────────
# SUBMENU: Lihat Antrian (sort + search terintegrasi)
# -------------------------------------------------------
def menu_lihat_antrian(antrian):
    sort_aktif = 'waktu'
    LABEL = {
        'waktu'    : 'Waktu Daftar (default)',
        'alpha'    : 'Alfabetis A-Z',
        'urgency'  : 'Urgensi (Darurat -> Normal)',
        'combined' : 'Urgensi + Alfabetis',
    }

    # Auto-tampilkan data urut waktu saat pertama kali masuk
    antrian.display_sorted('waktu')

    while True:
        print('\n' + '=' * 55)
        print('  LIHAT ANTRIAN'.center(55))
        print('=' * 55)
        print(f'  Sort aktif : [ {LABEL[sort_aktif]} ]')
        print('-' * 55)
        print('  -- Ganti Tampilan --')
        print('  [1] Waktu Daftar   (Pertama -> Terbaru)  *default*')
        print('  [2] Alfabetis      (A-Z)')
        print('  [3] Urgensi        (Darurat -> Normal)')
        print('  [4] Gabungan       (Darurat A-Z -> Normal A-Z)')
        print()
        print('  -- Aksi Lain --')
        print('  [5] Cari Pasien    (Nama / ID / Tanggal)')
        print('  [6] Refresh tampilan (sort saat ini)')
        print()
        print('  [0] Kembali ke Menu Utama')
        print('-' * 55)
        pilihan = input('  Pilih [0-6]: ').strip()

        if pilihan == '1':
            sort_aktif = 'waktu'
            antrian.display_sorted('waktu')
        elif pilihan == '2':
            sort_aktif = 'alpha'
            antrian.display_sorted('alpha')
        elif pilihan == '3':
            sort_aktif = 'urgency'
            antrian.display_sorted('urgency')
        elif pilihan == '4':
            sort_aktif = 'combined'
            antrian.display_sorted('combined')
        elif pilihan == '5':
            _cari_pasien_inline(antrian)
        elif pilihan == '6':
            antrian.display_sorted(sort_aktif)
        elif pilihan == '0':
            break
        else:
            print('\n  Pilihan tidak valid!')


def _cari_pasien_inline(antrian):
    print('\n' + '-' * 55)
    print('  CARI PASIEN')
    print('  Bisa cari berdasarkan:')
    print("    Nama (sebagian)  ->  'michael'   (Michael Flow & Michael Bart)")
    print("    ID pasien        ->  'P007'")
    print("    Tanggal/Waktu    ->  '2026-05-19'")
    print('-' * 55)
    keyword = input('  Kata kunci: ').strip()
    if keyword:
        antrian.search_pasien(keyword)
    else:
        print('\n  Kata kunci tidak boleh kosong.')


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
        header_klinik()

        # Statistik ringkas
        print(f"  STATS: [Menunggu: {antrian.size()}] | [Selesai: {antrian.get_log_count()}]")
        print("-" * 60)

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

            new_id = antrian.enqueue(nama, kategori)
            print(f"\n  ✅ Pasien '{nama}' terdaftar sebagai [{kategori}] dengan ID {new_id}")
            input("\n  Tekan Enter...")

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
            print("\n  Data berhasil disimpan. Sampai jumpa! 👋")
            break

        else:
            print("\n  Pilihan tidak valid!")
            input("  Tekan Enter...")

if __name__ == "__main__":
    main()
