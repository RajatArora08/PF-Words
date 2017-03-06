import pysolr
import CONSTANTS

solr = pysolr.Solr(CONSTANTS.SOLR_URL, timeout=10)

query = input('Enter query: ')

results = solr.search(query)

for result in results:
    print("The title is '{0}'.".format(result['id']))
    print("Contents= {0}".format(result['description']))
