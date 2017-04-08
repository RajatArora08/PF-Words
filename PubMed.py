import requests
import xml.etree.ElementTree as ET
from CONSTANTS import PUBMED_URL, DOC_FORMAT
import re
import SolrOperations


def fetch_pubmed_abstract(PubMedId_list):

    ret_value = []

    url = PUBMED_URL.format(",".join(PubMedId_list))
    response = requests.get(url)

    root = ET.fromstring(response.content)

    for child in root:

        temp = {}

        medical_citation = child.find('MedlineCitation')

        abstract = medical_citation.find('Article') \
            .find('Abstract')

        mesh_headings = medical_citation.find('MeshHeadingList')

        if abstract:
            temp['abstract'] = abstract.find('AbstractText').text

            if mesh_headings :
                mesh_terms_list = []

                for mesh_term in mesh_headings.findall('MeshHeading'):
                    mesh_terms_list.append(mesh_term.find('DescriptorName').text)

                temp['mesh_terms'] = ", ".join(mesh_terms_list)

            ret_value.append(temp)

    return ret_value


def add_pubmed_to_solr(pf_word, pubmed_list, doc_id):
    # pattern_parsed_doc_id = re.compile(r'^[0-9]*_([A-Za-z0-9_]*)')

    # Fetch all pubmed articles for each PF-Word
    pubmed_data = fetch_pubmed_abstract(pubmed_list)

    for pubmed in pubmed_data:
        # PF_word = re.findall(pattern_parsed_doc_id, pf_word)[0]

        data = {}

        data["id"] = DOC_FORMAT.format(doc_id, pf_word)

        if pubmed.__contains__('abstract'):
            data["description"] = pubmed['abstract']

        if pubmed.__contains__('mesh_terms'):
            data["mesh_terms"] = pubmed['mesh_terms']

        doc_id += 1

        SolrOperations.add_to_solr(data)

    return doc_id
