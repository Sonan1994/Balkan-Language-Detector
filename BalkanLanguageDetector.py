# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 20:40:37 2021

@author: Nenad Milosevic
"""

import numpy as np
from sklearn import datasets
from sklearn import model_selection
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model

import CustomPlot as cplt

np.random.seed(5)


dataset = datasets.load_files('short_paragraphs')

cplt.CreateAndShowHistogramPlot("Number of articles by language:", dataset)

#separate data to data for training and data for test
data_train, data_test, y_train, y_test = model_selection.train_test_split(dataset.data, dataset.target, test_size = 0.33, stratify = dataset.target)

#Tfid stands for term frequency-inverse document frequency
vectorizer = TfidfVectorizer(ngram_range=(1, 3), analyzer='char', use_idf = False, min_df=5)

#Learn vocabulary and idf from training set.
vectorizer.fit(data_train)

#Transform documents to document-term matrix
X_train = vectorizer.transform(data_train)
X_test = vectorizer.transform(data_test)

#In this example we are going to use LogisticRegression with One vs Rest
model = linear_model.LogisticRegression(multi_class='ovr')
model.fit(X_train, y_train)

#After we train our model, let's predict new y values for test inputs
y_predicted = model.predict(X_test)

#Show statistics
print(metrics.classification_report(y_test, y_predicted))

#Let's start with some random input in language
languageCode = model.predict(vectorizer.transform(["Поранешниот специјалец Спасов е осуден на казна затвор од 14 години за убиството на Мартин"]))

print(np.array(dataset.target_names)[languageCode])
