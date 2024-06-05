import generators
import sql_stmt


def user_login(username, password):
    try:
        p_word = generators.execute_sql(sql_stmt.user_login_1.format(address=username), result_flag=True)[1][0][0]
    except TypeError:
        return False
    except Exception as e:
        return False
    user_password = generators.execute_sql(sql_stmt.user_login_2.format(password=password), result_flag=True)[1][0][0]
    if p_word == user_password:
        sub_set = generators.execute_sql(sql_stmt.user_login_3.format(address=username), result_flag=False, commit_flag=True)
        return sub_set[0]
    return False


def session_update_section(password):
    pass


def user_logout(session_id):
    pass
