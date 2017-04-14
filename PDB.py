from CONSTANTS import PDB_URL, PDB_DIR
import requests
import xml.etree.ElementTree as ET
from pathlib import Path


def get_pdb_pubmed_list(input_pdb_list):

    pdb_list_for_api = list(input_pdb_list)

    pubmed_id_list = []

    for structureId in input_pdb_list:

        # Check if file is present in local
        file = Path(PDB_DIR.format(structureId))

        if file.is_file():
            pdb_list_for_api.remove(structureId)
            pubmed_id = read_from_xml_file(structureId)
            if pubmed_id:
                pubmed_id_list.append(pubmed_id)

    if pdb_list_for_api:
        pubmed_id_list += get_contents_from_api(pdb_list_for_api)


    return pubmed_id_list


def read_from_xml_file(structureId):

    tree = ET.parse(PDB_DIR.format(structureId))
    attributes = tree.getroot().attrib

    if attributes.__contains__('pubmedId'):
        pubmed_id = attributes['pubmedId']
        return pubmed_id

    return


def get_contents_from_api(pdb_list_for_api):
    index = 0
    pubmed_id_list = []

    slice_size = 50  # No of elements to retrieve in single request.
    list_length = len(pdb_list_for_api)

    while index <= list_length:

        sliced_pdb_list = pdb_list_for_api[index: index + slice_size]
        index += slice_size

        url = PDB_URL.format(",".join(sliced_pdb_list))

        response = requests.get(url)
        print('Called PDB API')

        root = ET.fromstring(response.content)

        for child in root:

            attributes_dict = child.attrib
            structureId = attributes_dict['structureId']

            if attributes_dict.__contains__('pubmedId'):
                pubmed_id_list.append(attributes_dict['pubmedId'])

            # Write to xml file
            ET.ElementTree(child).write(PDB_DIR.format(structureId))

    return pubmed_id_list