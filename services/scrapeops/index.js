const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;
const qs = require("querystring")

app.use(express.json());

const sqlite3 = require('sqlite3').verbose();
const databaseUrl = process.env.DATABASE_URL;
const dbPath = new URL(databaseUrl).pathname;
const db = new sqlite3.Database(dbPath);


const getValidApiKey = async (random = false) => {
  return new Promise((resolve, reject) => {
    const query = random
      ? 'SELECT key FROM api_keys WHERE expired = 0 ORDER BY RANDOM() LIMIT 1'
      : 'SELECT key FROM api_keys WHERE expired = 0 LIMIT 1';

    db.get(query, (err, row) => {
      if (err) {
        reject(err);
      } else if (row) {
        resolve(row.key);
      } else {
        resolve(null);
      }
    });
  });
}


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


const endpoint = () => {
  return async (req, res) => {
    try {
      // Construct the target URL
      const targetUrl = `https://proxy.scrapeops.io/v1/`;

      // Extract payload from the request
      const payload = req.body;

      // Function to handle the request and retry logic
      const makeRequestWithRetry = async (payload, retryCount = 0) => {
        try {
          const response = await axios.get(`${targetUrl}?${qs.stringify(payload)}`);
          return response;
        } catch (error) {
          if (retryCount < 3 && (error.response?.status === 401 || error.response?.status == 403)) {
            // Invalidate the current key and get a new one
            await invalidateApiKey(payload['api_key']);
            const newApiKey = await getValidApiKey();
            if (!newApiKey) {
              throw new Error('No valid API keys available');
            }
            payload['api_key'] = newApiKey;
            return makeRequestWithRetry(payload, retryCount + 1);
          } else if (error.response?.status === 429) {
            console.log("Error Originated due to Concurrency Limit. Switching API Key")
            payload['api_key'] = await getValidApiKey(true)
            return makeRequestWithRetry(payload, retryCount + 1)
          } else {
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
      const newPayload = { ...payload, 'api_key': initialApiKey }
      const response = await makeRequestWithRetry(newPayload);

      // Forward the response back to the client
      res.status(response.status).send(response.data);
    } catch (error) {
      // Handle any errors
      console.log("Error", error.message)
      res.status(error.response?.status || 500).send(error.message);
    }
  };
};

app.post('/v1', endpoint());

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
