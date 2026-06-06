import datetime
import pymysql
from typing import List

class Schedule:
    def __init__(
            self,
            title: str,
            start_time: datetime,
            end_time: datetime,
            description: str = None,
            remind_time: datetime = None,
            is_completed: bool = False,
            id: int = None
    ):
        self.id = id  # 数据库自增主键，新建时为None，保存后由数据库赋值
        self.title = title  # 日程标题，必填
        self.description = description  # 详细描述，可选
        self.start_time = start_time  # 开始时间，必填，应为datetime对象
        self.end_time = end_time  # 结束时间，必填，应为datetime对象
        self.remind_time = remind_time  # 提醒时间，可选，datetime对象
        self.is_completed = is_completed  # 是否完成，布尔值，默认False

    def to_dict(self):
        """将对象转换为字典，方便GUI显示或序列化"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M') if self.start_time else '',
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M') if self.end_time else '',
            'remind_time': self.remind_time.strftime('%Y-%m-%d %H:%M') if self.remind_time else '',
            'is_completed': self.is_completed
        }

    def __repr__(self):
        return f"<Schedule {self.id}: {self.title}>"

class ScheduleDB:
    def __init__(self, config):
        """初始化表格"""
        self.config = config
        self._conn = None

    def connect(self):
        """显式建立数据库连接"""
        if self._conn is None or not self._conn.open:
            self._conn = pymysql.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                charset=self.config.get('charset', 'utf8mb4'),
                cursorclass=pymysql.cursors.DictCursor,  # 使用字典游标，方便字段名访问
                autocommit=False  # 手动提交，保证事务一致性
            )

    def close(self):
        """关闭数据库连接"""
        if self._conn and self._conn.open:
            self._conn.close()
            self._conn = None

    def _get_connection(self):
        """内部使用的获取连接方法（自动调用 connect 如果尚未连接）"""
        if self._conn is None or not self._conn.open:
            self.connect()
        return self._conn

    def create_table(self):
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS schedules (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(200) NOT NULL,
                        description TEXT,
                        start_time DATETIME NOT NULL,
                        end_time DATETIME NOT NULL,
                        remind_time DATETIME,
                        is_completed TINYINT(1) DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
        finally:
            pass

    #-----------------增删改查--------------------

    def add_schedule(self, schedule: Schedule) -> int:
        """返回新日程id"""
        conn = self._get_connection()
        sql = """INSERT INTO schedules 
                         (title, description, start_time, end_time, remind_time, is_completed)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (
                    schedule.title,
                    schedule.description,
                    schedule.start_time,
                    schedule.end_time,
                    schedule.remind_time,
                    int(schedule.is_completed)  # 布尔值转为 0/1
                ))
                new_id = cursor.lastrowid
            conn.commit()
            return new_id
        except Exception:
            conn.rollback()
            raise

    def delete_schedule(self, schedule_id: int) -> bool:
        """
            根据 id 删除日程
            :param schedule_id: 要删除的日程 id
            :return: 是否成功删除（存在且被删除）
        """
        conn = self._get_connection()
        sql = "DELETE FROM schedules WHERE id = %s"
        try:
            with conn.cursor() as cursor:
                affected = cursor.execute(sql, (schedule_id,))
            conn.commit()
            return affected > 0
        except Exception:
            conn.rollback()
            raise

    def update_schedule(self, schedule: Schedule) -> bool:
        """
            更新一个已有的日程（通过 schedule.id 定位）
            :param schedule: 包含 id 及更新后字段的 Schedule 对象
            :return: 是否成功更新
        """
        if schedule.id is None:
            raise ValueError("更新操作需要日程的 id 不为空")
        conn = self._get_connection()
        sql = """UPDATE schedules 
                         SET title = %s,
                             description = %s,
                             start_time = %s,
                             end_time = %s,
                             remind_time = %s,
                             is_completed = %s
                         WHERE id = %s"""
        try:
            with conn.cursor() as cursor:
                affected = cursor.execute(sql, (
                    schedule.title,
                    schedule.description,
                    schedule.start_time,
                    schedule.end_time,
                    schedule.remind_time,
                    int(schedule.is_completed),
                    schedule.id
                ))
            conn.commit()
            return affected > 0
        except Exception:
            conn.rollback()
            raise

    def get_schedule_by_id(self, schedule_id: int) -> 'Schedule' or None:
        """
        根据 id 获取单个日程
        :return: Schedule 对象，如果不存在返回 None
        """
        conn = self._get_connection()
        sql = "SELECT * FROM schedules WHERE id = %s"
        with conn.cursor() as cursor:
            cursor.execute(sql, (schedule_id,))
            row = cursor.fetchone()
        if row:
            return self._row_to_schedule(row)
        return None

    def get_all_schedules(self) -> List['Schedule']:
        """获取所有日程，按开始时间升序排列"""
        conn = self._get_connection()
        sql = "SELECT * FROM schedules ORDER BY start_time ASC"
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        return [self._row_to_schedule(row) for row in rows]

    def search_schedules(self, keyword: str) -> List['Schedule']:
        """
        按关键词搜索日程（匹配标题或描述）
        :param keyword: 搜索关键词
        :return: 匹配的 Schedule 列表
        """
        conn = self._get_connection()
        sql = """SELECT * FROM schedules 
                 WHERE title LIKE %s OR description LIKE %s
                 ORDER BY start_time ASC"""
        param = f'%{keyword}%'
        with conn.cursor() as cursor:
            cursor.execute(sql, (param, param))
            rows = cursor.fetchall()
        return [self._row_to_schedule(row) for row in rows]

    # ---------- 内部辅助方法 ----------
    @staticmethod
    def _row_to_schedule(row: dict) -> 'Schedule':
        """将数据库查询的一行字典转换为 Schedule 对象"""
        return Schedule(
            id=row['id'],
            title=row['title'],
            description=row.get('description'),   # 可能为 None
            start_time=row['start_time'],
            end_time=row['end_time'],
            remind_time=row.get('remind_time'),
            is_completed=bool(row['is_completed'])
        )