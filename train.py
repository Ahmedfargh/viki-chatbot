from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import rasa_core
import rasa
from actions.knowledge import knowledgeBuilder

config="config.yml"
training_files="data/"
domain="domaing.yml"
output="models/"
model_path=rasa.train(domain,config,[training_files],output)