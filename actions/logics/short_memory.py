class question_generator_english:
    def __init__(self,theorm_file_path:str):
        with open(theorm_file_path,"r+") as f:
            #print(type(json.loads(f)))
            #print(json.load(f)["theorm_Allergy"])
            self.theorms=json.load(f)
            self.theorms_addr=list(self.theorms.keys())
        return
    def _preprocess_text(self,text:str):
        text=text.replace("_"," ")
        return text
    def generate_text(self,theorm_key:str):
        if not theorm_key in self.theorms_addr:
            raise("not defined theorm")
        else:
            theorm=self.theorms[theorm_key]
            questions=[]
            for argument in theorm:
                text=argument["attribute_2_data"]["attribute_value"]
                value_type=argument["attribute_2_data"]["type"]
                text=self._preprocess_text(text)
                if value_type.lower()=="str":
                    questions.append("do you have "+text+"?")
                elif value_type.lower()=="int":
                    questions.append(["how many [things] do you have?","how much [things] do you have?","how old are you?"])
            return questions