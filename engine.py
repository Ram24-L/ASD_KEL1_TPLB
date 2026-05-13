# engine.py
# Modul Logika Struktur Data - Kelompok 1

class Node:
    def __init__(self, id_pasien, nama, kategori):
        self.id_pasien = id_pasien
        self.nama = nama
        self.kategori = kategori  # "Normal" atau "Darurat"
        self.next = None

class PriorityQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0
        self.logs = [] # List sederhana untuk menyimpan riwayat (Stack-like)

    def is_empty(self):
        return self.head is None

    def size(self):
        return self._size

    def enqueue(self, nama, kategori):
        # Generate ID sederhana (P001, P002, dst)
        self._size += 1
        new_id = f"P{self._size:03d}"
        new_node = Node(new_id, nama, kategori)

        # LOGIKA PRIORITY:
        if self.is_empty():
            self.head = self.tail = new_node
        elif kategori == "Darurat":
            # Jika darurat, sisipkan di paling depan (Head)
            new_node.next = self.head
            self.head = new_node
        else:
            # Jika normal, masukkan ke paling belakang (Tail)
            self.tail.next = new_node
            self.tail = new_node
        
        print(f"\n[SISTEM] {nama} berhasil ditambahkan ke antrian {kategori}.")

    def dequeue(self):
        if self.is_empty():
            return None
        
        # Ambil data dari Head (FIFO)
        temp = self.head
        self.head = self.head.next
        
        if self.head is None:
            self.tail = None
            
        # Pemanis: Masukkan ke Log (Stack-like: data baru di index 0)
        self.logs.insert(0, temp) 
        return temp

    def display_all(self):
        if self.is_empty():
            print("\n--- Antrian Kosong ---")
            return

        print("\n" + "="*45)
        print(f"{'ID':<6} | {'NAMA PASIEN':<20} | {'KATEGORI'}")
        print("-" * 45)
        
        curr = self.head
        while curr:
            print(f"{curr.id_pasien:<6} | {curr.nama:<20} | {curr.kategori}")
            curr = curr.next
        print("="*45)

    def show_logs(self):
        if not self.logs:
            print("\nBelum ada pasien yang dilayani.")
            return

        print("\n" + "="*45)
        print("      RIWAYAT PELAYANAN (LOG STACK)      ")
        print("="*45)
        for p in self.logs:
            print(f"[{p.id_pasien}] {p.nama} - SELESAI")
        print("-" * 45)

    def get_log_count(self):
        return len(self.logs)

    def search_pasien(self, keyword):
        # Linear Search sederhana
        curr = self.head
        found = False
        while curr:
            if keyword.lower() in curr.nama.lower() or keyword.upper() == curr.id_pasien:
                print(f"\n[KETEMU] {curr.id_pasien} - {curr.nama} ({curr.kategori})")
                found = True
            curr = curr.next
        if not found:
            print(f"\nPasien dengan kata kunci '{keyword}' tidak ditemukan.")