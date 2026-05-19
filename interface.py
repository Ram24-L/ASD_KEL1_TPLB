# interface.py
# Modul Tampilan / UI - Kelompok 1

import time
import os

def header_klinik():
    """Menampilkan banner utama aplikasi."""
    print("=" * 60)
    print("SISTEM ANTRIAN KLINIK".center(60))
    print("Pelayanan Kesehatan Cepat & Responsif".center(60))
    print("=" * 60)

def display_menu():
    """Menampilkan daftar pilihan menu dengan format yang rapi."""
    print(" [1] Registrasi Pasien Baru")
    print(" [2] Panggil Pasien Berikutnya")
    print(" [3] Lihat & Cari Antrian")
    print(" [4] Riwayat Pelayanan (Log)")
    print(" [0] Keluar & Simpan Data")
    print("-" * 60)

def animasi_panggil(pasien):
    """Memberikan efek visual saat memanggil pasien."""
    print("\n" + "." * 30)
    print("📢 MENGHUBUNGKAN KE SPEAKER RUANG TUNGGU...")
    time.sleep(1)
    print("📢 MENGAMBIL DATA ANTRIAN TERDEPAN...")
    time.sleep(1)
    
    # Header khusus pemanggilan
    print("\n" + "*" * 60)
    print("             PASIEN HARAP MENUJU RUANG DOKTER             ")
    print("*" * 60)
    print(f"  ID PASIEN : {pasien.id_pasien}")
    print(f"  NAMA      : {pasien.nama.upper()}")
    print(f"  STATUS    : {pasien.kategori.upper()}")
    
    if pasien.kategori == "Darurat":
        print("  CATATAN   : SEGERA BERIKAN TINDAKAN MEDIS!")
    else:
        print("  CATATAN   : Mohon menunggu giliran dengan tertib.")
        
    print("*" * 60)
    input("\nTekan [Enter] setelah pasien selesai dilayani...")
    print("\n✅ Pasien telah selesai. Data dipindahkan ke Riwayat.")
    time.sleep(1)

def tabel_kosong():
    """Tampilan jika data tidak ditemukan."""
    print("\n" + "!" * 40)
    print("  DATA TIDAK DITEMUKAN / ANTRIAN KOSONG  ")
    print("!" * 40)