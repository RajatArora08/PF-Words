import requests
import xml.etree.ElementTree as ET
from CONSTANTS import PUBMED_URL


def fetch_pubmed_abstract(PubMedId_list):

    abstract_list = []

    url = PUBMED_URL.format(",".join(PubMedId_list))
    response = requests.get(url)

    root = ET.fromstring(response.content)

    for child in root:

        abstract = child \
            .find('MedlineCitation') \
            .find('Article') \
            .find('Abstract')

        if abstract:
            abstract_list.append(abstract.find('AbstractText').text)

    return abstract_list
