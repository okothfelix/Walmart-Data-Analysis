from datetime import datetime
import pytz
from collections import abc
from mysql.connector import connect
import config


def phone_num_checker(number):
    if number.startswith('0'):
        number = '+254' + number[1:]
    elif number.startswith('254'):
        number = '+' + number
    return number


def cur_date_generator():
    cur_date = str(datetime.now(pytz.timezone('Africa/Nairobi')))
    return cur_date[:cur_date.find(" ")]


def cur_day_generator():
    cur_date = str(datetime.now(pytz.timezone('Africa/Nairobi')))
    return cur_date[:cur_date.find(".")]


# update and keep the previous dict values.
def update_dict_section(orig_dict, new_dict):
    for key, val in new_dict.items():
        if isinstance(val, abc.Mapping):
            tmp = update_dict_section(orig_dict.get(key, {}), val)
            orig_dict[key] = tmp
        elif isinstance(val, list):
            orig_dict[key] = (orig_dict.get(key, []) + val)
        else:
            orig_dict[key] = new_dict[key]
    else:
        return orig_dict


def execute_sql(statement, result_flag=False, commit_flag=False):
    conn = connect(**config.mysql_config)
    c = conn.cursor()
    c.execute(statement)
    if result_flag:
        result_set = c.fetchall()
        conn.close()
        return True, result_set
    if commit_flag:
        conn.commit()
        conn.close()
        return True,
