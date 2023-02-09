WARNING: No more mantained! There is an issue with CORS policy, and I hadn't time to look behind it. The website opens, but the search doesn't return anything!!!

# How to start the search engine!

## (Solr) Stop all nodes if any are opened
```
./solr/bin/solr stop -all
```

## Opening Solr (more details about Solr in ./Solr) 
```
./solr/bin/solr start -c -p 8983 -s ./solr/example/cloud/node1/solr
./solr/bin/solr start -c -p 7574 -s ./solr/example/cloud/node2/solr -z localhost:9983
```

## Starting server:
```
npm run serve
```

If you see this error: Error message "error:0308010C:digital envelope routines::unsupported" 
I solved it thanks to stackoverflow:
https://stackoverflow.com/questions/69692842/error-message-error0308010cdigital-envelope-routinesunsupported)
