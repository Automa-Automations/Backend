# Input

This is a simple microservice allowing us to effectively query the serper.dev api via many api-keys stored in a special database.
This is hosted on a fly.io instance.

# Setup

Run Command:
`$ fly launch` & follow the setup from fly.io

---

Setup Database:
`$ fly console ssh`

---

You can then move a keys.txt file created in the /data/ directory to the /data/sqlite.db file via this command:
`$ python3 /app/_write_keys_to_temp_db.py`

You should now be able to do successful queries!
