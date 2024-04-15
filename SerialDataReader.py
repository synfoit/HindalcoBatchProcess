import time, logging
import codecs
import serial
from serial import Serial
from datetime import datetime
from threading import Thread
from model import BatchModel

logger = logging.getLogger('app_logger')


class SerialDataReader(Thread):

    def __init__(self, port: str, name: str | None = None):
        super().__init__(name=name)
        self.port = port

    def Convert(self, string):
        li = list(string.split(","))
        return li

    def ReadData(self):
        ser: Serial = None
        try:
            logger.info(f'Connecting on port {self.port}')

            ser = Serial(
                port=self.port,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.SEVENBITS
            )

            ser.isOpen()
            logger.info(f'Port open status: {ser.is_open}')
            print(f'Port open status: {ser.is_open}')

            while True:
                # configure the serial connections (the parameters differs on the device you are connecting to)

                # Reading the data from the serial port. This will be running in an infinite loop.
                bytesToRead = ser.inWaiting()
                data = ser.read(bytesToRead)

                # bytesToRead=b'S2,BCNT  9,G  95,T  5,N  90,Tot  2455!SIDB,START*\n\r'

                if (bytesToRead > 0):
                    logger.info(f'Received {bytesToRead} bytes to process.')
                    d = codecs.decode(data, 'UTF-8')
                    dataInString = str(d)
                    print(f'Received {bytesToRead} bytes to process.')
                    logger.info(f'Data: {dataInString}')
                    print(f'Data: {dataInString}')

                    if (len(dataInString) >= 40):
                        logger.info('Writing data in DB')
                        print('Writing data in DB')
                        now = datetime.now()
                        dataList = self.Convert(dataInString)
                        Batch_ID = dataList[0]
                        Batch = dataList[1].replace('BCNT', '')
                        TareWeigh = dataList[3].replace('T', '')
                        GrossWeight = dataList[2].replace('G', '')
                        NetWeight = dataList[4].replace('N', '')
                        ShipTotal = ''
                        if (Batch_ID == 'S2'):
                            ShipTotal = dataList[5].replace('Tot', '').replace('!SIDB', '')
                            BatchModel().insert(Batch_ID, Batch, TareWeigh, GrossWeight, NetWeight, ShipTotal, now)
                            print("ShipTotal",ShipTotal)
                        if (Batch_ID == 'S1'):
                            ShipTotal = dataList[5].replace('Tot', '').replace('!SIDA', '')
                            BatchModel().insert(Batch_ID, Batch, TareWeigh, GrossWeight, NetWeight, ShipTotal, now)
                            print("ShipTotal", ShipTotal)

                        logger.info('Wrote data in DB')

                time.sleep(1)
        finally:
            if ser and ser.is_open:
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser.close()

    def run(self) -> None:
        while True:
            try:
                self.ReadData()
            except Exception as ex:
                logger.error(f'An error occured on port {self.port}, restarting process.')
                logger.exception(ex)