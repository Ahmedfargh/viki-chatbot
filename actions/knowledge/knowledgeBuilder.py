import pandas as pd
import re
import nltk
from neo4j import GraphDatabase
from expertai.nlapi.cloud.client import ExpertAiClient
import csv
class knowledge_builder:
    def __init__(self,folderName):
        self.folderName=folderName
        self.dataset=pd.read_csv(folderName,encoding='latin')
        self.sentence_pointer=0
        self.entity_id=0
        self.rel_pointer=0
        self.rel_text=0
        self.query_set=[]
        #self.pipline=stanza.Pipeline(lang="en",download_method=None,processors="tokenize,pos,lemma,depparse",use_gpu=True) 
    def save_to_kb(self,relations,relation_text,doc_name):
        try:
            graph=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","vikiviki"))
            session=graph.session(connection_acquisition_timeout=999999.9,max_transaction_retry_time=999999999)
            rel_id=self.entity_id
            list_of_related_entity=[]
            q='create(n:relation_text{text:"'+relation_text+'",entity_id:'+str(self.rel_text)+'})return n;'
            self.rel_text+=1
            self.query_set.append(q)
            print(doc_name)
            q="match(doc:document{id:"+str(self.rel_pointer-1)+"}),(rel:relation_text{entity_id:"+str(self.rel_text-1)+"})create(doc)-[r:contain]->(rel)return doc,r,rel"
            self.query_set.append(q)
            for related in relations:
                q='create(n:noun{text:"'+related.text+'",entity_id:'+str(self.entity_id)+'})return n;'
                self.query_set.append(q)
                list_of_related_entity.append([self.entity_id,related.relation])
                self.entity_id=self.entity_id+1
            for entity in list_of_related_entity:    
                q='MATCH(n:noun{entity_id:'+str(entity[0])+'}),(rel:relation_text{entity_id:'+str(self.rel_text-1)+'})create(n)-[r:'+str(entity[1])+']->(rel)return n,r,rel'
                self.query_set.append(q)
        except:
            raise
    def extract_relation(self,tree,doc_name):
        client = ExpertAiClient()
        text = "Michael Jordan was one of the best basketball players of all time. Scoring was Jordan's stand-out skill, but he still holds a defensive NBA record, with eight steals in a half."
        language= 'en'
        sents=tree.split(".")
        for sent in sents:
            try:
                output = client.specific_resource_analysis(body={"document": {"text": sent}}, params={'language': language, 'resource': 'relations'})
                for relation in output.relations:
                    self.save_to_kb(relation.related,relation.verb.text,doc_name)
            except:
                continue
    def under_stand(self,sent_tree,doc_name):
        tree_id=0
        self.extract_relation(sent_tree,doc_name)
        return None
    def group_trees(self,tree):
        return tree
    def preprocess(self,doc):
        sentence = nltk.sent_tokenize(doc)
        sentence = [nltk.word_tokenize(s) for s in sentence]
        sentence = [nltk.pos_tag(s) for s in sentence]
        return sentence
    def study_Document(self,document,doc_name):
        self.under_stand(document,doc_name)
        return True
    def check_point(self,file_name):
        with open(file_name,"w",newline="") as output:
            csv_writer=csv.writer(output)
            i=0
            for content in self.query_set:
                csv_writer.writerow([content])
                i+=1
            output.close()
            #ahmedahmed
    def load_back_up(self,file_name):
        back_up=pd.read_csv(file_name)
        graph=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","vikiviki"))
        session=graph.session(connection_acquisition_timeout=999999.9,max_transaction_retry_time=999999999)
        for query in back_up.values:
            session.run(query[0])
        session.close()
    def study(self):
        print("Do you want to make me study the documents?y/n")
        response=str(input())
        if response.lower()=='y':
            try:
                i=0
                print("begining my studies")
                for doc in self.dataset.values:
                    i+=1
                    q='create(doc:document{text:"'+doc[1]+'",id:'+str(self.rel_pointer)+'})return doc;'
                    self.rel_pointer+=1
                    self.query_set.append(q)
                    self.study_Document(doc[0],doc[1])
                    print("document studied "+str(i)+" !!!")
                print("studies is Done")
                self.check_point("backup.csv")
                self.load_back_up('backup.csv')
                return True
            except Exception:
                self.check_point("backup.csv")
                self.load_back_up('backup.csv')
                raise
                return None
        print("thank you ,it would take all time to do it!!!!")
    def save_relation(disease,syptoms,graph,session,entity_id):
        disease=disease.replace(" ","")
        q="create(dis:disease{entity_id:"+str(entity_id)+",text:'"+disease+"'})return dis"
        dis_id=entity_id
        session.run(q)
        entity_id+=1
        for syptom in syptoms:
            if syptom=="Noun":
                break
            syptom=syptom.strip(" ")
            q="create(symp:symptoms{entity_id:"+str(entity_id)+",text:'"+syptom+"'})return symp"
            session.run(q)
            q="match(dis:disease{entity_id:"+str(dis_id)+"}) ,(symp:symptoms{entity_id:"+str(entity_id)+"}) create(symp)-[symptom:has_symptom]->(dis) return dis,symp;"
            session.run(q)
            entity_id+=1
        return None
    def descover_knowledge(dataset,target_value_index,target_name):
        graph=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","vikiviki"))
        session=graph.session(connection_acquisition_timeout=999999.9,max_transaction_retry_time=999999999)
        dataset=pd.read_csv(dataset)
        dataset=dataset.fillna("Noun")
        disease=dataset[target_name].unique()
        dataset_groups=dataset.groupby(target_name)
        i=0
        for dis in disease:
            print(dis)
            dis_syptoms=dataset_groups.get_group(dis).values[0]
            knowledge_builder.save_relation(dis,dis_syptoms,graph,session,i)
            i+=1
class KnowoledgeLinker(knowledge_builder):
    def __init__(self):
        super.__init__("preprocessed.csv")
        self.db_auth=("neo4j","ahmedahmed")
        self.GraphDatabase=GraphDatabase.driver("bolt://localhost:11005 ",auth=self.db_auth)
        self.session=self.GraphDatabase.session(connection_acquisition_timeout=999999.9,max_transaction_retry_time=999999999)
        self.pairs=[]
        return
    def _equal_concepts(self,concept1,concept2):
        return concept1.lower().replace(" ","")==concept2.lower().replace(" ","")
    def _get_relation_link(self,result):
        #print(result)
        return result["relation"][1]
    def _get_relation_text_id(self,result):
        return result["relationtxt"]["entity_id"]
    def _link_concept(self,concept,result):
        for entity in result:
            q="match(relationtxt_ent:relationtxt{entity_id:"+str(self._get_relation_text_id(entity))+"}),(n:noun{text:'"+str(concept["text"])+"'}) create(n)-[:"+self._get_relation_link(entity)+"]->(relationtxt_ent)return n,relationtxt_ent;"
            self.session.run(q)
        return None
    def _delete_concept(self,concept):
        q="match(n:noun{entity_id:"+str(concept["entity_id"])+"})detach delete n;"
        self.session.run(q)
        return None
    def _replace_concepts(self,concept1,concept2):
        q='match(n:noun),(n)-[relation]->(relationtxt:relation_text) where n.text="'+concept2["text"]+'" return relationtxt,relation;'
        result=self.session.run(q)
        result=result.data()
        self._link_concept(concept1,result)
        self._delete_concept(concept2)
        return None
    def link_all(self):
        all_concepts=self.session.run("MATCH(n:noun)return n;")
        all_concepts=all_concepts.data()
        current_id=0
        for concept in all_concepts:
            for concept_m in all_concepts:
                if self._equal_concepts(concept["n"]["text"],concept_m["n"]["text"]) and not concept["n"]["text"] in self.pairs:
                    print("linking operation: "+str(len(self.pairs)))
                    self.pairs.append(concept["n"]["text"])
                    self._replace_concepts(concept["n"],concept_m["n"])
            all_concepts.pop(current_id)
            current_id+=1
builder=knowledge_builder("actions/knowledge/preprocessed.csv")
builder.study()
builder.load_back_up("actions/knowledge/backup.csv")
knowledge_builder.descover_knowledge("actions/knowledge/dataset.csv",0,"Disease")
#linker=KnowoledgeLinker()
#linker.link_all()
