import tkinter as tk
from tkinter.filedialog import askopenfile, asksaveasfilename

class CheckerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x350")
        self.title("Checker")
        self.create_widgets()

    def create_widgets(self):
        self.firstbox = tk.Text(self, font=20, height=4, width=28, bg='white')
        self.firstbox.grid(row=0, column=1, columnspan=4)

        self.secondbox = tk.Text(self, font=20, height=10, width=28, bg='white')
        self.secondbox.grid(row=2, column=1, columnspan=4, pady=10)

        b1 = tk.Button(self, text='Open File', command=self.process_file, font=20, bg='cyan')
        b1.grid(row=1, column=1)

        b2 = tk.Button(self, text='Select All', command=self.select_all, font=20, bg='lightgreen')
        b2.grid(row=1, column=2, padx=2, pady=5)

        b3 = tk.Button(self, text='Copy', command=self.copy_select, font=20, bg='lightblue')
        b3.grid(row=1, column=3)

        b4 = tk.Button(self, text='Paste', command=self.paste_select, font=20, bg='lightyellow')
        b4.grid(row=1, column=4)

        b5 = tk.Button(self, text='Check pairs', command=self.check_for_pairs, font=20, bg='wheat1')
        b5.grid(row=1, column=5)

        b6 = tk.Button(self, text='Save File', command=self.save_output, font=20, bg='coral1')
        b6.grid(row=1, column=6)

    def open_file(self):
        file = askopenfile()
        if file is not None:
            content = file.read()
            return content

    def insert_content(self, content):
        self.firstbox.insert(tk.END, content)

    def insert_numbers(self, numbers):
        self.firstbox.insert(tk.END, numbers)

    def clear_firstbox(self):
        self.firstbox.delete('1.0', tk.END)

    def process_file(self):
        list1 = self.open_file()
        if list1:
            self.clear_firstbox()
            self.insert_content(list1)

    def select_all(self):
        self.firstbox.tag_add("sel", "1.0", "end")
        self.firstbox.tag_config("sel", background="green", foreground="red")

    def copy_select(self):
        if self.firstbox.selection_get():
            self.data = self.firstbox.selection_get()

    def paste_select(self):
        if hasattr(self, 'data') and self.data:
            self.secondbox.insert(tk.END, self.data)

    def check_for_pairs(self):
        pairs = []
        used_numbers = {}
        content = self.firstbox.get("1.0", tk.END).strip()
        numbers = [int(x) for x in content.split(',') if int(x) <= 12]
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if numbers[i] + numbers[j] == 12 and (
                        numbers[i] not in used_numbers or used_numbers[numbers[i]] < 2) and (
                        numbers[j] not in used_numbers or used_numbers[numbers[j]] < 2):
                    if numbers[i] < numbers[j]:
                        pairs.append((numbers[i], numbers[j]))
                    else:
                        pairs.append((numbers[j], numbers[i]))
                    used_numbers[numbers[i]] = used_numbers.get(numbers[i], 0) + 1
                    used_numbers[numbers[j]] = used_numbers.get(numbers[j], 0) + 1
        pairs.sort()
        if pairs:
            self.secondbox.delete('1.0', tk.END)
            for pair in pairs:
                self.secondbox.insert(tk.END, f"{pair[0]} {pair[1]}\n")
        else:
            self.secondbox.delete('1.0', tk.END)
            self.secondbox.insert(tk.END, "No pairs found that sum up to 12")

    def save_output(self):
        content = self.secondbox.get("1.0", tk.END).strip()
        file = asksaveasfilename(defaultextension=".txt")
        if file:
            with open(file, 'w') as f:
                f.write(content)

if __name__ == "__main__":
    app = CheckerGUI()
    app.mainloop()
