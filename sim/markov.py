import numpy as np

class Markov():
    def __init__(self, states,actual, probabilities):
        self.states=states
        self.actual=actual
        self.probabilities=probabilities
    
    def next_state(self):
        actual_state = self.states.index(self.actual)
        n_state = np.random.choice(self.states, p=self.probabilities[actual_state])
        self.actual=n_state
    
    def get_actual_state(self):
        return self.actual