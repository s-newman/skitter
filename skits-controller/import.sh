#!/bin/bash

if [[ $ESHOST == "" ]]; then
    ESHOST="elasticsearch"
fi

echo $ESHOST

while true; do
    curl -s $ESHOST:9200/.kibana | grep "kibanaSavedObjectMeta" >/dev/null 2>&1
    if [ $? -eq "0" ]; then
        break
    fi
    sleep 3
    echo "Waiting for kibana to connect to elasticsearch"
done

# Import skit Index
elasticdump --output=http://$ESHOST:9200/skit --input=skitIndex.json --type=mapping

# Import index-pattern, visualization and dashboard and making a default index-pattern
elasticdump --output=http://$ESHOST:9200/.kibana --input=kibana.json --type=data
