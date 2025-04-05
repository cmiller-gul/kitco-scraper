from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route("/")
def get_prices():
    url = "https://www.kitcometals.com/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        rows = soup.select("table td")

        aluminum = None
        tin = None

        for i, cell in enumerate(rows):
            text = cell.get_text(strip=True).lower()
            if "aluminum" in text and not aluminum:
                aluminum = rows[i + 1].get_text(strip=True)
            elif "tin" in text and not tin:
                tin = rows[i + 1].get_text(strip=True)

        return jsonify({
            "aluminum": aluminum or "Not found",
            "tin": tin or "Not found"
        })

    except Exception as e:
        print(f"Error scraping Kitco: {e}")
        return jsonify({"error": "Scraping failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
