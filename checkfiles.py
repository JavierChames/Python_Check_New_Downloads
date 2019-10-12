import os.path
import time
import datetime
import mysql.connector

dirpath = os.getcwd()
credentials_file_name = "credentials.txt"
path_file_name = "paths.txt"
query_file_name = "sql_query.sql"
update_db_query_file = "update_sql_query.sql"
host_to_ping = "host_to_ping.txt"


def read_from_paths(file_name):
    with open(file_name) as f:
        lineList = f.read().splitlines()
    f.close
    return lineList


def read_from_file(file_name):
    with open(file_name) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    f.close
    return content


def print_last_modified_time():
    time_stamps = []
    # call to function to read paths from file
    for path in read_from_paths(path_file_name):
        modified_date_time_before_format = time.ctime(os.path.getmtime(path))
        time_stamps.append(str(datetime.datetime.strptime(
            modified_date_time_before_format, "%a %b %d %H:%M:%S %Y")))
    return time_stamps


def read_one_line_from_file(file_name):
    f = open(file_name)
    query = f.readline()
    f.close
    return query


def read_from_db(credentials):

    query = read_one_line_from_file(query_file_name)
    db_credentials = []
    for each_credential in credentials:
        db_credentials.append(each_credential)

    mydb = mysql.connector.connect(
        host=db_credentials[0],
        user=db_credentials[1],
        passwd=db_credentials[2],
        database=db_credentials[3]
    )

    mycursor = mydb.cursor()
    mycursor.execute(query)

    field_names = [i[0] for i in mycursor.description]
    return mycursor.fetchone(), field_names, mycursor, mydb


def check_needed_update(sql_result, files_time_stamps, field_names, mycursor, mydb):
    update_query = read_one_line_from_file(update_db_query_file)
    flag = 0
    sql = list(sql_result)
    for x in range(len(sql)):
        if str(sql[x]) != str(files_time_stamps[x]):
            flag += 1
            update_query_sql = update_query + \
                str(field_names[x]) + " =" + \
                '"{}"'.format(str(files_time_stamps[x]))
            print(update_query_sql)
            mycursor.execute(update_query_sql)
            mydb.commit()
    return flag


def ping_ip():
    if os.system("ping -c 1 " + read_one_line_from_file(host_to_ping)) == 0:
        return True


def run_docker():
    myCmd = 'docker start kodi-docker'
    os.system(myCmd)
    time.sleep(90)
    myCmd = 'docker stop kodi-docker'
    os.system(myCmd)

if ping_ip() == True:
    credentials = read_from_file(credentials_file_name)
    files_time_stamps = print_last_modified_time()
    sql_query_result, field_names, mycursor, mydb = read_from_db(credentials)
    if check_needed_update(sql_query_result, files_time_stamps, field_names, mycursor, mydb):
        run_docker()