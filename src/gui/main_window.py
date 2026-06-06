import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from gui.schedule_list import ScheduleListWidget
from gui.schedule_form import ScheduleForm
from core.data_manager import ScheduleDataManager

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("模块化日程管理系统")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # 数据管理器
        self.data_manager = ScheduleDataManager()

        # 创建界面
        self._create_top_bar()
        self._create_schedule_list()
        self._bind_buttons()

        # 初始化显示今日日程
        self.show_today()

    def _create_top_bar(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.X)

        # 日期选择
        ttk.Label(frame, text="日期：").grid(row=0, column=0, padx=5)
        self.year = ttk.Combobox(frame, width=6, values=[str(i) for i in range(2020, 2031)])
        self.month = ttk.Combobox(frame, width=4, values=[f"{i:02d}" for i in range(1, 13)])
        self.day = ttk.Combobox(frame, width=4, values=[f"{i:02d}" for i in range(1, 32)])
        self.year.grid(row=0, column=1, padx=2)
        self.month.grid(row=0, column=2, padx=2)
        self.day.grid(row=0, column=3, padx=2)

        # 按钮
        self.btn_refresh = ttk.Button(frame, text="查看")
        self.btn_add = ttk.Button(frame, text="新增")
        self.btn_edit = ttk.Button(frame, text="编辑")
        self.btn_delete = ttk.Button(frame, text="删除")
        self.btn_refresh.grid(row=0, column=4, padx=5)
        self.btn_add.grid(row=0, column=5, padx=5)
        self.btn_edit.grid(row=0, column=6, padx=5)
        self.btn_delete.grid(row=0, column=7, padx=5)

        # 默认日期
        now = datetime.now()
        self.year.set(str(now.year))
        self.month.set(f"{now.month:02d}")
        self.day.set(f"{now.day:02d}")

    def _create_schedule_list(self):
        self.list_widget = ScheduleListWidget(self.root)
        self.list_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def _bind_buttons(self):
        self.btn_refresh.config(command=self.refresh_list)
        self.btn_add.config(command=self.add_schedule)
        self.btn_edit.config(command=self.edit_schedule)
        self.btn_delete.config(command=self.delete_schedule)

    def get_date_str(self):
        try:
            y = int(self.year.get())
            m = int(self.month.get())
            d = int(self.day.get())
            datetime(y, m, d)
            return f"{y}-{m:02d}-{d:02d}"
        except:
            messagebox.showerror("错误", "日期无效")
            return None

    def show_today(self):
        now = datetime.now()
        self.year.set(str(now.year))
        self.month.set(f"{now.month:02d}")
        self.day.set(f"{now.day:02d}")
        self.refresh_list()

    def refresh_list(self):
        date = self.get_date_str()
        if not date:
            return
        items = self.data_manager.get_by_date(date)
        self.list_widget.set_items(items)

    def add_schedule(self):
        date = self.get_date_str()
        if not date:
            return
        form = ScheduleForm(self.root, title="新增日程")
        if form.result:
            self.data_manager.add_item(date, form.result)
            self.refresh_list()
            messagebox.showinfo("成功", "已添加")

    def edit_schedule(self):
        idx = self.list_widget.get_selected_index()
        if idx is None:
            messagebox.showwarning("提示", "请选择一项")
            return
        date = self.get_date_str()
        item = self.data_manager.get_by_date(date)[idx]
        form = ScheduleForm(self.root, title="编辑日程", data=item)
        if form.result:
            self.data_manager.update_item(date, idx, form.result)
            self.refresh_list()
            messagebox.showinfo("成功", "已修改")

    def delete_schedule(self):
        idx = self.list_widget.get_selected_index()
        if idx is None:
            messagebox.showwarning("提示", "请选择一项")
            return
        if messagebox.askyesno("确认", "确定删除？"):
            date = self.get_date_str()
            self.data_manager.delete_item(date, idx)
            self.refresh_list()
            messagebox.showinfo("成功", "已删除")