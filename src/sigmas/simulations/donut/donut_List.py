import numpy as np
from .donut import Donut

class DonutList:
    def __init__(self, donuts):
        if not donuts:
            raise ValueError("The list of donuts cannot be empty.")
        
        self.donuts = donuts
        self.height, self.width = self.donuts[0].model.shape

        for donut in self.donuts:
            if donut.model.shape != (self.height, self.width):
                raise ValueError("All donuts must have the same shape.")
        
        self.combined = np.zeros((self.height, self.width), dtype=np.float32)

        self.combine()
    
    def combine(self):
        for donut in self.donuts:
            self.combined += donut.model

    def add_donut(self, donut):
        if donut.shape != (self.height, self.width):
            raise ValueError("Donut shape does not match the list shape.")
        self.combined += donut.model
    
    def get_combined(self):
        return self.combined
    
    def normalize(self):
        max_val = np.max(self.combined)
        if max_val > 0:
            self.combined /= max_val
        
