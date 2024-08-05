import time
from urllib.parse import urlparse, urlunparse

import dns.resolver
import requests


class MonkeypatchInternalRequests:
    cached_records = []
    last_cache_update = 0
    cache_duration = 180

    @staticmethod
    def _update_cache():
        """Updates the cache if it isn't valid anymore."""
        current_time = time.time()
        if (
            current_time - MonkeypatchInternalRequests.last_cache_update
        ) > MonkeypatchInternalRequests.cache_duration:
            MonkeypatchInternalRequests.cached_records = (
                MonkeypatchInternalRequests._fetch_dns_records()
            )
            MonkeypatchInternalRequests.last_cache_update = current_time

    @staticmethod
    def _fetch_dns_records():
        """Fetch and return a list of internal aliases."""
        internal_aliases = MonkeypatchInternalRequests.get_txt_records("_apps.internal")
        if internal_aliases:
            aliases = internal_aliases[0].split(",")
            print(f"Internal Aliases: {aliases}")
            return aliases
        return []

    @staticmethod
    def get_txt_records(domain):
        """Fetch TXT records from DNS."""
        try:
            answers = dns.resolver.resolve(domain, "TXT")
            txt_records = [txt_string.decode("utf-8") for rdata in answers for txt_string in rdata.strings]  # type: ignore
            return txt_records
        except Exception as e:
            print(f"Error retrieving TXT records for {domain}: {e}")
            return []

    @staticmethod
    def _make_request(method, url, *args, **kwargs):
        """Handle request, expanding internal URLs if the URL uses the .internal TLD."""
        MonkeypatchInternalRequests._update_cache()
        original_url = url

        parsed_url = urlparse(url)
        port = (
            "80" if ":" not in parsed_url.netloc else parsed_url.netloc.split(":")[-1]
        )

        if parsed_url.netloc.replace(":" + port, "").strip().endswith(".internal"):
            base_domain = (
                parsed_url.netloc.replace(":" + port, "").strip().split(".")[0]
            )

            matching_alias = min(
                (
                    alias
                    for alias in MonkeypatchInternalRequests.cached_records
                    if alias.startswith(base_domain)
                ),
                key=len,
                default=None,
            )

            if matching_alias:
                new_netloc = f"{matching_alias}.flycast:{port}"
                parsed_url = parsed_url._replace(netloc=new_netloc)
                url = urlunparse(parsed_url)

                print(f"Modified URL: {url} (Original: {original_url})")

        return method(url, *args, **kwargs)

    @staticmethod
    def patched_get(url, *args, **kwargs):
        return MonkeypatchInternalRequests._make_request(
            original_get, url, *args, **kwargs
        )

    @staticmethod
    def patched_post(url, *args, **kwargs):
        return MonkeypatchInternalRequests._make_request(
            original_post, url, *args, **kwargs
        )

    @staticmethod
    def patched_put(url, *args, **kwargs):
        return MonkeypatchInternalRequests._make_request(
            original_put, url, *args, **kwargs
        )

    @staticmethod
    def patched_delete(url, *args, **kwargs):
        return MonkeypatchInternalRequests._make_request(
            original_delete, url, *args, **kwargs
        )

    @staticmethod
    def patch_requests():
        """Patch both requests module and requests.Session."""
        global original_get, original_post, original_put, original_delete

        original_get = requests.get
        original_post = requests.post
        original_put = requests.put
        original_delete = requests.delete

        requests.get = MonkeypatchInternalRequests.patched_get
        requests.post = MonkeypatchInternalRequests.patched_post
        requests.put = MonkeypatchInternalRequests.patched_put
        requests.delete = MonkeypatchInternalRequests.patched_delete

        requests.Session.get = MonkeypatchInternalRequests.patched_get  # type: ignore
        requests.Session.post = MonkeypatchInternalRequests.patched_post  # type: ignore
        requests.Session.put = MonkeypatchInternalRequests.patched_put  # type: ignore
        requests.Session.delete = MonkeypatchInternalRequests.patched_delete  # type: ignore
