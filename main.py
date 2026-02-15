import os
from multiprocessing.managers import convert_to_error

import requests
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk, messagebox

from requests.packages import target

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    messagebox.showerror("ошибка - API-ключ не обнаружен проверьте файл .env")
    exit ()


# Функция для получения списка валют
def get_currency_list():
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
    responce = requests.get(url)
    if responce.status_code == 200:
        data = responce.json()
        return list(data["conversion_rates"].keys())
    else:
        messagebox.showerror("Ошибка", "не удалось получить список валют")
        return []


# Функция для конвертации валют
def convert_currency():
    base_currency = base_currency_var.get()
    target_currency = target_currency_var.get()
    amount = amount_entry.get()

    if not amount.isdigit():
        messagebox.showerror("Ошибка", "Введите корректное число для суммы нахрен")
        return

    amount = float(amount)
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    responce = requests.get(url)

    if responce.status_code == 200:
        data = responce.json()
        if target_currency in data["conversion_rates"]:
            rate = data["conversion_rates"][target_currency]
            converted_amount = amount * rate
            result_label.config(text=f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}")
        else:
            messagebox.showerror("ОШИБКА.", "ЦЕЛЕВОЙ ВАЛЮТЫ НЕМА В БАЗЕ АПИ")
    else:
        messagebox.showerror("Ошибка: ", "Не удалось получить данные с АПИ")

# Создаем главное окно
root = tk.Tk()
root.title("Конвертор валют")
root.geometry("400x300")
root.resizable(False, False)

# Получаем список валют
currencies = get_currency_list()

# Поля ввода и выпадающие списки
tk.Label(root, text="Сумма:").pack
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Исходная валюта:").pack()
base_currency_var = tk.StringVar(value="USD")
base_currency_menu = ttk.Combobox(root, textvariable=base_currency_var, values=currencies)
base_currency_menu.pack()

tk.Label(root, text="Целевая валюта:").pack()
target_currency_var = tk.StringVar(value="EUR")
target_currency_menu = ttk.Combobox(root, textvariable=target_currency_var, values=currencies)
target_currency_menu.pack()

# Кнопка дял конвертации
convert_button = tk.Button(root, text="Конвертировать", command=convert_currency)
convert_button.pack()

# Поле для вывода результата
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

# Запуск главного цикла Tkinter
root.mainloop()
