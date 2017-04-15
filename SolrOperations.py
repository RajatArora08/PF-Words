import pysolr
import CONSTANTS


def add_to_solr(data):
    solr = pysolr.Solr(CONSTANTS.SOLR_URL_TEST, timeout=10)

    output_file = open(CONSTANTS.PARSED_FILE, "a")

    if data["id"] == '7_EF_HAND_1':
        print("stop")
    solr.add([data])

    # Write all solr contents to file too
    # output_file.write("*********** {0} ************\n".format(data["id"]))
    # output_file.write("{0}\n\n".format(data["description"]))
    #
    # if data.__contains__('mesh_terms'):
    #     output_file.write("Mesh Terms: {0}\n\n".format(data["mesh_terms"]))
    #
    # # Add here to write mesh terms to file
    #
    # output_file.close()

    # print("{0} {1}".format(data["id"], data["description"]))
    print("{0}".format(data["id"]))

    return