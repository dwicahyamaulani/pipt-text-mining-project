import requests
from bs4 import BeautifulSoup

# inisialisasi
CATEGORIES = [
    "https://www.cnnindonesia.com/hiburan",
    "https://www.cnnindonesia.com/hiburan/seleb",
    "https://www.cnnindonesia.com/hiburan/musik",
    "https://www.cnnindonesia.com/hiburan/film",
]
NIM = "235150200111002"
INISIAL = "AFN"

output_file = "data/2_CRAWL_AufiiFathinNabila_2.txt"
headers = {"User-Agent": "Mozilla/5.0"}


# function ambil link
def get_article_links():
    links = []

    for url in CATEGORIES:
        print("Ambil link dari:", url)

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.find_all("a", href=True):
            link = a["href"]

            if link.startswith("https://www.cnnindonesia.com/hiburan/2"):
                if "/video/" not in link and "/foto/" not in link:
                    if link not in links:
                        links.append(link)
    return links


# function ambil content
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


# function simpan artikel ke file
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
