import math

# 1. BAGIAN RETRIEVAL (VSM)
def hitung_cosine(vektor_q, vektor_d):
    # Cari kata-kata yang ada di keduanya
    kata_irisan = set(vektor_q.keys()) & set(vektor_d.keys())
    
    # Hitung dot product
    atas = sum([vektor_q[kata] * vektor_d[kata] for kata in kata_irisan])
    
    # Hitung panjang vektor
    sum_q = sum([val**2 for val in vektor_q.values()])
    sum_d = sum([val**2 for val in vektor_d.values()])
    bawah = math.sqrt(sum_q) * math.sqrt(sum_d)
    
    if bawah == 0:
        return 0.0
    return atas / bawah

def cari_dokumen(query_vec, dict_vektor_doc, batas=15):
    skor_dokumen = {}
    
    for doc_id, doc_vec in dict_vektor_doc.items():
        skor = hitung_cosine(query_vec, doc_vec)
        if skor > 0:
            skor_dokumen[doc_id] = skor
            
    # Urutkan dari yang paling mirip
    hasil_urut = sorted(skor_dokumen.items(), key=lambda x: x[1], reverse=True)
    
    # Ambil sebanyak batas (minimal 10 sesuai soal)
    return hasil_urut[:batas]

# 2. BAGIAN EVALUASI
def evaluasi_per_query(hasil_pencarian, doc_relevan, k):
    top_k = hasil_pencarian[:k]
    # Pastikan perbandingan ID dilakukan dalam tipe data string agar akurat
    jml_relevan_ditemukan = len(set(str(d) for d in top_k) & set(str(r) for d in doc_relevan))
    
    precision = jml_relevan_ditemukan / k if k > 0 else 0.0
    recall = jml_relevan_ditemukan / len(doc_relevan) if len(doc_relevan) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return precision, recall, f1