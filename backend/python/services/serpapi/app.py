import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, jsonify, request
from fp.fp import FreeProxy
from searchit import GoogleScraper, ScrapeRequest

app = Flask(__name__)
executor = ThreadPoolExecutor()


premium_proxy = "http://gqnuguju-rotate:670myl2p6d9f@p.webshare.io:80/"


# Get a list of proxies
def get_proxies(count: int):
    proxies = [FreeProxy(rand=True).get() for _ in range(count)]
    return proxies


# Function to run the scraping process
def run_scrape(scrape_request):
    google_scraper = GoogleScraper(
        max_results_per_page=10,
    )
    return asyncio.run(google_scraper.scrape(scrape_request))


# Function to handle retries and proxy rotation
def fetch_results_with_proxy(scrape_request, proxies, max_retries=3):
    for attempt in range(max_retries):
        for proxy in proxies:
            try:
                scrape_request.proxy = proxy
                results = run_scrape(scrape_request)
                return results
            except Exception as e:
                print(f"Proxy failed: {proxy}, error: {str(e)}")
                time.sleep(2)  # Small delay before trying the next proxy

        # If all proxies fail, retry with the premium proxy
        print("Retrying with premium proxy...")
        scrape_request.proxy = premium_proxy
        try:
            return run_scrape(scrape_request)
        except Exception as e:
            print(f"Premium proxy failed, error: {str(e)}")
            time.sleep(2)

    raise Exception("All proxies and premium proxy failed")


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
        proxy="http://placeholder.proxy",  # This will be overridden by fetch_results_with_proxy
    )

    # Run the scraping asynchronously with retries and proxy rotation
    try:
        # Define a list of free proxies and the premium proxy
        proxy_list = get_proxies(2)  # Adjust the count as needed

        results = [
            {"title": i.title, "url": i.url}
            for i in executor.submit(
                fetch_results_with_proxy, scrape_request, proxy_list
            ).result()
        ]
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(results)


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
