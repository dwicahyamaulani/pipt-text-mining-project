import math

# 1. BAGIAN RETRIEVAL (VSM)
def hitung_cosine(vektor_q, vektor_d):

    # Cari kata yang sama pada query dan dokumen
    kata_irisan = set(vektor_q.keys()) & set(vektor_d.keys())

    # Hitung dot product
    atas = sum(
        [
            vektor_q[kata] * vektor_d[kata]
            for kata in kata_irisan
        ]
    )

    # Hitung panjang vektor query
    sum_q = sum([val**2 for val in vektor_q.values()])

    # Hitung panjang vektor dokumen
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

    # Urutkan dari similarity tertinggi
    hasil_urut = sorted(
        skor_dokumen.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # Ambil top-k dokumen
    return hasil_urut[:batas]


# 2. BAGIAN EVALUASI
def evaluasi_per_query(
    hasil_pencarian,
    doc_relevan,
    k
):

    # Ambil doc_id saja
    top_k = [
        str(doc_id)
        for doc_id, skor in hasil_pencarian[:k]
    ]

    # Hitung jumlah relevan ditemukan
    jml_relevan_ditemukan = len(
        set(top_k) &
        set(str(r) for r in doc_relevan)
    )

    # Precision@k
    precision = (
        jml_relevan_ditemukan / k
        if k > 0 else 0.0
    )

    # Recall@k
    recall = (
        jml_relevan_ditemukan / len(doc_relevan)
        if len(doc_relevan) > 0 else 0.0
    )

    # F1-score@k
    f1 = (
        2 * (precision * recall)
        / (precision + recall)
        if (precision + recall) > 0 else 0.0
    )

    return precision, recall, f1


# 3. MAP@K
def hitung_map(
    hasil_pencarian,
    doc_relevan,
    k
):

    # Ambil top-k dokumen
    top_k = [
        str(doc_id)
        for doc_id, skor in hasil_pencarian[:k]
    ]

    doc_relevan = set(
        str(r) for r in doc_relevan
    )

    jumlah_relevan = 0
    total_precision = 0

    for i, doc_id in enumerate(top_k, start=1):

        if doc_id in doc_relevan:

            jumlah_relevan += 1

            precision_i = (
                jumlah_relevan / i
            )

            total_precision += precision_i

    if len(doc_relevan) == 0:
        return 0.0

    map_score = (
        total_precision / len(doc_relevan)
    )

    return map_score