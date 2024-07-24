import tkinter as tk
from tkinter import messagebox
import os

class DiaryApp:
    def __init__(self):
        self.data_dir = 'data'

        # ディレクトリの作成
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # ウィンドウ設定
        self.root = tk.Tk()
        self.root.title("日記")
        self.root.geometry("500x400")

        # フレームの作成
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.show_login_page()

        # アプリケーションの開始
        self.root.mainloop()

    def show_login_page(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="ID").pack()
        self.id_entry = tk.Entry(self.frame)
        self.id_entry.pack()
        tk.Label(self.frame, text="Password").pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()
        login_button = tk.Button(self.frame, text="Login", command=self.login)
        login_button.pack()

    def login(self):
        id = self.id_entry.get()
        password = self.password_entry.get()
        if id == "user" and password == "1234":
            messagebox.showinfo("Success", "ログイン成功")
            self.show_home_page()
        else:
            messagebox.showwarning("Error", "IDまたはパスワードが違います")

    def show_home_page(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Button(self.frame, text="日記作成", command=self.open_register_window).pack()
        
        files = [f for f in os.listdir(self.data_dir) if os.path.isfile(os.path.join(self.data_dir, f))]
        
        for file in files:
            title = os.path.splitext(file)[0]
            button_frame = tk.Frame(self.frame)
            button_frame.pack(fill=tk.X, padx=5, pady=2)
            button = tk.Button(button_frame, text=title, command=lambda f=file: self.show_file_content(f))
            button.pack(side=tk.LEFT, fill=tk.X, expand=True)
            delete_button = tk.Button(button_frame, text="削除", command=lambda f=file: self.delete_file(f))
            delete_button.pack(side=tk.RIGHT)

    def show_file_content(self, filename):
        file_path = os.path.join(self.data_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        content_window = tk.Toplevel(self.root)
        content_window.title("日記内容")

        tk.Label(content_window, text="タイトル: " + os.path.splitext(filename)[0]).pack()
        
        text_widget = tk.Text(content_window, height=10, width=50, wrap=tk.WORD, bg="light grey", fg="black", font=("Arial", 12))
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)

    def open_register_window(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("日記作成")

        tk.Label(register_window, text="タイトル").pack()
        title_entry = tk.Entry(register_window)
        title_entry.pack()

        tk.Label(register_window, text="本文").pack()
        content_text = tk.Text(register_window, height=10, width=40)
        content_text.pack()

        def register():
            title = title_entry.get()
            content = content_text.get("1.0", tk.END).strip()
            if title and content:
                file_path = os.path.join(self.data_dir, f"{title}.txt")
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                messagebox.showinfo("登録成功", "日記を登録することができました。")
                register_window.destroy()
                self.show_home_page()  
            else:
                messagebox.showwarning("警告", "タイトルと本文をどっちも入力する必要があります。")

        register_button = tk.Button(register_window, text="登録", command=register)
        register_button.pack()

    def delete_file(self, filename):
        file_path = os.path.join(self.data_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            messagebox.showinfo("削除成功", f"{os.path.splitext(filename)[0]} のファイルが削除されました。")
            self.show_home_page()
        else:
            messagebox.showwarning("エラー", "ファイルが見つかりませんでした。")

# アプリケーションの開始
if __name__ == "__main__":
    app = DiaryApp()
