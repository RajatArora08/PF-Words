import requests
import re
from CONSTANTS import UNIPROT_URL


def get_uniprot_pubmed_list(uniprot_list):

    pubmed_list = []

    pattern_rx = re.compile(r'RX\s\s\sPubMed=([0-9]*);')

    for uniprot_id in uniprot_list:

        url = UNIPROT_URL.format(uniprot_id)

        response = requests.get(url)

        contents = response.content.decode("utf-8")

        pubmed_list.extend(re.findall(pattern_rx, contents))

    return pubmed_list
