# main.py
import tkinter as tk
from tkinter import messagebox
from config import DB_CONFIG
from db import ScheduleDB
from gui.main_window import MainWindow   # 合作者负责的模块


def main():
    # 1. 初始化数据库对象（只保存配置，不立即连接）
    db = ScheduleDB(DB_CONFIG)

    # 2. 尝试连接数据库并创建表（首次自动建表）
    try:
        db.connect()          # 显式建立连接（长连接或初始化）
        db.create_table()     # 如果表不存在则创建
    except Exception as e:
        # 如果连不上数据库，弹窗提示并退出，避免程序无声崩溃
        root = tk.Tk()
        root.withdraw()       # 隐藏主窗口
        messagebox.showerror(
            "数据库连接失败",
            f"无法连接到数据库，请检查 config.py 中的配置。\n\n错误详情：{e}"
        )
        return

    # 3. 启动 GUI 主窗口
    root = tk.Tk()
    root.title("日程管理系统")          # 窗口标题
    root.geometry("900x600")           # 默认大小，合作者可调整
    app = MainWindow(root, db)         # 把数据库对象传给主窗口
    root.mainloop()

    # 4. 窗口关闭后断开数据库连接
    db.close()


if __name__ == "__main__":
    main()