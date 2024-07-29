CREATE TABLE api_keys (
    key TEXT NOT NULL PRIMARY KEY,
    expired BOOLEAN NOT NULL,
    created_at INTEGER NOT NULL
);

