import pymysql

class ScheduleDB:
    def __init__(self, config):
        self.config = config

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
            conn.commit()
        finally:
            conn.close()

    def add_schedule(self, schedule: Schedule) -> int:
        """返回新日程id"""
        ...
    def delete_schedule(self, schedule_id: int) -> bool:
        ...
    def update_schedule(self, schedule: Schedule) -> bool:
        ...
    def get_all_schedules(self) -> list[Schedule]:
        ...
    def search_schedules(self, keyword: str) -> list[Schedule]:
        ...