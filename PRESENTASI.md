# 🏥 SISTEM ANTRIAN KLINIK - PRESENTASI FITUR

**Proyek Akhir: Algoritma & Struktur Data - Kelompok 1**

---

## 📋 DAFTAR ISI
1. [Pendahuluan](#pendahuluan)
2. [Struktur Data Utama](#struktur-data-utama)
3. [Menu Utama](#menu-utama)
4. [Submenu Lihat Antrian](#submenu-lihat-antrian)
5. [Algoritma Merge Sort](#algoritma-merge-sort)
6. [Contoh Penggunaan](#contoh-penggunaan)

---

## 📝 PENDAHULUAN

Sistem Antrian Klinik adalah aplikasi manajemen antrian pelayanan kesehatan yang menggunakan:
- **Struktur Data:** Linked List dengan Priority Queue
- **Algoritma Sorting:** Merge Sort (O(n log n))
- **Fitur Utama:** Registrasi, Panggilan Pasien, Sorting Dinamis, Pencarian

### Karakteristik Khusus
✅ Prioritas Emergency (Pasien Darurat mendapat urutan lebih awal)  
✅ Multiple Sorting Modes (Waktu, Alfabetis, Urgensi, Gabungan)  
✅ Pencarian Cerdas (Nama, ID, Tanggal)  
✅ Riwayat Pelayanan (Stack-based Logging)  
✅ Persistent Data (Disimpan ke CSV)

---

## 🔧 STRUKTUR DATA UTAMA

### Priority Queue dengan Linked List

```python
class Node:
    def __init__(self, id_pasien, nama, kategori, waktu):
        self.id_pasien = id_pasien    # Format: P001, P002, dst
        self.nama = nama              # Nama pasien
        self.kategori = kategori      # "Normal" atau "Darurat"
        self.waktu = waktu            # Format: "YYYY-MM-DD HH:MM:SS"
        self.next = None              # Pointer ke node berikutnya
```

### Priority Queue Class

```python
class PriorityQueue:
    def __init__(self):
        self.head = None                  # Pasien pertama dalam antrian
        self.tail = None                  # Pasien terakhir
        self.last_emergency = None        # Pointer ke pasien darurat terakhir
        self.last_id_num = 0              # Counter untuk ID unik
        self._size = 0                    # Jumlah antrian (O(1) access)
        self.logs = []                    # Riwayat pelayanan (Stack)
```

**Keunggulan Struktur Ini:**
- Dynamic sizing (tidak perlu pre-allocation)
- Efficient enqueue/dequeue O(1)
- Prioritas Darurat terintegrasi
- Logging otomatis untuk setiap pelayanan

---

## 🎯 MENU UTAMA

Aplikasi memiliki 5 menu utama yang dapat diakses dari halaman depan:

```
╔════════════════════════════════════════════════════════════╗
║              SISTEM ANTRIAN KLINIK                         ║
║          Pelayanan Kesehatan Cepat & Responsif             ║
╚════════════════════════════════════════════════════════════╝

  [1] Registrasi Pasien Baru
  [2] Panggil Pasien Berikutnya
  [3] Lihat Antrian Aktif (Fix Order)
  [4] Pencarian & Pengurutan Pasien
  [0] Keluar & Simpan Data

  Pilih menu [0-4]: _
```

---

## 📌 MENU 1: REGISTRASI PASIEN BARU

### Fungsi
Mendaftarkan pasien baru ke dalam sistem antrian dengan kategori Normal atau Darurat.

### Alur Program

```python
if pilihan == '1':
    # Registrasi Pasien
    clear_screen()
    print("\n" + "=" * 50)
    print("  REGISTRASI PASIEN BARU".center(50))
    print("=" * 50)
    
    # Input nama pasien
    nama = input("  Nama Pasien : ").strip()
    if not nama:
        print("\n  Nama tidak boleh kosong!")
        input("  Tekan Enter...")
        continue
    
    # Pilih kategori
    print("  Kategori    : 1. Normal  |  2. Darurat (Prioritas)")
    kat_input = input("  Pilih [1/2] : ").strip()
    kategori = "Darurat" if kat_input == '2' else "Normal"
    
    # Enqueue ke antrian
    new_id = antrian.enqueue(nama, kategori)
    print(f"\n  ✅ Pasien '{nama}' terdaftar sebagai [{kategori}] dengan ID {new_id}")
    input("\n  Tekan Enter...")
```

### Implementasi Enqueue

```python
def enqueue(self, nama, kategori, manual_id=None, manual_waktu=None):
    """
    Memasukkan pasien baru ke dalam antrian dengan prioritas.
    """
    # Generate ID baru jika tidak ada manual_id
    if manual_id:
        new_id = manual_id
        self.set_last_id(manual_id)
    else:
        self.last_id_num += 1
        new_id = f"P{self.last_id_num:03d}"
    
    # Set waktu ke GMT+7
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
        # Pasien darurat masuk setelah darurat terakhir, sebelum normal
        if self.last_emergency:
            new_node.next = self.last_emergency.next
            self.last_emergency.next = new_node
            if self.last_emergency == self.tail:
                self.tail = new_node
            self.last_emergency = new_node
        else:
            new_node.next = self.head
            self.head = new_node
            self.last_emergency = new_node
    
    else:
        # Pasien normal ke belakang (tail)
        self.tail.next = new_node
        self.tail = new_node
    
    save_data(self)
    return new_id
```

### Keunggulan
✅ ID otomatis & unik (P001, P002, dst)  
✅ Timestamp otomatis (GMT+7)  
✅ Prioritas Darurat terjaga FIFO  
✅ Data auto-save ke CSV  
✅ Validasi input nama

### Contoh Output
```
  ✅ Pasien 'Muhammad Ramdhan' terdaftar sebagai [Darurat] dengan ID P007
```

---

## 📞 MENU 2: PANGGIL PASIEN BERIKUTNYA

### Fungsi
Memanggil pasien pertama dalam antrian untuk dilayani, kemudian memindahkannya ke riwayat.

### Alur Program

```python
elif pilihan == '2':
    # Panggil Pasien (Dequeue)
    pasien_dipanggil = antrian.dequeue()
    if pasien_dipanggil:
        animasi_panggil(pasien_dipanggil)
    else:
        print("\n  Antrian kosong! Tidak ada pasien yang perlu dipanggil.")
        input("  Tekan Enter...")
```

### Implementasi Dequeue

```python
def dequeue(self):
    """
    Mengeluarkan pasien pertama dari antrian untuk pelayanan.
    """
    if self.is_empty():
        return None
    
    temp = self.head
    self.head = self.head.next
    self._size -= 1
    
    # Update tail jika antrian menjadi kosong
    if self.head is None:
        self.tail = None
        self.last_emergency = None
    
    # Update last_emergency jika pasien yang didequeue adalah pasien darurat terakhir
    elif temp == self.last_emergency:
        self.last_emergency = None
    
    # Masukkan ke Log (Stack)
    self.logs.append(temp)
    save_data(self)
    return temp
```

### Animasi Panggilan

```python
def animasi_panggil(pasien):
    """Memberikan efek visual saat memanggil pasien."""
    loading_spinner(1.5, "MENGHUBUNGKAN KE SPEAKER")
    
    border_color = Color.RED if pasien.kategori == "Darurat" else Color.GREEN
    
    print(f"\n{border_color}╔{'═' * 58}╗")
    print("║" + "PASIEN HARAP MENUJU RUANG DOKTER".center(58) + "║")
    print(f"╠{'═' * 58}╣{Color.RESET}")
    print(f"{border_color}║  {Color.BOLD}ID PASIEN :{Color.RESET} {pasien.id_pasien}" + " " * 40 + f"{border_color}║")
    print(f"{border_color}║  {Color.BOLD}NAMA      :{Color.RESET} {pasien.nama.upper()}" + " " * 30 + f"{border_color}║")
    print(f"{border_color}║  {Color.BOLD}STATUS    :{Color.RESET} {pasien.kategori.upper()}" + " " * 35 + f"{border_color}║")
    print(f"{border_color}╚{'═' * 58}╝{Color.RESET}")
    
    input(f"\n{Color.YELLOW}Tekan [Enter] setelah pasien selesai dilayani...{Color.RESET}")
    print(f"\n{Color.GREEN}✅ Pasien telah selesai. Data dipindahkan ke Riwayat.{Color.RESET}")
```

### Keunggulan
✅ Dequeue O(1) (instant)  
✅ Auto-logging ke riwayat  
✅ Visual feedback yang menarik  
✅ Warna berbeda untuk Darurat/Normal  
✅ Timestamp otomatis tersimpan

### Contoh Output
```
╔══════════════════════════════════════════════════════════╗
║      PASIEN HARAP MENUJU RUANG DOKTER                   ║
╠══════════════════════════════════════════════════════════╣
║  ID PASIEN : P001                                        ║
║  NAMA      : BUDI SANTOSO                               ║
║  STATUS    : NORMAL                                      ║
║  i CATATAN: Mohon menunggu giliran dengan tertib.       ║
╚══════════════════════════════════════════════════════════╝
```

---

## 👁️ MENU 3: LIHAT ANTRIAN AKTIF

### Fungsi
Menampilkan daftar pasien yang sedang menunggu dengan opsi pengurutan berbeda.

### Submenu Lihat Antrian

```
╔═══════════════════════════════════════════════════════╗
║             LIHAT ANTRIAN                             ║
║  Sort aktif : [ Alfabetis A-Z ]                       ║
╠═══════════════════════════════════════════════════════╣

  -- Ganti Tampilan --
  [1] Waktu Daftar   (Pertama -> Terbaru)  *default*
  [2] Alfabetis      (A-Z)
  [3] Urgensi        (Darurat -> Normal)
  [4] Gabungan       (Darurat A-Z -> Normal A-Z)

  -- Aksi Lain --
  [5] Cari Pasien    (Nama / ID / Tanggal)
  [6] Refresh tampilan (sort saat ini)

  [0] Kembali ke Menu Utama

  Pilih [0-6]: _
```

---

## 🔤 OPSI 1: WAKTU DAFTAR (Default)

### Fungsi
Menampilkan antrian dalam urutan kedatangan (FIFO).

### Kode
```python
def display_sorted(self, mode):
    """Menampilkan antrian dengan mode sort tertentu."""
    if self.is_empty():
        print(f"\n{Color.YELLOW}┌───────────────────────────┐")
        print(f"│ {Color.BOLD}ANTRIAN KOSONG SAAT INI{Color.RESET}{Color.YELLOW} │")
        print(f"└───────────────────────────┘{Color.RESET}")
        return
    
    nodes = self._to_list()
    
    # MODE: Waktu Daftar
    if mode == 'waktu':
        sorted_nodes = nodes  # Sudah dalam urutan FIFO dari linked list
        judul = "ANTRIAN — URUT WAKTU DAFTAR (Pertama -> Terbaru)"
```

### Keunggulan
✅ Real-time order (sesuai linked list)  
✅ Performa O(1) - tanpa sorting  
✅ FIFO Priority terjaga  

### Contoh Output
```
═════════════════════════════════════════════════════════════
            ANTRIAN — URUT WAKTU DAFTAR (Pertama -> Terbaru)
═════════════════════════════════════════════════════════════
| No  | ID     | NAMA PASIEN          | STATUS     | WAKTU DAFTAR
-────────────────────────────────────────────────────────────
| 1   | P001   | Budi Santoso         | DARURAT    | 2026-05-20 08:15:30
| 2   | P002   | Siti Nurhaliza       | NORMAL     | 2026-05-20 08:20:45
| 3   | P003   | Ahmad Wijaya         | NORMAL     | 2026-05-20 08:25:10
═════════════════════════════════════════════════════════════
  Total: 3 pasien
```

---

## 🔤 OPSI 2: ALFABETIS (A-Z)

### Fungsi
Menampilkan antrian terurut berdasarkan nama pasien dari A ke Z menggunakan **Merge Sort**.

### Kode Merge Sort

```python
def _merge_sort_alpha(self, nodes):
    """
    Merge Sort A-Z berdasarkan nama pasien (case-insensitive).
    
    Algoritma Divide and Conquer:
    - Kompleksitas waktu: O(n log n) — optimal untuk sorting
    - Kompleksitas ruang: O(n) — membutuhkan array tambahan
    - Stabil: Mempertahankan urutan relative elemen yang sama
    - Cocok untuk dataset besar dengan performa konsisten
    """
    if len(nodes) <= 1:
        return nodes[:]
    
    def merge(left, right):
        """Menggabungkan dua array yang sudah terurut."""
        result = []
        i = j = 0
        
        # Bandingkan elemen dari kedua array
        while i < len(left) and j < len(right):
            if left[i].nama.lower() <= right[j].nama.lower():
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Masukkan sisa elemen
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def merge_sort(arr):
        """Divide and conquer - membagi array hingga ukuran 1, lalu menggabungkannya."""
        if len(arr) <= 1:
            return arr
        
        # Divide: Bagi array menjadi 2 bagian
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        
        # Conquer: Gabungkan kedua bagian yang sudah terurut
        return merge(left, right)
    
    return merge_sort(nodes[:])
```

### Implementasi dalam Display

```python
if mode in ['nama', 'alpha']:
    # Merge Sort berdasarkan nama (A-Z)
    sorted_nodes = self._merge_sort_alpha(nodes)
    judul = "ANTRIAN — URUT ALFABETIS (A-Z)"
```

### Keunggulan
✅ Kompleksitas O(n log n) - lebih cepat dari insertion sort  
✅ Stable sort - mempertahankan order relative  
✅ Optimal untuk dataset besar  
✅ Case-insensitive (Ahmad = ahmad)  

### Contoh Output
```
═════════════════════════════════════════════════════════════
                  ANTRIAN — URUT ALFABETIS (A-Z)
═════════════════════════════════════════════════════════════
| No  | ID     | NAMA PASIEN          | STATUS     | WAKTU DAFTAR
-────────────────────────────────────────────────────────────
| 1   | P003   | Ahmad Wijaya         | NORMAL     | 2026-05-20 08:25:10
| 2   | P001   | Budi Santoso         | DARURAT    | 2026-05-20 08:15:30
| 3   | P002   | Siti Nurhaliza       | NORMAL     | 2026-05-20 08:20:45
═════════════════════════════════════════════════════════════
  Total: 3 pasien
```

---

## 🆘 OPSI 3: URGENSI (DARURAT → NORMAL)

### Fungsi
Menampilkan pasien Darurat terlebih dahulu, diikuti Pasien Normal dengan mempertahankan urutan kedatangan masing-masing.

### Kode

```python
elif mode in ['kategori', 'urgency']:
    # Pisahkan Darurat & Normal, pertahankan urutan kedatangan masing-masing
    darurat = [n for n in nodes if n.kategori == "Darurat"]
    normal  = [n for n in nodes if n.kategori == "Normal"]
    sorted_nodes = darurat + normal
    judul = "ANTRIAN — URUT URGENSI (Darurat → Normal)"
```

### Karakteristik
✅ Darurat selalu didepan (FIFO Priority)  
✅ FIFO terjaga dalam kategori  
✅ Performa O(n) - linear  
✅ Filter tanpa sorting kompleks  

### Contoh Output
```
═════════════════════════════════════════════════════════════
              ANTRIAN — URUT URGENSI (Darurat → Normal)
═════════════════════════════════════════════════════════════
| No  | ID     | NAMA PASIEN          | STATUS     | WAKTU DAFTAR
-────────────────────────────────────────────────────────────
| 1   | P001   | Budi Santoso         | DARURAT    | 2026-05-20 08:15:30
| 2   | P004   | Rini Handoko         | DARURAT    | 2026-05-20 08:30:00
| 3   | P002   | Siti Nurhaliza       | NORMAL     | 2026-05-20 08:20:45
| 4   | P003   | Ahmad Wijaya         | NORMAL     | 2026-05-20 08:25:10
═════════════════════════════════════════════════════════════
  Total: 4 pasien
```

---

## 🎯 OPSI 4: GABUNGAN (URGENSI + ALFABETIS)

### Fungsi
Menampilkan Pasien Darurat terurut A-Z, diikuti Pasien Normal terurut A-Z menggunakan **Merge Sort**.

### Kode

```python
elif mode in ['gabungan', 'combined']:
    # Darurat A-Z dulu, lalu Normal A-Z (menggunakan Merge Sort)
    darurat = self._merge_sort_alpha([n for n in nodes if n.kategori == "Darurat"])
    normal  = self._merge_sort_alpha([n for n in nodes if n.kategori == "Normal"])
    sorted_nodes = darurat + normal
    judul = "ANTRIAN — URGENSI + ALFABETIS (Darurat A-Z → Normal A-Z)"
```

### Keunggulan
✅ Prioritas Darurat terjaga  
✅ Sorting alfabetis dalam kategori  
✅ Merge Sort O(n log n) untuk masing-masing  
✅ Kombinasi prioritas + organisasi  

### Contoh Output
```
═════════════════════════════════════════════════════════════
     ANTRIAN — URGENSI + ALFABETIS (Darurat A-Z → Normal A-Z)
═════════════════════════════════════════════════════════════
| No  | ID     | NAMA PASIEN          | STATUS     | WAKTU DAFTAR
-────────────────────────────────────────────────────────────
| 1   | P004   | Bambang Irawan       | DARURAT    | 2026-05-20 08:30:00
| 2   | P001   | Budi Santoso         | DARURAT    | 2026-05-20 08:15:30
| 3   | P003   | Ahmad Wijaya         | NORMAL     | 2026-05-20 08:25:10
| 4   | P002   | Siti Nurhaliza       | NORMAL     | 2026-05-20 08:20:45
═════════════════════════════════════════════════════════════
  Total: 4 pasien
```

---

## 🔍 OPSI 5: CARI PASIEN

### Fungsi
Mencari pasien berdasarkan Nama (partial), ID (exact), atau Tanggal (partial).

### Alur Program

```python
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
```

### Implementasi Search

```python
def search_pasien(self, keyword):
    """
    Mencari pasien berdasarkan nama (partial), ID (exact), atau waktu (partial).
    """
    keyword_lower = keyword.lower().strip()
    curr = self.head
    hasil = []
    
    # Traversal linked list
    while curr:
        cocok_nama = keyword_lower in curr.nama.lower()
        cocok_id   = keyword.upper() == curr.id_pasien
        cocok_waktu = keyword in curr.waktu
        
        if cocok_nama or cocok_id or cocok_waktu:
            hasil.append(curr)
        
        curr = curr.next
    
    # Tampilkan hasil
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
```

### Keunggulan
✅ Search case-insensitive  
✅ Multi-kriteria (nama, ID, tanggal)  
✅ Partial matching support  
✅ Performa O(n) - linear search  

### Contoh Output
```
════════════════════════════════════════════════════════════
  Hasil pencarian untuk: "budi" (1 ditemukan)
════════════════════════════════════════════════════════════
  No   ID      NAMA PASIEN          STATUS    WAKTU DAFTAR
────────────────────────────────────────────────────────────
  1    P001    Budi Santoso         🔴 Darurat 2026-05-20 08:15:30
════════════════════════════════════════════════════════════
```

---

## 📋 MENU 4: RIWAYAT PELAYANAN

### Fungsi
Menampilkan log pasien yang sudah selesai dilayani menggunakan struktur **Stack** (LIFO).

### Alur Program

```python
elif pilihan == '4':
    # Riwayat Pelayanan (Log Stack)
    clear_screen()
    antrian.show_logs()
    input("\nTekan Enter untuk kembali...")
```

### Implementasi Show Logs

```python
def show_logs(self):
    """Menampilkan riwayat pelayanan dalam urutan terbaru terlebih dahulu."""
    if not self.logs:
        print(f"\n{Color.YELLOW}┌───────────────────────────┐")
        print(f"│ {Color.BOLD}BELUM ADA PASIEN DILAYANI{Color.RESET}{Color.YELLOW} │")
        print(f"└───────────────────────────┘{Color.RESET}")
        return
    
    print(f"\n{Color.BLUE}╔═══════════════════════════════════════════════════════╗")
    print(f"║ {Color.BOLD}RIWAYAT PELAYANAN (LOG STACK){Color.RESET}{Color.BLUE}".ljust(69) + "║")
    print(f"╠═══════════════════════════════════════════════════════╣{Color.RESET}")
    
    # Tampilkan dari yang terbaru (reversed) - Stack behavior (LIFO)
    for p in reversed(self.logs):
        print(f"{Color.BLUE}║ [{p.waktu}] {p.id_pasien} - {p.nama} {Color.GREEN}(SELESAI){Color.RESET}{Color.BLUE}".ljust(75) + f"║{Color.RESET}")
    
    print(f"{Color.BLUE}╚═══════════════════════════════════════════════════════╝{Color.RESET}")
```

### Keunggulan
✅ Stack-based (LIFO order - terbaru duluan)  
✅ Persistent logging (disimpan ke CSV)  
✅ Timestamp otomatis untuk setiap pelayanan  
✅ Audit trail lengkap  

### Contoh Output
```
╔═══════════════════════════════════════════════════════════╗
║              RIWAYAT PELAYANAN (LOG STACK)               ║
╠═══════════════════════════════════════════════════════════╣
║ [2026-05-20 09:15:45] P005 - Eka Putri (SELESAI)        ║
║ [2026-05-20 09:10:20] P004 - Rini Handoko (SELESAI)     ║
║ [2026-05-20 09:05:30] P001 - Budi Santoso (SELESAI)     ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🎓 ALGORITMA MERGE SORT

### Overview
Merge Sort adalah algoritma sorting yang menggunakan paradigma **Divide and Conquer** dengan kompleksitas **O(n log n)**.

### Gambaran Algoritma

```
Fase DIVIDE:
Array: [Charlie, Alice, Bob, David]
       ↓
       [Charlie, Alice] | [Bob, David]
       ↓
   [Charlie]|[Alice]    [Bob]|[David]

Fase MERGE:
[Alice, Charlie] | [Bob, David]
       ↓
    [Alice, Bob, Charlie, David]  ← SORTED
```

### Implementasi Lengkap

```python
def _merge_sort_alpha(self, nodes):
    """
    Merge Sort A-Z berdasarkan nama pasien (case-insensitive).
    """
    # Base case: array dengan 0 atau 1 elemen sudah terurut
    if len(nodes) <= 1:
        return nodes[:]
    
    # FASE MERGE: Fungsi helper untuk menggabungkan 2 array terurut
    def merge(left, right):
        """
        Menggabungkan dua array yang sudah terurut menjadi satu array terurut.
        """
        result = []
        i = j = 0
        
        # Bandingkan elemen dari kedua array, masukkan yang lebih kecil
        while i < len(left) and j < len(right):
            if left[i].nama.lower() <= right[j].nama.lower():
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Masukkan sisa elemen dari left (jika ada)
        result.extend(left[i:])
        
        # Masukkan sisa elemen dari right (jika ada)
        result.extend(right[j:])
        
        return result
    
    # FASE DIVIDE: Rekursi pembagian array
    def merge_sort(arr):
        """
        Divide array into smaller subarrays recursively, then merge them.
        """
        # Base case: array dengan 0 atau 1 elemen
        if len(arr) <= 1:
            return arr
        
        # Divide: Cari titik tengah
        mid = len(arr) // 2
        
        # Divide: Rekursi ke left half
        left = merge_sort(arr[:mid])
        
        # Divide: Rekursi ke right half
        right = merge_sort(arr[mid:])
        
        # Conquer: Gabungkan hasil
        return merge(left, right)
    
    # Mulai proses sorting
    return merge_sort(nodes[:])
```

### Analisis Kompleksitas

| Aspek | Nilai |
|-------|-------|
| **Time Complexity (Best)** | O(n log n) |
| **Time Complexity (Average)** | O(n log n) |
| **Time Complexity (Worst)** | O(n log n) |
| **Space Complexity** | O(n) |
| **Stability** | ✅ Stabil (mempertahankan order relative) |
| **In-place** | ❌ Tidak (perlu array tambahan) |

### Perbandingan dengan Insertion Sort

| Algoritma | Time | Space | Stabil | Best For |
|-----------|------|-------|--------|----------|
| **Insertion Sort** | O(n²) | O(1) | ✅ | Dataset kecil |
| **Merge Sort** | O(n log n) | O(n) | ✅ | Dataset besar |

### Kenapa Merge Sort Dipilih?
✅ Performa konsisten O(n log n)  
✅ Optimal untuk dataset antrian yang bisa besar  
✅ Stable sorting (penting untuk FIFO terjaga dalam kategori)  
✅ Divide and conquer elegant dan efisien  

---

## 💾 PERSISTENSI DATA

### Penyimpanan ke CSV

```python
def save_data(antrian):
    """Menyimpan data antrian ke file CSV."""
    # antrian.csv - untuk antrian aktif
    # log_pelayanan.csv - untuk riwayat pelayanan
```

### File Storage
```
ASD_KEL1_TPLB/
├── antrian.csv          # Antrian aktif saat ini
├── log_pelayanan.csv    # Riwayat pasien yang sudah dilayani
└── engine.py            # Logic
```

### Auto-Load saat Startup

```python
def main():
    # Inisialisasi struktur data
    antrian = PriorityQueue()
    
    # Load data dari CSV saat program dimulai
    load_data(antrian)
    
    # ... Main loop
```

---

## 🎯 FITUR UNGGULAN

### 1. Priority Queue Terintegrasi
```python
# Pasien darurat mendapat prioritas
if kategori == "Darurat":
    # Masuk di depan pasien normal
    new_node.next = self.last_emergency.next
    self.last_emergency.next = new_node
```

### 2. Merge Sort O(n log n)
```python
# Sorting efisien untuk dataset besar
left = merge_sort(arr[:mid])
right = merge_sort(arr[mid:])
return merge(left, right)
```

### 3. Multi-Mode Sorting
```
Mode 1: Waktu (Default FIFO)
Mode 2: Alfabetis (A-Z dengan Merge Sort)
Mode 3: Urgensi (Darurat → Normal)
Mode 4: Gabungan (Urgensi + Alfabetis)
```

### 4. Smart Search
```python
# Cari berdasarkan:
# - Nama (partial): "budi" → "Budi Santoso"
# - ID (exact): "P001"
# - Tanggal (partial): "2026-05-20"
```

### 5. Stack-based Logging
```python
# LIFO: pasien terbaru duluan
for p in reversed(self.logs):
    print(f"[{p.waktu}] {p.id_pasien} - {p.nama}")
```

---

## 📊 CONTOH PENGGUNAAN LENGKAP

### Scenario: Simulasi Hari Kerja Klinik

```
1. Pagi (09:00-10:00):
   ├─ Registrasi Budi Santoso (Normal)  → P001
   ├─ Registrasi Ahmad Wijaya (Normal)  → P002
   ├─ Registrasi Rini Handoko (Darurat) → P003
   └─ Registrasi Siti Nurhaliza (Normal)→ P004

2. Menampilkan Antrian (Mode Gabungan):
   ├─ P003 Rini Handoko (Darurat)
   ├─ P001 Budi Santoso (Normal)
   ├─ P002 Ahmad Wijaya (Normal)
   └─ P004 Siti Nurhaliza (Normal)

3. Pelayanan:
   ├─ Panggil P003 → Selesai → Log
   ├─ Panggil P001 → Selesai → Log
   └─ Panggil P002 → Selesai → Log

4. Riwayat Pelayanan (Stack):
   ├─ [09:45] P002 - Ahmad Wijaya (SELESAI)
   ├─ [09:30] P001 - Budi Santoso (SELESAI)
   └─ [09:15] P003 - Rini Handoko (SELESAI)
```

---

## ✨ KESIMPULAN

Sistem Antrian Klinik mengintegrasikan:

✅ **Struktur Data Optimal**: Linked List + Priority Queue  
✅ **Algoritma Efisien**: Merge Sort O(n log n)  
✅ **Multi-Mode Display**: 4 mode sorting berbeda  
✅ **Smart Features**: Pencarian cerdas + Logging otomatis  
✅ **User-Friendly**: Interface berwarna + Validasi input  
✅ **Persistent**: Auto-save ke CSV  

Hasil: **Sistem antrian yang cepat, responsive, dan mudah digunakan** 🏥✨

---

**Presentasi Kelompok 1 - ASD TPLB**  
*Muhammad Ramdhan Maulana (Ketua)*
