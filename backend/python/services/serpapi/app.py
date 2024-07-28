import asyncio
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, jsonify, request
from searchit import GoogleScraper, ScrapeRequest

app = Flask(__name__)
executor = ThreadPoolExecutor()


def run_scrape(scrape_request):
    google_scraper = GoogleScraper(
        max_results_per_page=10,
    )
    return asyncio.run(google_scraper.scrape(scrape_request))


@app.route("/search", methods=["GET"])
def search():
    # Extract query parameters from request
    query = request.args.get("query", default="watch movies online", type=str)
    max_results = request.args.get("max_results", default=30, type=int)
    lang = request.args.get("lang", default="en", type=str)
    geo = request.args.get("geo", default="us", type=str)

    # Create a ScrapeRequest instance with provided parameters
    scrape_request = ScrapeRequest(
        query,
        max_results,
        sleep=0,
        language=lang,
        geo=geo,
        proxy="http://gqnuguju-rotate:670myl2p6d9f@p.webshare.io:80/",
    )

    # Run the scraping asynchronously
    try:
        results = [
            {"title": i.title, "url": i.url}
            for i in executor.submit(run_scrape, scrape_request).result()
        ]
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(results)


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
