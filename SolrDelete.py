import pysolr
from CONSTANTS import SOLR_URL_CORE, SOLR_URL_TEST, SOLR_URL_INTER

query = 'id:*_PROTEIN_KINASE_ST'

solr = pysolr.Solr(SOLR_URL_TEST, timeout=10)
solr.delete(q=query)

solr_core = pysolr.Solr(SOLR_URL_CORE, timeout=10)
solr_core.delete(q=query)

solr_inter = pysolr.Solr(SOLR_URL_INTER, timeout=10)
solr_inter.delete(q=query)

print('Deletion successful!')
