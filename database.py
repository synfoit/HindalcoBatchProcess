import psycopg2


class Database:

    def __init__(self):
        self.db_handle = psycopg2.connect(
            database="Hindalco",
            user='postgres',
            password='Servilink@123',
            host='localhost',
            port='5432'
        )

        self.mycursor = self.db_handle.cursor()

    def get_single_data(self, table, query_columns_dict):
        selection_list = " AND ".join([
            f"{column_name} {query_columns_dict[column_name][0]} %s"
            for column_name in sorted(query_columns_dict.keys())
        ])

        sql = f"SELECT * FROM {table} WHERE {selection_list}"

        val = tuple(query_columns_dict[column_name][1] for column_name in sorted(query_columns_dict.keys()))

        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchone()

        return result

    def get_multiple_data(self, table, query_columns_dict):
        if query_columns_dict == None:
            sql = f"SELECT * FROM {table}"
            self.mycursor.execute(sql)
        else:
            selection_list = " AND ".join([
                f"{column_name} {query_columns_dict[column_name][0]} %s"
                for column_name in sorted(query_columns_dict.keys())
            ])
            sql = f"SELECT * FROM {table} WHERE {selection_list}"

            val = tuple(query_columns_dict[column_name][1] for column_name in sorted(query_columns_dict.keys()))
            self.mycursor.execute(sql, val)

        result = self.mycursor.fetchall()

        return result

    def insert_single_data(self, table, query_columns_dict):
        column_names = ",".join([f"{column_name}" for column_name in sorted(query_columns_dict.keys())])
        column_holders = ",".join([f"%s" for column_name in sorted(query_columns_dict.keys())])
        sql = f"INSERT INTO {table} ({column_names}) VALUES ({column_holders})"
        print("query_columns_dict",query_columns_dict)
        val = tuple(query_columns_dict[column_name] for column_name in sorted(query_columns_dict.keys()))

        self.mycursor.execute(sql, val)
        self.db_handle.commit()
        print("rowcount",self.mycursor.rowcount)
        return self.mycursor.rowcount

    def insert_multiple_data(self, table, columns, multiple_data):
        column_names = ",".join(columns)
        column_holders = ",".join([f"%s" for column_name in columns])
        sql = f"INSERT INTO {table} ({column_names}) VALUES ({column_holders})"

        self.mycursor.executemany(sql, multiple_data)
        self.db_handle.commit()

        return self.mycursor.rowcount

    def update_single_data(self, table, id,status,time):

        self.mycursor.execute(f"UPDATE {table} SET is_process = {status}, process_time = %s WHERE weighing_no = %s",
                              (time, id))

        self.db_handle.commit()

        return self.mycursor.rowcount
