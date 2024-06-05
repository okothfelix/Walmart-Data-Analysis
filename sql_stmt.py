import hashlib
import config


# user login statements
user_login_1 = "Select authentication_string from Analytics_Users where address = '{address}'"
user_login_2 = "Select SHA2('" + hashlib.sha3_512(eval("b'{password}'")).hexdigest() + "', 256)"
user_login_3 = "Update Analytics_Users set last_updated = '" + config.cur_day_generator() + "' where address = '{address}'"

