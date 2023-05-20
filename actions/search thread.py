import spacy
from neo4j import GraphDatabase
#import ds.bag as bag
from threading import Thread
import threading
obj = {}
obj_lock = threading.Lock()
class search_thread:
    def __init__(self,data,start,end,query):
        super(search_thread,self).__init__()
        self._start=start
        self._data=data
        self._end=end
        self._nlp=spacy.load("en_core_web_md")
        self._query=query
        self._bag=[]
    def _is_similer(self,query,node):
        node_text=self._nlp(node["n"]["text"])
        query_text=self._nlp(self._query)
        print(self._query)
        similarty=node_text.similarity(query_text)
        return similarty>=0.85,similarty
    def get_bag(self):
        return self._bag
    def _search(self):
        if not self._query:
            raise ValueError
        i= self._start
        while i<= self._end:
            is_sim,sim=self._is_similer(self._query,self._data[i])
            if is_sim:
                self._bag.append({"node":self._data[i],"sim":sim})
            i+=1
    def run(self):
        self._search()
class search:
    def __init__(self):
        self._graph=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","vikiviki"))
        self._session=self._graph.session(connection_acquisition_timeout=999999.9,max_transaction_retry_time=999999999)
        self._nlp=spacy.load("en_core_web_md")
        self._bag=[]
        self._buffer_start=500
        self._all_thread=[]
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
    def _run_search_threads(self,data,query):
        i=0
        while True:
            if len(data)-i<=self._buffer_start:
                break
            else:
                process=search_thread(data,i,self._buffer_start+i,query)
                thread_container={"object":process,"thread":Thread(target=process.run)}
                self._all_thread.append(thread_container)
            i+=self._buffer_start
        for thread in self._all_thread:
            thread["thread"].start()

    def get_all_bags(self):
        bags=[]
        for thread_obj in self._all_thread:
            bags.append(thread_obj.get_bag())
        return bags
    def run_search(self,query):
        #load all node from database has node type
        nodes=self._load_data("relation_text")
        #search and find the results
        bag=self._run_search_threads(nodes,query)
        if len(self._bag):
            results=self._rank_results(bag)
            return results
        else:
            return "NO_MATCH"
search_obj=search()
try:
    search_obj.run_search("to damage")
except:
    raise
print(search_obj.get_all_bags()) 