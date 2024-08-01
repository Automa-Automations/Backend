
const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

app.use(express.json());

const sqlite3 = require('sqlite3').verbose();
const databaseUrl = process.env.DATABASE_URL;
const dbPath = new URL(databaseUrl).pathname;
const db = new sqlite3.Database(dbPath);

const getValidApiKey = async () => {
  return new Promise((resolve, reject) => {
    db.get('SELECT key FROM api_keys WHERE expired = 0 LIMIT 1', (err, row) => {
      if (err) {
        reject(err);
      } else if (row) {
        resolve(row.key);
      } else {
        resolve(null);
      }
    });
  });
};

const insertAPIKey = async (key) => {
  return new Promise((resolve, reject) => {
    const timestamp = Math.floor(Date.now() / 1000);
    console.log(timestamp);
    db.run("INSERT INTO api_keys (key, expired, created_at) VALUES (?, ?, ?)", [key, 0, timestamp], (err) => {
      if (err) {
        reject(err)
      } else {
        resolve()
      }
    })
  })
}

// Invalidate an API key
const invalidateApiKey = async (key) => {
  return new Promise((resolve, reject) => {
    db.run('UPDATE api_keys SET expired = 1 WHERE key = ?', [key], (err) => {
      if (err) {
        reject(err);
      } else {
        resolve();
      }
    });
  });
};


const endpoint = (type) => {
  return async (req, res) => {
    try {
      // Construct the target URL
      const targetUrl = `https://google.serper.dev/${type}`;

      // Extract payload from the request
      const payload = req.body;

      // Function to handle the request and retry logic
      const makeRequestWithRetry = async (headers, retryCount = 0) => {
        try {
          const response = await axios.post(targetUrl, payload, { headers });
          return response;
        } catch (error) {
          if (retryCount < 3 && (error.response?.status === 400 || error.response?.status === 429 || error.response?.status === 403)) {
            // Invalidate the current key and get a new one
            await invalidateApiKey(headers['X-API-KEY']);
            const newApiKey = await getValidApiKey();
            if (!newApiKey) {
              throw new Error('No valid API keys available');
            }
            headers['X-API-KEY'] = newApiKey;
            return makeRequestWithRetry(headers, retryCount + 1);
          } else {
            // If maximum retries reached or error is not 400/429, throw the error
            throw error;
          }
        }
      };

      // Get the initial valid API key
      const initialApiKey = await getValidApiKey();
      if (!initialApiKey) {
        return res.status(500).send('No valid API keys available');
      }

      // Define the headers for the target API
      const headers = {
        'X-API-KEY': initialApiKey,
        'Content-Type': 'application/json'
      };

      // Make the request with retry logic
      const response = await makeRequestWithRetry(headers);

      // Forward the response back to the client
      res.status(response.status).send(response.data);
    } catch (error) {
      // Handle any errors
      res.status(error.response?.status || 500).send(error.message);
    }
  };
};
app.post('/search', endpoint('search'));

app.post('/images', endpoint('images'));

app.post('/videos', endpoint('videos'));


app.post('/places', endpoint('places'));

app.post('/maps', endpoint('maps'));

app.post('/news', endpoint('news'));

app.post('/shopping', endpoint('shopping'));

app.post('/scholar', endpoint('scholar'));

app.post('/autocomplete', endpoint('autocomplete'));

app.post('/patents', endpoint('patents'));

app.post('/add-api-key', async (req, res) => {
  try {
    const { apiKey } = req.body;

    if (!apiKey) {
      return res.status(400).json({ error: 'API key is required' });
    }

    await insertAPIKey(apiKey);

    res.status(200).json({ message: 'API key added successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


app.listen(port, () => {
  console.log(`API server listening at http://localhost:${port}`);
});

