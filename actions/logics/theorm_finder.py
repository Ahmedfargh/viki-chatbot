from nltk.metrics import edit_distance
from nltk.corpus import wordnet
import json
import spacy
import matplotlib.pyplot as plt
from question_Generation import question_generator_english
class theorm_finder:
    def __init__(self,theorm_file_path:str):
        with open(theorm_file_path,"r+") as f:
            #print(type(json.loads(f)))
            #print(json.load(f)["theorm_Allergy"])
            self.theorms=json.load(f)
            self.theorms_addr=list(self.theorms.keys())
            self.similariy_threshold=2
            self.similarity=0.9
            self.nlp = spacy.load("en_core_web_md")
            self.sum=0
    def search(self,query:str):
        """
        """
        ranks=[]
        ranks.append((self.theorms_addr[0],edit_distance(self.theorms_addr[0].lower(),query.lower())))
        for theorm in list(self.theorms_addr):
            candidate=edit_distance(theorm.lower(),query.lower())
            if ranks[len(ranks)-1][1]<candidate:
                ranks.append((theorm,candidate))
        return ranks.pop()
    def calc_theorm_Score(self,theorm,symptoms):
        i=0
        theorm_score=0
        while i<len(theorm[i]):
            if theorm[i] in ["or","and"]:
                print("no valed")
            symptom_detected=[]
            for symptom_given in symptoms:
                symptom=theorm[i]["attribute_2_data"]["attribute_value"]
                symptom_givien_vector=self.nlp(symptom_given.replace("_"," "))
                symptom_vector=self.nlp(symptom.replace("_"," "))
                sim_vect=symptom_vector.similarity(symptom_givien_vector)
                sim=edit_distance(symptom_given,symptom)
                if sim<self.similariy_threshold and sim_vect>self.similarity:
                    print("candidate:"+symptom)
                    print("given:"+symptom_given)
                    symptom_detected.append(symptom)
                    theorm_score+=1
            i+=2
        return theorm_score
    def get_theorms_score_gt_one(self,theorms):
        more_than_one=[]
        for theorm in theorms:
            if theorm[0]>0:
                more_than_one.append(theorm)
        return more_than_one
    def _specific_theorm(self,theorms):
        focesed_theorms={}
        for theorm in theorms:
            focesed_theorms[theorm]=self.theorms[theorm]
        self.theorms=focesed_theorms
        return 
    def focus_on_specific_theorms(self,theorms:list):
        x_axis,_=self.split_to_theorms_and_scorce(theorms)
        self.theorms_addr=x_axis
        return
    def find_best_theorms(self,symptoms:list):
        self.sum=0
        max_theorms=self.calc_theorm_Score(list(self.theorms[self.theorms_addr[0]]),symptoms)
        theorms=[]
        theorms.append((max_theorms,self.theorms_addr[0]))
        for theorm in self.theorms.items():
            print(theorm[0])
            theorm_score=self.calc_theorm_Score(theorm[1],symptoms)
            #if theorm_score>theorms[len(theorms)-1][0]:
            theorms.append((theorm_score,theorm[0]))
        return theorms
    def split_to_theorms_and_scorce(self,data):
        x_axis=[]
        y_axis=[]
        for item in data:
            x_axis.append(item[1])
            y_axis.append(item[0])
        return x_axis,y_axis
    def plot_search_results(self,results):
        x_axis,y_axis=self.split_to_theorms_and_scorce(results)
        plt.plot(x_axis,y_axis)
        plt.show()
    def get_theorm(self,key):
        return self.theorms[key]