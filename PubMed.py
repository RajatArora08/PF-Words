import requests
import xml.etree.ElementTree as ET
from CONSTANTS import PUBMED_URL


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
