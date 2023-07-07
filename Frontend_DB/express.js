const express = require('express');
const app = express();
const port = 3000;
const dotenv = require('dotenv');
const bodyParser = require('body-parser');
dotenv.config();

app.use(bodyParser.urlencoded({ extended: false }));

const db = require('./db');



// Set the view engine to EJS
app.set('view engine', 'ejs');




// Route for handling the form submission (update item)
app.post('/update', (req, res) => {
  console.log("put");

  console.log(req.body);
  const id = req.body.id;
  const address_0 = req.body.address_0;
  const address_1 = req.body.address_1;
  const address_2 = req.body.address_2;
  const address_3 = req.body.address_3;
  const address_4 = req.body.address_4;

  //const id = parseInt(req.params.id);
  const address_5 = req.body.address_5;
  const address_6= req.body.address_6;
  console.log(id + '  ' + address_0 + address_1 + address_2 + address_3 + address_4 + address_5 + address_6);
  const sql = `UPDATE PLC
  SET address_0 = ?,
      address_1 = ?,
      address_2 = ?,
      address_3 = ?,
      address_4 = ?,
      address_5 = ?,
      address_6 = ?,
      address_7 = ?,
      address_8 = ?,
      address_9 = ?,
      address_10 = ?,
      address_11 = ?,
      address_12 = ?,
      address_13 = ?,
      address_14 = ?,
      address_15 = ?
  WHERE id = ?`;

  const address_7 = "";
  const address_8 = "";
  const address_9 = "";
  const address_10 = "";

  const address_11 = "";
  const address_12= "";
  const address_13 = "";


  const address_14 = "";
  const address_15 = "";



  const { query } = require('./db');


  query(sql, [address_0, address_1, address_2, address_3, address_4, address_5, address_6 , address_7, address_8 , address_9, address_10, address_11, address_12, address_13, address_14, address_15, id], function (err) {
    if (err) {
      console.error(err.message);
      return;
    }
    console.log(`Record with ID ${id} updated successfully.`);
  });

  //const item = items.find(item => item.id === id);
  //item.name = req.body.name;
  console.log("put");
  res.redirect('/');
});

app.get('/', async (req, res) => {
  const message = 'No real time data from PLC';
 var database = "data";

 //console.log('All users:', users);

  // Perform a sample query
  const query = 'SELECT * FROM PLC';
  const PLC = await db.query(query);
  //console.log('All address:', PLC);

    database =  JSON.stringify(PLC);
    var database_json;
    database_json = JSON.parse(database);

  res.render('index', { message, database_json,  websocketUrl: process.env.WEBSOCKET_URL });


});


app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
