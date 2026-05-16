import os
import streamlit as st

from main import (
    muat_data,
    cari_folder_data,
    buat_vektor_kueri,
    cari_dokumen,
    ringkas_dokumen,
    ambil_info,
)


@st.cache_resource(show_spinner="Memuat data indeks...")
def muat_data_cached(folder):
    return muat_data(folder)


def main():
    st.set_page_config(
        page_title="Search Engine",
        page_icon="🔍",
        layout="wide",
    )

    st.markdown(
        """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        html, body, p, div, input, button, label,
        h1, h2, h3, h4, h5, h6, [class*="css"] {
            font-family: 'Poppins', sans-serif !important;
        }

        [data-testid="stSidebarCollapseButton"] span,
        [data-testid="collapsedControl"] span,
        .material-symbols-rounded,
        .material-icons {
            font-family: 'Material Symbols Rounded', 'Material Icons' !important;
        }
        
        .stApp { background: #0f0f13; color: #e8e8f0; }
        section[data-testid="stSidebar"] { background: #13131a !important; border-right: 1px solid #1e1e2e !important; }

        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: #0f0f13; }
        ::-webkit-scrollbar-thumb { background: #2a2a3d; border-radius: 4px; }

        /* Hero */
        .hero { text-align:center; padding:2.8rem 1rem 2rem; margin-bottom:1.5rem; }
        .hero .badge { display:inline-block; background:transparent; border:1.5px solid #7c6fff; color:#fff; font-size:0.72rem; font-weight:600; letter-spacing:1px; text-transform:uppercase; padding:4px 16px; border-radius:100px; margin-bottom:1rem; }
        .hero h1 { font-size:2.4rem; font-weight:700; color:#ffffff; margin:0 0 0.5rem; letter-spacing:-0.5px; }
        .hero h1 span { background:linear-gradient(180deg,#b8a8ff,#7c6fff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
        .hero p { color:#6b6b8a; font-size:0.88rem; font-weight:400; margin:0; }

        /* Search */
        .stTextInput > div > div > input { background:#1a1a26 !important; border:1.5px solid #2a2a3d !important; color:#e8e8f0 !important; border-radius:14px !important; font-size:0.95rem !important; padding:0.7rem 1.2rem !important; transition:border-color 0.2s,box-shadow 0.2s !important; }
        .stTextInput > div > div > input::placeholder { color:#9090b0 !important; }
        .stTextInput > div > div > input:focus { border-color:#7c6fff !important; box-shadow:0 0 0 3px #7c6fff22 !important; }

        /* Button — vertical gradient, atas ungu muda → bawah gelap */
        .stButton > button {
            background: linear-gradient(180deg, #a78fff 0%, #5b3fd4 100%) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 14px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            padding: 0.7rem 1.2rem !important;
            transition: background 0.2s, transform 0.15s, box-shadow 0.2s !important;
            box-shadow: 0 4px 20px #7c6fff44 !important;
            position: relative !important;
        }
        .stButton > button:hover {
            background: linear-gradient(180deg, #baa8ff 0%, #6d4fe0 100%) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 24px #7c6fff55 !important;
        }
        .stButton > button:active {
            transform: translateY(0px) !important;
            box-shadow: 0 2px 10px #7c6fff33 !important;
        }

        /* Stats pills */
        .stats-bar { display:flex; gap:0.8rem; margin-bottom:1.5rem; flex-wrap:wrap; }
        .stat-pill { background:#1a1a26; border:1px solid #2a2a3d; border-radius:100px; padding:6px 18px; font-size:0.78rem; color:#6b6b8a; display:inline-flex; align-items:center; gap:6px; }
        .stat-pill b { color:#e8e8f0; font-weight:600; }

        /* Hasil header */
        .hasil-header { font-size:0.78rem; color:#9090b0; font-weight:500; letter-spacing:0.5px; text-transform:uppercase; margin-bottom:1rem; padding-left:2px; }

        /* Cards */
        .result-card { background:#1a1a26; border:1px solid #2a2a3d; border-radius:16px; padding:1.2rem 1.4rem; margin-bottom:0.8rem; transition:border-color 0.2s,transform 0.15s; }
        .result-card:hover { border-color:#7c6fff44; transform:translateY(-1px); }
        .result-card.top3 { border-left:3px solid #7c6fff; }

        /* Rank badge */
        .rank-badge { display:inline-flex; align-items:center; justify-content:center; width:26px; height:26px; border-radius:8px; font-size:0.72rem; font-weight:700; margin-right:8px; flex-shrink:0; }
        .rank-1 { background:linear-gradient(180deg,#c9b8ff,#7c6fff); color:#0f0f13; }
        .rank-2 { background:linear-gradient(180deg,#a890f0,#5b3fd4); color:#fff; }
        .rank-3 { background:linear-gradient(180deg,#8b70e0,#3d25a8); color:#fff; }
        .rank-n  { background:#2a2a3d; color:#6b6b8a; }

        .doc-title-row { display:flex; align-items:center; margin-bottom:0.6rem; flex-wrap:wrap; gap:6px; }
        .doc-judul { font-size:0.92rem; font-weight:600; color:#c9b8ff; flex:1; }
        .doc-id-label { font-size:0.7rem; color:#9090b0; background:#13131a; border:1px solid #2a2a3d; border-radius:6px; padding:2px 8px; white-space:nowrap; }

        /* Kalimat */
        .kalimat-row { font-size:0.82rem; color:#9090b0; line-height:1.65; margin-bottom:0.4rem; padding-left:0.6rem; border-left:2px solid #2a2a3d; }
        .kalimat-row .idk { display:inline-block; background:#13131a; border:1px solid #2a2a3d; color:#7c6fff; font-size:0.68rem; font-weight:600; padding:0px 6px; border-radius:5px; margin-left:4px; vertical-align:middle; }

        /* Upload hint */
        .upload-hint { text-align:center; color:#9090b0; font-size:0.88rem; padding:4rem 1rem; border:1.5px dashed #2a2a3d; border-radius:16px; margin-top:2rem; }
        .upload-hint b { color:#6b6b8a; }
        .upload-hint code { background:#1a1a26; border:1px solid #2a2a3d; border-radius:5px; padding:1px 6px; color:#c9b8ff; font-size:0.82rem; }

        /* Sidebar */
        .file-list { background:#13131a; border:1px solid #2a2a3d; border-radius:10px; padding:10px 14px; font-size:0.75rem; color:#6b6b8a; line-height:2; }
        .file-list span { color:#c9b8ff; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="hero">
      <div class="badge">PIPT &nbsp;·&nbsp; Tugas 4</div>
      <h1>🔍 Search Engine</h1>
      <p>Aufii Fathin Nabila &nbsp;·&nbsp; Dwi Cahya Maulani &nbsp;·&nbsp; Afifah Nabila Devi</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown(
            "<div style='font-size:0.7rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#9090b0;margin-bottom:0.4rem'>Konfigurasi Data</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<hr style='border-color:#1e1e2e;margin:0.5rem 0 0.8rem'>",
            unsafe_allow_html=True,
        )

        default_folder = ""
        try:
            default_folder = cari_folder_data()
        except FileNotFoundError:
            pass

        folder_path = st.text_input(
            "Path folder data",
            value=default_folder,
            placeholder="/path/ke/tugas3",
            help="Folder yang berisi documents.json, doc_vectors.json, idf_values.json",
        )

        st.markdown(
            "<hr style='border-color:#1e1e2e;margin:0.8rem 0'>", unsafe_allow_html=True
        )
        st.markdown(
            """
        <div class="file-list">
          📄 <span>documents.json</span><br>
          📄 <span>doc_vectors.json</span><br>
          📄 <span>idf_values.json</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    if not folder_path or not os.path.exists(
        os.path.join(folder_path, "documents.json")
    ):
        st.markdown(
            """
        <div class="upload-hint">
          <div style="font-size:2.5rem;margin-bottom:0.8rem">📂</div>
          <b>Folder data belum ditemukan</b><br><br>
          Masukkan path folder data di sidebar kiri.<br><br>
          Pastikan berisi <code>documents.json</code>, <code>doc_vectors.json</code>, dan <code>idf_values.json</code>.
        </div>
        """,
            unsafe_allow_html=True,
        )
        return

    try:
        dokumen, vektor_doc, data_idf = muat_data_cached(folder_path)
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return

    st.markdown(
        f"""
    <div class="stats-bar">
      <div class="stat-pill">📚 Dokumen: <b>{len(dokumen):,}</b></div>
      <div class="stat-pill">📝 Term IDF: <b>{len(data_idf):,}</b></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        kueri_raw = st.text_input(
            "Kueri",
            placeholder="Masukkan kueri pencarian...",
            label_visibility="collapsed",
        )
    with col_btn:
        cari = st.button("Cari", use_container_width=True)

    if (cari or kueri_raw) and kueri_raw.strip():
        kueri_raw = kueri_raw.strip()

        v_kueri = buat_vektor_kueri(kueri_raw, data_idf)
        if not v_kueri:
            st.warning("Kata kunci tidak ditemukan dalam indeks. Coba kata lain.")
            return

        hasil = cari_dokumen(v_kueri, vektor_doc, batas=10)
        if not hasil:
            st.info("Tidak ada dokumen yang cocok.")
            return

        st.markdown(
            f"""
        <div class="hasil-header">
          Hasil Pencarian &nbsp;·&nbsp; kueri: '{kueri_raw}'
        </div>
        """,
            unsafe_allow_html=True,
        )

        for rank, (doc_id, _skor) in enumerate(hasil, start=1):
            info = ambil_info(dokumen, doc_id)
            judul = info.get("title") or info.get("judul") or "(judul tidak tersedia)"
            konten = info.get("content") or info.get("konten") or ""

            if rank == 1:
                badge = '<span class="rank-badge rank-1">1</span>'
            elif rank == 2:
                badge = '<span class="rank-badge rank-2">2</span>'
            elif rank == 3:
                badge = '<span class="rank-badge rank-3">3</span>'
            else:
                badge = f'<span class="rank-badge rank-n">{rank}</span>'

            if rank <= 3:
                ringkasan = ringkas_dokumen(konten, data_idf, top_n=3) if konten else []

                kalimat_html = ""
                if ringkasan:
                    for idx_kalimat, teks_kalimat in ringkasan:
                        tampil = (
                            teks_kalimat
                            if len(teks_kalimat) <= 300
                            else teks_kalimat[:297] + "..."
                        )
                        kalimat_html += f'<div class="kalimat-row">{tampil} <span class="idk">[{idx_kalimat}]</span></div>'
                else:
                    cuplikan = konten[:250] + "..." if len(konten) > 250 else konten
                    kalimat_html = f'<div class="kalimat-row">{cuplikan or "(konten tidak tersedia)"}</div>'

                st.markdown(
                    f"""
                <div class="result-card top3">
                  <div class="doc-title-row">
                    {badge}
                    <span class="doc-judul">{judul.upper()}</span>
                    <span class="doc-id-label">ID: {doc_id}</span>
                  </div>
                  {kalimat_html}
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                <div class="result-card">
                  <div class="doc-title-row">
                    {badge}
                    <span class="doc-judul">{judul}</span>
                    <span class="doc-id-label">ID: {doc_id}</span>
                  </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )


if __name__ == "__main__":
    main()
