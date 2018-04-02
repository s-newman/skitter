var express = require('express');
var app = express();

var PORT = 8080;

app.post('/addSkit', function(req, res) {

})

app.get('/getSkits', function(req, res) {

})

app.delete('/removeSkit', function(req, res) {

})

app.get('/', function(req, res) {
    res.send("pfffff go away.");
})

var server = app.listen(PORT);