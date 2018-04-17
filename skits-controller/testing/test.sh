#!/bin/bash
docker run --rm --name es -p 9200:9200 -tid docker.elastic.co/elasticsearch/elasticsearch-oss:6.2.3
docker run --rm --name nodeee -e ESHOST=172.17.0.2 -p 8080:8080 -tid nodee
docker run --rm --name kim -e ELASTICSEARCH_URL=http://172.17.0.2:9200 -p 5601:5601 -tid docker.elastic.co/kibana/kibana-oss:6.0.0
