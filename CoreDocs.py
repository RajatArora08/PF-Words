from PF_To_Be_Tested import PF_List
import re
import pysolr
import CONSTANTS
import PubMed


pattern_PF_name = re.compile(r'^\{[A-Za-z0-9]*; ([A-Za-z0-9_]*)\}\n$')
pattern_PF_ID = re.compile(r'^\{([A-Za-z0-9]*); [A-Za-z0-9_]*\}\n$')
# pattern_start_description = re.compile(r'^\{PS|^\{BEGIN}|^\*')
pattern_start_description = re.compile(r'^\{BEGIN}')
pattern_skip_line = re.compile(r'^\*')
pattern_end_description = re.compile(r'^-Consensus pattern')
pattern_end_doc = re.compile(r'^\{END}')
pattern_pubmedid = re.compile(r'PubMed=([0-9]*)')
pattern_parsed_doc_id = re.compile(r'^[0-9]*_([A-Za-z0-9_]*)')


def add_solr(data):
    solr = pysolr.Solr(CONSTANTS.SOLR_URL, timeout=10)

    output_file = open(CONSTANTS.PARSED_FILE, "a")

    solr.add([data])
    output_file.write("*********** {0} ************\n".format(data["id"]))
    output_file.write("{0}\n\n".format(data["description"]))

    output_file.close()

    print("{0} {1}".format(data["id"], data["description"]))

    return


def main():
    doc_id = 1

    with open(CONSTANTS.PROSITE_FILE, "r", encoding="ISO-8859-1") as file:
        for line in file:

            #Testing
            if line == '{PS00107; PROTEIN_KINASE_ATP}\n':
                print('Here')

            if re.match(pattern_PF_name, line):
                term = re.findall(pattern_PF_name, line)

                if any(term[0] == word for word in PF_List):
                    doc_list_with_same_doc = []
                    doc_list_with_same_doc.append('{0}_{1}'.format(doc_id, term[0]))
                    doc_id += 1

                    description = ''
                    pubmed_list = []

                    for line_further in file:

                        #For PF sharing same doc
                        if re.match(pattern_PF_name, line_further):
                            term_further = re.findall(pattern_PF_name, line_further)
                            if any(term_further[0] == word for word in PF_List):
                                doc_list_with_same_doc.append('{0}_{1}'.format(doc_id, term_further[0]))
                                doc_id += 1
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

                        #Testing
                        elif line_further == '-Last update: April 2006 / Pattern revised.\n':
                            print('hold')

                        else:
                            doc_contents += line_further

                    for doc_id_tmp in doc_list_with_same_doc:
                        data = {"id": doc_id_tmp, "description": description}

                        add_solr(data)

                        for pubmed_abtract in PubMed.fetch_pubmed_abstract(pubmed_list):
                            PF_word = re.findall(pattern_parsed_doc_id, doc_id_tmp)[0]

                            data = {"id": "{0}_{1}".format(doc_id, PF_word),
                                    "description": pubmed_abtract}
                            doc_id += 1

                            add_solr(data)

            # doc_list_with_same_doc.clear()

                # break

                # print(re.match(pattern_PF_name, line))
                # print(re.findall(pattern_PF_ID, line))

    file.close()


main()
