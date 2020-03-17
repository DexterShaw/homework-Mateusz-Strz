from typing import List

import pandas as pd

CONFIRMED_CASES_URL = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                      f"/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv "

"""
When downloading data it's better to do it in a global scope instead of a function.
This speeds up the tests significantly
"""
confirmed_cases = pd.read_csv(CONFIRMED_CASES_URL, error_bad_lines=False)


def poland_cases_by_date(day: int, month: int, year: int = 2020) -> int:
    """
    Returns confirmed infection cases for country 'Poland' given a date.

    Ex.
    >>> poland_cases_by_date(7, 3, 2020)
    5
    >>> poland_cases_by_date(11, 3)
    31

    :param year: 4 digit integer representation of the year to get the cases for, defaults to 2020
    :param day: Day of month to get the cases for as an integer indexed from 1
    :param month: Month to get the cases for as an integer indexed from 1
    :return: Number of cases on a given date as an integer
    """
    
    infection = confirmed_cases.loc[confirmed_cases["Country/Region"]=="Poland"][f"{month}/{day}/{year-2000}"].values[0]
    return infection


def top5_countries_by_date(day: int, month: int, year: int = 2020) -> List[str]:
    """
    Returns the top 5 infected countries given a date (confirmed cases).

    Ex.
    >>> top5_countries_by_date(27, 2, 2020)
    ['China', 'Korea, South', 'Cruise Ship', 'Italy', 'Iran']
    >>> top5_countries_by_date(12, 3)
    ['China', 'Italy', 'Iran', 'Korea, South', 'France']

    :param day: 4 digit integer representation of the year to get the countries for, defaults to 2020
    :param month: Day of month to get the countries for as an integer indexed from 1
    :param year: Month to get the countries for as an integer indexed from 1
    :return: A list of strings with the names of the coutires
    """
    data = f"{month}/{day}/{year-2000}"
    top =  confirmed_cases[['Province/State', 'Country/Region', data]]
    return list(top.groupby('Country/Region').sum().sort_values(by=data, ascending=False).head(5).index.values)


def no_new_cases_count(day: int, month: int, year: int = 2020) -> int:
    """
    Returns the number of countries/regions where the infection count in a given day was the same as the previous day.

    Ex.
    >>> no_new_cases_count(11, 2, 2020)
    35
    >>> no_new_cases_count(3, 3)
    57

    :param day: 4 digit integer representation of the year to get the cases for, defaults to 2020
    :param month: Day of month to get the countries for as an integer indexed from 1
    :param year: Month to get the countries for as an integer indexed from 1
    :return: Number of countries/regions where the count has not changed in a day
    """
    if day==0 or month==0 or year==0:
        raise ValueError("if either number was negative")
    data = f"{month}/{day}/{year-2000}"
    if day!=1:
        day_wczoraj = day -1
        month_wczoraj= month
        year_wczoraj = year
    else:
        if month in [2,4,6,9,11]:
            day_wczoraj = 31
            month_wczoraj= month -1
            year_wczoraj = year
        elif month == 3:
            if year%4==0:
                day_wczoraj=29
            else:
                day_wczoraj=28
            month_wczoraj= month -1
            year_wczoraj = year
        elif month ==1:
            day_wczoraj = 31
            month_wczoraj = 12
            year_wczoraj = year -1
        else:
            day_wczoraj = 30
            month_wczoraj= month -1
            year_wczoraj = year
    data_wczoraj= f"{month_wczoraj}/{day_wczoraj}/{year_wczoraj-2000}"
    wynik = confirmed_cases.groupby(['Country/Region']).sum()
    return wynik[wynik[data]!=wynik[data_wczoraj]].count()[0]
