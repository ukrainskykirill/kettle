import os
from datetime import datetime
import threading
import time

from dotenv import load_dotenv

from sqllite_keetle import connection, cursor, insert_with_param
from loggin import logger

load_dotenv()

time_of_boiling = int(os.getenv('TIME', 10))
temp = int(os.getenv('TEMP', 100))
litr = float(os.getenv('LITR', 1.0))


class Teapot:
    def __init__(self):
        self.state = 'off'
        self.water = 0.0
        self.temp_of_water = 0

    def check_mode(self):
        if temp == 100:
            self.boil()
        else:
            self.warm_up()

    def save_to_db(self):
        logger.info('save info in db')
        date = datetime.now().date()
        data_tuple = (self.water, self.temp_of_water, self.state, date)
        cursor.execute(insert_with_param, data_tuple)
        connection.commit()
        cursor.close()

    def done(self):
        if temp != 100:
            logger.info('kettle hot')
            self.state = 'hot'
            print(f'состояние чайника - {self.state}')
            self.temp_of_water = temp
            self.save_to_db()
        else:
            logger.info('kettle boiled')
            self.state = 'boiled'
            print(f'состояние чайника - {self.state}')
            self.temp_of_water = 100
            self.save_to_db()

    def stop(self, timer: threading.Timer):
        res = input('остановить чайник >>>')
        if res == 'stop':
            logger.warning('kettle was interrupted')
            if self.temp_of_water > 0:
                timer.cancel()
                self.state = 'interrupted'
                print(f'состояние чайника - {self.state}')
                self.save_to_db()
        elif res == 'off':
            logger.info('kettle off')
            self.state = 'off'
            print(f'состояние чайника - {self.state}')

    def temp_check(self, timer):
        logger.info('kettle working')
        while self.temp_of_water < temp-10:
            if timer.is_alive():
                if temp == 100:
                    time.sleep(1)
                    self.temp_of_water += temp/time_of_boiling
                    print(f'температра воды {self.temp_of_water} С')
                else:
                    time.sleep(1)
                    self.temp_of_water += 100 / time_of_boiling
                    print(f'температра воды {self.temp_of_water} С')
            else:
                self.temp_of_water = 0
                break

    def boil(self):
        logger.info('kettle will be boiled')
        ts = threading.Timer(time_of_boiling, self.done)
        th = threading.Thread(target=self.temp_check, args=(ts,))
        ts.start()
        th.start()
        self.stop(ts)

    def warm_up(self):
        logger.info('kettle will be hot')
        ts = threading.Timer(temp * time_of_boiling / 100, self.done)
        th = threading.Thread(target=self.temp_check, args=(ts,))
        ts.start()
        th.start()
        self.stop(ts)

    def kettle_on(self):
        self.state = 'on'
        print(f'состояние чайника - {self.state}')
        logger.info('kettle on')
        self.water = float(input(f"налейте воды (от 0.0 до {litr}) >>> "))
        if 0.0 < self.water <= litr:
            self.check_mode()
        else:
            self.water = float(input(f"налейте воды (от 0.0 до {litr}) >>> "))


if __name__ == '__main__':
    k = Teapot()
    k.kettle_on()
