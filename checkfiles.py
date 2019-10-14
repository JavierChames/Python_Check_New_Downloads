import os.path
import time
import datetime
import mysql.connector

credentials_file_name = "credentials.txt"
path_file_name = "paths.txt"
host_to_ping = "host_to_ping.txt"


def read_from_file(file_name):
    with open(file_name,'r') as f:
        file_content = f.read().splitlines()
    return file_content

def get_modified_time():
    time_stamps = []
    # call to function to read paths from file
    for path in read_from_file(path_file_name):
        modified_date_time_before_format = time.ctime(os.path.getmtime(path))
        time_stamps.append(datetime.datetime.strptime(
            modified_date_time_before_format, "%a %b %d %H:%M:%S %Y"))
    return time_stamps

def read_from_db(credentials):

    query = "SELECT * FROM Files"
    db_credentials = []
    mydb = mysql.connector.connect(
    host=credentials[0],
    user=credentials[1],
    passwd=credentials[2],
    database=credentials[3]
    )
    mycursor = mydb.cursor()
    mycursor.execute(query)
    field_names = [i[0] for i in mycursor.description]
    return mycursor.fetchone(), field_names, mycursor, mydb

def check_needed_update(sql_result, files_time_stamps, field_names, mycursor, mydb):
    flag = 0
    sql_result = list(sql_result)
    for x in range(len(sql_result)):
        if str(sql_result[x]) != str(files_time_stamps[x]):
            flag += 1
            update_query_sql = "UPDATE Files SET " + field_names[x] + " =" + '"{}"'.format((files_time_stamps[x]))
            mycursor.execute(update_query_sql)
            mydb.commit()
            mycursor.close()
            mydb.close()
    return flag

def ping_ip():
    return os.system("ping -c 1 " + ''.join(read_from_file(host_to_ping))) == 0

def run_docker():
    myCmd = 'docker start kodi-docker'
    os.system(myCmd)
    time.sleep(60)
    myCmd = 'docker stop kodi-docker'
    os.system(myCmd)

if __name__ == '__main__':
    if ping_ip() == True:
        credentials = read_from_file(credentials_file_name)
        files_time_stamps = get_modified_time()
        sql_query_result, field_names, mycursor, mydb = read_from_db(credentials)
        if check_needed_update(sql_query_result, files_time_stamps, field_names, mycursor, mydb):
            run_docker()