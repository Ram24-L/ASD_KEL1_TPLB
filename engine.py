#=============================================
#               Engine.py
#      Pusat struktur data program
#=============================================

import datetime

class Node:
    def __init__(self, id_pasien, nama, keluhan, jam_masuk, kategori):
        self.id_pasien = id_pasien
        self.nama = nama
        self.keluhan = keluhan
        self.jam_masuk = jam_masuk
        self.jam_diproses = "-"  # Akan diisi saat dequeue (dipanggil)
        self.kategori = kategori # "Darurat" atau "Normal"
        self.next = None

class PriorityQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self._count_total = 0 # Untuk generator ID unik
        self.logs = []        # Stack untuk riwayat pelayanan

    def is_empty(self):
        return self.head is None

    def size(self):
        """Menghitung jumlah antrian aktif saat ini."""
        count = 0
        curr = self.head
        while curr:
            count += 1
            curr = curr.next
        return count

    def enqueue(self, nama, keluhan, jam_masuk, kategori):
        """Menambah pasien ke antrian dengan logika Priority."""
        self._count_total += 1
        new_id = f"P{self._count_total:03d}"
        new_node = Node(new_id, nama, keluhan, jam_masuk, kategori)

        # LOGIKA PRIORITY:
        if self.is_empty():
            self.head = self.tail = new_node
        elif kategori == "Darurat":
            # Pasien darurat langsung disisipkan ke paling depan (Head)
            new_node.next = self.head
            self.head = new_node
        else:
            # Pasien normal masuk ke paling belakang (Tail)
            self.tail.next = new_node
            self.tail = new_node
            
        return new_id

    def dequeue(self):
        """Memanggil pasien terdepan dan mencatat waktu proses."""
        if self.is_empty():
            return None
        
        # Ambil data dari Head
        temp = self.head
        self.head = self.head.next
        
        if self.head is None:
            self.tail = None
            
        # Catat jam diproses (Pemanis)
        temp.jam_diproses = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Masukkan ke Log (Stack: Data terbaru di posisi paling atas/index 0)
        self.logs.insert(0, temp)
        return temp

    def display_all(self):
        """Menampilkan antrian aktif dalam bentuk tabel."""
        if self.is_empty():
            print("\n[!] Antrian saat ini kosong.")
            return

        print("\n" + "="*85)
        print(f"{'ID':<6} | {'NAMA':<18} | {'KELUHAN':<20} | {'MASUK':<10} | {'STATUS'}")
        print("-" * 85)
        
        curr = self.head
        while curr:
            print(f"{curr.id_pasien:<6} | {curr.nama[:18]:<18} | {curr.keluhan[:20]:<20} | {curr.jam_masuk:<10} | {curr.kategori}")
            curr = curr.next
        print("="*85)

    def show_logs(self):
        """Menampilkan riwayat pasien yang sudah dilayani (Stack)."""
        if not self.logs:
            print("\n[!] Belum ada riwayat pelayanan hari ini.")
            return

        print("\n" + "="*95)
        print("                           RIWAYAT PELAYANAN (LOG STACK)                          ")
        print("="*95)
        print(f"{'ID':<6} | {'NAMA':<18} | {'JAM MASUK':<12} | {'JAM PROSES':<12} | {'STATUS'}")
        print("-" * 95)
        for p in self.logs:
            print(f"{p.id_pasien:<6} | {p.nama[:18]:<18} | {p.jam_masuk:<12} | {p.jam_diproses:<12} | {p.kategori}")
        print("="*95)

    def search_pasien(self, keyword):
        """Mencari pasien di antrian aktif berdasarkan Nama atau ID."""
        if self.is_empty():
            print("\n[!] Antrian kosong, tidak ada yang bisa dicari.")
            return

        found = False
        curr = self.head
        print(f"\nSearching for: '{keyword}'...")
        while curr:
            if keyword.lower() in curr.nama.lower() or keyword.upper() == curr.id_pasien:
                print(f"-> [KETEMU] {curr.id_pasien} | {curr.nama} | Keluhan: {curr.keluhan} | Status: {curr.kategori}")
                found = True
            curr = curr.next
        
        if not found:
            print(f"-> Pasien dengan kata kunci '{keyword}' tidak ditemukan.")

    def get_log_count(self):
        return len(self.logs)