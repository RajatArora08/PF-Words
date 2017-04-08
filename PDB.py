from CONSTANTS import PDB_URL
import requests
import xml.etree.ElementTree as ET


def get_pdb_pubmed_list(input_pdb_list):

    index = 0

    slice_size = 50     # No of elements to retrieve in single request.
    list_length = len(input_pdb_list)

    pubmed_id_list = []

    while index <= list_length:

        sliced_pdb_list = input_pdb_list[index: index+slice_size]
        index += slice_size

        url = PDB_URL.format(",".join(sliced_pdb_list))

        response = requests.get(url)
        print('Called PDB API')

        root = ET.fromstring(response.content)

        for child in root:

            attributes_dict = child.attrib

            if attributes_dict.__contains__('pubmedId'):
                # print(attributes_dict['pubmedId'])
                pubmed_id_list.append(attributes_dict['pubmedId'])

    return pubmed_id_list
