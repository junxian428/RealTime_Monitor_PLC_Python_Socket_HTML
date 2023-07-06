const sqlite3 = require('sqlite3').verbose();
const config = require('./config');

// Create a database connection
const db = new sqlite3.Database(config.database);

// Function to execute a database query
function query(sql, values) {
  return new Promise((resolve, reject) => {
    db.all(sql, values, (err, rows) => {
      if (err) {
        reject(err);
        return;
      }

      resolve(rows);
    });
  });
}

module.exports = { query };
