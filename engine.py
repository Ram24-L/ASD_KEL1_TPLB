# engine.py
# Modul Logika Struktur Data - Kelompok 1

from interface import Color # Import Color untuk estetika
from datetime import datetime, timedelta, timezone

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
        """Mencetak tabel dari list node."""
        print("\n" + "=" * 60)
        print(f"  {judul}".center(60))
        print("=" * 60)
        print(f"  {'No':<4} {'ID':<7} {'NAMA PASIEN':<18} {'STATUS':<10} {'WAKTU DAFTAR'}")
        print("-" * 60)
        for i, node in enumerate(nodes, start=1):
            status_mark = "🔴" if node.kategori == "Darurat" else "🟢"
            print(f"  {i:<4} {node.id_pasien:<7} {node.nama:<18} {status_mark} {node.kategori:<8} {node.waktu}")
        print("=" * 60)
        print(f"  Total: {len(nodes)} pasien\n")

    def display_all(self):
        """Tampilkan antrian sesuai urutan asli (prioritas aktif)."""
        if self.is_empty():
            print("\n--- Antrian Kosong ---")
            return
        nodes = self._to_list()
        self._print_table(nodes, judul="ANTRIAN AKTIF (Urutan Pelayanan)")

    # ─────────────────────────────────────────────
    # SORT — hanya untuk tampilan, tidak ubah antrian
    # ─────────────────────────────────────────────
    def display_sorted(self, mode):
        """
        Menampilkan antrian dalam urutan tertentu (TIDAK mengubah antrian asli).

        mode:
          'alpha'    → Urut A-Z berdasarkan nama pasien
          'urgency'  → Darurat semua dulu, lalu Normal (urutan kedatangan dipertahankan)
          'combined' → Darurat dulu (A-Z), lalu Normal (A-Z)
        """
        if self.is_empty():
            print(f"\n{Color.YELLOW}┌───────────────────────────┐")
            print(f"│ {Color.BOLD}ANTRIAN KOSONG SAAT INI{Color.RESET}{Color.YELLOW} │")
            print(f"└───────────────────────────┘{Color.RESET}")
            return

<<<<<<< HEAD
        print(f"\n{Color.CYAN}╔═══════════════════════════════════════════════════════════╗")
        print(f"║ {Color.BOLD}DAFTAR ANTRIAN AKTIF{Color.RESET}{Color.CYAN}".ljust(73) + "║")
        print(f"╠═══════════════════════════════════════════════════════════╣")
        print(f"║ {Color.BOLD}{'ID':<6} | {'NAMA PASIEN':<15} | {'KAT':<8} | {'WAKTU DAFTAR':<19}{Color.RESET}{Color.CYAN} ║")
        print(f"╠═══════════════════════════════════════════════════════════╣{Color.RESET}")
        
        curr = self.head
        while curr:
            kategori_color = Color.RED if curr.kategori == "Darurat" else Color.GREEN
            print(f"{Color.CYAN}║ {curr.id_pasien:<6} | {curr.nama:<15} | {kategori_color}{curr.kategori:<8}{Color.RESET}{Color.CYAN} | {curr.waktu:<19} ║{Color.RESET}")
            curr = curr.next
        print(f"{Color.CYAN}╚═══════════════════════════════════════════════════════════╝{Color.RESET}")
=======
        nodes = self._to_list()
>>>>>>> Debug-phase

        if mode == 'alpha':
            # Insertion Sort berdasarkan nama (A-Z) — O(n²) tapi cocok untuk linked list kecil
            sorted_nodes = self._insertion_sort_alpha(nodes)
            judul = "ANTRIAN — URUT ALFABETIS (A-Z)"

        elif mode == 'urgency':
            # Pisahkan Darurat & Normal, pertahankan urutan kedatangan masing-masing
            darurat = [n for n in nodes if n.kategori == "Darurat"]
            normal  = [n for n in nodes if n.kategori == "Normal"]
            sorted_nodes = darurat + normal
            judul = "ANTRIAN — URUT URGENSI (Darurat → Normal)"

        elif mode == 'combined':
            # Darurat A-Z dulu, lalu Normal A-Z
            darurat = self._insertion_sort_alpha([n for n in nodes if n.kategori == "Darurat"])
            normal  = self._insertion_sort_alpha([n for n in nodes if n.kategori == "Normal"])
            sorted_nodes = darurat + normal
            judul = "ANTRIAN — URGENSI + ALFABETIS (Darurat A-Z → Normal A-Z)"

        else:
            print("[ERROR] Mode sort tidak dikenali.")
            return

        self._print_table(sorted_nodes, judul=judul)

    def _insertion_sort_alpha(self, nodes):
        """Insertion Sort A-Z berdasarkan nama (case-insensitive)."""
        arr = nodes[:]  # salin, jangan ubah asli
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j].nama.lower() > key.nama.lower():
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

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

<<<<<<< HEAD
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
            
=======
        print("\n" + "=" * 55)
        print("      RIWAYAT PELAYANAN (LOG STACK)      ".center(55))
        print("=" * 55)
        print(f"  {'No':<4} {'ID':<7} {'NAMA':<18} {'STATUS':<10} {'WAKTU'}")
        print("-" * 55)
        for i, p in enumerate(reversed(self.logs), start=1):
            status_mark = "🔴" if p.kategori == "Darurat" else "🟢"
            print(f"  {i:<4} {p.id_pasien:<7} {p.nama:<18} {status_mark} {p.kategori:<8} {p.waktu}")
        print("-" * 55)
        print(f"  Total pasien dilayani: {len(self.logs)}\n")

>>>>>>> Debug-phase
    def get_log_count(self):
        """Mengembalikan jumlah pasien yang sudah dilayani."""
        return len(self.logs)
