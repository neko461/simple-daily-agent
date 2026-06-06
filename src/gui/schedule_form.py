import tkinter as tk
from tkinter import ttk, messagebox

class ScheduleForm:
    def __init__(self, parent, title="", data=None):
        self.result = None
        self.data = data or {"title": "", "time": "", "remark": ""}
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("400x300")
        self.top.resizable(False, False)
        self.top.grab_set()
        self._create_widgets()
        self._fill_data()
        self.top.wait_window()

    def _create_widgets(self):
        frame = ttk.Frame(self.top, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="标题：").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_title = ttk.Entry(frame, width=30)
        self.entry_title.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="时间：").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_time = ttk.Entry(frame, width=30)
        self.entry_time.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="备注：").grid(row=2, column=0, sticky="nw", pady=5)
        self.text_remark = tk.Text(frame, width=23, height=5)
        self.text_remark.grid(row=2, column=1, pady=5)

        ttk.Button(frame, text="确定", command=self.on_ok).grid(row=3, column=0, columnspan=2, pady=10)

    def _fill_data(self):
        self.entry_title.insert(0, self.data["title"])
        self.entry_time.insert(0, self.data["time"])
        self.text_remark.insert("1.0", self.data["remark"])

    def on_ok(self):
        title = self.entry_title.get().strip()
        time = self.entry_time.get().strip()
        remark = self.text_remark.get("1.0", tk.END).strip()
        if not title:
            messagebox.showerror("错误", "标题不能为空")
            return
        self.result = {"title": title, "time": time, "remark": remark}
        self.top.destroy()