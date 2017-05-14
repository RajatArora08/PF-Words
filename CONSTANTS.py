PROSITE_FILE = "resources/prosite.doc"

PROSITE_DAT_FILE = "resources/prosite.dat"

PF_TESTED = "resources/PF-Test.txt"

PARSED_FILE = "resources/parsed.txt"

PD_CODE_FILE = "resources/pd_code.txt"

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

PDB_DIR = "resources/data/pdb/{0}.xml"

UNIPROT_DIR = "resources/data/uniprot/{0}.txt"

PUBMED_DIR = "resources/data/pubmed/{0}.xml"

CLASSIFIER_DIR_SVM = "resources/classifiers_svm/{0}/"
CLASSIFIER_DIR_NB = "resources/classifiers_nb/{0}/"


CLASSIFIER_FILE_SVM = CLASSIFIER_DIR_SVM + "{1}.pkl"
CLASSIFIER_FILE_NB = CLASSIFIER_DIR_NB + "{1}.pkl"


ANALYSIS_CSV_FILE = "resources/Analysis.csv"
