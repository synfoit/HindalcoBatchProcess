import os
from datetime import datetime
from database import Database
from icmplib import ping
from database_second_server import DatabaseTwo
from dotenv import load_dotenv

column_compare = {
    'EQUAL_TO': '=',
    'GREATER_THAN': '>',
    'GREATER_THAN_OR_EQUAL_TO': '>=',
    'LESSER_THAN': '<',
    'LESSER_THAN_OR_EQUAL_TO': '<='
}


class BatchModel:
    BATCH_TABLE = 'batches'
    load_dotenv()

    ip = os.getenv('SECOND_SERVER')

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self.host = ping(self.ip, interval=0.2)
        if self.host.is_alive:
            self.db_two = DatabaseTwo(self.ip)

        self._latest_error = ''
        self.time = datetime.now()

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_by_batch_id(self, batch_id):
        query_columns_dict = {
            'id': (column_compare['EQUAL_TO'], batch_id)
        }
        result = self._db.get_single_data(BatchModel.BATCH_TABLE, query_columns_dict)
        return result

    def insert(self, Batch_ID, Batch, Tare_Weight, Gross_Weight, Net_Weight, Ship_Total, time):
        try:
            self.latest_error = ''

            query_columns_dict = {
                'batch_id': Batch_ID,
                'batch': Batch,
                'tare_weight': Tare_Weight,
                'gross_weight': Gross_Weight,
                'net_weight': Net_Weight,
                'ship_total': Ship_Total,
                'time': time

            }
            print("query_columns_dict", query_columns_dict)
            row_count = self._db.insert_single_data(BatchModel.BATCH_TABLE, query_columns_dict)
            print("Data write in 1st DB row_count", row_count)
            query_columns_second_dict = {
                'batch_id': Batch_ID,
                'batch': Batch,
                'tare_weight': Tare_Weight,
                'gross_weight': Gross_Weight,
                'net_weight': Net_Weight,
                'ship_total': Ship_Total,
                'time': time,
                'is_process': True,
                'process_time': time

            }
            row_count_second = self.db_two.insert_single_data(BatchModel.BATCH_TABLE, query_columns_second_dict)
            print("Data write in 2nd DB row_count", row_count_second)

            query_columns_dict_select = {
                'batch_id': (column_compare['EQUAL_TO'], Batch_ID),
                'batch': (column_compare['EQUAL_TO'], Batch),
                'tare_weight': (column_compare['EQUAL_TO'], Tare_Weight),
                'gross_weight': (column_compare['EQUAL_TO'], Gross_Weight),
                'net_weight': (column_compare['EQUAL_TO'], Net_Weight),
                'ship_total': (column_compare['EQUAL_TO'], Ship_Total),
                'time': (column_compare['EQUAL_TO'], time),
            }

            uniq_id = self._db.get_single_data(BatchModel.BATCH_TABLE, query_columns_dict_select)
            print("uniq_id", uniq_id)
            if row_count_second == 1:
                row_update = self._db.update_single_data(BatchModel.BATCH_TABLE, uniq_id[0], True, self.time)
                print("Status Update 1st DB", row_update)

        except Exception as ex:

            print("Exception", ex)
