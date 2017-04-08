from PF_To_Be_Tested import PF_List
import re
import CONSTANTS
import PubMed
import SolrOperations


pattern_PF_name = re.compile(r'^\{[A-Za-z0-9]*; ([A-Za-z0-9_]*)\}\n$')
pattern_PF_ID = re.compile(r'^\{([A-Za-z0-9]*); [A-Za-z0-9_]*\}\n$')
# pattern_start_description = re.compile(r'^\{PS|^\{BEGIN}|^\*')
pattern_start_description = re.compile(r'^\{BEGIN}')
pattern_skip_line = re.compile(r'^\*')
pattern_end_description = re.compile(r'^-Consensus pattern')
pattern_end_doc = re.compile(r'^\{END}')
pattern_pubmedid = re.compile(r'PubMed=([0-9]*)')


def create_core_docs(doc_id):

    with open(CONSTANTS.PROSITE_FILE, "r", encoding="ISO-8859-1") as file:
        for line in file:

            if re.match(pattern_PF_name, line):
                word = re.findall(pattern_PF_name, line)[0]

                if any(word == pf_word for pf_word in PF_List):

                    # Testing only for 'EF_HAND_1'
                    if word == 'EF_HAND_1':
                        pf_word_list = []
                        pf_word_list.append(word)

                        description = ''
                        pubmed_list = []

                        for line_further in file:

                            #For PF sharing same doc
                            if re.match(pattern_PF_name, line_further):
                                term_further = re.findall(pattern_PF_name, line_further)
                                if any(term_further[0] == word for word in PF_List):
                                    pf_word_list.append(term_further[0])
                                    continue

                            #For '{BEGIN}'
                            elif re.match(pattern_start_description, line_further):
                                doc_contents = ''
                                continue

                            #For any text starting with '*'
                            elif re.match(pattern_skip_line, line_further):
                                continue

                            #For '-Consensus pattern'
                            elif re.match(pattern_end_description, line_further):
                                description = doc_contents
                                continue

                            #For '{END}'
                            elif re.match(pattern_end_doc, line_further):
                                break

                            #For pubmedid in references
                            elif re.search(pattern_pubmedid, line_further):
                                pubmed_list.append(re.findall(pattern_pubmedid, line_further)[0])
                                continue

                            else:
                                doc_contents += line_further

                        for temp_word in pf_word_list:

                            formatted_word = CONSTANTS.DOC_FORMAT.format(doc_id, temp_word)

                            data = {"id": formatted_word, "description": description}
                            doc_id += 1

                            SolrOperations.add_to_solr(data)

                            doc_id = PubMed.add_pubmed_to_solr(temp_word, pubmed_list, doc_id)

    file.close()
    return doc_id


if __name__ == '__main__':

    initial_doc_id = 1
    create_core_docs(initial_doc_id)
