from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import rasa_core
from rasa_core import *
try:
    from actions.knowledge import knowledgeBuilder
except:
    pass
logger = logging.getLogger(__name__)
def train_agent(interpreter):
    return train.train_dialog_model(domain_file="domain.yml",
    stories_file="data/stories.md",
    output_path="models",
    nlu_model_path=interpreter,
    endpoints="endpoints.yml",
    max_history=50,
    kwargs={"batch_size": 50,
    "epochs": 20,
    })
if __name__ == '__main__':
   utils.configure_colored_logging(loglevel="DEBUG")
   interpreter = NaturalLanguageInterpreter.create()
   agent = train_agent(interpreter)
   online.serve_agent(agent)