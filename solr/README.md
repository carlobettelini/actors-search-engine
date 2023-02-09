## How to use Solr for this project

# Start nodes (before starting server)
./bin/solr start -c -p 8983 -s example/cloud/node1/solr
./bin/solr start -c -p 7574 -s example/cloud/node2/solr -z localhost:9983

# Stop all nodes
bin/solr stop -all

# To reindex (always delete previous index before):
bin/post -c collection example/films/films.json

# To delete an index:
curl http://localhost:8983/solr/name/update --data '<delete><query>*:*</query></delete>' -H 'Content-type:text/xml; charset=utf-8'
curl http://localhost:8983/solr/name/update --data '<commit/>' -H 'Content-type:text/xml; charset=utf-8'