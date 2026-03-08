import requests
from bs4 import BeautifulSoup

# kategori yang akan dicrawl
CATEGORIES = [
    "https://www.cnnindonesia.com/gaya-hidup/health",
    "https://www.cnnindonesia.com/gaya-hidup/food",
    "https://www.cnnindonesia.com/gaya-hidup/travel",
    "https://www.cnnindonesia.com/gaya-hidup/trends"
]

# identitas mahasiswa
NIM = "235150201111003"
INISIAL = "DCM"

# file output
output_file = "1_CRAWL_DwiCahyaMaulani_Mahasiswa_1.txt"

# header supaya tidak diblokir website
headers = {
    "User-Agent": "Mozilla/5.0"
}


# mengambil link artikel dari semua kategori
def get_article_links():

    links = []

    for url in CATEGORIES:

        print("Mengambil link dari:", url)

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.find_all("a", href=True):

            link = a["href"]

            if link.startswith("https://www.cnnindonesia.com/gaya-hidup"):

                if "/video/" not in link and "/foto/" not in link:

                    if link not in links:
                        links.append(link)

    return links


# mengambil isi artikel
def get_article_content(url):

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1")

    content_div = soup.find("div", class_="detail-text")

    if not title_tag or not content_div:
        return None, None

    title = title_tag.text.strip()

    paragraphs = content_div.find_all("p")

    text = " ".join([p.text.strip() for p in paragraphs])

    return title, text


# menyimpan artikel ke file
def save_article(file, idx, title, url, text):

    file.write("<DOC>\r\n")
    file.write(f"<ID>{INISIAL}-{idx}</ID>\r\n")
    file.write(f"<NIM>{NIM}</NIM>\r\n")
    file.write(f"<TITLE>{title}</TITLE>\r\n")
    file.write(f"<URL>{url}</URL>\r\n")
    file.write("<TEXT>\r\n")
    file.write(text + "\r\n")
    file.write("</TEXT>\r\n")
    file.write("</DOC>\r\n\r\n")


def main():

    links = get_article_links()

    print("Total link ditemukan:", len(links))

    count = 0

    with open(output_file, "w", encoding="ascii", errors="ignore", newline="") as f:

        for link in links:

            if count == 25:
                break

            try:

                title, text = get_article_content(link)

                if not title or not text.strip():
                    continue

                count += 1

                print("Crawling artikel", count)

                save_article(f, count, title, link, text)

            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    main()