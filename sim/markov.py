import random

class Markov():
    def __init__(self, states,actual, probabilities):
        self.states=states
        self.actual=actual
        self.probabilities=probabilities
    
    def next_state(self):
        actual_state = self.states.index(self.actual)
        self.actual=self.select_next_state(self.states, self.probabilities[actual_state], random.random())

    def select_next_state(self,items, probabilities, r):
        sum_prob=0
        i=0
        for p in probabilities:
            sum_prob+=p
            if r<=sum_prob:
                break
            else:
                i+=1
        if i>=len(items):
            i=len(items)-1
        return items[i]

    def get_actual_state(self):
        return self.actual