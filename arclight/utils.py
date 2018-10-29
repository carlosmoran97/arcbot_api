import os
import json
import random
import numpy as np
from arclight.models import NLUModel
from rasa_nlu.model import Interpreter
from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer

class NLUModelManager():

    # Static class attributes

    output_folder_name = "models"
    project_name = "current"
    language = "es"
    pipeline = "tensorflow_embedding"
    config_file_name = "nlu_config.yml"

    # Constructor

    def __init__(self, nlu_model):
        self.nlu_model = nlu_model
        self.data_filename = "data_{}_{}.md".format(self.nlu_model._id.__str__(), self.nlu_model.name.lower())
        self.fixed_model_name = "nlu_{}".format(self.nlu_model._id.__str__())


    def get_model_route(self):
        # return "./{}/{}/{}".format(
        #     self.output_folder_name,
        #     self.project_name,
        #     self.fixed_model_name
        # )
        return self.nlu_model.model_directory

    def train(self):
        # verifying the number of intents
        if(len(self.nlu_model.intents.all()) >= 2):
            # generating the data and config file
            self.generate_training_data_file()
            self.generate_config_file()

            # actual training
            # resolving the sh: python: not found error
            # the following line was giving an error
            # os.system("python -m rasa_nlu.train -c {} --data {} -o {} --fixed_model_name {} --project {} --verbose".format(self.config_file_name, self.data_filename, self.output_folder_name, self.fixed_model_name, self.project_name))
            training_data = load_data(self.data_filename)
            trainer = Trainer(config.load(self.config_file_name))
            trainer.train(training_data)
            model_directory = trainer.persist(self.get_model_route())
            self.nlu_model.model_directory = model_directory
            self.nlu_model.save()
            # deleting the file because is already in the database [in django version,  it is suposed how it will be]
            self.delete_training_data_file()
            # self.delete_config_file() si se borra el entrenamiento de uno interfiere con el entrenamiento de otro
        else:
            raise ValueError('You must have two or more intent classifiers.')

    def generate_training_data_file(self):
        data_file = open(self.data_filename, 'w+')
        for intent in self.nlu_model.intents.all():
            data_file.write("## intent:{}\r\n".format(intent.name))
            for phrase in intent.phrases:
                data_file.write("- {}\r\n".format(phrase))
        data_file.close()


    def delete_training_data_file(self):
        self.delete_file(self.data_filename)


    def generate_config_file(self):
        config_file = open(self.config_file_name, 'w+')
        config_file.write("language: {}\r\n".format(self.language))
        config_file.write("pipeline: {}\r\n".format(self.pipeline))
        config_file.close()


    def delete_config_file(self):
        self.delete_file(self.config_file_name)


    def delete_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
        else:
            raise ValueError('File {} does not exists.'.format(filename))


    def load(self):
        if os.path.exists(self.get_model_route()):
            self.interpreter = Interpreter.load(self.get_model_route())


    def parse(self, phrase):
        if self.interpreter != None:
            result = self.interpreter.parse(phrase)
            return result
        else:
            raise ValueError('You must load the model first before parse.')



class NLUManagerBoundarie():

    def __init__(self):
        self.managers = self.loadAllManagers()
        for m in self.managers:
            m.load()

    def loadAllManagers(self):
        return np.array([NLUModelManager(nlu_model) for nlu_model in NLUModel.objects.all()])

    def getNluManager(self, model_id):
        for i in range(len(self.managers)):
            if self.managers[i].nlu_model._id.__str__() == model_id:
                return self.managers[i]


    def loadModel(self, model_id):
        nluManager = self.getNluManager(model_id)
        nluManager.load()

    def loadAllModels(self):
        for nlu_model_manager in self.managers:
            nlu_model_manager.load()

    def trainAllModels(self):
        for nlu_model_manager in self.managers:
            nlu_model_manager.train()
# End of NLUManagerBoundarie class definition
