import pysolr
import CONSTANTS
import SecondaryScoring


def search(query, scoring_method):

    solr = pysolr.Solr(CONSTANTS.SOLR_URL_TEST, timeout=10)

    # query = input('Enter query: ')

    #Test this for total
    # query = 'calcium'
    # query = '(description:calcium)^2 mesh_terms:calcium'

    #Test this for count vs total
    # query = 'sequence'

    results = solr.search(query, fl='id,score', rows=CONSTANTS.NO_OF_ROWS)

    for result in results:

        print("The title is '{0}'.".format(result['id']))
        print("The score is {0}.".format(result['score']))
        # print("Contents= {0}".format(result['description']))

    print('\nSelect Secondary scoring option:')
    print('1. Scores total')
    print('2. Scores total (log10)')
    print('3. No of Documents\n')

    #Testing
    # scoring_method = input('Enter scoring option: ')
    # scoring_method = 4

    options = {
        1: SecondaryScoring.total_scoring,
        2: SecondaryScoring.log10_scoring,
        3: SecondaryScoring.count_scoring,
        4: SecondaryScoring.highest_relevancy
    }

    #Printing all for testing
    # print(results.docs)
    print(SecondaryScoring.compute_total_scores(results))
    # print(options[1](results))
    # print(options[2](results))
    # print(options[3](results))

    #Printing input option
    # print(options[int(scoring_method)](results))
    # print(options[1](results))

    final_result = options[int(scoring_method)](results)

    return final_result
