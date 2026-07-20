<h1 align="center">Indonesian News Search Engine</h1>

<p align="center">
  <em>From Raw News Articles to a Working Search Engine</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/streamlit-app-ff4b4b" alt="Streamlit">
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status">
</p>

> An end-to-end Indonesian-language text mining pipeline: crawl news articles, preprocess and clean the corpus, build a TF-IDF vector space retrieval engine, and serve it through an interactive search app with automatic extractive summarization.

The project follows a classic text mining pipeline: **collect → clean & represent → rank & retrieve → serve**, with each stage building directly on the output of the one before it.

---

## Table of Contents

- [Overview](#overview)
- [Team](#team)
- [Pipeline](#pipeline)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)

---

## Overview

This project scrapes news articles from CNN Indonesia across multiple categories, turns them into a searchable TF-IDF corpus, and wraps it in a Streamlit search engine that returns ranked results with auto-generated 3-sentence summaries for the top matches, all built from scratch without external ML/NLP frameworks.

The final deliverable is a **Streamlit-based search engine interface**: type a query, hit search, and get ranked articles with extractive summaries for the top 3 matches.

<img width="2560" height="1328" alt="image" src="https://github.com/user-attachments/assets/ebf7e7f9-04ab-4f2b-96c2-1bfdfb051ac9" />

---

## Team

| Name | Initials |
| --- | --- |
| Aufii Fathin Nabila | AFN |
| Afifah Nabila Devi | AND |
| Dwi Cahya Maulani | DCM |

---

## Pipeline

| Stage | What it does | Output |
| --- | --- | --- |
| **1. Crawler** | Scrapes articles from CNN Indonesia (entertainment, international, etc.) with `requests` + `BeautifulSoup`. | Structured raw `.txt` corpus per category |
| **2. Preprocessing** | Tokenization, normalization, and text cleaning of the raw corpus. | Cleaned dataset (notebook) |
| **3. Retrieval Engine** | Builds TF-IDF weights, an inverted index, and evaluates retrieval quality (precision/recall). | `documents.json`, `doc_vectors.json`, `idf_values.json`, `inverted_index.json` |
| **4. Search App** | Cosine-similarity search with extractive TF-IDF summarization, served through a Streamlit UI. | `app.py`, `main.py` |

---

## Project Structure

```
pipt-text-mining-project/
├── data/
│   ├── tugas1/          # Raw crawled corpus, by category
│   └── tugas2/          # Preprocessed / cleaned data
└── src/
    ├── tugas1_crawl/
    │   ├── crawler_afn.py   # Entertainment category
    │   ├── crawler_and.py   # International category
    │   └── crawler_dcm.py   # Additional category
    ├── tugas2/
    │   └── notebook-tugas2.ipynb
    ├── tugas3/
    │   ├── main.py
    │   ├── retrieval_evaluasi.py
    │   ├── documents.json
    │   ├── doc_vectors.json / tfidf_weights.json
    │   ├── idf_values.json
    │   ├── inverted_index.json
    │   └── notebook-tugas3.ipynb
    └── tugas4/
        ├── app.py        # Streamlit search engine UI
        └── main.py        # Retrieval + summarization logic
```

---

## Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/dwicahyamaulani/pipt-text-mining-project.git
   cd pipt-text-mining-project
   ```

2. **Set up an environment and install dependencies**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   # source .venv/bin/activate # macOS/Linux

   pip install requests beautifulsoup4 streamlit
   ```

---

## Usage

### Run the search engine

```bash
cd src/tugas4
streamlit run app.py
```

On first launch, point **Path folder data** in the sidebar to the folder containing `documents.json`, `doc_vectors.json`, and `idf_values.json` (defaults to `src/tugas3`). Once the index loads, type a query and hit **Cari** — the top 3 results come with a 3-sentence extractive summary, the rest are ranked below.

It also runs as a plain CLI, no browser needed:

```bash
cd src/tugas4
python main.py /path/to/tugas3
```

### Re-run the crawler

```bash
cd src/tugas1_crawl
python crawler_afn.py   # or crawler_and.py / crawler_dcm.py
```

---

## How It Works

**Crawling**: each script scrapes a fixed set of CNN Indonesia category pages, pulls article title + body, and writes them into a structured `.txt` corpus (`<DOC>`, `<TITLE>`, `<URL>`, `<TEXT>`).

**Retrieval**: every document is represented as a TF-IDF vector. A query is turned into a vector the same way, and documents are ranked by cosine similarity against it.

**Summarization**: for the top 3 results, the document is split into sentences, each scored by its *average* TF-IDF (not sum, so long sentences aren't favored by default), and the 3 highest-scoring sentences are shown back in their original order.

**Interface**: a Streamlit app displays corpus stats (document count, IDF term count), a search box, and ranked result cards with summaries for the top matches.
