# -*- coding: utf-8 -*-
"""ПАЭД_ЛР_1_ФБИ22_ТимофеевГА.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10JZJI4I9rcroqFLaalehfXaFBbPnvLSm
"""

pip install apimoex

import yfinance as yf
import apimoex
import pandas as pd
import requests

"""Задание 1."""

### Использование yfinance

# Список тикеров акций
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Период выгрузки данных
start_date = '2023-01-01'
end_date = '2024-01-01'

# Выгрузка данных
data_yf = {}
for ticker in tickers:
    data_yf[ticker] = yf.download(ticker, start=start_date, end=end_date, interval='1mo')

# Пример вывода данных для всех акций
for ticker in tickers:
    print(f"Данные для {ticker}:")
    print(data_yf[ticker].head())
    print("\n")

from apimoex import get_board_history
### Использование apimoex
# Список тикеров акций
tickers_moex = ['GAZP', 'SBER', 'LKOH', 'YNDX', 'MGNT']

# Период выгрузки данных
start_date = '2023-01-01'
end_date = '2024-01-01'

# Выгрузка данных
data_moex = {}
with requests.Session() as session:
    for ticker in tickers_moex:
        data = apimoex.get_board_candles(session, ticker, 24, start_date, end_date, ('begin', 'open', 'high', 'low', 'close', 'value'))
        data_moex[ticker] = pd.DataFrame(data)

# Пример вывода данных для всех акций
for ticker in tickers_moex:
    print(f"Данные для {ticker}:")
    print(data_moex[ticker].head())
    print("\n")

"""Задание 2."""

import plotly.graph_objects as go

## Построение графиков с объемом торгов в дневной разбивке

# для акций с yfinance

for ticker in tickers:
    df = data_yf[ticker]
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close']),
                          go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='blue', yaxis='y2')])
    fig.update_layout(title=f'{ticker} Daily Candlestick Chart with Volume', xaxis_title='Date', yaxis_title='Price',
                      yaxis2=dict(title='Volume', overlaying='y', side='right', showgrid=False))
    fig.show()

# для тикеров с moex
for ticker in tickers_moex:
    df = data_moex[ticker]
    df['begin'] = pd.to_datetime(df['begin'])
    df.set_index('begin', inplace=True)
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close']),
                          go.Bar(x=df.index, y=df['value'], name='Volume', marker_color='blue', yaxis='y2')])
    fig.update_layout(title=f'{ticker} Daily Candlestick Chart with Volume', xaxis_title='Date', yaxis_title='Price',
                      yaxis2=dict(title='Volume', overlaying='y', side='right', showgrid=False))
    fig.show()

# для moex
for ticker in tickers_moex:
    df = data_moex[ticker].resample('W').agg({'open': 'first',
                                              'high': 'max',
                                              'low': 'min',
                                              'close': 'last',
                                              'value': 'sum'})
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close']),
                          go.Bar(x=df.index, y=df['value'], name='Volume', marker_color='blue', yaxis='y2')])
    fig.update_layout(title=f'{ticker} Weekly Candlestick Chart with Volume', xaxis_title='Date', yaxis_title='Price',
                      yaxis2=dict(title='Volume', overlaying='y', side='right', showgrid=False))
    fig.show()

## Построение графиков с объемом торгов в месячной разбивке

# для yfinance

for ticker in tickers:
    df = data_yf[ticker].resample('M').agg({'Open': 'first',
                                            'High': 'max',
                                            'Low': 'min',
                                            'Close': 'last',
                                            'Volume': 'sum'})
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close']),
                          go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='blue', yaxis='y2')])
    fig.update_layout(title=f'{ticker} Monthly Candlestick Chart with Volume', xaxis_title='Date', yaxis_title='Price',
                      yaxis2=dict(title='Volume', overlaying='y', side='right', showgrid=False))
    fig.show()

# для moex
for ticker in tickers_moex:
    df = data_moex[ticker].resample('M').agg({'open': 'first',
                                              'high': 'max',
                                              'low': 'min',
                                              'close': 'last',
                                              'value': 'sum'})
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close']),
                          go.Bar(x=df.index, y=df['value'], name='Volume', marker_color='blue', yaxis='y2')])
    fig.update_layout(title=f'{ticker} Monthly Candlestick Chart with Volume', xaxis_title='Date', yaxis_title='Price',
                      yaxis2=dict(title='Volume', overlaying='y', side='right', showgrid=False))
    fig.show()

"""Задание 3."""

## 3.1
# Выбор акции для расчета доходностей
ticker = 'AAPL'
df = data_yf[ticker]

import numpy as np

# Расчет относительных доходностей
df['Relative Return'] = df['Close'].pct_change()

# Расчет логарифмических доходностей
df['Log Return'] = np.log(df['Close'] / df['Close'].shift(1))

# Вывод первых 5 строк с рассчитанными доходностями
print(df[['Close', 'Relative Return', 'Log Return']].head())

# Построение графиков доходностей
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Relative Return'], mode='lines', name='Relative Return'))
fig.add_trace(go.Scatter(x=df.index, y=df['Log Return'], mode='lines', name='Log Return'))
fig.update_layout(title=f'{ticker} Daily Returns', xaxis_title='Date', yaxis_title='Return')
fig.show()

## 3.2
# Фильтрация данных за год
df_year = df[df.index.year == 2023]

# Рассчет C-среднего (среднего значения) для относительной и логарифмической доходности
c_mean_relative = df_year['Relative Return'].mean()
c_mean_log = df_year['Log Return'].mean()

# C-среднее для относительной доходности
c_mean_relative

# C-среднее для логарифмической доходности
c_mean_log

# Рассчет B-вариации (дисперсии) для относительной и логарифмической доходности
b_variance_relative = df_year['Relative Return'].var()
b_variance_log = df_year['Log Return'].var()

# B-вариация для относительной доходности
b_variance_relative

# B-вариация для логарифмической доходности
b_variance_log

## 3.3
# Рассчет месячных стандартных отклонений доходности
monthly_variances_relative = df['Relative Return'].resample('ME')
monthly_variances_log = df['Log Return'].resample('ME')

# Рассчет средне месячного стандартного отклонения доходности
average_monthly_variance_relative = monthly_variances_relative.std().mean()
average_monthly_variance_log = monthly_variances_log.std().mean()

average_monthly_variance_relative

# Рассчет годового стандартного отклонения доходности
annual_variance_relative = df['Relative Return'].resample('YE').std().iloc[0]
annual_variance_log = df['Log Return'].resample('YE').std().iloc[0]

# сравнение вариаций за месяц (в среднем) и год
print(monthly_variances_relative.var().mean())
print(df['Relative Return'].resample('YE').var().iloc[0])

# Проверка правила корень Т
expected_annual_variance_relative = np.sqrt(12) * average_monthly_variance_relative
expected_annual_variance_log = np.sqrt(12) * average_monthly_variance_log

# Допустимая погрешность (например, 5%)
tolerance = 0.05

# Условие сравнения для относительной доходности
if abs(annual_variance_relative - (expected_annual_variance_relative)/np.sqrt(12)) / expected_annual_variance_relative <= tolerance:
    print(f"Правило корень Т для относительной доходности выполняется.")
else:
    print(f"Правило корень Т для относительной доходности НЕ выполняется.")

print(f"Ожидаемая годовая вариация для относительной доходности (по правилу корень Т): {(expected_annual_variance_relative)/np.sqrt(12)}")
print(f"Годовая вариация для относительной доходности: {annual_variance_relative}")

# Условие сравнения для логарифмической доходности
if abs(annual_variance_log - (expected_annual_variance_log)/np.sqrt(12)) / expected_annual_variance_log <= tolerance:
    print(f"Правило корень Т для логарифмической доходности выполняется.")
else:
    print(f"Правило корень Т для логарифмической доходности НЕ выполняется.")

print(f"Ожидаемая годовая вариация для логарифмической доходности (по правилу корень Т): {(expected_annual_variance_log)/np.sqrt(12)}")
print(f"Годовая вариация для логарифмической доходности: {annual_variance_log}")

"""Задание 4."""

## 4.2
# Список тикеров акций для портфеля
portfolio_tickers = ['TASB', 'TATN']

# Период выгрузки данных
portfolio_start_date = '2023-01-01'
portfolio_end_date = '2024-01-01'

# Выгрузка данных для портфеля
portfolio_data = {}
with requests.Session() as session:
    for ticker in portfolio_tickers:
        data = apimoex.get_board_candles(session, ticker, 24, portfolio_start_date, portfolio_end_date, ('begin', 'open', 'high', 'low', 'close', 'value'))
        portfolio_data[ticker] = pd.DataFrame(data)

# Пример вывода данных для всех акций в портфеле
for ticker in portfolio_tickers:
    print(f"Данные для {ticker}:")
    print(portfolio_data[ticker].head())
    print("\n")

# Преобразование данных в единый DataFrame для портфеля
portfolio_df = pd.DataFrame(index=pd.to_datetime(portfolio_data['TASB']['begin']))

# Количество акций в портфеле
num_shares = {
    'TASB': 22,
    'TATN': 9
}

# Рассчет стоимости портфеля на каждый день

for ticker in portfolio_tickers:
    portfolio_data[ticker]['begin'] = pd.to_datetime(portfolio_data[ticker]['begin'])
    portfolio_data[ticker].set_index('begin', inplace=True)
    portfolio_data[ticker] *= num_shares[ticker]

portfolio_df['Portfolio Value'] = portfolio_data['TASB']['close'] + portfolio_data['TATN']['close']

fig = go.Figure()

# Добавление стоимости портфеля
fig.add_trace(go.Scatter(
    x=portfolio_df.index,
    y=(portfolio_data['TASB']['close'] * num_shares['TASB']) + (portfolio_data['TATN']['close'] * num_shares['TATN']),
    mode='lines',
    name='Portfolio Value',
    line=dict(color='blue', width=2)
))

# Добавление стоимости акций TASB
fig.add_trace(go.Scatter(
    x=portfolio_df.index,
    y=portfolio_data['TASB']['close'] * num_shares['TASB'],
    mode='lines',
    name='TASB Value',
    line=dict(color='green', width=2, dash='dash')
))

# Добавление стоимости акций TATN
fig.add_trace(go.Scatter(
    x=portfolio_df.index,
    y=portfolio_data['TATN']['close'] * num_shares['TATN'],
    mode='lines',
    name='TATN Value',
    line=dict(color='red', width=2, dash='dot')
))

# Обновление макета графика
fig.update_layout(
    title='Portfolio Value Over Time',
    xaxis_title='Date',
    yaxis_title='Portfolio Value',
    width=1000,  # ширина графика
    height=600,  # высота графика
    template='plotly_white',  # фон графика
    legend=dict(
        x=0.02,
        y=0.98,
        bgcolor='rgba(255, 255, 255, 0.5)',
        bordercolor='Black',
        borderwidth=1
    ),
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True)
)

fig.show()

# Агрегирование данных для портфеля
portfolio_df['open'] = sum([portfolio_data[ticker]['open'] for ticker in portfolio_tickers])
portfolio_df['high'] = sum([portfolio_data[ticker]['high'] for ticker in portfolio_tickers])
portfolio_df['low'] = sum([portfolio_data[ticker]['low'] for ticker in portfolio_tickers])
portfolio_df['close'] = sum([portfolio_data[ticker]['close'] for ticker in portfolio_tickers])

# Построение свечного графика для портфеля
fig = go.Figure(data=[go.Candlestick(x=portfolio_df.index,
                                     open=portfolio_df['open'],
                                     high=portfolio_df['high'],
                                     low=portfolio_df['low'],
                                     close=portfolio_df['close'])])
fig.update_layout(title='Candlestick Chart for Portfolio', xaxis_title='Date', yaxis_title='Price')
fig.show()

# 4.3
# Определение цены закрытия на ближайшую доступную дату
start_date = pd.to_datetime(portfolio_start_date)

# Выбор ближайшей доступной даты, если начальная дата является выходным днем
tasb_close_start_date = portfolio_data['TASB'].index[portfolio_data['TASB'].index >= start_date][0]
tatn_close_start_date = portfolio_data['TATN'].index[portfolio_data['TATN'].index >= start_date][0]

tasb_close_start = portfolio_data['TASB'].loc[tasb_close_start_date, 'close']
tatn_close_start = portfolio_data['TATN'].loc[tatn_close_start_date, 'close']

# Рассчет количества акций, чтобы стоимость была равна на начальную дату
initial_investment = 10000  # Например, 10000 рублей
num_shares_tasb = int(initial_investment / tasb_close_start)
num_shares_tatn = int(initial_investment / tatn_close_start)

print(f"Количество акций TASB: {num_shares_tasb}")
print(f"Количество акций TATN: {num_shares_tatn}")

# Преобразование данных в единый DataFrame для портфеля
portfolio_df = pd.DataFrame(index=pd.to_datetime(portfolio_data['TASB'].index))

# Рассчет стоимости портфеля на каждый день
portfolio_df['TASB_close'] = portfolio_data['TASB']['close'] * num_shares_tasb
portfolio_df['TATN_close'] = portfolio_data['TATN']['close'] * num_shares_tatn
portfolio_df['Portfolio_Value'] = portfolio_df['TASB_close'] + portfolio_df['TATN_close']

fig = go.Figure()

# Добавление стоимости портфеля
fig.add_trace(go.Scatter(
    x=portfolio_df.index,
    y=(portfolio_data['TASB']['close'] * num_shares_tasb) + (portfolio_data['TATN']['close'] * num_shares_tatn),
    mode='lines',
    name='Portfolio Value',
    line=dict(color='blue', width=2)
))

# Добавление стоимости акций TASB
fig.add_trace(go.Scatter(
    x=portfolio_df.index,
    y=portfolio_data['TASB']['close'] * num_shares_tasb,
    mode='lines',
    name='TASB Value',
    line=dict(color='green', width=2, dash='dash')
))

# Добавление стоимости акций TATN
fig.add_trace(go.Scatter(
    x=portfolio_df.index,
    y=portfolio_data['TATN']['close'] * num_shares_tatn,
    mode='lines',
    name='TATN Value',
    line=dict(color='red', width=2, dash='dot')
))

# Обновление макета графика
fig.update_layout(
    title='Portfolio Value Over Time',
    xaxis_title='Date',
    yaxis_title='Portfolio Value',
    width=1000,  # ширина графика
    height=600,  # высота графика
    template='plotly_white',  # фон графика
    legend=dict(
        x=0.02,
        y=0.98,
        bgcolor='rgba(255, 255, 255, 0.5)',
        bordercolor='Black',
        borderwidth=1
    ),
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True)
)

fig.show()

# Агрегирование данных для портфеля
portfolio_df['open'] = portfolio_data['TASB']['open'] * num_shares_tasb + portfolio_data['TATN']['open'] * num_shares_tatn
portfolio_df['high'] = portfolio_data['TASB']['high'] * num_shares_tasb + portfolio_data['TATN']['high'] * num_shares_tatn
portfolio_df['low'] = portfolio_data['TASB']['low'] * num_shares_tasb + portfolio_data['TATN']['low'] * num_shares_tatn
portfolio_df['close'] = portfolio_data['TASB']['close'] * num_shares_tasb + portfolio_data['TATN']['close'] * num_shares_tatn

# Построение свечного графика для портфеля
fig = go.Figure(data=[go.Candlestick(x=portfolio_df.index,
                                     open=portfolio_df['open'],
                                     high=portfolio_df['high'],
                                     low=portfolio_df['low'],
                                     close=portfolio_df['close'])])
fig.update_layout(title='Candlestick Chart for Portfolio', xaxis_title='Date', yaxis_title='Price')
fig.show()

# 4.4

# Ребалансировка портфеля через полгода
# rebalance_date = start_date + pd.DateOffset(months=6)
# rebalance_date = portfolio_data['TASB'].index[portfolio_data['TASB'].index >= rebalance_date][0]

# Вычисление разницы между стоимостью акций на каждый день
portfolio_df['Price_Difference'] = abs((portfolio_data['TASB']['close'].values) * num_shares_tasb - (portfolio_data['TATN']['close'].values) * num_shares_tatn)

# Поиск даты с максимальной разницей
rebalance_date = portfolio_df['Price_Difference'].idxmax()

# Определение цены закрытия на дату ребалансировки
tasb_close_rebalance = portfolio_data['TASB'].loc[rebalance_date, 'close']
tatn_close_rebalance = portfolio_data['TATN'].loc[rebalance_date, 'close']

print(f"Дата ребалансировки: {rebalance_date}")
print(f"Цена закрытия TASB на дату ребалансировки: {tasb_close_rebalance * num_shares_tasb}")
print(f"Цена закрытия TATN на дату ребалансировки: {tatn_close_rebalance * num_shares_tatn}")

# Рассчет стоимости портфеля на дату ребалансировки
portfolio_value_rebalance = portfolio_df.loc[rebalance_date, 'Portfolio_Value']

# Пересчет количества акций на дату ребалансировки, чтобы стоимость каждой акции была равна половине стоимости портфеля
half_portfolio_value = portfolio_value_rebalance / 2
num_shares_tasb_rebalance = int(half_portfolio_value / tasb_close_rebalance)
num_shares_tatn_rebalance = int(half_portfolio_value / tatn_close_rebalance)

print(f"Количество акций TASB после ребалансировки: {num_shares_tasb_rebalance}")
print(f"Количество акций TATN после ребалансировки: {num_shares_tatn_rebalance}")

# Рассчет стоимости портфеля на каждый день после ребалансировки
portfolio_df_rebalance = pd.DataFrame(index=pd.to_datetime(portfolio_data['TASB'].index))
portfolio_df_rebalance['TASB_close'] = portfolio_data['TASB']['close'] * num_shares_tasb_rebalance
portfolio_df_rebalance['TATN_close'] = portfolio_data['TATN']['close'] * num_shares_tatn_rebalance
portfolio_df_rebalance['Portfolio_Value'] = portfolio_df_rebalance['TASB_close'] + portfolio_df_rebalance['TATN_close']

# Объединение данных до и после ребалансировки
combined_df = pd.concat([portfolio_df[portfolio_df.index < rebalance_date], portfolio_df_rebalance[portfolio_df_rebalance.index >= rebalance_date]])

# Построение графика стоимости портфеля до и после ребалансировки
fig = go.Figure()
fig.add_trace(go.Scatter(x=combined_df.index, y=combined_df['Portfolio_Value'], mode='lines', name='Portfolio Value'))
fig.add_shape(type="line",
              x0=rebalance_date, y0=min(combined_df['Portfolio_Value']),
              x1=rebalance_date, y1=max(combined_df['Portfolio_Value']),
              line=dict(color="red", width=2))
fig.update_layout(title='Portfolio Value Over Time (Before and After Rebalancing)', xaxis_title='Date', yaxis_title='Portfolio Value')
fig.show()

# Рассчитываем относительную доходность до и после ребалансировки
# Получаем процентное изменение для всего периода
relative_return_before_rebalance = portfolio_df['Portfolio_Value'].pct_change().fillna(0).sum() * 100
relative_return_after_rebalance = combined_df['Portfolio_Value'].pct_change().fillna(0).sum() * 100

# Рассчитываем логарифмическую доходность
# Используем pct_change для логарифмической доходности
log_return_before_rebalance = np.log(portfolio_df['Portfolio_Value'].pct_change().fillna(0) + 1).sum() * 100
log_return_after_rebalance = np.log(combined_df['Portfolio_Value'].pct_change().fillna(0) + 1).sum() * 100

# Выводим результаты
print(f"Относительная доходность до ребалансировки: {relative_return_before_rebalance:.2f}%")
print(f"Относительная доходность после ребалансировки: {relative_return_after_rebalance:.2f}%")
print(f"Логарифмическая доходность до ребалансировки: {log_return_before_rebalance:.2f}%")
print(f"Логарифмическая доходность после ребалансировки: {log_return_after_rebalance:.2f}%")