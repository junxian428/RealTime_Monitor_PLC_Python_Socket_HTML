const express = require('express');
const app = express();
const port = 3000;
const dotenv = require('dotenv');
dotenv.config();


// Set the view engine to EJS
app.set('view engine', 'ejs');

app.get('/', (req, res) => {
  const message = 'No real time data from PLC';
 const database = "data";
  res.render('index', { message, database,  websocketUrl: process.env.WEBSOCKET_URL });


});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
