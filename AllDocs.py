import CoreDocs
import re
import PF_To_Be_Tested
import CONSTANTS
import PubMed
import PDB
import Uniprot


def parse_prosite_dat_file(PF_List, doc_id):
    pattern_pf_function = re.compile(r'^ID\s\s\s([A-Za-z0-9_]*);')

    with open(CONSTANTS.PROSITE_DAT_FILE, "r") as input_file:
        for line in input_file:

            if re.match(pattern_pf_function, line):
                word = re.findall(pattern_pf_function, line)[0]

                if any(word == pf_word for pf_word in PF_List):

                    #Testing only for 'EF_HAND_1'
                    if word == 'EF_HAND_1':

                        pubmed_list = get_pdb_uniprot_list(input_file)

                        doc_id = PubMed.add_pubmed_to_solr(word,
                                                           pubmed_list,
                                                           doc_id)

                        # print('{2}. {0}= {1}'.format(word, pdb_list, doc_id))


def get_pdb_uniprot_list(input_file):

    pubmed_list_combined = []

    pdb_list = []
    uniprot_list = []

    pattern_3d_line = re.compile(r'^3D')
    pattern_pdb_list = re.compile(r'([A-Za-z0-9]*);')

    pattern_dr_line = re.compile(r'^DR')
    pattern_uniprot = re.compile(r'([A-Z0-9]*)\s\s\s\s,\s[A-Z0-9_]*,\s([A-Z]);')

    for line in input_file:

        # 'DR' line= Uniprot
        if re.match(pattern_dr_line, line):

            uniprot = re.findall(pattern_uniprot, line)

            uniprot_list.extend([tuple_uniprot[0] for tuple_uniprot in uniprot
                                 if tuple_uniprot[1] == 'T' or tuple_uniprot == 'N'])

        # '3D' line= PDB.
        if re.match(pattern_3d_line, line):
            pdb_list.extend(re.findall(pattern_pdb_list, line))

        if line == '//\n':
            break

    uniprot_pubmed_list = Uniprot.get_uniprot_pubmed_list(uniprot_list)
    pdb_pubmed_list = PDB.get_pdb_pubmed_list(pdb_list)

    pubmed_list_combined = uniprot_pubmed_list + pdb_pubmed_list

    return pubmed_list_combined


def create_all_docs(doc_id):

    PF_list = PF_To_Be_Tested.PF_List
    parse_prosite_dat_file(PF_list, doc_id)


if __name__ == '__main__':

    initial_doc_id = 1
    # Comment for testing only all docs
    updated_doc_id = CoreDocs.create_core_docs(initial_doc_id)
    # updated_doc_id = 92
    create_all_docs(updated_doc_id)
