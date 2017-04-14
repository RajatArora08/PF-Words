import requests
import re
from CONSTANTS import UNIPROT_URL, headers, UNIPROT_DIR
from pathlib import Path

pattern_rx = re.compile(r'RX\s\s\sPubMed=([0-9]*);')


def get_uniprot_pubmed_list(uniprot_list):

    pubmed_list = []

    for uniprot_id in uniprot_list:

        # Check if file is present in local
        file = Path(UNIPROT_DIR.format(uniprot_id))

        if file.is_file():
            returned_list = read_from_file(uniprot_id)
            pubmed_list.extend(returned_list)

        else:

            print('Calling UniProt API for {0}'.format(uniprot_id))

            url = UNIPROT_URL.format(uniprot_id)
            response = requests.get(url, headers)
            contents = response.content.decode("utf-8")
            pubmed_list.extend(re.findall(pattern_rx, contents))

            write_to_file(uniprot_id, contents)

    return pubmed_list


def read_from_file(uniprot_id):

    file = open(UNIPROT_DIR.format(uniprot_id), "r")
    file_content = str(file.readlines())
    pubmed_list = re.findall(pattern_rx, file_content)
    file.close()

    return pubmed_list


def write_to_file(uniprot_id, contents):

    file = open(UNIPROT_DIR.format(uniprot_id), "w")
    file.write(contents)
    file.close()

    return
