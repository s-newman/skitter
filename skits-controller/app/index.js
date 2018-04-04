var express = require('express');
var bodyParser = require('body-parser');
var es = require('./es');
var kibana = require('./kibana');
var app = express();
var PORT = 8080;

// TODO loop startup
async function start() {
    app.listen(PORT);
}

app.use(bodyParser.json());

/*
    The request body needs to have at least the following information:
    - username: the RIT username
    - date_posted: a timestamp of the skit
    - content: a non-empty string that is fewer than 140 characters
*/
app.post('/addSkit', (req, res) => {
    let data = req.body;
    es.addDocument('skit', data)
    .then( (resp) => {
        res.json(resp);
    }, (reason) => {
        console.log(reason);
        res.send("Failed to add document");
    });
});

app.get('/getSkits', (req, res) => {

});

app.delete('/removeSkit', (req, res) => {

});

process.on('unhandledRejection', (reason, p) => {
    console.log('Unhandled Rejection at: Promise', p);
});

start();