import unittest
import tkinter as tk
import os
from unittest.mock import MagicMock, patch
from tkinter.filedialog import askopenfile, asksaveasfilename
from tkinter import Tk, Text
from checker_app import CheckerGUI


class TestCheckerGUI(unittest.TestCase):

    def setUp(self):
        self.app = CheckerGUI()
        self.app.firstbox = Text(self.app)
        self.app.firstbox.insert("1.0", "1 2 3 4 5")

    def test_widgets_exist(self):
        self.assertIsInstance(self.app.firstbox, tk.Text)
        self.assertIsInstance(self.app.secondbox, tk.Text)
        self.assertIsInstance(self.app.children['!button'], tk.Button)
        self.assertIsInstance(self.app.children['!button2'], tk.Button)
        self.assertIsInstance(self.app.children['!button3'], tk.Button)
        self.assertIsInstance(self.app.children['!button4'], tk.Button)
        self.assertIsInstance(self.app.children['!button5'], tk.Button)
        self.assertIsInstance(self.app.children['!button6'], tk.Button)


    def test_open_file(self):
        with patch('tkinter.filedialog.askopenfile', return_value=MagicMock(read=lambda: "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12")):
            self.assertEqual(self.app.open_file(),
                             "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12")  # Check that the file content is correctly read and parsed

    def test_insert_content(self):
        content = "1 2 3 4 5"
        self.assertEqual(self.app.firstbox.get("1.0", tk.END).strip(), content)

    def test_insert_numbers(self):
        self.assertEqual(self.app.firstbox.get("1.0", tk.END).strip(), "1 2 3 4 5")

    def test_clear_firstbox(self):
        self.app.clear_firstbox()
        self.assertEqual(self.app.firstbox.get("1.0", tk.END), "\n")

    def test_select_all(self):
        self.app.select_all()
        expected = "1 2 3 4 5\n"
        actual = self.app.firstbox.selection_get()
        self.assertEqual(expected, actual)

    def test_copy_select(self):
        self.app.select_all()
        self.app.copy_select()
        self.assertEqual(self.app.data, "1 2 3 4 5\n")

    def test_paste_select(self):
        app = CheckerGUI()
        app.secondbox.insert(tk.END, "1 2 3 4 5")
        app.secondbox.tag_add("sel", "1.0", "3.0")
        app.paste_select()
        expected_output = "1 2 3 4 5"
        self.assertEqual(app.secondbox.get("1.0", tk.END).strip(), expected_output)

    def test_check_for_pairs(self):
        self.test_clear_firstbox()
        self.app.firstbox.insert(tk.END, "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12")
        self.app.check_for_pairs()
        pairs = self.app.secondbox.get("1.0", tk.END).strip()
        self.assertEqual(pairs, "1 11\n2 10\n3 9\n4 8\n5 7")

    @patch('tkinter.filedialog.asksaveasfilename', return_value='C:/Pycode/random_numbers_output.txt')
    def test_save_output(self, mock_asksaveasfilename):
        self.app.secondbox.insert('1.0', '2 10\n6 6\n8 4\n')
        self.app.save_output()
        with open('C:/Pycode/random_numbers_output.txt', 'r') as f:
            saved_content = f.read()
        self.assertEqual(saved_content.strip(), '2 10\n6 6\n8 4')


if __name__ == "__main__":
    unittest.main()
