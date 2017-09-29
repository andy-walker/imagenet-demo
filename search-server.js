/**
 * *Very* quick and dirty application / rest server
 * @type {*}
 */

var express = require("express");
var app = express();

var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '',
  database : 'imagenet',
});
connection.connect();

app.get('/fetch', function(req, res) {
    var id = req.query.id;
    connection.query("SELECT * FROM classes c INNER JOIN images i ON i.class_id = c.id WHERE i.class_id ='" + id + "' ORDER BY i.score DESC LIMIT 100", function(err, rows, fields)
    {
        if (err) throw err;

        res.send(JSON.stringify({ status: 'ok', results: rows }));
    });
});

app.get('/search', function(req, res) {
    var query = req.query.q;
    connection.query("SELECT * FROM classes c INNER JOIN images i ON i.class_id = c.id WHERE c.name LIKE '%" + query + "%' ORDER BY i.score DESC LIMIT 10", function(err, rows, fields)
    {
      if (err) throw err;

      res.send(JSON.stringify({ status: 'ok', results: rows }));
    });
});

app.get('/categories', function(req, res) {
    connection.query("SELECT * FROM classes WHERE 1", function(err, rows, fields)
    {
        if (err) throw err;

        res.send(JSON.stringify({ status: 'ok', results: rows }));
    });
});

// main static files ..
app.use(express.static(__dirname + '/search-client/dist'));

// for image urls only ..
app.use(express.static(__dirname + '/search-client'));

var port = process.env.PORT || 5001;

app.listen(port, function() {
    console.log("Listening on " + port);
});
