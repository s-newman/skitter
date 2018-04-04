#!/bin/bash

# Import skit Index
elasticdump --output=http://localhost:9200/skit --input=skitIndex.json --type=mapping

# Import index-pattern, visualization and dashboard and making a default index-pattern
elasticdump --output=http://localhost:9200/.kibana --input=kibana.json --type=data
