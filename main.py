import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import json
import os
from password_generator import generate_password # <-- ДОБАВЛЕН импорт функции

HISTORY_FILE = 'history.json'
MAX_HISTORY = 20

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных паролей")
        self.root.geometry("500x500")
        self.history = []
        self.load_history()
        self.setup_ui()

    def setup_ui(self):
        settings_frame = ttk.LabelFrame(self.root, text="Настройки", padding=10)
        settings_frame.pack(fill="x", pady=10)

        # ИСПРАВЛЕНА строка с текстом
        ttk.Label(settings_frame, text="Длина пароля (8-32):").grid(row=0, column=0, sticky="w")
        
        self.length_var = tk.IntVar(value=12)
        length_scale = ttk.Scale(settings_frame, from_=8, to=32, variable=self.length_var,
                                 orient="horizontal", length=200)
        length_scale.grid(row=0, column=1, sticky="w")
        
        self.length_label = ttk.Label(settings_frame, text="12")
        self.length_label.grid(row=0, column=2, sticky="w")
        
        # Обновление текста на ползунке
        length_scale.bind("<ButtonRelease-1>", lambda e: self.length_label.config(text=self.length_var.get()))

        self.use_letters = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)

        ttk.Checkbutton(settings_frame, text="Буквы", variable=self.use_letters).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(settings_frame, text="Цифры", variable=self.use_digits).grid(row=1, column=1, sticky="w")
        ttk.Checkbutton(settings_frame, text="Спецсимволы", variable=self.use_special).grid(row=1, column=2, sticky="w")

        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Сгенерировать", command=self.generate).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Копировать", command=self.copy_to_clipboard).pack(side="left", padx=5)

        self.password_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.password_var, width=40).pack(pady=10)

        self.history_list = tk.Listbox(self.root, height=10, width=50)
        self.history_list.pack(pady=10)

    def generate(self):
        # Проверка: выбран ли хотя бы один тип символов
        if not (self.use_letters.get() or self.use_digits.get() or self.use_special.get()):
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
            return

        # Проверка диапазона длины (Scale уже ограничивает, но для надёжности)
        length = self.length_var.get()
        
        if length < 8 or length > 32:
            messagebox.showerror("Ошибка", "Длина пароля должна быть от 8 до 32 символов")
            return

        try:
            password = generate_password(
                length=length,
                use_letters=self.use_letters.get(),
                use_digits=self.use_digits.get(),
                use_special=self.use_special.get()
            )
            self.password_var.set(password)
            self.add_to_history(password)
            self.update_history_list()
            self.save_history()
            
        except Exception as e:
            messagebox.showerror("Ошибка генерации", str(e))

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")

    def add_to_history(self, password):
        self.history.append(password)
        if len(self.history) > MAX_HISTORY:
            self.history.pop(0) # Удаляем самый старый пароль

    def save_history(self):
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.history, f)

    def load_history(self):
        # Создаём файл с пустым массивом, если его нет (для первого запуска)
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'w') as f:
                json.dump([], f)
            return

        # Чтение с обработкой ошибок (файл пуст или повреждён)
        try:
            with open(HISTORY_FILE, 'r') as f:
                data = f.read()
                if data.strip() == '':
                    self.history = []
                else:
                    self.history = json.load(f)
                    if not isinstance(self.history, list):
                        raise ValueError("Формат истории неверный")
                
                self.update_history_list()
                
        except (json.JSONDecodeError, ValueError) as e:
            # Если JSON невалидный — сбрасываем историю на пустую и сохраняем
            self.history = []
            self.update_history_list()
            self.save_history()
            messagebox.showwarning("История", "Файл истории повреждён. История сброшена.")

    def update_history_list(self):
        self.history_list.delete(0, tk.END)
        for p in self.history:
            self.history_list.insert(tk.END, p)


if __name__ == '__main__':
    root = tk.Tk() # Точка входа верна
    app = PasswordGeneratorApp(root)
    root.mainloop()
