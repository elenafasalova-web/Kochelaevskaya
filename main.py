import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import json
import os

# Глобальные переменные
FAVORITES_FILE = 'favorites.json'
favorites = []

def load_favorites():
    global favorites
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r') as f:
            favorites = json.load(f)
    else:
        favorites = []

def save_favorites():
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f, indent=4)

def search_user():
    username = entry.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым.")
        return

    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        display_user(user_data)
    elif response.status_code == 404:
        messagebox.showinfo("Результат", "Пользователь не найден.")
    else:
        messagebox.showerror("Ошибка", f"Ошибка API: {response.status_code}")

def display_user(user_data):
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, f"Имя: {user_data.get('name', 'N/A')}")
    listbox.insert(tk.END, f"Логин: {user_data['login']}")
    listbox.insert(tk.END, f"Количество подписчиков: {user_data['followers']}")
    listbox.insert(tk.END, f"Количество репозиториев: {user_data['public_repos']}")
    listbox.insert(tk.END, f"URL: {user_data['html_url']}")

    # Добавить кнопку "Добавить в избранное"
    add_fav_button.config(state=tk.NORMAL)
    add_fav_button.user_data = user_data

def add_to_favorites():
    user_data = add_fav_button.user_data
    # Проверить, есть ли пользователь в избранных
    if any(u['login'] == user_data['login'] for u in favorites):
        messagebox.showinfo("Информация", "Этот пользователь уже в избранных.")
        return
    favorites.append(user_data)
    save_favorites()
    messagebox.showinfo("Успех", "Пользователь добавлен в избранные!")

def show_favorites():
    fav_window = tk.Toplevel(root)
    fav_window.title("Избранные пользователи")
    listbox_fav = tk.Listbox(fav_window, width=50)
    listbox_fav.pack(padx=10, pady=10)
    for user in favorites:
        listbox_fav.insert(tk.END, f"{user['login']} ({user.get('name', 'N/A')})")

# Инициализация
root = tk.Tk()
root.title("GitHub User Finder")

load_favorites()

# Элементы интерфейса
tk.Label(root, text="Введите логин GitHub:").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack()

search_button = tk.Button(root, text="Поиск", command=search_user)
search_button.pack(pady=5)

listbox = tk.Listbox(root, width=50, height=6)
listbox.pack(padx=10, pady=10)

add_fav_button = tk.Button(root, text="Добавить в избранное", state=tk.DISABLED, command=add_to_favorites)
add_fav_button.pack(pady=5)

show_favorites_button = tk.Button(root, text="Показать избранных", command=show_favorites)
show_favorites_button.pack(pady=5)

root.mainloop()
