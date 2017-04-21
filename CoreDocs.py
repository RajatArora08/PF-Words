from PF_To_Be_Tested import PF_List
import re
import CONSTANTS
import SolrOperations
import variables
import PubMed

pattern_PF_name = re.compile(r'^\{([A-Za-z0-9]*); ([A-Za-z0-9_]*)\}\n$')
pattern_start_description = re.compile(r'^\{BEGIN}')
pattern_title = re.compile(r'^\*\s(.*)\s\*$')
pattern_skip_line = re.compile(r'^\*\*')
pattern_end_description = re.compile(r'^-Consensus pattern')
pattern_end_doc = re.compile(r'^\{END}')
pattern_pubmedid = re.compile(r'PubMed=([0-9]*)')


def create_core_docs():

    with open(CONSTANTS.PROSITE_FILE, "r", encoding="ISO-8859-1") as file:
        for line in file:

            if re.match(pattern_PF_name, line):
                tup = re.findall(pattern_PF_name, line)[0]
                id = tup[0]
                word = tup[1]

                if any(word == pf_word for pf_word in PF_List):

                    # Testing only for 'EF_HAND_1'
                    if word == 'ZINC_PROTEASE':

                        pubmed_set = set()
                        pf_word_list = []
                        pf_word_list.append((id, word))

                        description = ''
                        title = ''

                        for line_further in file:

                            #For PF sharing same doc
                            if re.match(pattern_PF_name, line_further):
                                tup = re.findall(pattern_PF_name, line_further)[0]
                                id_further = tup[0]
                                term_further = tup[1]

                                if any(term_further == word for word in PF_List):
                                    pf_word_list.append((id_further, term_further))
                                    continue

                            #For '{BEGIN}'
                            elif re.match(pattern_start_description, line_further):
                                doc_contents = ''
                                continue

                            #For any text starting with '**'
                            elif re.match(pattern_skip_line, line_further):
                                continue

                            #For title
                            elif re.match(pattern_title, line_further):
                                title = re.findall(pattern_title, line_further)[0]
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
                                pubmed_id = re.findall(pattern_pubmedid, line_further)[0]
                                pubmed_set.add(pubmed_id)
                                continue

                            else:
                                doc_contents += line_further

                        for temp_word in pf_word_list:

                            variables.PubMedId[temp_word[1]] = pubmed_set
                            variables.PubMedId_core[temp_word[1]] = set(pubmed_set)

                            formatted_word = CONSTANTS.DOC_FORMAT.format(variables.DOC_ID, temp_word[1])

                            data = {"id": formatted_word,
                                    "description": description,
                                    "source": variables.Source.Prosite.format(temp_word[0]),
                                    "title": title}

                            variables.DOC_ID += 1

                            SolrOperations.add_to_solr(data)
                            SolrOperations.add_to_solr_core(data)

    file.close()
    return


if __name__ == '__main__':

    create_core_docs()
    PubMed.add_pubmed_to_solr(Doc='core')
