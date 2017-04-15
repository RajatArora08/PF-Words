import pysolr
from CONSTANTS import SOLR_URL_CORE

solr = pysolr.Solr('http://localhost:8983/solr/PF-WORDS', timeout=10)
solr.delete(q='*:*')

solr_core = pysolr.Solr(SOLR_URL_CORE, timeout=10)
solr_core.delete(q='*:*')

print('Deletion successful!')
