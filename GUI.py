import time
import flet as ft
import requests
import pandas as pd
from numpy import array
from pandas.core.common import flatten
from flatten_json import flatten
import matplotlib
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import numpy as np


class State:
    toggle = True
s = State()

def main(page: ft.Page):
    page.title = "HH"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    user_data = ft.TextField(label='Set skill', width=400)


    matplotlib.use("svg")
    fig, ax = plt.subplots(figsize=(17, 7))
    ax.set_xlabel("period:", color='#1f77b4')
    ax.set_ylabel("measure:", color='#1f77b4')
    plt.xticks(rotation=45, color='#1f77b4')
    plt.yticks(color='#1f77b4')
    plt.title('HH.ru query:', color='#1f77b4')
    # plt.grid()
    chart = MatplotlibChart(fig, expand=True, original_size=False, transparent=True, isolated=True)


    def get_info(e):
        str_json = []
        start = time.process_time()

        URL = f'https://api.hh.ru/vacancies?text={user_data.value}&area={1}&per_page={10}&page={1}'
        vac_count = requests.get(URL).json()
        tmp = int(vac_count['found']) // 100 if int(vac_count['found']) // 100 < 20 else 1


        for i in range(0, tmp):
            URL = f'https://api.hh.ru/vacancies?text={user_data.value}&area={1}&per_page={100}&page={i}'
            res = requests.get(URL).json()

            for j in range(0, len(res['items'])):
                select_columns = {key: res['items'][j][key] for key in
                                  ['id', 'salary', 'published_at']}

                str_json.append(flatten(select_columns))

        if len(str_json) == 0:
            # income = pd.read_csv('income.csv')
            plt.cla()
            plt.title('HH.ru query:', color='#1f77b4')
            x = [2, 2, 2, 2.5, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4.5, 4.5, 4.5, 4.5, 5, 5, 5, 5, 5, 6, 6, 6, 6.5, 7, 7, 7,
                 7, 7]
            y = [8, 7, 6, 6, 8, 7, 6, 5, 4, 8, 7, 6, 5, 4, 8, 8, 4, 4, 8, 7, 6, 5, 4, 8, 7, 6, 6, 8, 7, 6, 5, 4]
            ax.set_xlabel(":", color='#1f77b4')
            ax.set_ylabel(":", color='#1f77b4')
            plt.xticks(rotation=45, color='#1f77b4')
            plt.yticks(color='#1f77b4')
            ax.plot(x, y, marker='o',
                    markersize=29, color='r', dashes=[0, 1, 1])
            # plt.grid()
            # time.sleep(time.process_time() - start)
            chart.update()

        df = pd.DataFrame(str_json)


        df['published_at'] = df['published_at'].str[:10]

        # chart pics
        pics = pd.DataFrame(df.groupby(['published_at']).size().reset_index(name='count'))
        pics_x = pics['published_at']
        pics_y = pics['count']
        pics.to_csv('pics.csv', sep=',', index=False, encoding='utf-8')
        # chart income
        df['published_at_week'] = pd.to_datetime(df['published_at'], dayfirst=False).dt.isocalendar().week
        df_from = df[['salary_from', 'salary_currency', 'salary_gross', 'published_at_week']]
        df_to = df[['salary_to', 'salary_currency', 'salary_gross', 'published_at_week']]
        df_from = df_from.rename(columns={'salary_from': 'salary'})
        df_to = df_from.rename(columns={'salary_to': 'salary'})
        df_app = df_from._append(df_to)
        df_app['income_net'] = np.where(df_app.salary_gross == True, df_app.salary/1.13/1000, df_app.salary/1000)
        df_app = df_app[(df_app['salary_currency'] == 'RUR') & (df_app['salary'] > 0)]
        income = df_app.groupby('published_at_week').agg({"income_net": [np.median, np.size]}).reset_index()
        income.to_csv('income.csv', sep=',', index=False, encoding='utf-8')
        #chart

        plt.cla()
        plt.title(f'HH.ru query,:{user_data.value}', color='#1f77b4')
        ax.set_xlabel("period:", color='#1f77b4')
        ax.set_ylabel("measure:pics", color='#1f77b4')
        plt.xticks(rotation=45, color='#1f77b4')
        plt.yticks(color='#1f77b4')
        ax.bar(pics_x, pics_y)
        plt.grid()
        time.sleep(time.process_time() - start)
        chart.update()

    def toggle_data(e):
        if s.toggle:
            income = pd.read_csv('income.csv')
            plt.cla()
            plt.title(f'HH.ru query, income RUR net: {user_data.value}', color='#1f77b4')
            ax.set_xlabel("period week:", color='#1f77b4')
            ax.set_ylabel("income, RUR net:", color='#1f77b4')
            plt.xticks(list(array(income.iloc[range(1, len(income.index.get_level_values(0))), [0]].values.tolist()).flat), rotation=45, color='#1f77b4')
            plt.yticks(color='#1f77b4')
            xs = list(map(float, list(array(income.iloc[range(1, len(income.index.get_level_values(0))), [1]].values.tolist()).flat)))
            ax.plot(list(array(income.iloc[range(1, income.shape[0]), [0]].values.tolist()).flat), xs,  marker='o', markersize=15, color='r', dashes=[0, 1, 1])
            plt.grid()
            # time.sleep(time.process_time() - start)
            chart.update()
        else:
            pics = pd.read_csv('pics.csv')
            plt.cla()
            ax.set_xlabel("period:", color='#1f77b4')
            ax.set_ylabel("measure:pics", color='#1f77b4')
            plt.xticks(rotation=45, color='#1f77b4')
            plt.yticks(color='#1f77b4')
            ax.bar(pics.iloc[[], [0]], pics.iloc[[], [1]])
            plt.grid()
            # time.sleep(time.process_time() - start)
            chart.update()

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    page.add(
        ft.Row(
            [ft.IconButton(ft.icons.SUNNY, on_click=change_theme)],
            # alignment = ft.MainAxisAlignment.CENTER
        ),
        ft.Row([user_data], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.ElevatedButton(text='Get vacancies', on_click=get_info)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.IconButton(ft.icons.CURRENCY_YEN_ROUNDED, on_click=toggle_data), chart])


    )




ft.app(target=main)