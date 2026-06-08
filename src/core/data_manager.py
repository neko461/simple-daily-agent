# core/data_manager.py
from datetime import timedelta
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

    def _normalize_time(self, time_str):
        """将 '2026-6-1 9:5' 转为 '2026-06-01 09:05'"""
        from datetime import datetime
        # 先尝试直接解析，如果失败则拆开补零
        try:
            return datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        except ValueError:
            parts = time_str.split(' ')
            date_part = parts[0]
            time_part = parts[1] if len(parts) > 1 else '00:00'
            y, m, d = date_part.split('-')
            h, mi = time_part.split(':')
            fixed = f"{int(y):04d}-{int(m):02d}-{int(d):02d} {int(h):02d}:{int(mi):02d}"
            return datetime.strptime(fixed, '%Y-%m-%d %H:%M')

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
        """获取指定日期的所有日程（包含跨天日程）"""
        all_schedules = self.db.get_all_schedules()
        result = []
        target = datetime.strptime(date, '%Y-%m-%d').date()
        # 第二天的 00:00 作为区间终点
        next_day = target + timedelta(days=1)

        for s in all_schedules:
            # 检查日程是否覆盖了查询日期
            # 条件：日程开始时间 < 查询日期的次日  且  日程结束时间 > 查询日期的开始
            if s.start_time.date() < next_day and s.end_time.date() > target:
                # 也可以写成：
                # if s.start_time < datetime.combine(next_day, datetime.min.time()) and s.end_time > datetime.combine(target, datetime.min.time()):
                d = s.to_dict()
                d['time'] = d['start_time']
                d['remark'] = d.get('description', '') or ''
                result.append(d)

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