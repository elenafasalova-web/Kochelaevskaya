import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("400x500")
        self.fav_file = "favorites.json"

        # 1. Поле ввода
        tk.Label(root, text="Введите логин GitHub:").pack(pady=5)
        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=5)

        # Кнопка поиска
        tk.Button(root, text="Найти", command=self.search_user).pack(pady=5)

        # 2. Список результатов
        tk.Label(root, text="Результаты поиска:").pack(pady=5)
        self.results_list = tk.Listbox(root, height=5, width=40)
        self.results_list.pack(pady=5)

        # 3. Добавление в избранное
        tk.Button(root, text="Добавить в избранное", command=self.add_to_fav).pack(pady=5)

        # Список избранных (для наглядности)
        tk.Label(root, text="Избранные (сохранено в JSON):").pack(pady=5)
        self.fav_listbox = tk.Listbox(root, height=10, width=40, fg="blue")
        self.fav_listbox.pack(pady=5)

        self.load_fav_from_json()

    def search_user(self):
        username = self.entry.get().strip()
        
        # 5. Проверка корректности ввода
        if not username:
            messagebox.showerror("Ошибка", "Поле поиска не должно быть пустым!")
            return

        self.results_list.delete(0, tk.END)
        try:
            response = requests.get(f"https://github.com{username}")
            if response.status_code == 200:
                data = response.json()
                # Отображаем в списке (Пункт 2)
                self.results_list.insert(tk.END, data['login'])
                self.last_found = data['login']
            else:
                messagebox.showwarning("Внимание", "Пользователь не найден")
        except Exception as e:
            messagebox.showerror("Ошибка сети", str(e))

    def add_to_fav(self):
        selection = self.results_list.curselection()
        if not selection:
            messagebox.showwarning("Внимание", "Сначала найдите и выберите пользователя!")
            return

        user = self.results_list.get(selection[0])
        
        # 4. Сохранение в JSON
        favs = self.get_favs()
        if user not in favs:
            favs.append(user)
            with open(self.fav_file, "w") as f:
                json.dump(favs, f)
            self.load_fav_from_json()
            messagebox.showinfo("Успех", f"{user} добавлен в избранное")

    def get_favs(self):
        if not os.path.exists(self.fav_file):
            return []
        with open(self.fav_file, "r") as f:
            return json.load(f)

    def load_fav_from_json(self):
        self.fav_listbox.delete(0, tk.END)
        for user in self.get_favs():
            self.fav_listbox.insert(tk.END, user)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
