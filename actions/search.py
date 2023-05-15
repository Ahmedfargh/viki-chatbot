import spacy
from neo4j import GraphDatabase
class search:
    def __init__(self):
        self._graph=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","vikiviki"))
        self._session=self._graph.session(connection_acquisition_timeout=999999.9,max_transaction_retry_time=999999999)
        self._nlp=spacy.load("en_core_web_md")
        self._bag=[]
    def _load_data(self,node_type=None):
        pass
    def _rank_results():
        pass
    def _search(self,keyword=None):
        if keyword:
            raise ValueError
        pass
    def run_search():
        pass
