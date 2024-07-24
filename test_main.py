import unittest
from unittest.mock import patch, mock_open
import os
import shutil
from main import DiaryApp

class TestDiaryApp(unittest.TestCase):

    @patch('os.makedirs')
    def test_directory_creation(self, mock_makedirs):
        app = DiaryApp()
        mock_makedirs.assert_called_once_with('data')
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_directory_exists(self, mock_makedirs, mock_exists):
        mock_exists.return_value = True
        app = DiaryApp()
        mock_makedirs.assert_not_called()
    
    @patch('os.listdir')
    @patch('os.path.isfile')
    def test_show_home_page(self, mock_isfile, mock_listdir):
        mock_listdir.return_value = ['test1.txt', 'test2.txt']
        mock_isfile.return_value = True
        app = DiaryApp()
        app.show_home_page()
        self.assertEqual(len(app.frame.winfo_children()), 3)  # 1 button and 2 diary files

    @patch('builtins.open', new_callable=mock_open, read_data='test content')
    def test_show_file_content(self, mock_open):
        app = DiaryApp()
        app.show_file_content('test.txt')
        mock_open.assert_called_once_with(os.path.join('data', 'test.txt'), 'r', encoding='utf-8')

    @patch('os.remove')
    @patch('os.path.exists')
    def test_delete_file(self, mock_exists, mock_remove):
        mock_exists.return_value = True
        app = DiaryApp()
        app.delete_file('test.txt')
        mock_remove.assert_called_once_with(os.path.join('data', 'test.txt'))

    @patch('builtins.open', new_callable=mock_open)
    def test_register_diary(self, mock_open):
        app = DiaryApp()
        app.open_register_window()
        register_window = app.root.winfo_children()[-1]  # The new Toplevel window
        title_entry = register_window.winfo_children()[1]
        content_text = register_window.winfo_children()[3]
        title_entry.insert(0, "Test Title")
        content_text.insert('1.0', "Test Content")

        register_button = register_window.winfo_children()[5]
        register_button.invoke()
        
        file_path = os.path.join('data', 'Test Title.txt')
        mock_open.assert_called_once_with(file_path, 'w', encoding='utf-8')
        handle = mock_open()
        handle.write.assert_called_once_with("Test Content")

    @patch('tkinter.messagebox.showinfo')
    def test_successful_login(self, mock_showinfo):
        app = DiaryApp()
        app.show_login_page()
        app.id_entry.insert(0, "user")
        app.password_entry.insert(0, "1234")
        app.login()
        mock_showinfo.assert_called_once_with("Success", "ログイン成功")

    @patch('tkinter.messagebox.showwarning')
    def test_unsuccessful_login(self, mock_showwarning):
        app = DiaryApp()
        app.show_login_page()
        app.id_entry.insert(0, "wronguser")
        app.password_entry.insert(0, "wrongpassword")
        app.login()
        mock_showwarning.assert_called_once_with("Error", "IDまたはパスワードが違います")
        
if __name__ == '__main__':
    unittest.main()
