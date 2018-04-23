var express = require('express');
var bodyParser = require('body-parser');
var es = require('./es');
var app = express();
var PORT = 8080;

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
        //res.json(resp);
        res.json({
            success: true,
            skitID: resp['_id'],
            data: req.body
        });
    }, (reason) => {
        console.log(reason);
        res.json({
            success: false
        });
    });
});

/*
    The request body needs to have at least the following information:
    - username: the RIT username
    - date_posted: a timestamp of the skit
    - content: a non-empty string that is fewer than 140 characters
    - skitID: the ID of the skit
*/
app.post('/addSkitReply', (req, res) => {
    let data = req.body;
    es.addDocument('skit-reply', data)
    .then( (resp) => {
        res.json({
            success: true,
            skitReplyID: resp['_id'],
            data: req.body
        });
    }, (reason) => {
        console.log(reason);
        res.json({
            success: false
        });
    });
});

/*
    Get all the skits by a user
    - username: the RIT username to get skits from
    - index: the index to search in, either skit or skitreply. By default it's skit.
*/
app.get('/getSkits', (req, res) => {
    let username = req.query.username;
    let indexName = req.query.index || "skit";

    es.searchDocument(indexName, 'username: ' + username)
    .then( (resp) => {
        let data = [];
        for (var i = 0; i < resp['hits']['hits'].length; i++) {
            let entry = {};
            entry['skitID'] = resp['hits']['hits'][i]['_id'];
            entry['skit'] = resp['hits']['hits'][i]['_source'];
            data.push(entry);
        }
        res.json({
            success: true,
            username: req.query.username,
            data: data
        });
    }, (reason) => {
        console.log(reason);
        res.json({
            success: false
        });
    });
});

/*
    Get all replies of a skit
    - skitID: the ID of the skit
*/
app.get('/getSkitReplies', (req, res) => {
    let indexName = 'skit-reply';
    let skitID = req.query.skitID;
    es.searchDocument(indexName, 'skitID :' + skitID)
    .then( (resp) => {
        let data = [];
        for (var i = 0; i < resp['hits']['hits'].length; i++) {
            let entry = {};
            entry['skitReplyID'] = resp['hits']['hits'][i]['_id'];
            entry['skitReply'] = resp['hits']['hits'][i]['_source'];
            data.push(entry);
        }
        res.json({
            success: true,
            skitID: req.query.skitID,
            data: data
        });
    }, (reason) => {
        console.log(reason);
        res.json({
            success: false
        });
    });
});

/*
    Get a skit by its ID in elasticsearch
    - id: The ID of the skit
    - index: the index to search in, either skit or skitreply. By default it's skit.
*/
app.get('/getSkitById', (req, res) => {
    let id = req.query.id;
    let indexName = req.query.index || "skit"; // Search in the skit index by default
    es.getDocumentById(indexName, id)
    .then( (resp) => {
        res.json({
            success: true,
            skitID: resp['_id'],
            data: resp['_source']
        });
    }, (reason) => {
        console.log(reason);
        res.json({
            success: false
        });
    });
});

app.get('/removeSkit', (req, res) => {
    let id = req.query.id;
    let indexName = req.query.index || "skit";
    es.deleteDocumentById(indexName, id)
    .then( (resp) => {
        res.json({
            success: true
        })
    }, (reason) => {
        console.log(reason);
        res.json({
            success: false
        });
    });
});

process.on('unhandledRejection', (reason, p) => {
    console.log('Unhandled Rejection at: Promise', p);
});

start();