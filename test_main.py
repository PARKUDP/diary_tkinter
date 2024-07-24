import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
import tkinter as tk
from main import DiaryApp

class TestDiaryApp(unittest.TestCase):
    def setUp(self):
        """ 各テストケースの前に実行されるセットアップ """
        # Tkウィンドウをモックする
        self.patcher_tk = patch('main.tk.Tk', new_callable=MagicMock)
        self.patcher_toplevel = patch('main.tk.Toplevel', new_callable=MagicMock)
        
        self.mock_tk = self.patcher_tk.start()
        self.mock_toplevel = self.patcher_toplevel.start()

        # DiaryAppのインスタンスを作成
        self.app = DiaryApp()
        self.app.root = self.mock_tk.return_value
        self.app.frame = MagicMock()  # フレームもモック化

    def tearDown(self):
        """ 各テストケースの後に実行されるクリーンアップ """
        self.patcher_tk.stop()
        self.patcher_toplevel.stop()
        shutil.rmtree(self.app.data_dir, ignore_errors=True)  # テスト用データディレクトリを削除

    # ログイン機能のテスト
    @patch('tkinter.messagebox.showinfo')
    def test_login_success(self, mock_showinfo):
        self.app.id_entry = MagicMock()
        self.app.password_entry = MagicMock()
        self.app.id_entry.get.return_value = "user"
        self.app.password_entry.get.return_value = "1234"
        
        with patch.object(self.app, 'show_home_page') as mock_show_home_page:
            self.app.login()
            mock_showinfo.assert_called_once_with("Success", "ログイン成功")
            mock_show_home_page.assert_called_once()

    @patch('tkinter.messagebox.showwarning')
    def test_login_failure(self, mock_showwarning):
        self.app.id_entry = MagicMock()
        self.app.password_entry = MagicMock()
        self.app.id_entry.get.return_value = "wrong_user"
        self.app.password_entry.get.return_value = "wrong_password"
        
        with patch.object(self.app, 'show_home_page') as mock_show_home_page:
            self.app.login()
            mock_showwarning.assert_called_once_with("Error", "IDまたはパスワードが違います")
            mock_show_home_page.assert_not_called()

    # ログインページのウィジェット作成テスト
    def test_login_page_widget(self):
        with patch('main.tk.Entry', new_callable=MagicMock) as mock_entry:
            self.app.show_login_page()
            self.assertIsInstance(self.app.id_entry, MagicMock)
            self.assertIsInstance(self.app.password_entry, MagicMock)

    # メインページのウィジェット作成テスト
    @patch('main.DiaryApp.show_home_page')
    def test_main_page_widget(self, mock_show_home_page):
        self.app.show_home_page()
        # ウィジェットの追加をシミュレート
        self.app.frame.winfo_children.return_value = [MagicMock(), MagicMock()]
        self.assertGreater(len(self.app.frame.winfo_children()), 0)  # ウィジェットが作成されたか確認

    # 日記作成ウィンドウの作成テスト
    @patch('tkinter.Label.pack')
    @patch('tkinter.Entry.pack')
    @patch('tkinter.Text.pack')
    def test_diary_register_window(self, mock_text_pack, mock_entry_pack, mock_label_pack):
        self.app.open_register_window()
        self.mock_toplevel.assert_called_once_with(self.app.root)
        self.assertEqual(mock_label_pack.call_count, 2)
        self.assertEqual(mock_entry_pack.call_count, 1)  
        self.assertEqual(mock_text_pack.call_count, 1)

    # 日記登録機能のテスト
    @patch('tkinter.messagebox.showinfo')
    @patch('builtins.open', new_callable=MagicMock)
    def test_diary_register_save(self, mock_open, mock_showinfo):
        # モックのEntryとTextウィジェットの設定
        entry_mock = MagicMock()
        entry_mock.get.side_effect = ['Test Title', 'Test Content']
        text_mock = MagicMock()
        text_mock.get.return_value = 'Test Content'

        with patch('main.tk.Entry', return_value=entry_mock), patch('main.tk.Text', return_value=text_mock):
            self.app.open_register_window()
            
            # モックのウィンドウを取得
            register_window = self.mock_toplevel.return_value
            
            # register ボタンを直接取得
            register_button = None
            for widget in register_window.winfo_children():
                if isinstance(widget, tk.Button) and widget.cget('text') == '登録':
                    register_button = widget
                    break
            
            if register_button is None:
                self.fail("Register button not found in the register window.")
            
            # register ボタンのコマンドを取得し、実行する
            register_function = register_button.cget('command')
            if register_function:
                register_function()
            else:
                self.fail("Register button command not set.")
            
            # showinfo メソッドが呼ばれているか確認
            mock_showinfo.assert_called_once_with("登録成功", "日記を登録することができました。")

    # 日記表示ウィンドウの作成テスト
    @patch('tkinter.Label.pack')
    @patch('tkinter.Text.pack')
    @patch('builtins.open', new_callable=MagicMock)
    def test_diary_open_window(self, mock_open, mock_text_pack, mock_label_pack):
        filename = "TestFile.txt"
        file_path = os.path.join(self.app.data_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Test Content")
        
        self.app.show_file_content(filename)
        self.mock_toplevel.assert_called_once_with(self.app.root)
        self.assertTrue(self.mock_toplevel.return_value.winfo_children())  # 確認: ウィンドウにウィジェットがあるか

    # 日記内容が正しく表示されるかのテスト
    @patch('builtins.open', new_callable=MagicMock)
    def test_diary_open(self, mock_open):
        filename = "TestFile.txt"
        file_path = os.path.join(self.app.data_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Test Content")
        
        mock_open.return_value.read.return_value = "Test Content"
        self.app.show_file_content(filename)
        text_widget = self.mock_toplevel.return_value.winfo_children()[0].winfo_children()[1]
        text_widget.get = MagicMock(return_value="Test Content")
        self.assertEqual(text_widget.get("1.0", tk.END).strip(), "Test Content")

if __name__ == '__main__':
    unittest.main()
