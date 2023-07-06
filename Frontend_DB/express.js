const express = require('express');
const app = express();
const port = 3000;
const dotenv = require('dotenv');
const bodyParser = require('body-parser');
dotenv.config();

app.use(express.urlencoded({ extended: true })); // Parse URL-encoded bodies

const db = require('./db');


app.use(bodyParser.json());

// Set the view engine to EJS
app.set('view engine', 'ejs');


// Handle the POST request
app.put('/', (req, res) => {
    const formData = req.body; // Get the form data from the request body
    console.log(formData);
    const id = formData.id;
    console.log(id);
});


app.get('/', async (req, res) => {
  const message = 'No real time data from PLC';
 var database = "data";

 //console.log('All users:', users);

  // Perform a sample query
  const query = 'SELECT * FROM PLC';
  const PLC = await db.query(query);
  console.log('All address:', PLC);

    database =  JSON.stringify(PLC);
    var database_json;
    database_json = JSON.parse(database);

  res.render('index', { message, database_json,  websocketUrl: process.env.WEBSOCKET_URL });


});


app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
