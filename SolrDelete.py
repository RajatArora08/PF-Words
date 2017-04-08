import pysolr

solr = pysolr.Solr('http://localhost:8983/solr/PF-WORDS', timeout=10)

solr.delete(q='*:*')

print('Deletion successful!')
