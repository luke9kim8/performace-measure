import os
from datetime import datetime

print("hey its docker2")
os.system("sudo docker-compose exec mysql-legacy mysql --version")
os.system("sudo docker-compose exec mysql-new mysql --version")
docker_header_legacy = "sudo docker-compose exec mysql-legacy"
docker_header_new = "sudo docker-compose exec mysql-new"
n = 259

def select_time_wrap(query, db):
    if db == "my":
        time_query = "select date_format(NOW(3),'%Y-%m-%d %H:%i:%s.%f') \
            as date_val"
        return "%s;%s;%s;" % (time_query, query, time_query)
    elif db == "sq":
        time_query = " select strftime('%Y-%m-%d %H:%M:%f', 'NOW');"
        return "%s;%s;%s;" % (time_query, query, time_query)
    elif db == "pg":
        return "\o tmp/tmp.pg_dump \n select now();%s;select now();\n" % query
    else:
        raise NotImplemented

def calctime(header, footer):
    htime = header.split("+")[0]
    htime = htime.replace("-04", "")

    ftime = footer.split("+")[0]
    ftime = ftime.replace("-04", "")

    if htime.split("-")[0] == "20":
        htime = "20" + htime
    if ftime.split("-")[0] == "20":
        ftime = "20" + ftime

    hdtime = float(datetime.strptime(
        htime, "%Y-%m-%d %H:%M:%S.%f").strftime('%s.%f'))
    fdtime = float(datetime.strptime(
        ftime, "%Y-%m-%d %H:%M:%S.%f").strftime('%s.%f'))

    elapsed = fdtime - hdtime

    if elapsed > 0:
        return elapsed
    else:
        return 0.001

def my_get_header_footer(output):
    header = output.split("\n")[1]
    footer = output.split("\n")[3]
    return (header, footer)

def pg_get_header_footer(output):
    header = output.split("\n")[2][1:]
    footer = output.split("\n")[11][1:]
    return (header, footer)

def run_query(num, db):
    with open('queries/{}.{}_query'.format(num, db),'r') as file:
        query = file.read()
        timed_query = select_time_wrap(query, db)
        tmp_path = 'tmp/tmp.{}_query'.format(db)

        with open(tmp_path, 'w') as tmp:
            tmp.write(timed_query)
        
        if db == "my":
            os.system("mysql -u mysql -pmysql mysqldb < %s > %s" % (tmp_path, "tmp/tmp.my_dump"))
        elif db == "pg":
            os.system("psql -d postgresdb -f %s" % tmp_path)
        
        with open("tmp/tmp.{}_dump".format(db), "r") as dumpfile:
            output = dumpfile.read()
            if db == "my":
                header, footer = my_get_header_footer(output)
                exectime = calctime(header, footer)
            elif db == "pg":
                header, footer = pg_get_header_footer(output)
                exectime = calctime(header, footer)
            
            


run_query(n, "pg")



# print(query)

# print("Running mysql...")
# os.system("mysql -u mysql -pmysql mysqldb < queries/{}.my_query".format(n))
# print("Running psql...")
# os.system("psql -d postgresdb -f queries/{}.pg_query".format(n))

