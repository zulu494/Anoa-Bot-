from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pandas as pd

label = { 0: 'Aman', 1: 'Penipuan', 2: 'Promo' }

def get_label(dataset, message):
    data_train, data_test, label_train, label_test = train_test_split(
        dataset[1],
        dataset[0],
        test_size=0.2,
        random_state=40
    )
    
    pipe = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB())
    ])

    pipe.fit(data_train, label_train)
    result = pipe.predict([message])

    # !!! for data mining purpose !!!
    f = open("collect.txt", "a")
    f.write(result[0] + ',' + message + "\n")
    f.close()
    # !!! for data mining purpose !!!

    return label[int(result[0])]