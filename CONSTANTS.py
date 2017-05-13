PROSITE_FILE = "/home/rajatar08/PF-Project/prosite.doc"

PROSITE_DAT_FILE = "/home/rajatar08/PF-Project/prosite.dat"

PF_TESTED = "/home/rajatar08/PF-Project/PF-Test.txt"

PARSED_FILE = "/home/rajatar08/PF-Project/parsed.txt"

PD_CODE_FILE = "/home/rajatar08/PF-Project/pd_code.txt"

PUBMED_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" \
             "db=pubmed" \
             "&retmode=xml" \
             "&tool=pf_words" \
             "&email=rarora@mail.sfsu.edu" \
             "&id={0}"

PDB_URL = "http://www.rcsb.org/pdb/rest/describePDB?structureId={0}"

UNIPROT_URL = "http://www.uniprot.org/uniprot/{0}.txt"

# Collections
# 1. All Docs
SOLR_URL_TEST = 'http://localhost:8983/solr/PF-WORDS'

# 2. Core Docs
SOLR_URL_CORE = 'http://localhost:8983/solr/PF-Core'

# 3. Intermediate Docs
SOLR_URL_INTER = 'http://localhost:8983/solr/PF-Intermediate'

NO_OF_ROWS = '100'

DOC_FORMAT = "{0}_{1}"

headers = {'User-Agent': 'rarora@mail.sfsu.edu'}

PDB_DIR = "/home/rajatar08/PF-Project/resources/pdb/{0}.xml"

UNIPROT_DIR = "/home/rajatar08/PF-Project/resources/uniprot/{0}.txt"

PUBMED_DIR = "/home/rajatar08/PF-Project/resources/pubmed/{0}.xml"

CLASSIFIER_DIR = "/home/rajatar08/PF-Project/classifiers/{0}/"

CLASSIFIER_FILE = CLASSIFIER_DIR + "{1}.pkl"
VECTOR_FILE = CLASSIFIER_DIR + "vector.pkl"

ANALYSIS_CSV_FILE = "/home/rajatar08/PF-Project/Analysis.csv"
