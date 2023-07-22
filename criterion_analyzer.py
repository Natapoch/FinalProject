# -*- coding: cp1251 -*-
from read_write import read_parameters, write_parameters
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, accuracy_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from rus_vectors import rus_vectorize

NUMBER_OF_CRITERIA = 12
VECTOR_SIZE_MIN = 1
VECTOR_SIZE_MAX = 15
DESIRED_WIDTH = 300
MAX_COLUMNS = 17
INDENT_SIGN = '¶'
ORIGINAL_TEXT_ANALYZE = False

ALGORITMS = [
    (Lasso, 'Лассо', [0.01, 0.1, 1.0, 5.0, 10.0, 50.0, 100.0, 500., 1000.]),
    (KNeighborsRegressor, 'регрессия ближайшими соседями', [3, 4, 5, 6, 7, 8, 9, 10]),
    (DecisionTreeClassifier, 'классификатор деревом решений', []),
    (DecisionTreeRegressor, 'регрессия деревом решений', []),
    (LogisticRegression, 'логистическая регрессия', []),
    (SVC, 'опорных векторов ', []),
            ]

PARAMETERS = {
    'Vectorizer' : 0,     # 0 - Doc2Vec
    'Algorithm' : 0,      # 0 - Random mark, 1 - Ridge Regression, 2 - Classification
}


def set_dataframe_print_options(desired_width, max_columns): #df size for pycharm
    pd.set_option('display.width', desired_width)
    np.set_printoptions(linewidth=desired_width)
    pd.set_option('display.max_columns', max_columns)

def construct_dataframe(*args, criterion_num, original_text_flag):
    print('Подготовка данных')
    data2 = pd.read_csv(args[1], encoding='utf-8')
    if not original_text_flag:
        data = pd.read_csv(args[0], encoding='utf-8')
        all_data = pd.concat([data, data2], ignore_index=True)
    else:
        all_data = data2
    if 0 < criterion_num <= NUMBER_OF_CRITERIA:
        all_data = all_data.dropna(subset=[f"Критерий K{criterion_num}"])
    if criterion_num == NUMBER_OF_CRITERIA + 1:
        all_data = all_data.dropna()
    all_data['Текст сочинения'] = all_data['Текст сочинения'].apply(punctuation_shift)
    all_data['Текст сочинения'] = all_data['Текст сочинения'].apply(lambda x: x.lower().strip('\xa0').split())
    if original_text_flag:
        all_data['Оригинальный текст'] = all_data['Оригинальный текст'].apply(punctuation_shift)
        all_data['Оригинальный текст'] = all_data['Оригинальный текст'].apply(lambda x: x.lower().strip('\xa0').split())
    #columns = [f'Критерий K{j}' for j in range(1, NUMBER_OF_CRITERIA + 1)]
    columns = [f'Критерий K{criterion_num}' for criterion_num in range(1, NUMBER_OF_CRITERIA + 1)]
    if original_text_flag:
        all_data.insert(loc=15, column='Критерий K13', value=all_data[columns].sum(axis=1, skipna=False))
    else:
        all_data.insert(loc=14, column='Критерий K13', value=all_data[columns].sum(axis=1, skipna=False))
    return all_data
    # write_parameters(args[2], 5, {'PARAMETER1': 11, 'PARAMETER2': 17})
    # write_parameters(args[2], 7, {'PARAMETER1': -90, 'PARAMETER2': 17})
    # print(read_parameters(args[2], 5))
    # print(read_parameters(args[2], 7))

def vectorizer(data, vectoriser_num, original_text_flag, *params):
    if vectoriser_num == 0: #Doc2Vec #добавить другие
        input_text = list(data['Текст сочинения'].values)
        documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(input_text)]
        model_d2v = Doc2Vec(documents, vector_size=params[0], window=params[1], min_count=params[2], workers=4)
        vectors = []
        if original_text_flag:
            original_text = list(data['Оригинальный текст'].values)
            documents_original = [TaggedDocument(doc, [i]) for i, doc in enumerate(original_text)]
            model_d2v_original = Doc2Vec(documents_original, vector_size=params[0], window=params[1], min_count=params[2], workers=4)
            for index in range(len(documents)):
                vec = list(model_d2v_original.dv[documents_original[index].tags][0]) + list(model_d2v.dv[documents[index].tags][0])
                vectors.append(vec)
            return pd.DataFrame(vectors, columns=[str(i) for i in range(1, 2*params[0] + 1)])
        else:
            for x in documents:
                vec = list(model_d2v.dv[x.tags][0])
                vectors.append(vec)
            return pd.DataFrame(vectors, columns=[str(i) for i in range(1, params[0] + 1)])
    elif vectoriser_num == 1:
        input_text = list(data['Текст сочинения'].values)
        vec_list = rus_vectorize(input_text)
        vectors = []
        if original_text_flag:
            original_text = list(data['Оригинальный текст'].values)
            original_vec_list = rus_vectorize(original_text)
            for index in range(len(vec_list)):
                vec = vec_list[index] + original_vec_list[index]
                vectors.append(vec)
            return pd.DataFrame(vectors, columns=[str(i) for i in range(1, 601)])
        else:
            # for x in documents:
            #     vec = list(model_d2v.dv[x.tags][0])
            #     vectors.append(vec)
            return pd.DataFrame(vec_list, columns=[str(i) for i in range(1, 301)])


def train_model(vectorized_df, y, criterion_num):
    X_train, X_test, y_train, y_test = train_test_split(vectorized_df, y, random_state=3)
    for method, method_name, parameters_list in ALGORITMS:
        min_error = None
        min_accuracy_percents = None
        if len(parameters_list) > 0:
            for parameter in parameters_list:             #если алгоритм с параметрами (альфа, число ближайщих соседей и др.)
                regression = method(parameter)
                regression.fit(X_train, y_train)
                y_preds = regression.predict(X_test)
                y_preds = np.rint(y_preds)
                current_error = mean_absolute_error(y_test, y_preds)
                accuracy_percents = accuracy_score(y_test, y_preds)
                if min_error is None or current_error < min_error:
                    min_error = current_error
                    min_accuracy_percents = accuracy_percents
        else:                                          #если алгоритм без параметров
            regression = method()
            regression.fit(X_train, y_train)
            y_preds = regression.predict(X_test)
            y_preds = np.rint(y_preds)
            min_error = mean_absolute_error(y_test, y_preds)
            min_accuracy_percents = accuracy_score(y_test, y_preds)
        print(f'Ошибка метода {method_name} для критерия K{criterion_num}: {min_error} ({100 * min_accuracy_percents :.1f} %)')

def trivial_model(df, criterion_num):            #средняя температура по больнице
    y_test = df[f'Критерий K{criterion_num}']
    y_preds = list(map(round, [sum(y_test) / len(y_test)] * len(y_test)))
    #y_preds = regression.predict(X_test)
    accuracy_percents = accuracy_score(y_test, y_preds)
    print(f'Ошибка тривиальной модели для критерия K{criterion_num} с баллом {y_preds[0]}: {mean_absolute_error(y_test, y_preds)} ({100 * accuracy_percents :.1f} %)')

def criterion_analyze(*args, criterion_num = None):
    set_dataframe_print_options(DESIRED_WIDTH, MAX_COLUMNS)
    if criterion_num is None:
        criterion_num = int(input('Введите номер критерия: '))
    original_text_flag = True if (criterion_num in [1, 2, 3, 4]) and ORIGINAL_TEXT_ANALYZE else False
    df = construct_dataframe(*args, criterion_num=criterion_num, original_text_flag=original_text_flag)
    trivial_model(df, criterion_num)
    print('-' * 75)
    print('Word2Vec')
    print('-' * 75)
    vectorized_df = vectorizer(df, 0, original_text_flag, 5, 3, 1)
    train_model(vectorized_df, df[f'Критерий K{criterion_num}'], criterion_num)
    print('-' * 75)
    print('RusVectors')
    print('-' * 75)
    vectorized_df = vectorizer(df, 1, original_text_flag)
    train_model(vectorized_df, df[f'Критерий K{criterion_num}'], criterion_num)
    print('~' * 75)

def all_criteria_analyze(*args):
    for criterion_num_ in range(1, NUMBER_OF_CRITERIA + 2):
        criterion_analyze(*args, criterion_num = criterion_num_)

def punctuation_shift(text):
    for punctuation_sign in [',', '.', '!', '?', ':', '–', ';', '"', '«', '»']:
        #print(f"|{punctuation_sign}|", end=' ')
        text = text.replace(punctuation_sign, f" {punctuation_sign} ")
    return text

def punctuation_delete(text):
    for punctuation_sign in [',', '.', '!', '?', ':', '–', ';', '"', '«', '»']:
        #print(f"|{punctuation_sign}|", end=' ')
        text = text.replace(punctuation_sign, f" ")
    return text

















