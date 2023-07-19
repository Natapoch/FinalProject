# -*- coding: cp1251 -*-
import numpy as np
import requests as rq
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from parser import ending
NUMBER_OF_CRITERIA = 12
BIG_PAUSE_TIME = 300
PAUSE_TIME = 1
INDENT_SIGN = '¶'

#
def parse2(*args):
    ege_link_and_title = []
    url = 'https://mogu-pisat.ru/sochinenie/ege/?temp_teacher=&filter_napravlenie=&filter_result=&filter_unchecked=on&filter_teacher=&temp_teacher=&PAGEN_1='
    #print(rq.get(url))
    with open('log2.txt', 'w', encoding='utf-8') as log_file:
        for page_num in range(1, 102): # до 102
            flag_page = False
            while not flag_page:
                try:
                    page = rq.get(url + str(page_num))
                    soup = BeautifulSoup(page.text, features="html.parser")
                    if len(soup.find_all('a')) == 0:
                        print(f'Fail page {page_num}')
                        time.sleep(BIG_PAUSE_TIME)
                        continue
                    print(f'Success page {page_num}')
                except Exception:
                    time.sleep(BIG_PAUSE_TIME)
                    print('Error')
                    continue
                flag_page = True

            for link in soup.find_all('a'):
               if 'sochinenie/ege/?ELEMENT_ID=' in link.get('href'):
                   ege_link_and_title.append(('https://mogu-pisat.ru' + link.get('href'), link.text))
            time.sleep(PAUSE_TIME)

        counter = 0
        len_ = len(ege_link_and_title)
        len_percent = len_ // 100
        ege_list_with_essays = []
        #print(ege_link_and_title)
        for link, title in ege_link_and_title:
            if counter % (len_percent + 1) == len_percent:
                pass
                print(f'Обработан{ending(int(100 * counter / len_))} {int(100 * counter / len_)}% сочинений')
            counter += 1
            flag_page = False  # загружена ли страница (да/нет)
            while not flag_page:
                try:
                    page = rq.get(link)
                except Exception:
                    time.sleep(300)
                    continue
                flag_page = True
            soup = BeautifulSoup(page.text, 'lxml')
            log_file.write("\n----------------------------------\n")

            #for elem in soup.find_all('div', class_='news-detail'):
            if len(soup.find_all('div', class_='news-detail')) > 0:
                elem = soup.find_all('div', class_='news-detail')[0]
            else:
                #print('Empty page')
                continue
            log_file.write(elem.text)
            # try:
            #     log_file.write(elem.text)
            # except UnicodeEncodeError:
            #     log_file.write('Ошибка кодирования')
            #     print('Ошибка кодирования')
            if elem.text.find('Автор:') == -1 or elem.text.find('Количество слов') == -1:
                continue
            essay_index_start = elem.text.find('Автор:') + elem.text[elem.text.find('Автор:'):].find('\n')
            essay_index_end = elem.text.find('Количество слов')
            #print(title, essay_index_start, essay_index_end)
            essay = elem.text[essay_index_start: essay_index_end]
            # if len(essay.split()) == 0:
            #     print(f"Error in essay {counter}")
            #print(essay[:20])
            log_file.write('\n************************\nТекст сочинения\n')
            log_file.write(essay)
            if elem.text.find('Баллы по критериям') == -1 or elem.text.find('Итоговый балл') == -1:
                continue
            criteria_index_start = elem.text.find('Баллы по критериям')
            criteria_index_end = elem.text.find('Итоговый балл')
            criteria = elem.text[criteria_index_start: criteria_index_end]
            log_file.write('\n************************\nКРИТЕРИИ\n')
            log_file.write(criteria)
            criteria_list = [np.NaN] * NUMBER_OF_CRITERIA
            for criteria_num in range(1, NUMBER_OF_CRITERIA + 1):
                if criteria.find(f'К{criteria_num}') != -1:
                    criteria_index = criteria.find(f'К{criteria_num}')
                elif criteria.find(f'K{criteria_num}') != -1:
                    criteria_index = criteria.find(f'K{criteria_num}')
                else:
                    continue
                # if criteria_num == 2:
                #     print('first ', criteria_index)
                while criteria[(criteria_index + 1):].find(f'К{criteria_num}') != -1 or criteria[(criteria_index + 1):].find(f'K{criteria_num}') != -1:
                    if criteria[(criteria_index + 1):].find(f'К{criteria_num}') != -1:
                        criteria_index += 1 + criteria[(criteria_index + 1):].find(f'К{criteria_num}')
                    else:
                        criteria_index += 1 + criteria[(criteria_index + 1):].find(f'K{criteria_num}')
                    # if criteria_num == 2:
                    #     print('then ', criteria_index)
                #print(criteria_index + criteria[criteria_index:].find('\n') - 1, len(criteria))
                if criteria[criteria_index + criteria[criteria_index:].find('\n') - 1] in [str(i) for i in range(0, 7)]:
                    criteria_list[criteria_num - 1] = criteria[criteria_index + criteria[criteria_index:].find('\n') - 1]
            log_file.write('\n&&&&&&&&&\nБАЛЛЫ\n')
            log_file.write(' '.join(list(map(str, criteria_list))))
            ege_list_with_essays.append((indent_replace(essay), *criteria_list))
            time.sleep(PAUSE_TIME)


        for essay_num in range(len(ege_list_with_essays)):
            log_file.write('~' * 71 + str(essay_num) + '~' * 71 + '\n')
            log_file.write(ege_list_with_essays[essay_num][0])
            log_file.write('\n' + ('~' * 144))

        encode_error_counter = 0
        with open('Essays with kriteria2.txt', 'w', encoding='utf-8') as file_:  # добавили в файл
            for essay, *criteria_list in ege_list_with_essays:
                file_.write(essay)
                file_.write('\n')
                for criteria_num, criteria_score in enumerate(criteria_list):
                    file_.write(f"Критерий К{criteria_num + 1}: {criteria_score} ")  # f строка - форматированная, чтоб красиво
                    file_.write('\n\n')


        print(f"Read {len(ege_list_with_essays)} essays")
        print(f"Encode error in {encode_error_counter} essays")
        column_names = ['Текст сочинения']
        for num in range(1, NUMBER_OF_CRITERIA + 1):
            column_names.append(f'Критерий K{num}')
        df = pd.DataFrame(ege_list_with_essays, columns=column_names)
        # df.to_excel('table with K6,K9.xlsx')
        df.to_csv(args[1])

def indent_replace(text):
    text = re.sub(r'\n(\s*\n)*', INDENT_SIGN, text)
    text = text.replace('\n', INDENT_SIGN)
    while text[0] in [INDENT_SIGN, ' ', '\t']:
        text = text[1:]
    while text[-1] in [INDENT_SIGN, ' ', '\t']:
        text = text[:-1]
    return text