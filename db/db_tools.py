import sqlite3
from typing import Optional, List, Dict, Any
import os


class SQLiteDB:
    def __init__(self, db_path: str = "database.db"):
        """初始化数据库连接
        :param db_path: 数据库文件路径，例如 'D:/data.db'
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """支持with语句上下文管理"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出with语句时自动关闭连接"""
        self.close()

    def connect(self):
        """连接数据库"""
        self.connection = sqlite3.connect(self.db_path)
        # 设置返回字典格式的结果
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        print(f"已连接到数据库: {self.db_path}")

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("数据库连接已关闭")

    def create_table(self, table_name: str, columns: Dict[str, str], primary_key: Optional[str] = None):
        """创建表
        :param table_name: 表名
        :param columns: 列名和类型的字典，如 {'id': 'INTEGER', 'name': 'TEXT'}
        :param primary_key: 主键列名
        """
        columns_def = []
        for name, type_ in columns.items():
            col_def = f"{name} {type_}"
            if primary_key and name == primary_key:
                col_def += " PRIMARY KEY"
            columns_def.append(col_def)

        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_def)})"
        self.cursor.execute(sql)
        self.connection.commit()
        print(f"表 {table_name} 已创建或已存在")

    def insert(self, table_name: str, data: Dict[str, Any]):
        """插入单条数据
        :param table_name: 表名
        :param data: 要插入的数据字典
        :return: 插入行的ID
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        self.cursor.execute(sql, tuple(data.values()))
        self.connection.commit()

    def insert_many(self, table_name: str, data_list: List[Dict[str, Any]]):
        """批量插入数据
        :param table_name: 表名
        :param data_list: 字典列表
        """
        if not data_list:
            return

        columns = ', '.join(data_list[0].keys())
        placeholders = ', '.join(['?'] * len(data_list[0]))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        values = [tuple(data.values()) for data in data_list]
        self.cursor.executemany(sql, values)
        self.connection.commit()
        print(f"已批量插入 {len(data_list)} 条数据到 {table_name}")

    def select(self, table_name: str, columns: List[str] = None,
               where: Optional[str] = None, params: tuple = None,
               fetch_all: bool = True) -> List[Dict]:
        """查询数据
        :param table_name: 表名
        :param columns: 要查询的列名列表，None表示所有列
        :param where: WHERE条件语句（不含WHERE关键字）
        :param params: WHERE条件的参数
        :param fetch_all: True返回所有结果，False返回第一条
        :return: 结果字典列表
        """
        cols = '*' if columns is None else ', '.join(columns)
        sql = f"SELECT {cols} FROM {table_name}"

        if where:
            sql += f" WHERE {where}"

        self.cursor.execute(sql, params or ())

        if fetch_all:
            results = self.cursor.fetchall()
            if results:
                return [dict(row) for row in results]
            else:
                return results # []
        else:
            result = self.cursor.fetchone()
            return [dict(result)] if result else []

    def update(self, table_name: str, data: Dict[str, Any], where: str, params: tuple = None):
        """更新数据
        :param table_name: 表名
        :param data: 要更新的数据字典
        :param where: WHERE条件语句（不含WHERE关键字）
        :param params: WHERE条件的额外参数
        """
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {where}"

        # 合并数据值和条件参数
        values = tuple(data.values()) + (params or ())
        self.cursor.execute(sql, values)
        self.connection.commit()
        print(f"已更新 {self.cursor.rowcount} 条数据")

    def delete(self, table_name: str, where: str, params: tuple = None):
        """删除数据
        :param table_name: 表名
        :param where: WHERE条件语句（不含WHERE关键字）
        :param params: 条件参数
        """
        sql = f"DELETE FROM {table_name} WHERE {where}"
        self.cursor.execute(sql, params or ())
        self.connection.commit()
        print(f"已删除 {self.cursor.rowcount} 条数据")

    def execute_sql(self, sql: str):
        """执行自定义SQL语句
        :param sql: SQL语句
        :return: None
        """
        self.cursor.execute(sql)
        self.connection.commit()
        print(f"执行成功，影响行数: {self.cursor.rowcount}")
        return None

    @staticmethod
    def create_db(db_path):
        if not os.path.exists(db_path):
            with open(db_path, "w", encoding="utf-8") as f:
                pass
            print(f'Create DB...{db_path}')
