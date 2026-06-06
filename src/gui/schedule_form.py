import tkinter as tk
from tkinter import ttk, messagebox

class ScheduleForm:
    def __init__(self, parent, title="", data=None):
        self.result = None
        # 默认数据结构 与数据库层保持一致
        self.data = data or {
            "title": "",
            "start_time": "",
            "end_time": "",
            "description": "",
            "remind_time": ""
        }
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("500x380")  # 调整窗口大小适配更多字段
        self.top.resizable(False, False)
        self.top.grab_set()
        self._create_widgets()
        self._fill_data()
        self.top.wait_window()

    def _create_widgets(self):
        frame = ttk.Frame(self.top, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        ttk.Label(frame, text="标题：").grid(row=0, column=0, sticky="w", pady=8)
        self.entry_title = ttk.Entry(frame, width=35)
        self.entry_title.grid(row=0, column=1, pady=8)

        # 开始时间
        ttk.Label(frame, text="开始时间：").grid(row=1, column=0, sticky="w", pady=8)
        self.entry_start = ttk.Entry(frame, width=35)
        self.entry_start.grid(row=1, column=1, pady=8)

        # 结束时间
        ttk.Label(frame, text="结束时间：").grid(row=2, column=0, sticky="w", pady=8)
        self.entry_end = ttk.Entry(frame, width=35)
        self.entry_end.grid(row=2, column=1, pady=8)

        # 提醒时间
        ttk.Label(frame, text="提醒时间：").grid(row=3, column=0, sticky="w", pady=8)
        self.entry_remind = ttk.Entry(frame, width=35)
        self.entry_remind.grid(row=3, column=1, pady=8)

        # 描述/备注
        ttk.Label(frame, text="描述：").grid(row=4, column=0, sticky="nw", pady=8)
        self.text_desc = tk.Text(frame, width=30, height=6)
        self.text_desc.grid(row=4, column=1, pady=8)

        # 确定按钮
        ttk.Button(frame, text="确定", command=self.on_ok).grid(
            row=5, column=0, columnspan=2, pady=15
        )

    def _fill_data(self):
        # 填充原有数据
        self.entry_title.insert(0, self.data["title"])
        self.entry_start.insert(0, self.data["start_time"])
        self.entry_end.insert(0, self.data["end_time"])
        self.entry_remind.insert(0, self.data["remind_time"])
        self.text_desc.insert("1.0", self.data["description"])

    def on_ok(self):
        # 获取输入内容并去除空格
        title = self.entry_title.get().strip()
        start_time = self.entry_start.get().strip()
        end_time = self.entry_end.get().strip()
        remind_time = self.entry_remind.get().strip()
        description = self.text_desc.get("1.0", tk.END).strip()

        # 必填项校验
        if not title:
            messagebox.showerror("错误", "标题不能为空")
            return
        if not start_time:
            messagebox.showerror("错误", "开始时间不能为空")
            return

        self.result = {
            "title": title,
            "start_time": start_time,
            "end_time": end_time,
            "description": description,
            "remind_time": remind_time
        }

        self.top.destroy()