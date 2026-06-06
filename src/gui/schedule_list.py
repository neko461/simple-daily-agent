import tkinter as tk
from tkinter import ttk

class ScheduleListWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.items = []
        self._create_list()

    def _create_list(self):
        self.listbox = tk.Listbox(self, font=("微软雅黑", 10))
        scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scroll.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def set_items(self, items):
        self.items = items
        self.listbox.delete(0, tk.END)
        for idx, item in enumerate(items, 1):
            text = f"{idx}. [{item['time']}] {item['title']} | {item['remark']}"
            self.listbox.insert(tk.END, text)

    def get_selected_index(self):
        sel = self.listbox.curselection()
        return sel[0] if sel else None