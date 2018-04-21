import re
import pandas as pd
import datetime as dt


def get_year(string):
    """Find substrings that suit the pattern of a possible year, do a sanity check, return the first substring
    that satisfies all conditions

    :param string: string, a text of an advertisement
    :return: int if year found, else None
    """
    match = re.findall('[1-2][0-9][0-9][0-9]\D', string)
    match = [int(item[:-1]) for item in match if 1000 < int(item[:-1]) <= dt.datetime.now().year]
    if len(match) > 0:
        return match[0]
    return


def count_na(series):
    """Check if elements of series are NaN and count the NaNs

    :param series: array-like object
    :return: int, number of NaNs
    """
    return len(series[pd.isna(series)])


def task(path):
    """Load data from the path, do the task and print the results

    :param path: string, a path to file with recorded advertisements
    """
    data = pd.read_table(path, header=None, names=['ad_text'])
    data['year'] = data.ad_text.apply(get_year)
    ratio = len(data[data.year < 2000])/len(data[data.year > 2000])
    print('{} advertisements without release year found'.format(count_na(data.year)))
    print('Coins released before 2000 to coins released after 2000 ratio: {}'.format(round(ratio, 2)))


