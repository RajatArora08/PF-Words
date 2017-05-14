from CONSTANTS import SOLR_URL_TEST, ANALYSIS_CSV_FILE
import pysolr
import PF_To_Be_Tested
import csv

PF_list = PF_To_Be_Tested.PF_List

solr = pysolr.Solr(SOLR_URL_TEST, timeout=10)
query = "id:*_{0}"

file = open(ANALYSIS_CSV_FILE, "w")
writer = csv.writer(file)
writer.writerow(['PF-WORD', 'Count', 'Start', 'End'])

for pf_word in PF_list:

    if pf_word == 'PROTEIN_KINASE_ST' or pf_word == 'PROTEIN_KINASE_TYR':
        continue

    results = solr.search(query.format(pf_word), rows=999999)

    id_list = list()

    for result in results:
        id = result.get('id').split('_', 1)[0]
        id_list.append(int(id))

    id_list.sort()
    writer.writerow([pf_word, len(id_list), id_list[0], id_list[-1]])

file.close()
