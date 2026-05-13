import csv
import os

FILE_ANTRIAN = 'antrian.csv'
FILE_LOG = 'log_pelayanan.csv'

def load_data(queue_obj):
    if os.path.exists(FILE_ANTRIAN):
        try:
            with open(FILE_ANTRIAN, mode='r', newline='')as file:
                reader = csv.DictReader(file)
                for row in reader:
                    #masuk ke queue lagi
                    # enqueue tanpa print
                    queue_obj.enqueue(row['nama'], row['kategori'])
                    print(f"[STORAGE] berhasil memuat antrian dari {FILE_ANTRIAN}")
        except Exception as e:
            print(f"[ERROR] gagal membaca file antrian: {e}")

            if os.path.exists(FILE_LOG):
                try:
                    with open(FILE_LOG, mode='r', newline='') as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            #membuat objek dummy
                            from engine import Node
                            node_log = Node(row['id'], row['nama'], row['kategori'])

                            queue_obj.logs.append(node_log)
                except Exception as e:
                    print(f"[ERROR] gagal membaca file log: {e}") 

def save_data(queue_obj):
    #1. simpan antrian
    try:
        with open(FILE_ANTRIAN, mode='w', newline='') as file:
            fieldnames = ['id', 'nama', 'kategori']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            curr = queue_obj.head
            while curr:
                writer.writerow({'id': curr.id, 'nama': curr.nama, 'kategori': curr.kategori})
                curr = curr.next
    except Exception as e:
        print(f"[ERROR] gagal menyimpan file antrian: {e}")
    
    try:
        with open(FILE_LOG, mode='w', newline='') as file:
            fieldnames = ['id', 'nama', 'kategori']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for p in queue_obj.logs:
                writer.writerow({'id': p.id_pasien, 'nama': p.nama, 'kategori': p.kategori})

    except Exception as e:
        print(f"[ERROR] gagal menyimpan log : {e}")