# engine.py
# Modul Logika Struktur Data - Kelompok 1

from interface import Color # Import Color untuk estetika
from datetime import datetime, timedelta, timezone
from interface import Color
from storage import save_data

class Node:
    def __init__(self, id_pasien, nama, kategori, waktu):
        self.id_pasien = id_pasien
        self.nama = nama
        self.kategori = kategori  # "Normal" atau "Darurat"
        self.waktu = waktu  # Format: "YYYY-MM-DD HH:MM:SS"
        self.next = None

class PriorityQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.last_emergency = None  # Pointer ke pasien darurat terakhir (untuk FIFO sesama darurat)
        self.last_id_num = 0  # Counter untuk ID unik
        self._size = 0  # Counter efisien untuk jumlah antrian
        self.logs = []  # Simpan riwayat (Stack-like)

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

    def enqueue(self, nama, kategori, manual_id=None, manual_waktu=None):
        """
        Jika manual_id/waktu ada (saat load data), gunakan itu.
        Jika tidak (pasien baru), buat ID baru secara otomatis.
        """
        if manual_id:
            new_id = manual_id
            self.set_last_id(manual_id)
        else:
            self.last_id_num += 1
            new_id = f"P{self.last_id_num:03d}"

        # Set waktu ke GMT+7 jika tidak ada manual_waktu
        if manual_waktu:
            waktu_final = manual_waktu
        else:
            tz_gmt7 = timezone(timedelta(hours=7))
            waktu_final = datetime.now(tz_gmt7).strftime("%Y-%m-%d %H:%M:%S")

        new_node = Node(new_id, nama, kategori, waktu_final)
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


        save_data(self)
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
        save_data(self)
        return temp

    # ─────────────────────────────────────────────
    # HELPER: ambil semua node dari linked list
    # ─────────────────────────────────────────────
    def _to_list(self):
        """Mengonversi linked list ke Python list (hanya untuk keperluan tampilan/sort)."""
        result = []
        curr = self.head
        while curr:
            result.append(curr)
            curr = curr.next
        return result

    # ─────────────────────────────────────────────
    # DISPLAY (tampilan asli / urutan antrian)
    # ─────────────────────────────────────────────
    def _print_table(self, nodes, judul="ANTRIAN AKTIF"):
        """Mencetak tabel dari list node dengan pewarnaan terstandardisasi."""
        print("\n" + f"{Color.CYAN}=" * 73)
        print(f"{Color.RESET}{Color.BOLD}{judul}{Color.RESET}".center(65))
        print(f"{Color.CYAN}=" * 73)
        print(f"| {'No':<4} | {'ID':<6} | {'NAMA PASIEN':<20} | {'STATUS':<10} | {'WAKTU DAFTAR'}")
        print(f"-" * 73 + f"{Color.RESET}")
        
        for i, node in enumerate(nodes, start=1):
            if node.kategori == "Darurat":
                kat_warna = f"{Color.RED}{node.kategori:<10}{Color.RESET}"
            else:
                kat_warna = f"{Color.GREEN}{node.kategori:<10}{Color.RESET}"
                
            print(f"| {i:<4} | {node.id_pasien:<6} | {node.nama:<20} | {kat_warna} | {node.waktu}")
            
        print(f"{Color.CYAN}=" * 73 + f"{Color.RESET}")
        print(f"  Total: {Color.BOLD}{len(nodes)}{Color.RESET} pasien\n")

    def display_all(self):
        if self.is_empty():
            print(f"\n{Color.RED}--- Antrian Kosong ---{Color.RESET}")
            return

        # Header Tabel menggunakan warna Cyan agar konsisten dengan menu utama
        print("\n" + f"{Color.CYAN}="*52 + f"{Color.RESET}")
        print(f"| {'ID':<6} | {'NAMA PASIEN':<20} | {'KATEGORI':<12} |")
        print(f"{Color.CYAN}-"*52 + f"{Color.RESET}")
        
        curr = self.head
        while curr:
            # Berikan warna pembeda pada kolom kategori secara dinamis
            if curr.kategori == "Darurat":
                kat_warna = f"{Color.RED}{curr.kategori:<12}{Color.RESET}"
            else:
                kat_warna = f"{Color.GREEN}{curr.kategori:<12}{Color.RESET}"
                
            # Cetak baris data pasien
            print(f"{Color.CYAN}|{Color.RESET} {curr.id_pasien:<6} {Color.CYAN}|{Color.RESET} {curr.nama:<20} {Color.CYAN}|{Color.RESET} {kat_warna} {Color.CYAN}|{Color.RESET}")
            curr = curr.next
            
        print(f"{Color.CYAN}="*52 + f"{Color.RESET}")

    # ─────────────────────────────────────────────────────────
    # SORT — Hanya untuk tampilan, TIDAK mengubah antrian asli
    # ─────────────────────────────────────────────────────────
    def display_sorted(self, mode):
        """
        Menampilkan antrian dalam urutan tertentu (TIDAK mengubah antrian asli).
        mode:
          'nama' / 'alpha'       → Urut A-Z berdasarkan nama pasien
          'kategori' / 'urgency' → Darurat semua dulu, lalu Normal (urutan kedatangan dipertahankan)
          'gabungan' / 'combined'→ Darurat dulu (A-Z), lalu Normal (A-Z)
        """
        if self.is_empty():
            print(f"\n{Color.YELLOW}┌───────────────────────────┐")
            print(f"│ {Color.BOLD}ANTRIAN KOSONG SAAT INI{Color.RESET}{Color.YELLOW} │")
            print(f"└───────────────────────────┘{Color.RESET}")
            return

        # Ambil semua node dari linked list ke dalam list penolong (Array lokal)
        nodes = self._to_list()

        if mode in ['nama', 'alpha']:
            # Merge Sort berdasarkan nama (A-Z)
            sorted_nodes = self._merge_sort_alpha(nodes)
            judul = "ANTRIAN — URUT ALFABETIS (A-Z)"

        elif mode in ['kategori', 'urgency']:
            # Pisahkan Darurat & Normal, pertahankan urutan kedatangan masing-masing (FIFO Priority)
            darurat = [n for n in nodes if n.kategori == "Darurat"]
            normal  = [n for n in nodes if n.kategori == "Normal"]
            sorted_nodes = darurat + normal
            judul = "ANTRIAN — URUT URGENSI (Darurat → Normal)"

        elif mode in ['gabungan', 'combined']:
            # Merge Sort - Darurat A-Z dulu, lalu Normal A-Z
            darurat = self._merge_sort_alpha([n for n in nodes if n.kategori == "Darurat"])
            normal  = self._merge_sort_alpha([n for n in nodes if n.kategori == "Normal"])
            sorted_nodes = darurat + normal
            judul = "ANTRIAN — URGENSI + ALFABETIS (MERGE SORT)"

        else:
            print(f"{Color.RED}[ERROR] Mode sort tidak dikenali.{Color.RESET}")
            return

        # Panggil fungsi pembantu untuk menampilkan array yang sudah terurut
        self._print_table(sorted_nodes, judul=judul)

    def _merge_sort_alpha(self, nodes):
        """Merge Sort A-Z berdasarkan nama (case-insensitive). O(n log n)"""
        if len(nodes) <= 1:
            return nodes[:]
        
        def merge(left, right):
            """Menggabungkan dua array yang sudah terurut."""
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i].nama.lower() <= right[j].nama.lower():
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        
        def merge_sort(arr):
            """Divide and conquer - membagi array hingga ukuran 1, lalu menggabungkannya."""
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = merge_sort(arr[:mid])
            right = merge_sort(arr[mid:])
            return merge(left, right)
        
        return merge_sort(nodes[:])


    def _merge(self, left, right):
        """Logika penggabungan dua array yang sudah terurut secara alfabetis."""
        result = []
        i = j = 0

        # Bandingkan elemen dari kedua sub-array
        while i < len(left) and j < len(right):
            if left[i].nama.lower() <= right[j].nama.lower():
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        # Ambil sisa elemen yang belum dimasukkan
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    # ─────────────────────────────────────────────
    # SEARCH — partial match, semua hasil ditampilkan
    # ─────────────────────────────────────────────
    def search_pasien(self, keyword):
        """
        Mencari pasien berdasarkan nama (partial), ID (exact), atau waktu (partial).
        Contoh: keyword "michael" → menemukan "Michael Flow" DAN "Michael Bart".
        """
        keyword_lower = keyword.lower().strip()
        curr = self.head
        hasil = []

        while curr:
            cocok_nama = keyword_lower in curr.nama.lower()
            cocok_id   = keyword.upper() == curr.id_pasien
            cocok_waktu = keyword in curr.waktu
            if cocok_nama or cocok_id or cocok_waktu:
                hasil.append(curr)
            curr = curr.next

        print("\n" + "=" * 60)
        if hasil:
            print(f"  Hasil pencarian untuk: \"{keyword}\" ({len(hasil)} ditemukan)")
            print("=" * 60)
            print(f"  {'No':<4} {'ID':<7} {'NAMA PASIEN':<18} {'STATUS':<10} {'WAKTU DAFTAR'}")
            print("-" * 60)
            for i, node in enumerate(hasil, start=1):
                status_mark = "🔴" if node.kategori == "Darurat" else "🟢"
                print(f"  {i:<4} {node.id_pasien:<7} {node.nama:<18} {status_mark} {node.kategori:<8} {node.waktu}")
            print("=" * 60)
        else:
            print(f"  Tidak ada pasien yang cocok dengan \"{keyword}\".")
            print("=" * 60)

    # ─────────────────────────────────────────────
    # LOG & RIWAYAT
    # ─────────────────────────────────────────────
    def show_logs(self):
        if not self.logs:
            print(f"\n{Color.YELLOW}┌───────────────────────────┐")
            print(f"│ {Color.BOLD}BELUM ADA PASIEN DILAYANI{Color.RESET}{Color.YELLOW} │")
            print(f"└───────────────────────────┘{Color.RESET}")
            return

        print(f"\n{Color.BLUE}╔═══════════════════════════════════════════════════════╗")
        print(f"║ {Color.BOLD}RIWAYAT PELAYANAN (LOG STACK){Color.RESET}{Color.BLUE}".ljust(69) + "║")
        print(f"╠═══════════════════════════════════════════════════════╣{Color.RESET}")
        for p in reversed(self.logs):  # Tampilkan dari yang terbaru
            print(f"{Color.BLUE}║ [{p.waktu}] {p.id_pasien} - {p.nama} {Color.GREEN}(SELESAI){Color.RESET}{Color.BLUE}".ljust(75) + f"║{Color.RESET}")
        print(f"{Color.BLUE}╚═══════════════════════════════════════════════════════╝{Color.RESET}")

    def search_pasien(self, keyword):
        curr = self.head
        found = False
        print(f"\n{Color.YELLOW}Mencari pasien dengan keyword '{keyword}'...{Color.RESET}")
        while curr:
            # Sekarang bisa mencari berdasarkan Nama, ID, atau bagian dari Waktu (misal: "2023-10")
            if (keyword.lower() in curr.nama.lower() or 
                keyword.upper() == curr.id_pasien or 
                keyword in curr.waktu):
                print(f"{Color.GREEN}✅ DITEMUKAN: {Color.BOLD}{curr.id_pasien}{Color.RESET} - {curr.nama} [{curr.kategori}] (Daftar: {curr.waktu}){Color.RESET}")
                found = True
            curr = curr.next
        if not found:
            print(f"{Color.RED}❌ Pasien '{keyword}' tidak ditemukan.{Color.RESET}")
            
    def get_log_count(self):
        """Mengembalikan jumlah pasien yang sudah dilayani."""
        return len(self.logs)
    
    def display_by_kategori(self, target_kategori):
        """
        Menampilkan daftar antrian yang difilter berdasarkan kategori tertentu.
        target_kategori: "Darurat" atau "Normal"
        """
        if self.is_empty():
            print(f"\n{Color.YELLOW}┌───────────────────────────┐")
            print(f"│ {Color.BOLD}ANTRIAN KOSONG SAAT INI{Color.RESET}{Color.YELLOW} │")
            print(f"└───────────────────────────┘{Color.RESET}")
            return

        # Ambil semua node linked list ke dalam list penolong
        nodes = self._to_list()
        # Filter hanya yang kategorinya cocok
        filtered_nodes = [n for n in nodes if n.kategori == target_kategori]

        if not filtered_nodes:
            print(f"\n{Color.RED}❌ Tidak ada pasien dengan kategori '{target_kategori}' di dalam antrian.{Color.RESET}")
            return

        judul = f"ANTRIAN AKTIF — KHUSUS KATEGORI {target_kategori.upper()}"
        
        # Manfaatkan fungsi cetak tabel yang sudah kita perbaiki sebelumnya
        self._print_table(filtered_nodes, judul=judul)