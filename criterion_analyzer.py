# -*- coding: cp1251 -*-
from read_write import read_parameters, write_parameters
import pandas as pd
import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

from string import punctuation
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

NUMBER_OF_CRITERIA = 12
VECTOR_SIZE_MIN = 1
VECTOR_SIZE_MAX = 15
DESIRED_WIDTH = 300
MAX_COLUMNS = 17
IS_REMEMBERED = False
REMEMBERED_INFO = None
INDENT_SIGN = '�'

ALGORITMS = [
    (Lasso, '�����', [0.01, 0.1, 1.0, 5.0, 10.0, 50.0, 100.0, 500., 1000.]),
    (KNeighborsRegressor, '��������� ���������� ��������', [3, 4, 5, 6, 7, 8, 9, 10]),
    (DecisionTreeClassifier, '������������� ������� �������', []),
    (DecisionTreeRegressor, '��������� ������� �������', []),
    (LogisticRegression, '������������� ���������', []),
    (SVC, '������� �������� ', []),
            ]

PARAMETERS = {
    'Vectorizer' : 0,     # 0 - Doc2Vec
    'Algorithm' : 0,      # 0 - Random mark, 1 - Ridge Regression, 2 - Classification
}


def set_dataframe_print_options(desired_width, max_columns): #df size for pycharm
    pd.set_option('display.width', desired_width)
    np.set_printoptions(linewidth=desired_width)
    pd.set_option('display.max_columns', max_columns)

#���� �� ������������: ��������� ��� ����������� ���������� ���������� �������
def reminder(func):
     def wrapper(*args):
        global IS_REMEMBERED
        global REMEMBERED_INFO
        if IS_REMEMBERED:
            #print('���������')
            return REMEMBERED_INFO
        else:
            IS_REMEMBERED = True
            #print(*args)
            REMEMBERED_INFO = func(*args)
            return REMEMBERED_INFO
     return wrapper ###

def construct_dataframe(*args, criterion_num):
    print('���������� ������')
    data = pd.read_csv(args[0], encoding='utf-8')
    data2 = pd.read_csv(args[1], encoding='utf-8')
    all_data = pd.concat([data, data2], ignore_index=True)
    if 0 < criterion_num <= NUMBER_OF_CRITERIA:
        all_data = all_data.dropna(subset=[f"�������� K{criterion_num}"])
    if criterion_num == NUMBER_OF_CRITERIA + 1:
        all_data = all_data.dropna()
    all_data['����� ���������'] = all_data['����� ���������'].apply(punctuation_shift)
    all_data['����� ���������'] = all_data['����� ���������'].apply(lambda x: x.lower().strip('\xa0').split())
    #columns = [f'�������� K{j}' for j in range(1, NUMBER_OF_CRITERIA + 1)]
    columns = [f'�������� K{criterion_num}' for criterion_num in range(1, NUMBER_OF_CRITERIA + 1)]
    all_data.insert(loc=14, column='�������� K13', value=all_data[columns].sum(axis=1, skipna=False))
    return all_data
    # write_parameters(args[2], 5, {'PARAMETER1': 11, 'PARAMETER2': 17})
    # write_parameters(args[2], 7, {'PARAMETER1': -90, 'PARAMETER2': 17})
    # print(read_parameters(args[2], 5))
    # print(read_parameters(args[2], 7))

def vectorizer(data, vectoriser_num, *params):
    if vectoriser_num == 0: #Doc2Vec #�������� ������
        input_text = list(data['����� ���������'].values)
        documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(input_text)]
        model_d2v = Doc2Vec(documents, vector_size=params[0], window=params[1], min_count=params[2], workers=4)
        vectors = []
        for x in documents:
            vec = list(model_d2v.dv[x.tags][0])
            vectors.append(vec)
        return pd.DataFrame(vectors, columns=[str(i) for i in range(1, params[0] + 1)])

def train_model(vectorized_df, y, criterion_num):
    X_train, X_test, y_train, y_test = train_test_split(vectorized_df, y, random_state=3)
    for method, method_name, parameters_list in ALGORITMS:
        min_error = None
        if len(parameters_list) > 0:
            for parameter in parameters_list:             #���� �������� � ����������� (�����, ����� ��������� ������� � ��.)
                regression = method(parameter)
                regression.fit(X_train, y_train)
                y_preds = regression.predict(X_test)
                current_error = mean_absolute_error(y_test, y_preds)
                if min_error is None or current_error < min_error:
                    min_error = current_error
        else:                                          #���� �������� ��� ����������
            regression = method()
            regression.fit(X_train, y_train)
            y_preds = regression.predict(X_test)
            min_error = mean_absolute_error(y_test, y_preds)
        print(f'������ ������ {method_name} ��� �������� K{criterion_num}: {min_error}')

def trivial_model(df, criterion_num):            #������� ����������� �� ��������
    y_test = df[f'�������� K{criterion_num}']
    y_preds = [sum(y_test) / len(y_test)] * len(y_test)
    #y_preds = regression.predict(X_test)
    print(f'������ ����������� ������ ��� �������� K{criterion_num}: {mean_absolute_error(y_test, y_preds)}')

def criterion_analyze(*args, criterion_num = None):
    set_dataframe_print_options(DESIRED_WIDTH, MAX_COLUMNS)
    if criterion_num is None:
        criterion_num = int(input('������� ����� ��������: '))
    df = construct_dataframe(*args, criterion_num=criterion_num)
    trivial_model(df, criterion_num)
    vectorized_df = vectorizer(df, 0, 5, 3, 1)   #�������� ���� �� ������� ������ ���������� (!!!)
    train_model(vectorized_df, df[f'�������� K{criterion_num}'], criterion_num)
    print('~' * 75)

def all_criteria_analyze(*args):
    for criterion_num_ in range(1, NUMBER_OF_CRITERIA + 2):
        criterion_analyze(*args, criterion_num = criterion_num_)

def punctuation_shift(text):
    for punctuation_sign in [',', '.', '!', '?', ':', '�', ';', '"', '�', '�']:
        #print(f"|{punctuation_sign}|", end=' ')
        text = text.replace(punctuation_sign, f" {punctuation_sign} ")
    return text

def punctuation_delete(text):
    for punctuation_sign in [',', '.', '!', '?', ':', '�', ';', '"', '�', '�']:
        #print(f"|{punctuation_sign}|", end=' ')
        text = text.replace(punctuation_sign, f" ")
    return text

















