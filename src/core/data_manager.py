# core/data_manager.py
from db import ScheduleDB
from models import Schedule
from datetime import datetime

class ScheduleDataManager:
    def __init__(self, db: ScheduleDB):
        self.db = db

    def add_schedule(self, schedule: Schedule) -> int:
        return self.db.add_schedule(schedule)

    def delete_schedule(self, schedule_id: int) -> bool:
        return self.db.delete_schedule(schedule_id)

    def update_schedule(self, schedule: Schedule) -> bool:
        return self.db.update_schedule(schedule)

    def get_all_schedules(self) -> list:
        return self.db.get_all_schedules()

    def search_schedules(self, keyword: str) -> list:
        return self.db.search_schedules(keyword)

class ScheduleDataManager:
    """封装 ScheduleDB，提供按日期操作的接口，匹配现有 GUI 需求"""

    def __init__(self, db: ScheduleDB):
        self.db = db

    def _date_to_range(self, date: str):
        """将 'YYYY-MM-DD' 转换为当天 00:00:00 到 23:59:59 的 datetime 范围"""
        try:
            dt = datetime.strptime(date, '%Y-%m-%d')
            start = dt
            end = dt.replace(hour=23, minute=59, second=59)
            return start, end
        except ValueError:
            return None, None

    def get_by_date(self, date: str) -> list:
        """获取指定日期的所有日程，返回字典列表（便于列表控件显示）"""
        # 这里暂用全量获取再过滤，如果数据量大可改为数据库层面范围查询
        all_schedules = self.db.get_all_schedules()
        result = []
        target = datetime.strptime(date, '%Y-%m-%d').date()
        for s in all_schedules:
            if s.start_time.date() == target:
                result.append(s.to_dict())
        return result

    def add_item(self, date: str, item: dict):
        """添加一个日程，item 是字典，包含 title, start_time, end_time 等"""
        # 将字典转换为 Schedule 对象
        schedule = Schedule(
            title=item.get('title', '未命名'),
            start_time=datetime.fromisoformat(item['start_time']),
            end_time=datetime.fromisoformat(item['end_time']),
            description=item.get('description'),
            remind_time=datetime.fromisoformat(item['remind_time']) if item.get('remind_time') else None
        )
        self.db.add_schedule(schedule)

    def update_item(self, date: str, idx: int, item: dict):
        """更新指定日期的第 idx 项日程（GUI 采用日期+索引定位）"""
        schedules = self.get_by_date(date)
        if 0 <= idx < len(schedules):
            target = schedules[idx]
            schedule_id = target['id']
            # 创建更新后的 Schedule 对象
            updated = Schedule(
                id=schedule_id,
                title=item.get('title'),
                start_time=datetime.fromisoformat(item['start_time']),
                end_time=datetime.fromisoformat(item['end_time']),
                description=item.get('description'),
                remind_time=datetime.fromisoformat(item['remind_time']) if item.get('remind_time') else None,
                is_completed=item.get('is_completed', False)
            )
            self.db.update_schedule(updated)

    def delete_item(self, date: str, idx: int):
        """删除指定日期的第 idx 项日程"""
        schedules = self.get_by_date(date)
        if 0 <= idx < len(schedules):
            schedule_id = schedules[idx]['id']
            self.db.delete_schedule(schedule_id)