import os, time
from io import StringIO
from datetime import datetime
import requests 
from bs4 import BeautifulSoup
import pandas as pd


def get_csv(query):
    res = requests.get(query)
    time.sleep(1)

    def filter_bad_url_symbols(res_text):
        bad_url_symbols = ['^', '\t', '\'', ':', '<', '>']
        for symbol in bad_url_symbols:
            res_text = res_text.replace(symbol, '')
        return res_text

    csv_io = StringIO(filter_bad_url_symbols(res.text))

    _df = pd.read_csv(csv_io)
    _df['CollectDate'] = datetime.now()
    return _df

def get_theme_news(theme, country):
    query = '{0}query={1}%20sourcecountry:{2}&output=artlist&dropdup=true'.format(url, theme, country)

    res = requests.get(query)
    time.sleep(1)
    soup = BeautifulSoup(res.text, "html.parser") 
    tag_a = soup.select('td a')
    _df = pd.DataFrame()

    for a in tag_a:
        title = a.select_one('b').text
        publish_date = a.select_one('script').text.split("'")[1].replace(' UTC', '')
        link = a.get('href').split("'")[1]

        row_df = pd.DataFrame({
                    'Theme':[theme], 
                    'Title':[title], 
                    'PublishDate':[publish_date], 
                    'NewsLink':[link]
                })
        _df = _df.append(row_df, ignore_index=True)

    return _df

def save(table_name, _df):
    timenow = datetime.now().strftime("%H%M")

    file_name = '{d}{t}_{f}.csv'.format(d=directory, t=timenow, f=table_name)
    _df.to_csv(file_name, sep=',', index=False, encoding='utf-8')
    print('Save [ ' + timenow + table_name + ' ] to >>> ' + directory)


def main(country):
    theme_query = 'query=sourcecountry:{}&output=wordcloudcsv'.format(country)
    df = get_csv(url + theme_query)
    if df.empty:
        print('\n\n\n********** ERROR! [ {} ] No Content!! **********\n\n'.format(country))
        return
    themes = df['Theme']
    related_words_df = pd.DataFrame()
    newsdf = pd.DataFrame()
    print('\n********** MISSION :[ '+ country +' ] DATE : [ ' + str(datetime.now().date()) + ' ] **********')

    for rank, theme in enumerate(themes):
        print('[{0}] >>> {1}'.format(str(rank).zfill(2), theme))
        
        _df = get_csv('{0}query={1}%20sourcecountry:{2}&output=wordcloudcsv'.format(url, theme, country))
        # _df = get_csv(url + 'query=' + theme + '%20sourcecountry:india&output=wordcloudcsv')
        _df['From'] = theme
        related_words_df = related_words_df.append(_df, ignore_index=True)
        newsdf = newsdf.append(pd.merge(get_theme_news(theme,country), df, on='Theme'))
    save('{}_Theme'.format(country), newsdf)
    save('{}_RelatedWord'.format(country), related_words_df)


if __name__ == '__main__':
    dir_name = datetime.strftime(datetime.now(), '%Y%m%d') + '/'
    url = 'http://api.gdeltproject.org/api/v1/search_ftxtsearch/search_ftxtsearch?'
    directory = '/Users/Urien/Desktop/Taitra/GDELT/gdelt-keywords/data/' + dir_name

    if not os.path.exists(directory):
        os.makedirs(directory)
    country_list = country_list = ['indonesia','malaysia','philippines','singapore','thailand','brunei','laos','myanmar','cambodia','vietnam','india','germany','unitedstates','japan']
    for country in country_list:
        main(country)
