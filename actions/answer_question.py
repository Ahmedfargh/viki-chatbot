# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import search as search_mod
import spacy
from neo4j import GraphDatabase
question_flags=[
    "when","why","how","whome","where","who","?"
]
#
#
class answerQuestion(Action):
     def _preprocess_query(self,query):
        nlp=spacy.load("en_core_web_md")
        query_doc=nlp(query.lower())
        query_token=[token.text for token in query_doc]
        query_token=[token for token in query_token if not token in question_flags]
        return query_token.join(" ")
     def get_answer(self,question_type:list,best_node:dict):
        _graph=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","vikiviki"))
        _session=_graph.session(connection_acquisition_timeout=999999.9,max_transaction_retry_time=999999999)
        query="MATCH (p:noun)-[r:"
        for question in question_type:
            query=question+"]->(rel_text:relation_text{entity_id:"+str(best_node["node"]["entity_id"])+"}) RETURN p LIMIT 25"
            result=_session.run(query).data()
            if len(result):
                return result[0]["text"]
        return None
     def determine_what_answer(self,connection,bridge,tracker): 
        question_type=[]
        qeustion_tool=tracker.get_slot("questiontool")
        if qeustion_tool=="why":
            question_type.append("becauseof_what")
            return question_type
        elif qeustion_tool=="who":
            try:
                slot_test=tracker.get_slot("subject")
                question_type.append("sbj_what")
                return question_type
            except:
                try:
                    slot_test=tracker.get_slot("object")
                    question_type.append('obj_what')
                    return question_type
                except:
                    return None
        elif qeustion_tool=="when":
            question_type.append("before_who")
            question_type.append("by_what")
            question_type.append("in_what")
            question_type.append("at_what")
            question_type.append("after_what")
            question_type.append("at_what")
            return question_type
        elif qeustion_tool=="where":
            question_type.append("backof_what")
            question_type.append("behind_what")
            question_type.append("beneath_what")
            question_type.append("infronof_what")
            question_type.append("between_what")
            question_type.append("in_what")
            question_type.append("in_who")
            question_type.append("inside_what")
            question_type.append("inthemiddle_what")
            question_type.append("near_what")
            question_type.append("near_who")
            question_type.append("below_what")
            question_type.append("beside_what")
            return question_type
        return None
     def name(self) -> Text:
         return "answerQuestion"
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        search_object=search_mod.search()
        query=tracker.latest_message["text"]
        query=self._preprocess_query(query)
        results=search_object.run_search(query)
        if not results=="NO_MATCH":
             what_lock_at=self.determine_what_answer(search_object.get_session(),results[0],tracker)
             #dispatcher.utter_message(text=results[])
             answer=self.get_answer(what_lock_at,results)
             if answer:
                dispatcher.utter_message(text=self.get_answer())
             else:
                dispatcher.utter_message(text="I don't know may be I can't remeber")
        dispatcher.utter_message(text="I don't know,or may be you asked in bad way!!!!")
        return []
