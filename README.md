## How to start the search engine!

# Project (link for TAs):
https://drive.google.com/drive/folders/1WXr5fvFy8YAZeTowZfMkjlq5HPw74eXw?usp=sharing

# Opening Solr (more details about Solr in ./Solr) 
./solr/bin/solr start -c -p 8983 -s ./solr/example/cloud/node1/solr
./solr/bin/solr start -c -p 7574 -s ./solr/example/cloud/node2/solr -z localhost:9983

# Stop all nodes
./solr/bin/solr stop -all

# Starting server:
npm run serve
(It may not run, if you see this error: Error message "error:0308010C:digital envelope routines::unsupported" 
I solved it here:
https://stackoverflow.com/questions/69692842/error-message-error0308010cdigital-envelope-routinesunsupported)
