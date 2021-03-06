# -*- coding: utf-8 -*-
"""breast_sonography_v1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SSnrWR0zug50OAYR8LYpit9EBVHhu7WE

**Import Packages**
"""

from re import X
import numpy as np
import csv
from numpy.core.defchararray import encode
from numpy.core.numeric import NaN
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,  f1_score
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings("ignore")

"""**Up Sampling**"""

def upsampling(X_train, y_train):
  # upsampling on training data only
  from imblearn.over_sampling import SMOTE
  smt = SMOTE(random_state = 1126)
  X_train, y_train = smt.fit_resample(X_train, y_train)
  from collections import Counter
  print(sorted(Counter(y_train).items()))
  return X_train, y_train

"""**Read Data from Google Drive**"""

from google.colab import drive
import pandas as pd
drive.mount('/content/gdrive') # 此處需要登入google帳號
# 獲取授權碼之後輸入即可連動雲端硬碟
#!"/content/gdrive/MyDrive/breast/BreastSonor7Features.csv"
train_path = "/content/gdrive/MyDrive/breast/BreastSonor7Features.csv"

"""**Data Loader**"""

import pandas as pd 
def data_loader(train_path):
    data = pd.read_csv(train_path)
    data_top = list(data.columns)
    with open(train_path, 'r') as fp:     
        data_train = list(csv.reader(fp))
        data_label = data_train
        data_train = np.array(data_train[1:])[:, 0:7]
        data_label = np.array(data_label[1:])[:, 7]    
    return data_train, data_label

"""**RMSE**"""

import math
def RMSE(prediction, ground):
  length = len(prediction)
  sum = 0
  RMSE = 0
  for i in range(length):
    sum += (float(prediction[i]) - float(ground[i]))**2
  sum /= length
  RMSE = math.sqrt(sum)
  return RMSE

"""**COLOR**"""

CRED = '\033[91m'
CEND = '\033[0m'

"""**Naive Bayes classifier**"""

def NB(X_train, X_val, y_train, y_val):
    from sklearn.naive_bayes import GaussianNB
    gnb = GaussianNB().fit(X_train, y_train)
    val_predictions = gnb.predict(X_val)
    #RMSE
    NB_RMSE = 0
    NB_RMSE = RMSE(val_predictions, y_val)
    print(CRED +"NB RMSE = "+CEND,NB_RMSE)
    # Validation accuracy
    accuracy = gnb.score(X_val, y_val)
    #print('NB accuracy')
    #print(accuracy)
    # Validation confusion matrix
    cm = confusion_matrix(y_val, val_predictions)
    #print('NB CFmap')
    #print(cm)
    numOfBigError = 0
    for i in range(len(y_val)):
      error = abs(float(y_val[i])-float(val_predictions[i]))
      if error > 1:
        numOfBigError+=1
    print("num of error > 1 = ",numOfBigError)
    #testing
    #test_predictions = gnb.predict(x_test)
    return True

"""**KNN**"""

def KNN(X_train, X_val, y_train, y_val):
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors = 7).fit(X_train, y_train)
    print(knn)
    # model accuracy for X_test 
    accuracy = knn.score(X_val, y_val)
    #print('KNN accuracy')
    #print(accuracy)
    # creating a confusion matrix
    knn_predictions = knn.predict(X_val)
    #RMSE
    KNN_RMSE = 0
    KNN_RMSE = RMSE(knn_predictions, y_val)
    print(CRED +"KNN RMSE = "+CEND,KNN_RMSE)
    cm = confusion_matrix(y_val, knn_predictions)
    numOfBigError = 0
    for i in range(len(y_val)):
      error = abs(float(y_val[i])-float(knn_predictions[i]))
      if error > 1:
        numOfBigError+=1
    print("num of error > 1 = ",numOfBigError)
    #print('KNN CFmap')
    #print(cm)
    #testing
    #test_predictions = knn.predict(x_test)
    return True

"""**Random Forest**"""

def RF(X_train, X_val, y_train, y_val, grid = False):
    from sklearn.ensemble import RandomForestClassifier

    #grid search
    if grid == True:
        rf = RandomForestClassifier()
        parameters = {'n_estimators':range(100, 1000, 100)}
        clf = GridSearchCV(rf, parameters)
        clf.fit(X_train, y_train)
        rf = clf.best_estimator_

    if grid == False:
        rf = RandomForestClassifier()
        rf.fit(X_train, y_train)
    
    #result
    rf_predictions = rf.predict(X_val)
    #RMSE
    RF_RMSE = 0
    RF_RMSE = RMSE(rf_predictions, y_val)
    error = 0
    numOfBigError = 0
    for i in range(len(y_val)):
      #print("truth ",i," = ",y_val[i])
      #print("prediction ",i," = ",rf_predictions[i])
      error = abs(float(y_val[i])-float(rf_predictions[i]))
      if error > 1:
        numOfBigError+=1
        #print(CRED+"big error = "+CEND, error)
    print(CRED+"RF RMSE = "+CEND,RF_RMSE)
    print("num of error > 1 = ",numOfBigError)
    accuracy = rf.score(X_val, y_val)
    #print('RF accuracy')
    #print(accuracy)
    cm = confusion_matrix(y_val, rf_predictions)
    #print('RF CFmap')
    #print(cm)
    #print('RF f1 score')
    #print(f1_score(y_val, rf_predictions, average = 'macro'))
    #testing
    #test_predictions = rf.predict(x_test)
    return True

"""**GradientBoosting**"""

def GradientBoosting(X_train, X_val, y_train, y_val, grid = False):
    from sklearn.ensemble import GradientBoostingClassifier

    if grid == True:
        gb = GradientBoostingClassifier()
        parameters = {'n_estimators': range(100, 500, 100),
                      'learning_rate': [0.01, 0.05, 0.1, 0.5, 1]
                      }
        clf = GridSearchCV(gb, parameters)
        clf.fit(X_train, y_train)
        print(clf.best_params_)
        gb = clf.best_estimator_

    else:
        gb = GradientBoostingClassifier(n_estimators = 100, learning_rate = 0.1, random_state = 1126)
        gb = Pipeline([ #('pca', PCA(n_components = 5)),
                        ('clf', gb)
                    ])
        gb.fit(X_train, y_train)

    # Validation
    accuracy = gb.score(X_val, y_val)
    #print('GB accuracy')
    #print(accuracy)
    # creating a confusion matrix
    gb_predictions = gb.predict(X_val)
    cm = confusion_matrix(y_val, gb_predictions)
    #RMSE
    GB_RMSE = 0
    GB_RMSE = RMSE(gb_predictions, y_val)
    print(CRED+"GB RMSE = "+CEND,GB_RMSE)
    numOfBigError = 0
    for i in range(len(y_val)):
      error = abs(float(y_val[i])-float(gb_predictions[i]))
      if error > 1:
        numOfBigError+=1
    print("num of error > 1 = ",numOfBigError)
    '''
    #print('GB CFmap')
    #print(cm)
    #print('GB f1 score')
    #print(f1_score(y_val, gb_predictions, average = 'macro'))
    # add validation-set into sub-training set
    X_trainval = np.vstack((np.array(X_train), np.array(X_val)))
    y_trainval = np.hstack((np.array(y_train), np.array(y_val)))

    # retraining w/ full training set
    if grid == True:
        gb = GradientBoostingClassifier(clf.best_params_)
    else:
        gb = GradientBoostingClassifier(n_estimators = 400, learning_rate = 0.5, random_state = 1126)

    gb.fit(X_trainval, y_trainval)
    # testing
    #test_predictions = gb.predict(x_test)
    '''
    return True

"""**Read in data**"""

data_trainval, data_label = data_loader(train_path)
print(data_trainval)
print(data_label)

"""**Split data**"""

X_train, X_val, y_train, y_val = train_test_split(data_trainval, data_label, random_state = 1126, train_size = 0.8)

'''
#upsampling
from imblearn.over_sampling import SMOTE
smt = SMOTE(random_state = 1126)
X_train, y_train = smt.fit_resample(X_train, y_train)
from collections import Counter
'''

"""**Trainning Prediction**"""

print("NB Predicrion")
predictions_NB = NB(X_train, X_val, y_train, y_val)

print("\nKNN Predicrion")
predictions_KNN = KNN(X_train, X_val, y_train, y_val)

print("\nRF Predicrion")
predictions_RF = RF(X_train, X_val, y_train, y_val, False)

print("\nGB Predicrion")
predictions_GB = GradientBoosting(X_train, X_val, y_train, y_val, False)