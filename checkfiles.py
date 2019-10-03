import os.path
import time
import datetime
import mysql.connector
credentials_file_name = "credentials.txt"
path_file_name = "paths.txt"
query_file_name = "sql_query.sql"
update_db_query_file = "update_sql_query.sql"


def read_from_paths(file_name):
    locations = {}
    with open(file_name) as f:
        for line in f:
            (key, val) = line.split()
            locations[key] = val
    return locations


def read_from_file(file_name):
    with open(file_name) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    f.close
    return content


def print_last_modified_time():
    time_stamps = []
    # call to function to read paths from file
    for path in read_from_paths(path_file_name).values():
        modified_date_time_before_format = time.ctime(os.path.getmtime(path))
        time_stamps.append(str(datetime.datetime.strptime(
            modified_date_time_before_format, "%a %b %d %H:%M:%S %Y")))
    return time_stamps


def read_one_line_from_file(file_name):
    f = open(file_name)
    query = f.readline()
    return query


def read_from_db(credentials):
    query = read_one_line_from_file(query_file_name)
    update_query = read_one_line_from_file(update_db_query_file)
    db_credentials = []
    for each_credential in credentials:
        db_credentials.append(each_credential)

    mydb = mysql.connector.connect(
        host="localhost",
        user=db_credentials[0],
        passwd=db_credentials[1],
        database=db_credentials[2]
    )

    mycursor = mydb.cursor()
    mycursor.execute(query)
    myresult = mycursor.fetchone()

    y = 0
        
    for x in myresult:
        if str(myresult[y]) != modified_time_of_files[y]:
            column = mycursor.description[y][0]
            update_query = update_query + column + " =" + \
                '"{}"'.format(
                    modified_time_of_files[y]) + " where " + column + " = " + '"{}"'.format(str(myresult[y]))
            mycursor.execute(update_query)
            mydb.commit()
        y+=1

credentials = read_from_file(credentials_file_name)
modified_time_of_files = (print_last_modified_time())
read_from_db(credentials)
