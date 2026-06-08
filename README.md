# 日程管理系统 (Schedule Manager)

一个基于 Python + Tkinter + PyMySQL 的轻量级日程管理应用，支持日程的增删改查、按日期浏览，数据持久化到阿里云 MySQL 数据库。

## 功能特性

- 图形化用户界面，操作直观
- 日程的添加、编辑、删除和查看
- 按日期显示当日所有日程
- 数据库自动建表，首次运行即完成初始化
- 事务管理，保证数据一致性
- 异常处理与用户友好提示
以下是你们日程管理系统的 README.md 内容，可以直接复制到项目根目录的 README.md 文件中：

markdown
# 日程管理系统 (Schedule Manager)

一个基于 Python + Tkinter + PyMySQL 的轻量级日程管理应用，支持日程的增删改查、按日期浏览，数据持久化到阿里云 MySQL 数据库。

## 功能特性

- 图形化用户界面，操作直观
- 日程的添加、编辑、删除和查看
- 按日期显示当日所有日程
- 数据库自动建表，首次运行即完成初始化
- 事务管理，保证数据一致性
- 异常处理与用户友好提示

## 技术栈

- **语言**：Python 3.8+
- **GUI 库**：Tkinter（Python 标准库）
- **数据库驱动**：PyMySQL
- **数据库**：MySQL 8.0（阿里云 RDS）
- **版本控制**：Git / GitHub

## 项目结构
schedule_manager/
├── main.py # 程序入口
├── config.py # 数据库连接配置
├── db.py # 数据库操作封装 (ScheduleDB)
├── models.py # 日程数据模型 (Schedule)
├── core/
│ ├── init.py
│ └── data_manager.py # 业务适配层
├── gui/
│ ├── init.py
│ ├── main_window.py # 主窗口
│ ├── schedule_form.py # 日程编辑表单
│ └── schedule_list.py # 日程列表组件
├── requirements.txt # 依赖列表
└── README.md

text

## 环境准备

### 1. 安装 MySQL 数据库
- 本地或远程 MySQL 8.0 实例（项目使用阿里云 RDS）
- 创建一个数据库：
  ```sql
  CREATE DATABASE schedule_db DEFAULT CHARACTER SET utf8mb4;
2. 安装 Python 依赖
bash
pip install -r requirements.txt
或手动安装：

bash
pip install pymysql
Tkinter 为 Python 内置，无需额外安装。

3. 配置数据库连接
编辑 config.py 文件，填入你的数据库信息：

python
DB_CONFIG = {
    'host': '你的数据库地址',
    'port': 3306,
    'user': '你的用户名',
    'password': '你的密码',
    'database': 'schedule_db',
    'charset': 'utf8mb4'
}
注意：若使用阿里云 RDS，请将本机公网 IP 加入白名单，并确保外网地址已开通。

4. 运行程序
bash
python main.py
首次运行将自动创建数据库表，随后打开图形界面。

使用说明
查看日程：通过日期选择器选择日期，点击“查看”刷新当日日程列表。

新增日程：点击“新增”，在弹窗中填写标题、开始时间、结束时间（格式：YYYY-MM-DD HH:MM）等信息，确定后保存。

编辑日程：在列表中选中一项，点击“编辑”，修改后确定。

删除日程：选中一项，点击“删除”，确认后移除。

协作开发
分支管理
main 分支为稳定版本。

开发者请基于 main 创建功能分支，如 feature/gui，完成后提交 Pull Request。

提交规范
代码提交前务必拉取最新 main 分支，解决冲突后再推送。

禁止强制推送 (--force) 到共享分支。

常见问题
Q: 连接数据库报错“无法连接到数据库”
A: 检查 config.py 中主机地址、端口、用户名、密码是否正确；是否在数据库白名单中添加了本机 IP；阿里云 RDS 需确认外网地址已申请。

Q: 导入模块报错 ModuleNotFoundError
A: 确保在项目根目录（包含 main.py 的目录）下运行程序；若 IDE 报红，请将项目根目录标记为 Sources Root。

Q: 时间格式错误
A: 时间输入请严格遵循 YYYY-MM-DD HH:MM 格式，例如 2026-06-06 14:30。

致谢
PyMySQL

Python 官方 Tkinter 文档

阿里云 RDS 团队

许可证
本项目仅供学习交流使用。