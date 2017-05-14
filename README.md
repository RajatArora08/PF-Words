# PF-Words: Literature powered Protein Function Search Engine 

This project is a search engine for Protein Function. Its designed to be able to attend to free text queries to retrieve relevant ranked results of Protein Functions.

Pre-reqs:
1. The program downloads a lot of data from API's. 
2. Please ensure that atleast 2 GB space is free.
3. It takes a while to run the classification program.
4. Solr version 6.4 is required for indexing.
5. Three collections have to be created in Solr: PF-WORDS, PF-Core, PF-Intermediate
5. Ensure the newly configured collection in Solr matches the managed schema in the git repo.

Following libraries are required:
1. pysolr (https://github.com/django-haystack/pysolr)
2. sklearn (https://github.com/scikit-learn/scikit-learn)
3. flask (https://github.com/pallets/flask)
4. NLTK (http://www.nltk.org/install.html)
5. numpy (https://www.scipy.org/install.html)



To run:

1. Run UI
```
python3 FlaskContainer.py
```
Go to: http://localhost:5000/test/

2. Compile All Docs and Core Docs:
```
python3 AllDocs.py
```

3. Classify documents (Train: SVM, NB | Predict: SVM):
 ```
 python3 Classification.py
 ```
