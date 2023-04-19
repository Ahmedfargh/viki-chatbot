from neo4j import GraphDatabase
import json
class relation_ops:
    ##in this class I write code depend on data in neo4j database
    ##this class is to handle knowledge representation and reasoning 
    def __init__(self):
        self.graph=GraphDatabase.driver("bolt://localhost:11005",auth=("neo4j","ahmedahmed"))
        self.session=self.graph.session(connection_acquisition_timeout=999999.9,max_transaction_retry_time=999999999)
    def run_query(self,query:str):
        """
        #this is a query runner to run cipher query and return the results
        """
        return self.session.run(query).data()
    def check_attribute_to_attribute(self,attribute_1_data:dict,attribute_2_data:dict,relation:str,inverter:int):
        """
        #this is a and atribute to atribute checker
        """
        query=""
        if attribute_1_data["type"]=="int" and attribute_2_data["type"]=="int":
            query="MATCH(node_1:"+attribute_1_data["node_type"]+"{"+attribute_1_data["attribute_name"]+":"+attribute_1_data["attribute_value"]+"})<-[relation:"+relation+"]-(node_2:"+attribute_2_data["node_type"]+"{"+attribute_2_data["attribute_name"]+":"+attribute_2_data["attribute_value"]+"}) return node_1,node_2,relation;"
        elif attribute_1_data["type"]=="str" and attribute_2_data["type"]=="str":
            query="MATCH(node_1:"+attribute_1_data["node_type"]+"{"+attribute_1_data["attribute_name"]+":'"+attribute_1_data["attribute_value"]+"'})<-[relation:"+relation+"]-(node_2:"+attribute_2_data["node_type"]+"{"+attribute_2_data["attribute_name"]+":'"+attribute_2_data["attribute_value"]+"'}) return node_1,node_2,relation;"
        elif attribute_1_data["type"]=="str":
            query="MATCH(node_1:"+attribute_1_data["node_type"]+"{"+attribute_1_data["attribute_name"]+":'"+attribute_1_data["attribute_value"]+"'})<-[relation:"+relation+"]-(node_2:"+attribute_2_data["node_type"]+"{"+attribute_2_data["attribute_name"]+":"+attribute_2_data["attribute_value"]+"}) return node_1,node_2,relation;"
        elif attribute_2_data["type"]=="str":
            query="MATCH(node_1:"+attribute_1_data["node_type"]+"{"+attribute_1_data["attribute_name"]+":"+attribute_1_data["attribute_value"]+"})<-[relation:"+relation+"]-(node_2:"+attribute_2_data["node_type"]+"{"+attribute_2_data["attribute_name"]+":'"+attribute_2_data["attribute_value"]+"'}) return node_1,node_2,relation;"
        print(query)
        result=len(self.run_query(query))>0
        if inverter:
            return not result
        else:
            return result
    def evaluate_final_expression(self,results:list,argument:list):
        op_index=1
        final_result=[]
        if argument[op_index].lower()=="or":
            final_result.append(results[0] or results[1])
        elif argument[op_index].lower()=="and":
            final_result.append(results[0] and results[1])
        i=2
        while op_index<len(argument):
            if argument[op_index].lower()=="or":
                final_result.append(final_result[len(final_result)-1]or results[i-1])
            elif argument[op_index].lower()=="and":
                final_result.append(final_result[len(final_result)-1]and results[i-1])
            op_index+=2
            i+=1
        return final_result[len(final_result)-1]
    def check_syntax(self,argument:list):
        return len(argument)%2==0
    def think(self,arguments:list):
        print("good")
        if self.check_syntax(arguments):
            return "UN_balanced_question"
        try:
            results=[]
            for argument in arguments:
                try:
                    if argument.lower() in ["or","and","not"]:
                        continue
                except: 
                    results.append(self.check_attribute_to_attribute(argument["attribute_1_data"],argument["attribute_2_data"],argument["relation"],argument["not"]))
            return self.evaluate_final_expression(results,arguments)
        except:
            return results[0]
    def _formalate_node_data(self,data:dict):
        node_data="{"
        if data["type"].lower()=="str":
            node_data+=data["attribute_name"]+":"+"'"+data["attribute_value"]+"'"
        if data["type"].lower()=="int":
            node_data+=data["attribute_name"]+":"+data["attribute_value"]
        return node_data+"}"
    def load_data(self,condition_obj:dict):
        query=self._formalate_node_data(condition_obj)
        query="MATCH(node:"+condition_obj["node_type"]+""+query+")return node;"
        return self.run_query(query)
    def load_all_nodes(self,node):
        return self.run_query("MATCH(N:"+node+")return N;")
    def check_relation(self,node_1_name,node_1,node_data_2,node_2):
        node_1_important=node_1["important"]
        query="MATCH (n1:"+node_1_name+"{"+node_1["important"]+":'"+node_1[node_1["important"]]+"'})-[relation:has_symptom]->(n2:"+node_2+"{"+node_data_2["important"]+":'"+node_data_2["text"]+"'})return relation,n2"
        print(query)
        return self.run_query(query)
    def formalate_argument(self,node_name_1,node_name_2,node_data_1,node_data_2,relation,important):

        return {
            "attribute_1_data":{"node_type":node_name_1,"type":"str","attribute_name":important,"attribute_value":node_data_1.replace("","")},
            "attribute_2_data":{"node_type":node_name_2,"type":"str","attribute_name":important,"attribute_value":node_data_2.replace("_"," ")},
            "not":0,
            "relation":relation
        }
    def get_all_relations(self,node,node_data,node_2):
        query="MATCH(node:"+node+"{"+node_data["important"]+":'"+node_data[node_data["important"]]+"'})<-[relation]-(N2:"+node_2+") return relation,N2"
        print(query)
        return self.run_query(query)
    def link_Relation(self,node_1,node_2,data_1,data_2,result,important):
        arguments=[]
        if len(result)==0:
            print("no relation")
            return None
        else:
            for rel in result:
                variable=self.formalate_argument(node_1,node_2,data_1,data_2,rel["relation"],important)
                arguments.append(variable)
                arguments.append("and")
            arguments.pop()
            return arguments
    def save_knowledge_mining_results(self,all_arguments):
       json_dumps=json.dumps((all_arguments))
       with open("theorms.json","w+") as theorms:
           theorms.write(json_dumps)
       return None
    def knowledge_mining(self,node_1,node_2,important_data):
        all_arguments={}
        node_1_data=self.load_all_nodes(node_1)
        node_2_data=self.load_all_nodes(node_2)
        for data_1 in node_1_data:
            data_1["N"]["important"]=important_data
            arguments=[]
            relations=self.get_all_relations(node_1,data_1["N"],node_2)
            print(relations[0])
            if len(relations):
                for rel in relations:
                    arguments.append(self.formalate_argument(node_1,node_2,data_1["N"][important_data],rel["N2"]["text"],rel["relation"][1],important_data))
            """for data_2 in node_2_data:
                data_2["N"]["important"]=important_data
                result=self.check_relation(node_1,data_2["N"],data_1["N"],node_2)
                if len(result):
                    print("relation")
                    print(result)
                    arguments=self.link_Relation(node_1,node_2,data_2["N"],data_1["N"],result,important_data)
            if len(arguments):"""
            all_arguments["theorm_"+data_1["N"]["text"]]=arguments
            
        self.save_knowledge_mining_results(all_arguments)
"""argument=[{"attribute_1_data":
     {"node_type":"symptoms","type":"str","attribute_name":"text","attribute_value":"shivering"},
     "attribute_2_data":
     {"node_type":"disease","type":"str","attribute_name":"text","attribute_value":"Chronic cholestasis"},
     "relation":"has_symptom","not":0},
    "and",
    {"attribute_1_data":{
    "node_type":"symptoms",
    "type":"str",
    "attribute_name":"text",
    "attribute_value":"yellowish_skin"},
     "attribute_2_data":{"node_type":"disease","type":"str","attribute_name":"text","attribute_value":"Chronic cholestasis"},
     "relation":"has_symptom","not":0},
    "and",
    {"attribute_1_data":{"node_type":"symptoms","type":"str","attribute_name":"text","attribute_value":"vomiting"},
     "attribute_2_data":{"node_type":"disease","type":"str","attribute_name":"text","attribute_value":"Chronic cholestasis"},
     "relation":"has_symptom","not":0},
    "and",
    {"attribute_1_data":{"node_type":"symptoms","type":"str","attribute_name":"text","attribute_value":"vomiting"},
     "attribute_2_data":{"node_type":"disease","type":"str","attribute_name":"text","attribute_value":"Chronic cholestasis"},
     "relation":"has_symptom","not":0}
]"""
mind=relation_ops()
mind.knowledge_mining("disease","symptoms","text")
with open("theorms.json","r+") as f:
    #print(type(json.loads(f)))
    #print(json.load(f)["theorm_Allergy"])
    json.load(f)