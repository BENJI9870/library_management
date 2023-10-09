import pymysql

class DatabaseManager:
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Waterloo67!',
        'database': 'main'
    }

    @staticmethod
    def execute_query(query, params):
        try:
            connection = pymysql.connect(**DatabaseManager.config)
            cursor = connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
            return result
        except pymysql.MySQLError as e:
            print(e)
            return None