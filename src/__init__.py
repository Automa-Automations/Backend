from .init.monkeypatch import MonkeypatchInternalRequests

MonkeypatchInternalRequests.patch_requests()

print("Requests Patched")
