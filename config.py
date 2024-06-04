from datetime import datetime
import pytz

mysql_config = {
    'host': '127.0.0.1',
    'user': 'beemulti_admin',
    'password': 'Obierofelix_1',
    'database': 'beemulti_BeeMultiscent'
}


def cur_date_generator():
    cur_date = str(datetime.now(pytz.timezone('Africa/Nairobi')))
    return cur_date[:cur_date.find(" ")]


def cur_day_generator():
    cur_date = str(datetime.now(pytz.timezone('Africa/Nairobi')))
    return cur_date[:cur_date.find(".")]