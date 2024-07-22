import tkinter as tk
from tkinter import messagebox
import os

# ディレクトリの作成
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

def show_login_page():
    global frame
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="ID").pack()
    id_entry = tk.Entry(frame)
    id_entry.pack()
    tk.Label(frame, text="Password").pack()
    password_entry = tk.Entry(frame, show="*")  # パスワードを非表示にする
    password_entry.pack()
    login_button = tk.Button(frame, text="Login", command=lambda: login(id_entry.get(), password_entry.get()))
    login_button.pack()

    def login(id, password):
        print(id, password)
        if id == "user" and password == "1234":
            messagebox.showinfo("Success", "ログイン成功")
            show_home_page()
        else:
            messagebox.showwarning("Error", "IDまたはパスワードが違います")

def show_home_page():
    global frame
    for widget in frame.winfo_children():
        widget.destroy()

    # 日記作成ボタン
    tk.Button(frame, text="日記作成", command=open_register_window).pack()

    # 保存されたファイルをリストアップ
    files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
    
    for file in files:
        # ファイル名から拡張子を取り除く
        title = os.path.splitext(file)[0]
        button_frame = tk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=5, pady=2)
        button = tk.Button(button_frame, text=title, command=lambda f=file: show_file_content(f))
        button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        delete_button = tk.Button(button_frame, text="削除", command=lambda f=file: delete_file(f))
        delete_button.pack(side=tk.RIGHT)

def show_file_content(filename):
    file_path = os.path.join(data_dir, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 内容を表示するサブウィンドウ
    content_window = tk.Toplevel(root)
    content_window.title("日記内容")

    tk.Label(content_window, text="タイトル: " + os.path.splitext(filename)[0]).pack()
    
    # コンテンツ表示用のTextウィジェット
    text_widget = tk.Text(content_window, height=10, width=50, wrap=tk.WORD, bg="light grey", fg="black", font=("Arial", 12))
    text_widget.pack(padx=10, pady=10)
    text_widget.insert(tk.END, content)
    text_widget.config(state=tk.DISABLED)  # 編集不可にする

def open_register_window():
    register_window = tk.Toplevel(root)
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
            file_path = os.path.join(data_dir, f"{title}.txt")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            register_window.destroy()
            messagebox.showinfo("登録成功", "日記を登録することができました。")
            show_home_page()  
        else:
            messagebox.showwarning("警告", "タイトルと本文をどっちも入力する必要があります。")

    register_button = tk.Button(register_window, text="登録", command=register)
    register_button.pack()

def delete_file(filename):
    file_path = os.path.join(data_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        messagebox.showinfo("削除成功", f"{os.path.splitext(filename)[0]} のファイルが削除されました。")
        show_home_page()
    else:
        messagebox.showwarning("エラー", "ファイルが見つかりませんでした。")

# ウィンドウの作成と、Tkinterオブジェクトの取得
root = tk.Tk()

# タイトル
root.title("日記")

# ウィンドウサイズ
width = 500
height = 400
root.geometry(f"{width}x{height}")

# フレームの作成
frame = tk.Frame(root)
frame.pack(expand=True, fill=tk.BOTH)

show_login_page()
root.mainloop()
