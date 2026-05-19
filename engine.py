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
        self.last_emergency = None  # Pointer ke pasien darurat terakhir (untuk FIFO sesama darurat)
        self.last_id_num = 0  # Counter untuk ID unik
        self._size = 0  # Counter efisien untuk jumlah antrian
        self.logs = [] # Simpan riwayat (Stack-like)

    def is_empty(self):
        return self.head is None

    def size(self):
        """Mengembalikan jumlah antrian secara instan O(1)."""
        return self._size

    def set_last_id(self, id_str):
        """Memastikan ID baru tidak bentrok dengan ID lama di CSV."""
        try:
            num = int(id_str.replace("P", ""))
            if num > self.last_id_num:
                self.last_id_num = num
        except:
            pass

    def enqueue(self, nama, kategori, manual_id=None):
        """
        Jika manual_id ada (saat load data), gunakan itu.
        Jika tidak (pasien baru), buat ID baru secara otomatis.
        """
        if manual_id:
            new_id = manual_id
            self.set_last_id(manual_id)
        else:
            self.last_id_num += 1
            new_id = f"P{self.last_id_num:03d}"

        new_node = Node(new_id, nama, kategori)
        self._size += 1

        # LOGIKA PRIORITY
        if self.is_empty():
            self.head = self.tail = new_node
            if kategori == "Darurat":
                self.last_emergency = new_node
        elif kategori == "Darurat":
            # Darurat dimasukkan setelah pasien darurat terakhir, sebelum pasien normal (FIFO Priority)
            if self.last_emergency:
                new_node.next = self.last_emergency.next
                self.last_emergency.next = new_node
                if self.last_emergency == self.tail:
                    self.tail = new_node
                self.last_emergency = new_node
            else:
                # Pasien darurat pertama di tengah antrian normal
                new_node.next = self.head
                self.head = new_node
                self.last_emergency = new_node
        else:
            # Normal ke belakang (Tail)
            self.tail.next = new_node
            self.tail = new_node
        
        return new_id

    def dequeue(self):
        if self.is_empty():
            return None
        
        temp = self.head
        self.head = self.head.next
        self._size -= 1
        
        if self.head is None:
            self.tail = None
            self.last_emergency = None
        elif temp == self.last_emergency:
            self.last_emergency = None
            
        # Masukkan ke Log (Gunakan append agar O(1))
        self.logs.append(temp) 
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
        for p in reversed(self.logs):  # Tampilkan dari yang terbaru
            print(f"[{p.id_pasien}] {p.nama} - SELESAI")
        print("-" * 45)

    def search_pasien(self, keyword):
        curr = self.head
        found = False
        while curr:
            if keyword.lower() in curr.nama.lower() or keyword.upper() == curr.id_pasien:
                print(f"\n[KETEMU] {curr.id_pasien} - {curr.nama} ({curr.kategori})")
                found = True
            curr = curr.next
        if not found:
            print(f"\nPasien '{keyword}' tidak ditemukan.")
            
    def get_log_count(self):
        """Mengembalikan jumlah pasien yang sudah dilayani (isi dari list logs)."""
        return len(self.logs)