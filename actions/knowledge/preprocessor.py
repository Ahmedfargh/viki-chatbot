import os
import re
import nltk
import csv
class knowledge_preprocessor:
    def __init__(self):
        self.read_files=[]
        self.dataset=None
        self.text_read=[]
        self.cleaned_Text=[]
    def _find_txt_files(self):#get all txt files
        for folderName,subfolders,filenames in os.walk(os.getcwd()):
            print(folderName)
            for filename in filenames:
                if re.search(r".txt",filename):
                    self.read_files.append(folderName)
    def read_each_File(self):#do some preprocessing
        self._find_txt_files()
        text=""
        for file in self.read_files:
            with open(file) as file_obj:
                text=file_obj.read()
            self.text_read.append(text)
            text=""
    def preprocess_single_file_content(self,text):
        return text
    def preprocess_files_content(self):
        with open("preprocessed.csv","w",newline="") as output:
            csv_writer=csv.writer(output)
            #csv_writer.writerow(["content","document_name"])
            i=0
            for content in self.text_read:
                text=self.preprocess_single_file_content(content)
                csv_writer.writerow([text,self.read_files[i-1]])
                i+=1
            print(self.text_read[0])
            output.close()
preprocessor=knowledge_preprocessor()
preprocessor.read_each_File()
preprocessor.preprocess_files_content()