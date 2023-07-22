# -*- coding: cp1251 -*-
import zipfile
import gensim
from ufal.udpipe import Model, Pipeline
import os
import re
import sys
import re
from string import punctuation
from collections import Counter

MODEL_FILE = 'udpipe_syntagrus.model'
IS_REMEMBERED = False
REMEMBERED_INFO = None

# def preprocess(text):
#     tokens = re.sub('#+', ' ', text.lower()).split()
#     tokens = [token.strip(punctuation) for token in tokens]
#     tokens = [token for token in tokens if token]
#     return tokens

#пока не используется: декоратор для запоминания результата выполнения функции
def reminder(func):
     def wrapper(*args):
        global IS_REMEMBERED
        global REMEMBERED_INFO
        if IS_REMEMBERED:
            #print('Запомнили')
            return REMEMBERED_INFO
        else:
            IS_REMEMBERED = True
            #print(*args)
            REMEMBERED_INFO = func(*args)
            return REMEMBERED_INFO
     return wrapper ###

def process(pipeline, text='Строка', keep_pos=True, keep_punct=False):
    entities = {'PROPN'}
    named = False
    memory = []
    mem_case = None
    mem_number = None
    tagged_propn = []

    # обрабатываем текст, получаем результат в формате conllu:
    processed = pipeline.process(text)

    # пропускаем строки со служебной информацией:
    content = [l for l in processed.split('\n') if not l.startswith('#')]

    # извлекаем из обработанного текста леммы, тэги и морфологические характеристики
    tagged = [w.split('\t') for w in content if w]

    for t in tagged:
        if len(t) != 10:
            continue
        (word_id, token, lemma, pos, xpos, feats, head, deprel, deps, misc) = t
        if not lemma or not token:
            continue
        if pos in entities:
            if '|' not in feats:
                tagged_propn.append('%s_%s' % (lemma, pos))
                continue
            morph = {el.split('=')[0]: el.split('=')[1] for el in feats.split('|')}
            if 'Case' not in morph or 'Number' not in morph:
                tagged_propn.append('%s_%s' % (lemma, pos))
                continue
            if not named:
                named = True
                mem_case = morph['Case']
                mem_number = morph['Number']
            if morph['Case'] == mem_case and morph['Number'] == mem_number:
                memory.append(lemma)
                if 'SpacesAfter=\\n' in misc or 'SpacesAfter=\s\\n' in misc:
                    named = False
                    past_lemma = '::'.join(memory)
                    memory = []
                    tagged_propn.append(past_lemma + '_PROPN ')
            else:
                named = False
                past_lemma = '::'.join(memory)
                memory = []
                tagged_propn.append(past_lemma + '_PROPN ')
                tagged_propn.append('%s_%s' % (lemma, pos))
        else:
            if not named:
                if pos == 'NUM' and token.isdigit():  # Заменяем числа на xxxxx той же длины
                    lemma = num_replace(token)
                tagged_propn.append('%s_%s' % (lemma, pos))
            else:
                named = False
                past_lemma = '::'.join(memory)
                memory = []
                tagged_propn.append(past_lemma + '_PROPN ')
                tagged_propn.append('%s_%s' % (lemma, pos))

    if not keep_punct:
        tagged_propn = [word for word in tagged_propn if word.split('_')[1] != 'PUNCT']
    if not keep_pos:
        tagged_propn = [word.split('_')[0] for word in tagged_propn]
    return tagged_propn

'''
def tag_ud(text='Текст нужно передать функции в виде строки!', modelfile=MODEL_FILE):
    udpipe_model_url = 'https://rusvectores.org/static/models/udpipe_syntagrus.model'
    udpipe_filename = udpipe_model_url.split('/')[-1]

    #print('\nLoading the model...', file=sys.stderr)
    model = Model.load(modelfile)
    process_pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')

    #print('Processing input...', file=sys.stderr)
    lines = text.split('\n')
    tagged = []
    for line in lines:
        # line = unify_sym(line.strip()) # здесь могла бы быть ваша функция очистки текста
        output = process(process_pipeline, text=line)
        tagged_line = ' '.join(output)
        tagged.append(tagged_line)
    return '\n'.join(tagged)
'''

# @reminder
# def construct_models():
#     return model_0, process_pipeline

def rus_vectorize(list_of_texts):
    model_0 = gensim.models.KeyedVectors.load_word2vec_format('180/model.bin', binary=True)
    udpipe_model_url = 'https://rusvectores.org/static/models/udpipe_syntagrus.model'
    udpipe_filename = udpipe_model_url.split('/')[-1]
    model = Model.load(MODEL_FILE)
    process_pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')
    def tag_ud(word):
        tagged = []
        output = process(process_pipeline, text=word)
        tagged_line = ' '.join(output)
        tagged.append(tagged_line)
        return '\n'.join(tagged)
    result_list = []
    for text in list_of_texts:
        vec = [0] * 300
        counter = 0
        for word in text:
            try:
                add_vec = model_0[tag_ud(word)]
                vec = list(map(sum, zip(vec, add_vec)))
                counter += 1
            except KeyError:
                pass
        vec = list(map(lambda x: x/counter, vec))
        result_list.append(vec)
    return result_list

def num_replace(word):
    newtoken = 'x' * len(word)
    return newtoken