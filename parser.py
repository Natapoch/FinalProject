#убрала для гита кодировку, чтобы не слетала кодировка в комментариях, но запускала код с -*- coding: cp1251 -*-
import requests as rq
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import numpy as np
#import copy
NUMBER_OF_CRITERIA = 12
MINIMAL_NUMBER_OF_KRITERIA = 3
INDENT_SIGN = '¶'

def ending(number):     #это для того, чтобы красиво дальше считать % скачанных текстов
    if number % 100 == 11:
        return 'о'
    number %= 10
    if number == 1:
        return ' '
    else:
        return 'о'

def delete_ending_symbols(text):
    text = re.sub(r'Содержание сочинения', '', text)
    #print(index_words[0], type(index_words[0]))
    # if len(number_of_words) > 0:
    #     index_words = text.find(number_of_words[0])
    #     text = text[:index_words]
    text = re.sub(r'\(\s*\d*\s*слов[ао]?\s*\)', '', text)
    #text = re.sub(r'\(\s*\d*\s*слова\s*\)', '', text)
    #text = re.sub(r'\(\s*\d*\s*слово\s*\)', '', text)
    text = re.sub(r'{INDENT_SIGN}{INDENT_SIGN} {INDENT_SIGN}', '', text)
    while text[0] in [INDENT_SIGN, ' ', '\t']:
        text = text[1:]
    while text[-1] in [INDENT_SIGN, ' ', '\t']:
        text = text[:-1]
    return text

#(280 слова)

def parse(*args):
    url = 'https://www.kritika24.ru/page.php?id=1907&top=kritik&cat=EGJe_2013&page='

    ege_link_and_title = []
    number_of_indefined_essays = 0
    #print('Составление списка ссылок с сочинениями\n\n\n')
    with open('log.txt', 'w', encoding='utf-8') as log_file:
        print('Выгрузка страниц')
        for page_num in range(1, 33): #нужны ссылки с 1 по 32 страницу
            flag_page = False        #показывает, удалось ли считать информацию со страницы

            while not flag_page:
                try:
                    page = rq.get(url + str(page_num))
                except Exception:             #отказывался парсить
                    time.sleep(1)
                    print('Ошибка загрузки...')
                    continue
                flag_page = True
            #time.sleep(1)
            soup = BeautifulSoup(page.text, features="html.parser")  #utf-8 не идёт
            #print(soup.prettify())
            #print(soup.text)
            list_ = []
            for link in soup.find_all("a"):        #найдем гиперссылки и соединим их с номером страницы + семью элементами до php?id=
                list_.append((str(link.get('href')), link.text))
            for link, title in list_:
                index = link.find('php?id=')
                #print(link[index + 7:])
                try:
                    number = int(link[index + 7:]) #по кол-ву символом (слово 'page' тоже учитывалось)
                except ValueError:
                    number = -1
                if index != -1 and link.find('EGJe') == -1 and number > 4917: #задали промежуток: !== от 0 до 4917
                    ege_link_and_title.append(('https://www.kritika24.ru/' + link, title))
            ege_link_and_title.pop() #убрали лишнее с конца
            ege_link_and_title.pop()
            time.sleep(0.07)
            #print(ege_link_and_title)

        ege_link_and_title.pop(0) #исключить первые три сочинения, т.к. они нам не подходят
        ege_link_and_title.pop(0)
        ege_link_and_title.pop(0)
        ege_link_and_title.pop(0)
        ege_list_with_essays = []
        #print(ege_link_and_title)
        print('Выгрузка сочинений')
        counter = 0
        len_ = len(ege_link_and_title)
        len_percent = len_ // 100

        for link, title in ege_link_and_title:
            if counter % (len_percent + 1) == len_percent:
                print(f'Обработан{ending(int(100 * counter / len_))} {int(100 * counter / len_)}% сочинений')
            counter += 1
            flag_page = False  # загружена ли страница (да/нет)
            while not flag_page:
                try:
                    page = rq.get(link)
                except Exception:
                    time.sleep(1)
                    print('Ошибка загрузки...')
                    continue
                flag_page = True

            soup = BeautifulSoup(page.text, 'lxml')
            flag_img = False                       #убираем все ссылки на изображения: тег img + scr=screen'
            for elem in soup.find_all('img'):
                if elem['src'].startswith('screen'):
                    #print(elem['src'])
                    flag_img = True
            if flag_img:
                continue
            essay = '' #создали строку
            flag_K = False                   #работаем с критериями: отбираем по тегу с текстом К6 и К9
            kriteria_list = [np.NaN] * NUMBER_OF_CRITERIA
            kriteria_counter = 1
            defined_kriteria_counter = 0
            score_list = []
            kriteria_str = ''
            #log_file.write("Текст критериев:\n")
            for elem in soup.find_all('p'):
                #log_file.write(elem.text)
                #log_file.write('\n')
                if elem.text.find('Наши эксперты могут проверить Ваше сочинение по критериям ЕГЭ') != -1:
                    break
                if not flag_K:
                    if elem.text.find('К1') == -1: #не найдено К1, еще идет текст
                        essay += elem.text
                        essay += INDENT_SIGN
                    else:
                        flag_K = True         #если нашел К1, дальше идут критерии, в текст не пишет
                        shift_flag = True
                if flag_K:
                    if elem.text.find(f'К{kriteria_counter + 1}') != -1:
                        shift_flag = True
                        log_file.write(f'Для критерия: {kriteria_counter}\n')
                        #log_file.write(' '.join(list(map(str, score_list))))
                        log_file.write(kriteria_str)
                        log_file.write('\n')
                        if 0 < len(score_list):
                            if len(score_list) < 3:  # нам нужен 1-й элемент, т.к. запись мб разной: 2 из 2 или 2/2. Если длина будет ноль - значит, оценок не было
                                kriteria_list[kriteria_counter - 1] = score_list[0]
                                defined_kriteria_counter += 1
                            else:
                                #log_file.write(f"\nKriteria: {kriteria_counter} Number1 {log_str.find(f'К{kriteria_counter}')}, Number2 {len(f'К{kriteria_counter}')}\n")
                                #test_text = log_str[(log_str.find(f'К{kriteria_counter}') + len(f'К{kriteria_counter}')):]
                                #test_index = test_text.find(score_list[0])
                                #log_file.write(f'Test text:\n{test_text[test_index:]}\nTest: {test_text[test_index:].find("пример")} {test_text[test_index:].find("ошиб")}\n')
                                # if -1 < test_text[test_index:].find('пример') < 4 or -1 < test_text[test_index:].find('ошиб') < 4:
                                #     log_file.write(log_str)
                                #     log_file.write(f'\nПредполагаемая оценка: {score_list[-2]} (пример/ошибка)\n')
                                # else:
                                #     pass
                                #log_file.write(log_str)
                                test_index_shift = kriteria_str.find('(')
                                test_index = test_index_shift
                                while test_index_shift != -1:
                                    #print('1', test_index, len(log_str))
                                    for index_shift in range(-2, 3):
                                        if 0 <= test_index + index_shift < len(kriteria_str) and kriteria_str[test_index + index_shift] in [str(i) for i in range(0, 7)]:
                                            #log_file.write(f'\nПредполагаемая оценка: {kriteria_str[test_index + index_shift]}\n')
                                            kriteria_list[kriteria_counter - 1] = kriteria_str[test_index + index_shift]
                                            defined_kriteria_counter += 1
                                            test_index = len(kriteria_str)
                                            break
                                    #print('2', test_index, len(log_str))
                                    test_index_shift = kriteria_str[test_index + 1:].find('(')
                                    test_index += test_index_shift + 1
                                #log_file.write(f'\nПредполагаемая оценка: {None}\n')
                        kriteria_counter += 1
                        score_list = []
                        kriteria_str = ''
                        #print(f'К{kriteria_num}')
                        log_file.write(f'Балл за критерий: {kriteria_list[kriteria_counter - 2]}\n')
                    if shift_flag:
                        score_list += re.findall(r'[0-6]', elem.text[(elem.text.find(f'К{kriteria_counter}') + len(f'К{kriteria_counter}')):])
                    else:
                        score_list += re.findall(r'[0-6]', elem.text)
                    shift_flag = False
                    kriteria_str += elem.text
                    #log_file.write(elem.text)
                    #log_file.write('\n')
            log_file.write(f'Для критерия: {kriteria_counter}\n')
            # log_file.write(' '.join(list(map(str, score_list))))
            log_file.write(kriteria_str)
            log_file.write('\n')
            if 0 < len(score_list):
                if len(score_list) < 3:  # нам нужен 1-й элемент, т.к. запись мб разной: 2 из 2 или 2/2. Если длина будет ноль - значит, оценок не было
                    kriteria_list[kriteria_counter - 1] = score_list[0]
                    defined_kriteria_counter += 1
                    score_list = []
                else:
                    # test_text = log_str[(log_str.find(f'К{kriteria_counter}') + len(f'К{kriteria_counter}')):]
                    # test_index = test_text.find(score_list[0])
                    # #log_file.write(f'Test text:\n{test_text[test_index:]}\nTest: {test_text[test_index:].find("пример")} {test_text[test_index:].find("ошиб")}\n')
                    # if -1 < test_text[test_index:].find('пример') < 4 or -1 < test_text[test_index:].find('ошиб') < 4:
                    #     log_file.write(log_str)
                    #     log_file.write(f'\nПредполагаемая оценка: {score_list[-2]} (пример/ошибка)\n')
                    # else:
                    #     pass
                    #log_file.write(log_str)
                    test_index_shift = kriteria_str.find('(')
                    test_index = test_index_shift
                    while test_index_shift != -1:
                        # print('1', test_index, len(log_str))
                        for index_shift in range(-2, 3):
                            if 0 <= test_index + index_shift < len(kriteria_str) and kriteria_str[test_index + index_shift] in [str(i) for i in range(0, 7)]:
                                #log_file.write(f'\nПредполагаемая оценка: {kriteria_str[test_index + index_shift]}\n')
                                kriteria_list[kriteria_counter - 1] = kriteria_str[test_index + index_shift]
                                defined_kriteria_counter += 1
                                test_index = len(kriteria_str)
                                break
                        # print('2', test_index, len(log_str))
                        test_index_shift = kriteria_str[test_index + 1:].find('(')
                        test_index += test_index_shift + 1
                log_file.write(f'Балл за критерий: {kriteria_list[kriteria_counter - 1]}\n')
                        #log_file.write(f'\nПредполагаемая оценка: {score_list[0]}\n')
                            #kriteria_counter += 1

                            # if elem.text.find('К9') != -1:
                            #     score_list = re.findall(r'[0-2]', elem.text)
                            #     if len(score_list) > 0:
                            #         k_9 = score_list[0]
            #print("---------------------")
            #log_file.write("Сочинение:\n")
            #log_file.write(essay)
            #log_file.write('\n')
            #log_file.write("Критерии:\n")
            #log_file.write(str(" ".join(list(map(str, kriteria_list)))))
            #log_file.write('\n\n')
            if defined_kriteria_counter >= MINIMAL_NUMBER_OF_KRITERIA:
                #ege_list_with_essays.append((link, title, essay, *kriteria_list))
                #print(delete_ending_symbols(essay)[-10:])
                #print(list(map(ord, delete_ending_symbols(essay)[-10:])))
                ege_list_with_essays.append((delete_ending_symbols(essay), *kriteria_list))
            if 0 < defined_kriteria_counter < NUMBER_OF_CRITERIA:
                #print(kriteria_counter, NUMBER_OF_CRITERIA)
                #print(essay)
                #print(*kriteria_list)
                number_of_indefined_essays += 1
            time.sleep(0.07)
        # for essay_num in range(len(ege_list_with_essays)):
        #     log_file.write('~' * 71 + str(essay_num) + '~' * 71 + '\n')
        #     log_file.write(ege_list_with_essays[essay_num][0])
        #     log_file.write('\n' + ('~' * 144))

    print(f"Number of indefined essays: {number_of_indefined_essays}")
    with open('Essays with kriteria.txt', 'w', encoding='utf-8') as file_: #добавили в файл
        for essay, *kriteria_list in ege_list_with_essays:
            file_.write(essay)
            file_.write('\n')
            for kriteria_num, kriteria_score in enumerate(kriteria_list):
                file_.write(f"Критерий К{kriteria_num + 1}: {kriteria_score} ") #f строка - форматированная, чтоб красиво
            file_.write('\n\n')

    print(f"Read {len(ege_list_with_essays)} essays")
    #column_names = ['Ссылка', 'Заголовок', 'Текст сочинения']
    column_names = ['Текст сочинения']
    for num in range(1, NUMBER_OF_CRITERIA + 1):
        column_names.append(f'Критерий K{num}')
    df = pd.DataFrame(ege_list_with_essays, columns=column_names)
    #df.to_excel('table with K6,K9.xlsx')
    df.to_csv(args[0])