from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def get_prices():
    url = "https://www.kitcometals.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        rows = soup.select("table td")
        aluminum = None
        tin = None

        for i, cell in enumerate(rows):
            text = cell.get_text(strip=True).lower()
            if "aluminum" in text:
                aluminum = rows[i + 1].get_text(strip=True)
            elif "tin" in text:
                tin = rows[i + 1].get_text(strip=True)

        return jsonify({
            "aluminum": aluminum,
            "tin": tin
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
