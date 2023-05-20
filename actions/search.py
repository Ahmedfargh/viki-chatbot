import spacy
from neo4j import GraphDatabase
#import ds.bag as bag
class search:
    def __init__(self):
        self._graph=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","vikiviki"))
        self._session=self._graph.session(connection_acquisition_timeout=999999.9,max_transaction_retry_time=999999999)
        self._nlp=spacy.load("en_core_web_md")
        self._bag=[]
    def get_session(self):
        return self._session
    def _load_data(self,node_type=None):
        query=""
        if node_type:
            query="MATCH(n:"+node_type+")return n;"
        else:
            query="MATCH(n)return n;"
        results=self._session.run(query)
        return results.data()
    def _find_max(self,results):
        max_index=0
        max_sim=results[0]
        index=0
        for item in results:
            if max_sim["sim"]<item["sim"]:
                max_sim=item
                max_index=index
            index+=1
        try:
            max_sim=results.pop(max_index)
        except:
            print("")
        return max_sim
    def _rank_results(self,results):
        ranked_results=[]
        while results:
            max_sim=self._find_max(results)
            if max_sim:
                ranked_results.append(max_sim)
            else:
                break
        return ranked_results
    def _is_similer(self,query,node):
        node_text=self._nlp(node["n"]["text"])
        query_text=self._nlp(query)
        similarty=node_text.similarity(query_text)
        return similarty>=0.85,similarty
    def _search(self,nodes,keyword=None):
        if not keyword:
            raise ValueError
        for node in nodes:
            is_sim,sim=self._is_similer(keyword,node)

            if is_sim:
                self._bag.append({"node":node,"sim":sim})
        return self._bag
    def run_search(self,query):
        #load all node from database has node type
        nodes=self._load_data("relation_text")
        #search and find the results
        bag=self._search(nodes,query)
        if len(self._bag):
            results=self._rank_results(bag)
            return results
        else:
            return "NO_MATCH"
print(search().run_search("to damage"))