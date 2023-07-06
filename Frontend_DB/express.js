const express = require('express');
const app = express();
const port = 3000;
const dotenv = require('dotenv');
dotenv.config();


const db = require('./db');



// Set the view engine to EJS
app.set('view engine', 'ejs');


app.get('/', async (req, res) => {
  const message = 'No real time data from PLC';
 var database = "data";

 //console.log('All users:', users);

  // Perform a sample query
  const query = 'SELECT * FROM PLC';
  const PLC = await db.query(query);
  console.log('All address:', PLC);

    database =  JSON.stringify(PLC);

  res.render('index', { message, database,  websocketUrl: process.env.WEBSOCKET_URL });


});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
