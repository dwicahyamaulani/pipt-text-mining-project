import json
import re
import math
import os
import sys


# BAGIAN 1: UTILITAS PREPROCESSING
def bersihkan_token(teks):
    """Tokenisasi sederhana: ubah ke huruf kecil, hapus tanda baca."""
    bersih = re.sub(r'[^\w\s]', '', teks.lower())
    return [t for t in bersih.split() if t]


def pecah_kalimat(teks):
    """
    Memecah teks menjadi daftar kalimat.
    Pemisah: titik, tanda tanya, tanda seru.
    Kalimat dengan < 3 kata diabaikan.
    """
    kalimat_raw = re.split(r'(?<=[.!?])\s+', teks)
    return [k.strip() for k in kalimat_raw if len(k.strip().split()) >= 3]


# BAGIAN 2: PERINGKASAN EXTRACTIVE BERBASIS TF-IDF 
def hitung_tf_kalimat(tokens):
    """
    Hitung Term Frequency (TF) untuk sebuah kalimat.
    TF(t, kalimat) = frekuensi(t) / jumlah_kata_kalimat
    """
    tf = {}
    n = len(tokens)
    if n == 0:
        return tf
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1
    for t in tf:
        tf[t] = tf[t] / n
    return tf


def skor_kalimat_tfidf(kalimat, data_idf):
    """
    Hitung skor TF-IDF sebuah kalimat.

    Rumus per kata:  TF(t, kalimat) x IDF(t, korpus)
    Skor kalimat  :  rata-rata TF-IDF dari semua kata yang ada di IDF

    Menggunakan rata-rata (bukan jumlah) agar kalimat panjang
    tidak otomatis mendapat skor lebih tinggi dari kalimat pendek.
    """
    tokens = bersihkan_token(kalimat)
    if not tokens:
        return 0.0
    tf = hitung_tf_kalimat(tokens)
    total_skor = 0.0
    jumlah_kata_ada = 0
    for kata, nilai_tf in tf.items():
        if kata in data_idf:
            total_skor += nilai_tf * data_idf[kata]
            jumlah_kata_ada += 1
    return total_skor / jumlah_kata_ada if jumlah_kata_ada else 0.0


def ringkas_dokumen(konten, data_idf, top_n=3):
    """
    Peringkasan teks extractive: pilih top_n kalimat berdasarkan skor TF-IDF.

    Algoritma:
      1. Pecah dokumen menjadi kalimat
      2. Hitung skor TF-IDF tiap kalimat (TF per-kalimat, IDF dari korpus)
      3. Ambil top_n kalimat skor tertinggi
      4. Urutkan kembali sesuai urutan kemunculan asli di dokumen

    Returns:
        list of (indeks_kalimat_asli: int, teks_kalimat: str)
        [IDK] = indeks kalimat, dimulai dari 0 (kalimat pertama)
    """
    kalimat = pecah_kalimat(konten)
    if not kalimat:
        return []

    skor_list = [(idx, k, skor_kalimat_tfidf(k, data_idf))
                 for idx, k in enumerate(kalimat)]

    # Ambil top_n berdasarkan skor tertinggi
    skor_urut = sorted(skor_list, key=lambda x: x[2], reverse=True)
    top_indices = sorted(item[0] for item in skor_urut[:top_n])

    # Kembalikan dalam urutan asli dokumen
    return [(idx, kalimat[idx]) for idx in top_indices]


# BAGIAN 3: RETRIEVAL – Vector Space Model (dari Tugas 3)
def hitung_cosine(vektor_q, vektor_d):
    """Cosine similarity antara dua vektor TF-IDF."""
    irisan = set(vektor_q.keys()) & set(vektor_d.keys())
    atas   = sum(vektor_q[k] * vektor_d[k] for k in irisan)
    sum_q  = sum(v ** 2 for v in vektor_q.values())
    sum_d  = sum(v ** 2 for v in vektor_d.values())
    bawah  = math.sqrt(sum_q) * math.sqrt(sum_d)
    return atas / bawah if bawah != 0 else 0.0


def buat_vektor_kueri(teks, data_idf):
    """Buat vektor TF-IDF dari teks kueri (TF dihitung dari kueri)."""
    tokens = bersihkan_token(teks)
    tf_q = {}
    for t in tokens:
        tf_q[t] = tf_q.get(t, 0) + 1
    return {kata: tf * data_idf[kata]
            for kata, tf in tf_q.items() if kata in data_idf}


def cari_dokumen(vektor_kueri, vektor_doc, batas=10):
    """Kembalikan top-batas dokumen paling relevan (cosine similarity)."""
    skor = {}
    for doc_id, doc_vec in vektor_doc.items():
        s = hitung_cosine(vektor_kueri, doc_vec)
        if s > 0:
            skor[doc_id] = s
    return sorted(skor.items(), key=lambda x: x[1], reverse=True)[:batas]


# BAGIAN 4: LOADER & TAMPILAN
def cari_folder_data():
    """Cari folder yang berisi documents.json secara otomatis."""
    kandidat = [
        os.getcwd(),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tugas3'),
        os.path.dirname(os.path.abspath(__file__)),
    ]
    if len(sys.argv) > 1:
        kandidat.insert(0, sys.argv[1])

    for folder in kandidat:
        if os.path.exists(os.path.join(folder, 'documents.json')):
            return os.path.abspath(folder)

    raise FileNotFoundError(
        "Tidak dapat menemukan folder data (documents.json).\n"
        "Jalankan dari folder tugas3, atau berikan path sebagai argumen:\n"
        "  python main.py /path/ke/tugas3"
    )


def muat_data(folder):
    """Muat tiga file JSON dari folder data."""
    def baca(nama):
        with open(os.path.join(folder, nama), 'r', encoding='utf-8') as f:
            return json.load(f)
    print(f"  Folder data : {folder}")
    return baca('documents.json'), baca('doc_vectors.json'), baca('idf_values.json')


def ambil_info(dokumen, doc_id):
    """Ambil info dokumen dengan key string maupun int."""
    return dokumen.get(str(doc_id), dokumen.get(doc_id, {}))


def tampilkan_ringkasan(rank, doc_id, info, data_idf):
    """Tampilkan hasil pencarian dengan peringkasan extractive TF-IDF."""
    judul  = info.get('title') or info.get('judul') or "(judul tidak tersedia)"
    konten = info.get('content') or info.get('konten') or ""

    print(f"\n{rank}. {judul.upper()} | ID={doc_id}")

    ringkasan = ringkas_dokumen(konten, data_idf, top_n=3) if konten else []

    if ringkasan:
        for idx_kalimat, teks_kalimat in ringkasan:
            tampil = (teks_kalimat if len(teks_kalimat) <= 300
                      else teks_kalimat[:297] + "...")
            print(f"   {tampil} [{idx_kalimat}]")
    else:
        cuplikan = konten[:250] + "..." if len(konten) > 250 else konten
        print(f"   {cuplikan or '(konten tidak tersedia)'}")


# BAGIAN 5: PROGRAM UTAMA
def main():
    print("=" * 65)
    print("  Mesin Pencari + Peringkasan Teks Extractive (TF-IDF)")
    print("  Tugas 4 – PIPT 2026")
    print("=" * 65)
    print("Memuat data...", flush=True)

    try:
        folder = cari_folder_data()
        dokumen, vektor_doc, data_idf = muat_data(folder)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"\n[ERROR] {e}")
        return

    print(f"  Jumlah dokumen  : {len(dokumen):,}")
    print(f"  Jumlah term IDF : {len(data_idf):,}")
    print("-" * 65)

    while True:
        kueri_raw = input("\nMasukkan kueri (atau 'keluar' untuk berhenti): ").strip()
        if not kueri_raw or kueri_raw.lower() in ('keluar', 'exit', 'quit', 'q'):
            print("Program selesai.")
            break

        v_kueri = buat_vektor_kueri(kueri_raw, data_idf)
        if not v_kueri:
            print("  Kata kunci tidak ditemukan dalam indeks. Coba kata lain.")
            continue

        hasil = cari_dokumen(v_kueri, vektor_doc, batas=10)
        if not hasil:
            print("  Tidak ada dokumen yang cocok.")
            continue

        print(f"\nHASIL PENCARIAN: (kueri='{kueri_raw}', {len(hasil)} dokumen)")
        print("=" * 65)

        for rank, (doc_id, skor) in enumerate(hasil, start=1):
            info = ambil_info(dokumen, doc_id)

            if rank <= 3:
                # Top-3: tampilkan dengan ringkasan extractive TF-IDF
                tampilkan_ringkasan(rank, doc_id, info, data_idf)
            else:
                # Rank 4+: judul saja
                judul = info.get('title') or info.get('judul') or "(judul tidak tersedia)"
                print(f"\n{rank}. {judul} | ID={doc_id}")

        print("\n" + "=" * 65)


if __name__ == "__main__":
    main()