var elasticsearch = require('elasticsearch');
var HOST = process.env['ESHOST'] || 'elasticsearch';

var client = new elasticsearch.Client({
    host: HOST + ':9200', // For testing only, will be changed in products
    log: 'info'
});

function checkIndex(index) {
    return client.indices.exists({
        index: index
    });
}

function addIndex(index, data) {
    return client.indices.create({
        index: index,
        body: data
    });
}

function deleteIndex(index) {
    return client.indices.delete({
        index: index
    });
}

async function initIndex(indexName, data) {
    let res = await checkIndex(indexName);
    if (res) {
        await deleteIndex(indexName);
    }
    return addIndex(indexName, data);
}

function addDocument(indexName, data) {
    return client.index({
        index: indexName,
        type: '_doc',
        body: data
    });
}

function deleteDocumentById(indexName, id) {
    return client.delete({
        index: indexName,
        type: '_doc',
        id: id
    });
}

function getDocumentById(indexName, id) {
    return client.get({
        index: indexName,
        type: '_doc',
        id: id
    });
}

async function searchDocument(indexName, query) {
    let count = await countDocument(indexName, query);
    count = count['count']; // Because the response itself is JSON, not a string
    return client.search({
        index: indexName,
        q: query,
        size: count
    });
}

function countDocument(indexName, query) {
    return client.count({
        index: indexName,
        q: query
    });
}

module.exports = {
    checkIndex: checkIndex,
    addIndex: addIndex,
    deleteIndex: deleteIndex,
    initIndex: initIndex,
    addDocument: addDocument,
    deleteDocumentById: deleteDocumentById,
    getDocumentById: getDocumentById,
    searchDocument: searchDocument,
    countDocument: countDocument,
    HOST: HOST,
}
