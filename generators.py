from datetime import datetime
import pytz
from collections import abc
from mysql.connector import connect


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


mysql_config = {
    'host': '127.0.0.1',
    'user': 'beemulti_admin',
    'password': 'Obierofelix_1',
    'database': 'beemulti_BeeMultiscent'
}


def connect_to_mysql():
    conn = connect(**mysql_config)
    return conn


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


def session_details_section(session_id):
    conn = connect_to_mysql()
    if conn:
        c = conn.cursor(buffered=True)
        c.execute("Select address from BeeMultiscent_Sessions where session_code = '" + session_id + "'")
        address = c.fetchone()[0]
        conn.close()
        # return True/False/None (Flag to check on the password expiration, none is to do nothing), address, name, account_type(user/ administrator)
        return True, '', address


def session_update_section(session_id, address, user_type):
    conn = connect_to_mysql()
    if conn:
        c = conn.cursor(buffered=True)
        cur_date = cur_day_generator()
        sql_stmt = "Insert into BeeMultiscent_Sessions (session_code, address, user_type, date_created, last_update)" " values(%s, %s, %s, %s, %s)"
        data = (session_id, address, user_type, cur_date, cur_date)
        try:
            c.execute(sql_stmt, data)
        except Exception as e:
            if str(e)[:str(e).find(" ")] == "1146":
                c.execute(
                    "Create table BeeMultiscent_Sessions(session_id int not null primary key auto_increment, session_code varchar(20) not null, address varchar(50) not null, user_type tinyint not null, date_created timestamp not null, last_update timestamp not null, unique key codes (session_code))")
                c.execute(sql_stmt, data)
            elif str(e)[:str(e).find(" ")] == "1062":
                # checking if 15 minutes has elapsed
                c.execute("Select last_update from BeeMultiscent_Sessions where session_code = '" + session_id + "'")
                last_update = c.fetchone()[0]
                c.execute("Select date_add('" + str(last_update) + "', interval 15 minute)")
                new_date = c.fetchone()[0]
                conn.close()
                return True
                # if new_date >= datetime.now(pytz.timezone('Africa/Nairobi')):
                #     db.close()
                #     return False
                # c.execute("Update sessions set last_update = '" + cur_date + "' where session_id = '" + session_id + "'")
            else:
                print(e)
                conn.close()
                return
        conn.commit()
        conn.close()
        return True


def user_details_section(session_id):
    conn = connect_to_mysql()
    if conn:
        c = conn.cursor(buffered=True)
        cur_day = cur_day_generator()
        sql_stmt = "Insert into BeeMultiscent_Sessions (session_code, date_created, last_update)" " values (%s, %s, %s)"
        data = (session_id, cur_day, cur_day)
        try:
            c.execute("Select address, user_type from BeeMultiscent_Sessions where session_code = '" + session_id + "'")
            result_set = c.fetchone()
        except TypeError:
            c.execute(sql_stmt, data)
            result_set = ("", 100)
        except Exception as e:
            if str(e)[:str(e).find(" ")] == "1146":
                c.execute(
                    "Create table BeeMultiscent_Sessions(session_id int not null primary key auto_increment, session_code varchar(20) not null, address varchar(50) not null default '', user_type tinyint not null default 100, date_created timestamp not null, last_update timestamp not null, unique key codes (session_code))")
                c.execute(sql_stmt, data)
                result_set = ('', 100)
            else:
                print(e)
                conn.close()
                return
        try:
            if result_set[1] == 0:
                c.execute("Select user_id from BeeMultiscent_Users where address = '" + result_set[0] + "'")
                user_type = 0
                sub_set = c.fetchone()[0]
            elif result_set[1] == 3:
                c.execute("Select admin_id from BeeMultiscent_Administrators where address = '" + result_set[0] + "'")
                user_type = 3
                sub_set = c.fetchone()[0]
            else:
                user_type = 100
                sub_set = ''
            c.execute(
                "Update BeeMultiscent_Sessions set last_update = '" + cur_day + "' where session_code = '" + session_id + "'")
        except TypeError:
            try:
                c.execute(sql_stmt, data)
                user_type = 100
                sub_set = ''
                result_set = ("", 100)
            except Exception as e:
                print(e)
                conn.close()
                return

        conn.commit()
        conn.close()
        return user_type, sub_set, result_set[0]


def cur_user_details(session_id):
    conn = connect_to_mysql()
    if conn:
        c = conn.cursor(buffered=True)
        c.execute("Select address, user_type from BeeMultiscent_Sessions where session_code = '" + session_id + "'")
        result_set = c.fetchone()
        if result_set[1] == 0:
            c.execute("Select user_id, first_name from BeeMultiscent_Users where address = '" + result_set[0] + "'")
            result = c.fetchone()
        else:
            c.execute(
                "Select admin_id, first_name from BeeMultiscent_Administrators where address = '" + result_set[0] + "'")
            result = c.fetchone()
        conn.close()
        return result[1], result_set[0], result[0]


def cur_user_logout(session_id):
    conn = connect_to_mysql()
    if conn:
        c = conn.cursor(buffered=True)
        c.execute("Update BeeMultiscent_Sessions set user_type = 100 where session_id = '" + session_id + "'")
        conn.commit()
        conn.close()
