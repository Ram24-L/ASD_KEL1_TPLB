# storage.py
# Modul File Handling (CSV) - Kelompok 1

import csv
import os

# Nama file penyimpanan
FILE_ANTRIAN = 'antrian.csv'
FILE_LOG = 'log_pelayanan.csv'

def load_data(queue_obj):
    """Membaca data dari CSV ke dalam struktur data Linked List saat start."""
    # Load Antrian Aktif
    if os.path.exists(FILE_ANTRIAN):
        try:
            with open(FILE_ANTRIAN, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Kita masukkan kembali ke queue
                    # Gunakan enqueue tanpa print agar tidak memenuhi layar saat start
                    queue_obj.enqueue(row['nama'], row['kategori'])
            print(f"[STORAGE] Berhasil memuat antrian dari {FILE_ANTRIAN}")
        except Exception as e:
            print(f"[ERROR] Gagal membaca file antrian: {e}")

    # Load Log Pelayanan (Opsional untuk Stack)
    # Catatan: Karena logs di engine.py adalah list, kita tinggal append
    if os.path.exists(FILE_LOG):
        try:
            with open(FILE_LOG, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Membuat objek dummy/Node untuk log
                    from engine import Node
                    node_log = Node(row['id'], row['nama'], row['kategori'])
                    queue_obj.logs.append(node_log)
        except Exception as e:
            print(f"[ERROR] Gagal membaca log: {e}")

def save_data(queue_obj):
    """Menyimpan data dari Linked List ke dalam CSV saat exit."""
    # 1. Simpan Antrian yang masih menunggu
    try:
        with open(FILE_ANTRIAN, mode='w', newline='') as file:
            fieldnames = ['id', 'nama', 'kategori']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            curr = queue_obj.head
            while curr:
                writer.writerow({
                    'id': curr.id_pasien,
                    'nama': curr.nama,
                    'kategori': curr.kategori
                })
                curr = curr.next
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan antrian: {e}")

    # 2. Simpan Log Pelayanan (History)
    try:
        with open(FILE_LOG, mode='w', newline='') as file:
            fieldnames = ['id', 'nama', 'kategori']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for p in queue_obj.logs:
                writer.writerow({
                    'id': p.id_pasien,
                    'nama': p.nama,
                    'kategori': p.kategori
                })
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan log: {e}")