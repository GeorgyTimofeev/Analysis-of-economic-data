# -*- coding: utf-8 -*-
"""ПАЭД_ЛР_2_ФБИ22_ТимофеевГА.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KEdJbapVZurt1Ka2gXxH3r5Paalc_ztr
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import yfinance as yf

"""# Задание 1"""

# Загрузка данных по акции T-Mobile (TMUS)
ticker = "TMUS"

start_date = '2020-09-22'
end_date = '2021-09-22'

data_TMUS = yf.download(ticker, start=start_date, end=end_date)

print(data_TMUS.head())

# Относительная и логорифмическая доходности

data_TMUS['Relative Return'] = data_TMUS['Adj Close'].pct_change()

data_TMUS['Log Return'] = np.log(data_TMUS['Adj Close'] / data_TMUS['Adj Close'].shift(1))

print(data_TMUS[['Adj Close', 'Relative Return', 'Log Return']].head())

# Рассчет C-среднего (среднего значения) для относительной и логарифмической доходности
c_mean_relative = data_TMUS['Relative Return'].mean()
c_mean_log = data_TMUS['Log Return'].mean()

# Рассчет B-вариации (дисперсии) для относительной и логарифмической доходности
b_variance_relative = data_TMUS['Relative Return'].var()
b_variance_log = data_TMUS['Log Return'].var()

print(f"C-среднее для относительной доходности: {c_mean_relative:.6f}")
print(f"C-среднее для логарифмической доходности: {c_mean_log:.6f}")
print(f"B-вариация для относительной доходности: {b_variance_relative:.6f}")
print(f"B-вариация для логарифмической доходности: {b_variance_log:.6f}")

# Количество рабочих дней за 6 месяцев
days_6_months = 125

# Прогнозируемая логарифмическая доходность за 6 месяцев
forecast_log_return_6_months = c_mean_log * days_6_months

# Прогнозируемая цена фьючерса
initial_price = data_TMUS['Adj Close'].iloc[0]
initial_price_value = initial_price.item()  # Преобразование Series в скалярное значение
forecast_price = initial_price_value * np.exp(forecast_log_return_6_months)

print(f"Цена на 22.09.2020: {initial_price_value:.2f}")
print(f"Прогнозируемая цена через 6 месяцев: {forecast_price:.2f}")

# Рассчет стандартного отклонения логарифмической доходности
std_log_return = data_TMUS['Log Return'].std()

# Количество рабочих дней за 6 месяцев (примерно 125 дней)
days_6_months = 125

# Масштабирование стандартного отклонения на 6 месяцев
std_log_return_6_months = std_log_return * np.sqrt(days_6_months)

# Начальная цена актива
initial_price = data_TMUS['Adj Close'].iloc[0]
initial_price_value = initial_price.item()  # Преобразование Series в скалярное значение

# Рассчет VaR и гарантийного обеспечения для 1, 2 и 3 сигм на 6 месяцев
sigmas = [1, 2, 3]
for sigma in sigmas:
    VaR = std_log_return_6_months * sigma
    margin_requirement = initial_price_value * VaR
    print(f"Для {sigma} сигмы (6 месяцев):")
    print(f"Value at Risk (VaR): {VaR:.6f}")
    print(f"Гарантийное обеспечение: {margin_requirement:.2f}\n")

# Пороговые значения для 1, 2 и 3 сигм на дневной основе
thresholds = {
    '1_sigma': std_log_return,
    '2_sigma': 2 * std_log_return,
    '3_sigma': 3 * std_log_return
}

# Подсчет количества случаев выхода доходности за пределы пороговых значений
exceedances = {key: 0 for key in thresholds}
exceedance_dates = {key: [] for key in thresholds}

for key, threshold in thresholds.items():
    exceedances[key] = np.sum(np.abs(data_TMUS['Log Return'].dropna()) > threshold)
    exceedance_dates[key] = data_TMUS[np.abs(data_TMUS['Log Return']) > threshold].index

# Вывод результатов
for key, count in exceedances.items():
    print(f"Количество случаев выхода доходности за пределы {key}: {count}")

# Построение графика изменения цены акции
plt.figure(figsize=(14, 7))
plt.plot(data_TMUS['Adj Close'], label='Цена акции (Adj Close)', color='blue')

# Отметка случаев выхода доходности за пределы пороговых значений
colors = {'1_sigma': 'orange', '2_sigma': 'red', '3_sigma': 'purple'}
for key, dates in exceedance_dates.items():
    plt.scatter(dates, data_TMUS.loc[dates, 'Adj Close'], color=colors[key], label=f'Выход за пределы {key}', marker='x')

plt.title('Изменение цены акции T-Mobile (TMUS) и случаи выхода доходности за пределы пороговых значений')
plt.xlabel('Дата')
plt.ylabel('Цена акции (Adj Close)')
plt.legend()
plt.grid(True)
plt.show()

# Дневная ставка дисконтирования (10% годовых)
daily_discount_rate = 0.10 / 250

# Применение дисконтирования к прогнозируемой цене актива
discount_factor = np.exp(-daily_discount_rate * days_6_months)
discounted_initial_price = initial_price_value * discount_factor

# Рассчет VaR и гарантийного обеспечения для 1, 2 и 3 сигм на 6 месяцев с учетом дисконтирования
sigmas = [1, 2, 3]
for sigma in sigmas:
    VaR = std_log_return_6_months * sigma
    margin_requirement = discounted_initial_price * VaR
    print(f"Для {sigma} сигмы (6 месяцев) с учетом дисконтирования:")
    print(f"Value at Risk (VaR): {VaR:.6f}")
    print(f"Гарантийное обеспечение: {margin_requirement:.2f}\n")

"""# Задание 2"""

# Рассчет средней цены акции
average_price = data_TMUS['Adj Close'].mean()
average_price_value = average_price.item()

# Определение цены исполнения (страйк)
strike_price = average_price * 1.02
strike_price_value = strike_price.item()  # Преобразование Series в скалярное значение

# Количество симуляций
num_simulations = 10000

# Количество рабочих дней за 6 месяцев (примерно 125 дней)
days_6_months = 125

# Рассчет стандартного отклонения логарифмической доходности
std_log_return = data_TMUS['Log Return'].std()

# Начальная цена актива
initial_price = data_TMUS['Adj Close'].iloc[-1]
initial_price_value = initial_price.item()  # Преобразование Series в скалярное значение

# Проведение симуляций методом Монте-Карло
simulated_prices = np.zeros(num_simulations)
for i in range(num_simulations):
    # Генерация случайных доходностей
    random_returns = np.random.normal(0, std_log_return, days_6_months)
    # Симуляция цены акции на дату истечения опциона
    simulated_price = initial_price_value * np.exp(np.sum(random_returns))
    simulated_prices[i] = simulated_price

# Рассчет выплат по опциону
payoffs = np.maximum(simulated_prices - strike_price_value, 0)

# Оценка стоимости опциона (ставка дисконтирования 0%)
option_price = np.mean(payoffs)

# Вывод дополнительной информации
print(f"Средняя цена акции: {average_price_value:.2f}")
print(f"Цена исполнения (страйк): {strike_price_value:.2f}")
print(f"Оценка стоимости опциона CALL: {option_price:.2f}")
print(f"Средняя симулированная цена акции: {np.mean(simulated_prices):.2f}")
print(f"Медианная симулированная цена акции: {np.median(simulated_prices):.2f}")
print(f"Средняя выплата по опциону: {np.mean(payoffs):.2f}")
print(f"Медианная выплата по опциону: {np.median(payoffs):.2f}")

# Построение гистограммы распределения выплат по опциону
plt.figure(figsize=(14, 7))
counts, bins, patches = plt.hist(payoffs, bins=50, color='blue', edgecolor='black')

# Добавление подписей к столбцам
bin_centers = 0.5 * (bins[:-1] + bins[1:])
for count, x in zip(counts, bin_centers):
    plt.text(x, count, f'{x:.2f}', ha='center', va='bottom')

plt.title('Распределение выплат по опциону CALL на акцию T-Mobile (TMUS)')
plt.xlabel('Цена опциона')
plt.ylabel('Частота')
plt.grid(True)
plt.show()

from scipy.stats import norm

T = days_6_months / 250

# Рассчет стоимости опциона Call по модели Блэка-Шоулза
S0 = initial_price_value
K = strike_price_value
r = 0  # Безрисковая ставка
sigma = std_log_return
d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)
option_price_bs = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Вывод результатов
print(f"Средняя цена акции: {average_price_value:.2f}")
print(f"Цена исполнения (страйк): {strike_price_value:.2f}")
print(f"Оценка стоимости опциона CALL методом Монте-Карло: {option_price:.2f}")
print(f"Оценка стоимости опциона CALL по модели Блэка-Шоулза: {option_price_bs:.6f}")

"""# Задание 3"""

# Определение тикеров акций и рыночного индекса
tickers_capm = ["T", "TSLA", "TXN", "TMUS"]
market_index = "^GSPC"

# Период для выгрузки данных
start_date_capm = '2020-09-22'
end_date_capm = '2021-09-22'

# Загрузка данных по акциям и рыночному индексу
data_capm = yf.download(tickers_capm + [market_index], start=start_date_capm, end=end_date_capm)

# Вывод первых строк данных для проверки
print(data_capm.head())

# Рассчет дневных доходностей
returns_capm = data_capm['Adj Close'].pct_change().dropna()

# Рассчет средней дневной доходности (R-среднее) для каждого инструмента и рыночного индекса
mean_returns = returns_capm.mean()

# Рассчет бета-коэффициента для каждого инструмента относительно рыночного индекса
market_returns = returns_capm[market_index]
betas = {}
for ticker in tickers_capm:
    cov_matrix = np.cov(returns_capm[ticker], market_returns)
    beta = cov_matrix[0, 1] / cov_matrix[1, 1]
    betas[ticker] = beta

# Безрисковая ставка (например, 5% годовых)
Rfree = 0.05 / 250  # Преобразование в дневную ставку

# Рассчет ожидаемой доходности (Rs) для каждого инструмента с использованием формулы CAPM
Rm = mean_returns[market_index]
expected_returns = {}
for ticker in tickers_capm:
    Rs = Rfree + betas[ticker] * (Rm - Rfree)
    expected_returns[ticker] = Rs

# Вывод результатов
print("Средняя дневная доходность (R-среднее) для каждого инструмента:")
print(mean_returns)
print("\nБета-коэффициенты для каждого инструмента:")
print(betas)
print("\nОжидаемая доходность (Rs) для каждого инструмента по модели CAPM:")
print(expected_returns)

"""# Задание 4"""

# Определение тикеров акций
tickers_markowitz = ["T", "TSLA", "TXN", "TMUS"]

# Период для выгрузки данных
start_date_markowitz = '2020-09-22'
end_date_markowitz = '2021-09-22'

# Загрузка данных по акциям
data_markowitz = yf.download(tickers_markowitz, start=start_date_markowitz, end=end_date_markowitz)

# Рассчет логарифмических доходностей
log_returns_markowitz = np.log(data_markowitz['Adj Close'] / data_markowitz['Adj Close'].shift(1)).dropna()

# Рассчет средней логарифмической доходности (C-среднее) для каждого инструмента
mean_log_returns_markowitz = log_returns_markowitz.mean()

# Рассчет дисперсии логарифмических доходностей (B-вариация) для каждого инструмента
variance_log_returns_markowitz = log_returns_markowitz.var()

# Вывод результатов
print("\nСредняя логарифмическая доходность (C-среднее) для каждого инструмента:")
print(mean_log_returns_markowitz)
print("\nДисперсия логарифмических доходностей (B-вариация) для каждого инструмента:")
print(variance_log_returns_markowitz)

# Выбор двух инструментов с минимальной и максимальной доходностью и вариацией
min_return_ticker = mean_log_returns_markowitz.idxmin()
max_return_ticker = mean_log_returns_markowitz.idxmax()

# Перебор долей с шагом 0.1
weights = np.arange(0, 1.1, 0.1)
portfolio_returns = []
portfolio_variances = []

for w in weights:
    portfolio_return = w * mean_log_returns_markowitz[min_return_ticker] + (1 - w) * mean_log_returns_markowitz[max_return_ticker]
    portfolio_variance = (w**2 * variance_log_returns_markowitz[min_return_ticker] +
                          (1 - w)**2 * variance_log_returns_markowitz[max_return_ticker] +
                          2 * w * (1 - w) * log_returns_markowitz[min_return_ticker].cov(log_returns_markowitz[max_return_ticker]))
    portfolio_returns.append(portfolio_return)
    portfolio_variances.append(portfolio_variance)

# Вывод результатов
print(f"\nИнструмент с минимальной доходностью: {min_return_ticker}")
print(f"Инструмент с максимальной доходностью: {max_return_ticker}")

# Построение "пули"
plt.figure(figsize=(10, 6))
plt.plot(np.sqrt(portfolio_variances), portfolio_returns, 'o-', markersize=8, label='Эффективный фронт')
plt.xlabel('Стандартное отклонение (риск)')
plt.ylabel('Ожидаемая доходность')
plt.title('Эффективный фронт (пуля)')
plt.legend()
plt.grid(True)
plt.show()

# Рассчет корреляции доходностей между выбранными инструментами
correlation = log_returns_markowitz[min_return_ticker].corr(log_returns_markowitz[max_return_ticker])

# Нахождение долей, при которых портфель имеет минимальный риск
min_risk_index = np.argmin(portfolio_variances)
min_risk_weight = weights[min_risk_index]
min_risk_return = portfolio_returns[min_risk_index]
min_risk_variance = portfolio_variances[min_risk_index]

print(f"\nКорреляция доходностей между {min_return_ticker} и {max_return_ticker}: {correlation:.4f}")
print(f"\nМинимальный риск портфеля достигается при доле {min_return_ticker}: {min_risk_weight:.2f}")
print(f"Ожидаемая доходность портфеля с минимальным риском: {min_risk_return:.4f}")
print(f"Дисперсия портфеля с минимальным риском: {min_risk_variance:.8f}")
print(f"Стандартное отклонение портфеля с минимальным риском: {np.sqrt(min_risk_variance):.4f}")

from scipy.optimize import minimize

# Рассчет корреляционной матрицы доходностей
correlation_matrix = log_returns_markowitz.corr()

# Функция для расчета доходности портфеля
def portfolio_return(weights, mean_returns):
    return np.sum(weights * mean_returns)

# Функция для расчета риска портфеля (стандартного отклонения)
def portfolio_risk(weights, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

# Функция для расчета коэффициента Шарпа
def sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0):
    port_return = portfolio_return(weights, mean_returns)
    port_risk = portfolio_risk(weights, cov_matrix)
    return (port_return - risk_free_rate) / port_risk

# Функция для минимизации (отрицательный коэффициент Шарпа)
def negative_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0):
    return -sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate)

# Ограничения и начальные значения
num_assets = len(tickers_markowitz)
args = (mean_log_returns_markowitz, log_returns_markowitz.cov())
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bounds = tuple((0, 1) for asset in range(num_assets))
initial_weights = np.array(num_assets * [1. / num_assets])

# Оптимизация портфеля для максимального коэффициента Шарпа
opt_result_sharpe = minimize(negative_sharpe_ratio, initial_weights, args=args, method='SLSQP', bounds=bounds, constraints=constraints)
max_sharpe_weights = opt_result_sharpe.x
max_sharpe_return = portfolio_return(max_sharpe_weights, mean_log_returns_markowitz)
max_sharpe_std = portfolio_risk(max_sharpe_weights, log_returns_markowitz.cov())
max_sharpe_ratio = sharpe_ratio(max_sharpe_weights, mean_log_returns_markowitz, log_returns_markowitz.cov())

# Вывод результатов
print("\nКорреляционная матрица доходностей:")
print(correlation_matrix)
print(f"\nОптимальный портфель для минимального риска:")
print(f"Доли: {min_risk_weights}")
print(f"Ожидаемая доходность: {min_risk_return:.4f}")
print(f"Стандартное отклонение: {min_risk_std:.4f}")
print(f"\nОптимальный портфель для наивысшей доходности:")
print(f"Доли: {max_return_weights}")
print(f"Ожидаемая доходность: {max_return:.4f}")
print(f"Стандартное отклонение: {max_return_std:.4f}")

# Построение "пули"
weights = np.linspace(0, 1, 100)
portfolio_returns = []
portfolio_risks = []

for w in weights:
    combined_weights = w * max_sharpe_weights + (1 - w) * initial_weights
    portfolio_returns.append(portfolio_return(combined_weights, mean_log_returns_markowitz))
    portfolio_risks.append(portfolio_risk(combined_weights, log_returns_markowitz.cov()))

plt.figure(figsize=(10, 6))
plt.plot(portfolio_risks, portfolio_returns, 'o-', markersize=8, label='Эффективный фронт')
plt.scatter(min_risk_std, min_risk_return, color='blue', marker='x', s=100, label='Минимальный риск')
plt.scatter(max_sharpe_std, max_sharpe_return, color='red', marker='x', s=100, label='Макс. коэффициент Шарпа')
plt.xlabel('Стандартное отклонение (риск)')
plt.ylabel('Ожидаемая доходность')
plt.title('Эффективный фронт (пуля)')
plt.legend()
plt.grid(True)
plt.show()

# Функция для минимизации (отрицательная доходность)
def negative_portfolio_return(weights, mean_returns):
    return -portfolio_return(weights, mean_returns)

# Заданный уровень риска (например, 0.01)
target_risk = 0.01

# Ограничения и начальные значения
num_assets = len(tickers_markowitz)
args = (mean_log_returns_markowitz, log_returns_markowitz.cov())
constraints = (
    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Сумма весов должна быть равна 1
    {'type': 'ineq', 'fun': lambda x: target_risk - portfolio_risk(x, log_returns_markowitz.cov())}  # Ограничение на риск
)
bounds = tuple((0, 1) for asset in range(num_assets))
initial_weights = np.array(num_assets * [1. / num_assets])

# Оптимизация портфеля для максимальной доходности при ограничении риска
opt_result_max_return = minimize(negative_portfolio_return, initial_weights, args=(mean_log_returns_markowitz,), method='SLSQP', bounds=bounds, constraints=constraints)
max_return_weights = opt_result_max_return.x
max_return = portfolio_return(max_return_weights, mean_log_returns_markowitz)
max_return_std = portfolio_risk(max_return_weights, log_returns_markowitz.cov())

# Вывод результатов
print(f"\nОптимальный портфель для максимальной доходности при ограничении риска ({target_risk}):")
print(f"Доли: {max_return_weights}")
print(f"Ожидаемая доходность: {max_return:.4f}")
print(f"Стандартное отклонение: {max_return_std:.4f}")

weights = np.linspace(0, 1, 100)
portfolio_returns = []
portfolio_risks = []

for w in weights:
    combined_weights = w * max_sharpe_weights + (1 - w) * initial_weights
    portfolio_returns.append(portfolio_return(combined_weights, mean_log_returns_markowitz))
    portfolio_risks.append(portfolio_risk(combined_weights, log_returns_markowitz.cov()))

plt.figure(figsize=(10, 6))
plt.plot(portfolio_risks, portfolio_returns, 'o-', markersize=8, label='Эффективный фронт')
plt.scatter(min_risk_std, min_risk_return, color='blue', marker='x', s=100, label='Минимальный риск')
plt.scatter(max_sharpe_std, max_sharpe_return, color='red', marker='x', s=100, label='Макс. коэффициент Шарпа')
plt.scatter(max_return_std, max_return, color='green', marker='x', s=100, label='Макс. доходность при ограничении риска')
plt.xlabel('Стандартное отклонение (риск)')
plt.ylabel('Ожидаемая доходность')
plt.title('Эффективный фронт (пуля)')
plt.legend()
plt.grid(True)
plt.show()

# Рассчет ковариационной матрицы логарифмических доходностей
cov_matrix = log_returns_markowitz.cov()

# Функция для генерации случайного портфеля
def randPortf(cnt):
    res = np.exp(np.random.randn(cnt))
    res = res / res.sum()
    return res

# Функция для расчета доходности портфеля
def dohPortf(r, mean_returns):
    return np.matmul(mean_returns.values, r)

# Функция для расчета риска портфеля
def riskPortf(r, cov_matrix):
    return np.sqrt(np.matmul(np.matmul(r, cov_matrix.values), r))

# Количество случайных портфелей
N = 10000
cnt = len(tickers_markowitz)

# Массивы для хранения результатов
risk = np.zeros(N)
doh = np.zeros(N)
portf = np.zeros((N, cnt))

# Генерация случайных портфелей и расчет их характеристик
for n in range(N):
    r = randPortf(cnt)
    portf[n, :] = r
    risk[n] = riskPortf(r, cov_matrix)
    doh[n] = dohPortf(r, mean_log_returns_markowitz)

# Построение графика "пули"
plt.figure(figsize=(10, 8))
plt.scatter(risk * 100, doh * 100, c='y', marker='.')
plt.xlabel('Риск, %')
plt.ylabel('Доходность, %')
plt.title("Облако портфелей")

# Нахождение портфеля с минимальным риском
min_risk = np.argmin(risk)
plt.scatter([risk[min_risk] * 100], [doh[min_risk] * 100], c='r', marker='*', label='Минимальный риск')

# Нахождение портфеля с максимальным коэффициентом Шарпа
max_sharpe_ratio = np.argmax(doh / risk)
plt.scatter([risk[max_sharpe_ratio] * 100], [doh[max_sharpe_ratio] * 100], c='g', marker='o', label='Максимальный коэффициент Шарпа')

# Усредненный портфель
r_mean = np.ones(cnt) / cnt
risk_mean = riskPortf(r_mean, cov_matrix)
doh_mean = dohPortf(r_mean, mean_log_returns_markowitz)
plt.scatter([risk_mean * 100], [doh_mean * 100], c='b', marker='x', label='Усредненный портфель')

plt.legend()
plt.show()

# Вывод данных найденных портфелей
print('---------- Минимальный риск ----------')
print()
print("Риск = %1.2f%%" % (float(risk[min_risk]) * 100.))
print("Доходность = %1.2f%%" % (float(doh[min_risk]) * 100.))
print()
print(pd.DataFrame([portf[min_risk] * 100], columns=tickers_markowitz, index=['Доли, %']).T)
print()

print('---------- Максимальный коэффициент Шарпа ----------')
print()
print("Риск = %1.2f%%" % (float(risk[max_sharpe_ratio]) * 100.))
print("Доходность = %1.2f%%" % (float(doh[max_sharpe_ratio]) * 100.))
print()
print(pd.DataFrame([portf[max_sharpe_ratio] * 100], columns=tickers_markowitz, index=['Доли, %']).T)
print()

print('---------- Средний портфель ----------')
print()
print("Риск = %1.2f%%" % (float(risk_mean) * 100.))
print("Доходность = %1.2f%%" % (float(doh_mean) * 100.))
print()
print(pd.DataFrame([r_mean * 100], columns=tickers_markowitz, index=['Доли, %']).T)
print()

"""# Доп.Раздел"""

from datetime import datetime

# Определение тикера актива и даты
ticker = "TSLA"  # Например, Tesla
start_date = '2023-10-26'  # Начальная дата для расчета исторической волатильности
end_date = '2024-10-26'  # Конечная дата для расчета исторической волатильности
expiration_date = '2025-04-17'  # Дата истечения опциона

# Загрузка данных по акции
data = yf.download(ticker, start=start_date, end=end_date)
S0 = data['Adj Close'].iloc[-1]  # текущая цена актива на конец периода

# Рассчет исторической волатильности
data['Log Returns'] = np.log(data['Adj Close'] / data['Adj Close'].shift(1))
historical_volatility = data['Log Returns'].std() * np.sqrt(252)  # 252 торговых дня в году

# Загрузка данных по опционам
stock = yf.Ticker(ticker)
options = stock.option_chain(expiration_date)

# Получение страйк-цен для колл- и пут-опционов
call_strikes = options.calls['strike']
put_strikes = options.puts['strike']

# Выбор страйк-цены (например, ближайшей к текущей цене актива)
K = call_strikes.iloc[(call_strikes - S0).abs().argsort()[:1]].values[0]

# Параметры опциона
T = (datetime(2025, 4, 17) - datetime(2024, 10, 26)).days / 365  # время до истечения в годах
r = 0.01  # безрисковая процентная ставка (примерная)
sigma = historical_volatility  # волатильность

print("\n")
print(K)
print(sigma)

import scipy.stats as si

# Функция для расчета стоимости опциона по модели Блэка-Шоулза
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        option_price = S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0)
    elif option_type == 'put':
        option_price = K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * si.norm.cdf(-d1, 0.0, 1.0)

    return option_price.item()  # Преобразование в скалярное значение

# Функция для расчета стоимости опциона методом Монте-Карло
def monte_carlo(S, K, T, r, sigma, num_simulations=10000, option_type='call'):
    np.random.seed(0)
    dt = T / num_simulations
    price_paths = np.zeros(num_simulations)
    price_paths[0] = S

    for t in range(1, num_simulations):
        z = np.random.standard_normal()
        price_paths[t] = price_paths[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z)

    if option_type == 'call':
        payoff = np.maximum(price_paths - K, 0)
    elif option_type == 'put':
        payoff = np.maximum(K - price_paths, 0)

    option_price = np.exp(-r * T) * np.mean(payoff)

    return option_price.item()  # Преобразование в скалярное значение

# Расчет стоимости опциона по модели Блэка-Шоулза
bs_call_price = black_scholes(S0, K, T, r, sigma, option_type='call')
bs_put_price = black_scholes(S0, K, T, r, sigma, option_type='put')

# Расчет стоимости опциона методом Монте-Карло
mc_call_price = monte_carlo(S0, K, T, r, sigma, num_simulations=100000, option_type='call')
mc_put_price = monte_carlo(S0, K, T, r, sigma, num_simulations=100000, option_type='put')

# Выгрузка реальных рыночных цен опционов
real_call_price = options.calls[options.calls['strike'] == K]['lastPrice'].values[0]
real_put_price = options.puts[options.puts['strike'] == K]['lastPrice'].values[0]

# Вывод результатов
print(f"Стоимость колл-опциона по модели Блэка-Шоулза: {bs_call_price:.2f}")
print(f"Стоимость пут-опциона по модели Блэка-Шоулза: {bs_put_price:.2f}")
print(f"Стоимость колл-опциона методом Монте-Карло: {mc_call_price:.2f}")
print(f"Стоимость пут-опциона методом Монте-Карло: {mc_put_price:.2f}")
print("\n")

print(f"Реальная рыночная стоимость колл-опциона: {real_call_price:.2f}")
print(f"Реальная рыночная стоимость пут-опциона: {real_put_price:.2f}")