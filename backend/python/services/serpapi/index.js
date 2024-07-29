
const express = require('express');
const axios = require('axios');
const app = express();
const port = 3989;

// Middleware to parse JSON bodies
app.use(express.json());

// API endpoint
const endpoint = (type) => {
  return async (req, res) => {

    try {
      // Construct the target URL
      const targetUrl = `https://google.serper.dev/${type}`;

      // Extract payload and headers from the request
      // Define the headers for the target API
      const headers = {
        'X-API-KEY': internalApiKey,
        'Content-Type': 'application/json'
      };

      // Make the request to the target API
      const response = await axios.post(targetUrl, req.body, { headers });

      // Forward the response back to the client
      res.status(response.status).send(response.data);
    } catch (error) {
      // Handle any errors
      res.status(error.response?.status || 500).send(error.message);
    }
  }
}
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

app.listen(port, () => {
  console.log(`API server listening at http://localhost:${port}`);
});

