# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 19:28:02 2021

@author: Nenad Milosevic
"""
import numpy as np
from matplotlib import pyplot as plt

def CreateAndShowHistogramPlot(title, dataset):
    plt.title("Number of articles by language:")
    
    lengthOfTargetNames = len(dataset.target_names)
    
    plt.barh(np.arange(0, lengthOfTargetNames), np.bincount(dataset.target), color = 'green')
    plt.yticks(np.arange(0, lengthOfTargetNames), dataset.target_names)
    
    plt.show()

    