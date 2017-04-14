import requests
import xml.etree.ElementTree as ET
from CONSTANTS import PUBMED_URL, DOC_FORMAT, PUBMED_DIR
import SolrOperations
import variables
from pathlib import Path
import time


def fetch_pubmed_abstract(PubMedId_list):

    pubmed_abstracts = []

    pubmed_list_for_api = list(PubMedId_list)

    for pubmed_id in PubMedId_list:

        print(pubmed_id)

        if pubmed_id == '16094673':
            print('pause')

        # Check if file is present in local
        file = Path(PUBMED_DIR.format(pubmed_id))

        if file.is_file():
            data = read_from_xml(pubmed_id)
            if data:
                pubmed_abstracts.append(data)
            pubmed_list_for_api.remove(pubmed_id)

    if pubmed_list_for_api:

        index = 0

        slice_size = 50  # No of elements to retrieve in single request.
        list_length = len(pubmed_list_for_api)

        while index <= list_length:
            sliced_pdb_list = pubmed_list_for_api[index: index + slice_size]
            index += slice_size

            url = PUBMED_URL.format(",".join(sliced_pdb_list))
            print("PubMed API call")
            response = requests.get(url)

            root = ET.fromstring(response.content)

            for child in root:
                data = parse_xml(child)
                if data.__contains__('abstract'):
                    pubmed_abstracts.append(data)

                # Write to xml file
                ET.ElementTree(child).write(PUBMED_DIR.format(data['id']))

            # Sleep before next request
            time.sleep(1)

    return pubmed_abstracts


def read_from_xml(pubmed_id):

    tree = ET.parse(PUBMED_DIR.format(pubmed_id))
    return parse_xml(tree.getroot())


def parse_xml(child):
    data = {}

    medical_citation = child.find('MedlineCitation')

    pmid = medical_citation.find('PMID')

    abstract = medical_citation.find('Article') \
        .find('Abstract')

    title = medical_citation.find('Article') \
        .find('ArticleTitle')

    mesh_headings = medical_citation.find('MeshHeadingList')

    data["id"] = pmid.text

    if abstract:
        data['abstract'] = abstract.find('AbstractText').text
        data['title'] = title.text

        if mesh_headings:
            mesh_terms_list = []

            for mesh_term in mesh_headings.findall('MeshHeading'):
                mesh_terms_list.append(mesh_term.find('DescriptorName').text)

            data['mesh_terms'] = ", ".join(mesh_terms_list)


    return data


def add_pubmed_to_solr():
    # pattern_parsed_doc_id = re.compile(r'^[0-9]*_([A-Za-z0-9_]*)')

    for pf_word in variables.PubMedId:

        # Fetch all pubmed articles for each PF-Word
        pubmed_data = fetch_pubmed_abstract(variables.PubMedId[pf_word])

        for pubmed in pubmed_data:
            # PF_word = re.findall(pattern_parsed_doc_id, pf_word)[0]

            data = {}

            data["id"] = DOC_FORMAT.format(variables.DOC_ID, pf_word)
            variables.DOC_ID += 1

            data["source"] = variables.Source.PubMed.format(pubmed['id'])

            if pubmed.__contains__('abstract'):
                data["description"] = pubmed['abstract']

            if pubmed.__contains__('mesh_terms'):
                data["mesh_terms"] = pubmed['mesh_terms']

            if pubmed.__contains__('title'):
                data["title"] = pubmed['title']

            SolrOperations.add_to_solr(data)

    return
