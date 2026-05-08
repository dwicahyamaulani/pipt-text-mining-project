import json
import re
import retrieval_evaluasi as reval

def bersihkan_kueri(teks):
    # Regex manual untuk hapus tanda baca dan kecilkan huruf
    bersih = re.sub(r'[^\w\s]', '', teks.lower())
    return bersih.split()

def buat_vektor(teks_user, data_idf):
    tokens = bersihkan_kueri(teks_user)
    # Hitung TF sederhana
    tf_q = {}
    for t in tokens:
        tf_q[t] = tf_q.get(t, 0) + 1
    
    # Hitung TF-IDF kueri
    vektor_q = {}
    for kata, nilai_tf in tf_q.items():
        if kata in data_idf:
            vektor_q[kata] = nilai_tf * data_idf[kata]
    return vektor_q

def main():
    print("Menyiapkan mesin pencari...")
    
    # Load data dengan encoding UTF-8
    try:
        with open('documents.json', 'r', encoding='utf-8') as f:
            data_asli = json.load(f)
        with open('doc_vectors.json', 'r', encoding='utf-8') as f:
            vektor_doc = json.load(f)
        with open('idf_values.json', 'r', encoding='utf-8') as f:
            data_idf = json.load(f)
    except Exception as e:
        print(f"Gagal memuat file: {e}")
        return

    print("-" * 50)
    kueri_raw = input("Masukkan kueri: ")
    v_kueri = buat_vektor(kueri_raw, data_idf)
    
    if not v_kueri:
        print("\nKata kunci tidak ditemukan di dokumen manapun.")
        return

    # Cari dokumen (top 15 agar > 10 sesuai soal)[cite: 2]
    hasil = reval.cari_dokumen(v_kueri, vektor_doc, batas=15)
    
    print("\nHASIL PENCARIAN:")
    for rank, (doc_id, skor) in enumerate(hasil, start=1):
        # Ambil info dokumen berdasarkan ID (pastikan ID dalam bentuk string)
        info = data_asli.get(str(doc_id), {})
        
        # Coba ambil judul (antisipasi nama key berbeda)
        judul = info.get('judul') or info.get('title') or "Judul tidak ditemukan"
        # Coba ambil konten
        konten = info.get('konten') or info.get('isi') or info.get('content') or "Konten kosong"
        
        # Tampilkan format sesuai soal: Judul | ID[cite: 2]
        print(f"{rank}. {judul.upper()} | ID={doc_id}")
        # Konten maksimal 200 karakter[cite: 2]
        print(f"   {konten[:200]}...\n")

    # Evaluasi
    doc_relevan = input(
        "\nMasukkan ID dokumen relevan "
        "(pisahkan dengan koma): "
    )

    doc_relevan = [
        x.strip()
        for x in doc_relevan.split(",")
    ]

    precision, recall, f1 = reval.evaluasi_per_query(
        hasil,
        doc_relevan,
        k=5
    )

    map_score = reval.hitung_map(
        hasil,
        doc_relevan,
        k=5
    )

    print("\nHASIL EVALUASI")
    print(f"Precision@5 : {precision:.2f}")
    print(f"Recall@5    : {recall:.2f}")
    print(f"F1-score@5  : {f1:.2f}")
    print(f"MAP@5       : {map_score:.2f}")

if __name__ == "__main__":
    main()