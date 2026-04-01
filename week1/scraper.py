from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_contents(url):
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]


def fetch_via_jina(url):
    # Thêm r.jina.ai trước URL để mượn server của họ vượt rào
    headers = {"X-Return-Format": "markdown"}
    response = requests.get(f"https://r.jina.ai/{url}", headers=headers)
    return response.text[:2000]


def fetch_website_links(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        # Kiểm tra nếu request thành công
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Sử dụng set để loại bỏ link trùng lặp
        links = set()
        for tag in soup.find_all("a", href=True):
            href = tag.get("href")
            # Chuyển link tương đối thành link tuyệt đối
            full_url = urljoin(url, href)
            links.add(full_url)

        return list(links)

    except requests.exceptions.RequestException as e:
        print(f"Lỗi rồi: {e}")
        return []
