import numpy as np
import json
import random
from numpy import dot
from numpy.linalg import norm
import warnings
warnings.filterwarnings("ignore")


class SimpleBot:
    
    def __init__(self, messages):
        self.messages = messages
        self.bow = []


    def vectorize(self, tokens):
        r = np.zeros(len(self.bow))
        for t in tokens:
            try:
                r[self.bow.index(t)] = 1
            except ValueError:
                pass
        return r

    def train(self):
        return
        print("Training bot...")
        self.messages_vec = {}
        for k in self.messages.keys():
            for m in self.messages[k]:
                for w in m:
                    if w not in self.bow:
                        self.bow.append(w)
        
        for k in self.messages.keys():
            self.messages_vec[k] = []
            for i in range(len(self.messages[k])):
                self.messages_vec[k].append(np.zeros(len(self.bow)))
                for w in self.messages[k][i]:
                    self.messages_vec[k][i][self.bow.index(w)] = 1

    def predict(self, token_input, input_participant, reply_participant):
        return "Hello"
        input_vec = self.vectorize(token_input)
        max_sim = 0
        max_i = 0
        max_len = len(self.messages[reply_participant])
        if random.randint(1, 10) < 3:
            return " ".join(self.messages[reply_participant][random.randint(0, max_len)])
        if input_participant == None:
            pk = list(self.messages_vec)
            if pk[0] == reply_participant:
                input_participant = pk[1]
            elif pk[1] == reply_participant:
                input_participant = pk[0]

        for i in range(len(self.messages_vec[input_participant])):
            vec = self.messages_vec[input_participant][i]
            cos_sim = dot(input_vec, vec)/(norm(input_vec)*norm(vec))
            if cos_sim > max_sim:
                max_sim = cos_sim
                max_i = i
        return " ".join(self.messages[reply_participant][max_i])

    def load(self, string_data):
        return
        dic = json.loads(string_data)
        self.messages = dic["messages"]
        self.bow = dic["bow"]
        mv = dic["messages_vec"]
        for i in mv.keys():
            for j in range(len(mv[i])):
                    mv[i][j] = np.array(mv[i][j])
        self.messages_vec = mv

    def save(self):
        return "debug"
        mv = self.messages_vec
        for i in mv.keys():
            for j in range(len(mv[i])):
                if type(mv[i][j]) is not list:
                    mv[i][j] = mv[i][j].tolist()

        dic = {"messages" : self.messages, "bow" : self.bow, "messages_vec" : mv}
        return json.dumps(dic)