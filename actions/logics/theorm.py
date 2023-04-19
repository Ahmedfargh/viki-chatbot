from theorm_finder import theorm_finder
from nltk.metrics import edit_distance
from nltk.corpus import wordnet
import json
import spacy
import matplotlib.pyplot as plt
from theorm_finder import *
from question_Generation import question_generator_english
class theorms(theorm_finder):
    def __init__(self, theorm_file_path: str):
        super().__init__(theorm_file_path)
    def get_argument_atom_variables(self,theorm,key):
        argument=self.theorms[theorm]
        atom_variable=[]
        for attribute in argument:
            atom_variable.append(attribute[key])
        return atom_variable
    def get_all_theorms_arguments(self,key):
        atom_variables={}
        for theorm in self.theorms_addr:
            atom_variables[theorm]=self.get_argument_atom_variables(theorm,key)
        return atom_variables
    def get_all_attribute(self,current_theorm_):
        pass
    def get_values(self,theorm,key,attribute):
        result=[]
        for arg in theorm:
            result.append(arg[attribute])
        return result
    def compare(self,atom_variable,theorm_keys,pointer,key,attribute):
        current_theorm_argument=atom_variable[theorm_keys[pointer]]
        compare_pointer=0
        result={}
        staging_result=[]
        while compare_pointer< len(atom_variable):
            if compare_pointer==pointer:
                compare_pointer+=1
                continue
            current_theorm_values=self.get_values(current_theorm_argument,key,attribute)
            next_theorm_value=self.get_values(atom_variable[theorm_keys[compare_pointer]],key,attribute)
            staging_result=[value for value in current_theorm_values if not value in next_theorm_value]
            result[theorm_keys[compare_pointer]]=staging_result                
            compare_pointer+=1
        return result
    def _unify(self,results):
        results_keys=list(results.keys())
        unified_results=[]
        for key in results_keys:
            uniques=results[key]
            for unique in uniques:
                if not unique in unified_results:
                    unified_results.append(unique)
        return unified_results
    def seperate(self,atom_variables,key,attribute):
        theorm_keys=list(atom_variables.keys())
        pointer=0
        unique={}
        while pointer < len(theorm_keys):
            result=self.compare(atom_variables,theorm_keys,pointer,key,attribute)
            unique[theorm_keys[pointer]]=self._unify(result)
            pointer+=1
        return unique
    def choose(self,unique):
        keys=list(unique.keys())
        for key in keys:
            candidates=set(unique[key])
            results=[]
            for key2 in keys:
                if key2==key:
                    continue
                set1=set(unique[key2])
                candidates=set(candidates.difference(set1))
            unique[key]=list(candidates)
        return unique
    def get_unique_argument_attributes(self,argument_seprator,key,attribute):
        theorms_arguments={}
        atom_variables=self.get_all_theorms_arguments(key)
        unique=self.seperate(atom_variables,key,attribute)
        unique=self.choose(unique)
        print(unique)
        return unique
                