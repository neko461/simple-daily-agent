import datetime


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