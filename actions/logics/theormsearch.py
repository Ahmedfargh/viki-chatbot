from nltk.metrics import edit_distance
from nltk.corpus import wordnet
import json
import spacy
import matplotlib.pyplot as plt
from theorm_finder import *
from question_Generation import question_generator_english
from theorm import theorms
class short_memory:
    def __init__(self):
        self._memory={}
    def keep(self,key,data):
        if key in list(self._memory.keys()):
            raise("key found choose another key")
        else:
            self._memory[key]=data
    def get_data(self,key):
        if key in list(self._memory.keys()):
            raise("key found choose another key")
        else:
            return self._memory[key]
    def forget_data(self,key):
        del self._memory[key]
def example():
    theorm_finder_obj=theorms("theorms.json")
    theorm_addr=theorm_finder_obj.search("theorm_Diabetes ")[0]
    print("**********************search_theorm_output*************************")
    print(theorm_addr)
    print("*********************question generation***************************")
    eng_que_gen=question_generator_english("theorms.json")
    print(eng_que_gen.generate_text(theorm_addr))
    print("******************** find best therom******************************")
    data=theorm_finder_obj.find_best_theorms([
        "fatigue",
        "extra marital contacts",
        "patches in throat",
        "abdominal pain",
        "loss of appetite",
        "excessive hunger",
        "burning micturition",
        "urination",
        "irregular sugar level",
        "restlessness"])
    print(data)
    print("******************** get theorm************************************")
    print(theorm_finder_obj.get_theorm("theorm_Diabetes"))
    print("******************** get_theorms_score_gt_one ************************************")
    data=theorm_finder_obj.get_theorms_score_gt_one(data)
    print(data)
    print("******************** plot result for debug***************************************")
    theorm_finder_obj.plot_search_results(data)
    print("******************** focus on returned theorms ***************************************")
    theorm_finder_obj.focus_on_specific_theorms(data)
    print(print("******************** get unique for every desease***************************************"))
    theorm_finder_obj.get_unique_argument_attributes("","attribute_2_data","attribute_value")
example()