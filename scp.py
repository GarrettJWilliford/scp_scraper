from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import pickle
import re
import pandas as pd




def remove_html(inp):
    rems = ['<strong>', '</strong>', '<em>', '</em>', '<sup>', '</sup>', '<br>']
    if '<span' in inp:
        return False
    if '<a href' in inp:
        return False
    if '<iframe' in inp:
        return False
    for r in rems:
        inp = re.sub(r, '', inp)
    return inp

def remove_repeat(inp):
    repeat = ['SCP by Series', 'SCP Tales by Series', 'SCP Library', 'Discover Content', 'SCP Community', 'User Resources']
    if inp in repeat:
        return False
    return inp




def driver_init(headless = True):
    if not headless:
        return webdriver.Firefox()
    fop = Options()
    fop.add_argument('--headless')
    fop.add_argument('--window_size1920x1080')
    return webdriver.Firefox(options = fop)




def scp(driver):
    driver.get('http://www.scp-wiki.net/')
    while True:
        os.system('clear')
        print('<<<<<<<<<<SCP_FOUNDATION>>>>>>>>>>')
        command = input('>>SELECT_SCP>> ')
        if command == 'BACK':
            driver.quit()
            return
        if command.isdigit():
            print('<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>')
            driver.get('http://www.scp-wiki.net/scp-' + str(command))
            p = driver.find_elements_by_tag_name('p')
            for pp in p:
                a = pp.get_attribute('innerHTML')
                a = remove_repeat(remove_html(a))
                if not a:
                    continue
                print(a)
            command = input('<<|PRESS_ENTER_TO_CONTINUE|>>')


def scp_nickname(driver):
    scps = {'scp_num' : [], 'nickname' : []}
    series = ['series', 'series-2', 'series-3', 'series-4', 'series-5']
    for s in series:
        #print('<<|SCRAPING ' + s + '|>>')
        driver.get('http://www.scp-wiki.net/scp-' + s)
        li = driver.find_elements_by_tag_name('li')
        for l in li:
            words = l.get_attribute('innerHTML')
            words = words[words.index('>') + 1::]
            words = re.sub('</a> -', '', words)
            words = remove_html(words)
            if type(words) == bool:
                continue
            if words[4:7].isdigit():
                s = [w for w in words if w.isdigit() and words.index(w) < 8]
                scps['scp_num'].append(''.join(s))
                scps['nickname'].append(words[8::])
            #except:
                print('SCP_NUM : ' + ''.join(s))
                print('SCP_NICK : '+ words[8::])
            print('<<<<<>>>>>')
    driver.quit()
    return scps

def scp_scraper(driver):
    total_dict = {'scp_num' : [], 'scp_class' : [], 'Description' : []}
    for i in range(100, 4000):
        des = False
        print('Scraping SCP- %s' % (str(i)))
        driver.get('http://www.scp-wiki.net/scp-%s' % str(i))
        total_dict['scp_num'].append(str(i))
        items = driver.find_elements_by_tag_name('p')
        string = ''
        scp_class = '<<!ERROR!>>'
        for it in items:
            it = remove_repeat(remove_html(it.get_attribute('innerHTML')))
            if not it:
                continue
            if 'Object Class:' in it:
                print('<<<<<>>>>>')
                scp_class = it[14::]
            print(it)
            print('<><><><><><><><><><>')
            if des:
                string = string + it
                continue
            if 'Description:' in it:
                #print(it)
                des = True
        total_dict['scp_class'].append(scp_class)
        total_dict['Description'].append(string)
    driver.quit()
    return total_dict


                
            

