import os
from datetime import datetime

# os.system("sudo docker-compose exec mysql-legacy mysql -u mysql -ppassword --version")
# os.system("sudo docker-compose exec mysql-new mysql --version")
my_legacy_docker_header = "sudo docker-compose exec -T mysql-legacy "
my_new_docker_header = "sudo docker-compose exec -T mysql-new "
# os.system("sudo docker-compose exec postgreSQL-new psql --help")
# os.system("sudo docker-compose exec postgreSQL-legacy psql --help")
pg_legacy_docker_header = "sudo docker-compose exec postgreSQL-legacy "
pg_new_docker_header = "sudo docker-compose exec postgreSQL-new "
SQLITE4_DB_DIR = "/home/vagrant/sqlite4db.db"
SQLITE3_DB_DIR = "/home/vagrant/sqlite3db.db"
n = 275
num_map = {}
def select_time_wrap(query, db):
    if db == "my":
        time_query = "select date_format(NOW(3),'%Y-%m-%d %H:%i:%s.%f') \
            as date_val"
        return "%s;%s;%s;" % (time_query, query, time_query)
    elif db == "sq":
        time_query = " select strftime('%Y-%m-%d %H:%M:%f', 'NOW');"
        return "%s;%s;%s;" % (time_query, query, time_query)
    elif db == "pg":
        return "\n select now();%s;select now();\n" % query
    elif db == "cr":
        return query
    else:
        raise NotImplemented

def calctime(header, footer):
    try:
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
    except (AttributeError, SyntaxError):
        return -1.0

def my_get_header_footer(output):
    time_stamps = []
    for line in output.split("\n"):
        if "2020-11-22" in line:
            time_stamps.append(line)
    return time_stamps if len(time_stamps) == 2 else [0.0, 0.0]

def pg_get_header_footer(output):
    time_stamps = []
    for line in output.split("\n"):
        if "2020-11-22" in line:
            time_stamps.append(line[1:])
    return time_stamps if len(time_stamps) == 2 else [0.0, 0.0]


def run_query(num, db, path=None, out_path="out/out.txt"):
    path = '../queries/{}.{}_query'.format(num, db) if path is None else path
    with open(path,'r') as file:
        query = file.read()
        timed_query = select_time_wrap(query, db)
        tmp_query_path= 'tmp/tmp.{}_query'.format(db)
        dump_new_path = "/vagrant/perf-measure-compose/tmp/tmp.{}_new_dump".format(db)
        dump_legacy_path = "/vagrant/perf-measure-compose/tmp/tmp.{}_legacy_dump".format(db)

        if db == 'pg':
            tmp_query_path = "/vagrant/perf-measure-compose/" + tmp_query_path

        with open(tmp_query_path, 'w') as tmp:
            tmp.write(timed_query)
        
        if db == "my":
            print("running my_new")
            os.system(my_new_docker_header + " mysql -uroot -ppassword mysqldb < %s > %s"% (tmp_query_path, dump_new_path))
            print("running my_legacy")
            os.system(my_legacy_docker_header + " mysql -uroot -ppassword mysqldb < %s > %s" % (tmp_query_path, dump_legacy_path))
        elif db == "pg":
            print("running pg_new")
            os.system(pg_new_docker_header+" psql -U postgres -d postgresdb -f %s > %s" % (tmp_query_path, dump_new_path))
            print("running pg_legacy")
            os.system(pg_legacy_docker_header+" psql -U postgres -d postgresdb -f %s > %s" % (tmp_query_path, dump_legacy_path))
        elif db == "sq":
            print("running sq_new")
            os.system("sqlite4 %s '.read %s' > %s" % (SQLITE4_DB_DIR, tmp_query_path, dump_new_path))
            print("running sq_legacy")
            os.system("sqlite3 %s '.read %s' > %s" % (SQLITE3_DB_DIR, tmp_query_path, dump_legacy_path))
   

        exectime_legacy = 0
        exectime_new = 0

        with open(dump_legacy_path, "r") as dump_legacy, open(dump_new_path, 'r') as dump_new:
            output_legacy = dump_legacy.read()
            output_new = dump_new.read()
            if db == "my" or db == "sq":
                header_legacy, footer_legacy = my_get_header_footer(output_legacy)
                header_new, footer_new = my_get_header_footer(output_new)
                exectime_legacy = calctime(header_legacy, footer_legacy)
                exectime_new = calctime(header_new, footer_new)
            elif db == "pg":
                header_legacy, footer_legacy = pg_get_header_footer(output_legacy)
                header_new, footer_new = pg_get_header_footer(output_new)
                exectime_legacy = calctime(header_legacy, footer_legacy)
                exectime_new = calctime(header_new, footer_new)
        
        with open("out/iffy.txt", 'a') as file:
            if exectime_legacy < 0 or exectime_new < 0:
                file.write("{} {} \n".format(db, num))
                return
        timeRatio = 0 if float(exectime_legacy) == 0.0 else float(exectime_new) / float(exectime_legacy) 
        with open("out/ratio.txt", 'a') as file:
            file.write("{} {} {}\n".format(num,db, timeRatio))
        # num, db, legacy version execution time, new version execution time, time difference
        print(timeRatio)
        with open(out_path, 'a') as out:
            if timeRatio > 4.999:
                out.write("{}:{}:{}:{}:{}\n".format(num,db,exectime_legacy, exectime_new, str(timeRatio)))


def get_numbers():
    queries = os.listdir('../queries')
    for query in queries:
        number, db_sql = query.split(".")
        if "_" not in db_sql or number == "list": 
            continue
        db, sql = db_sql.split("_")
        if number not in num_map:
            num_map[number] = [db]
        else:
            num_map[number].append(db)
    with open("num_map.txt", "w") as file:
        for entry in num_map:
            file.write(entry+": "+ str(num_map[entry])+ "\n")

    
def run_multiple_queries(start, end):
    queries = os.listdir('../queries')
    limit_counter = 0
    num_list = list(num_map.keys())
    i = start
    num_list = sorted(num_list, key=lambda num: int(num))
    while (i < end ):
        num = num_list[i]
        for db in num_map[num]:
            if db == "cr":
                continue
            run_query(num, db)
        i+=1
    print("Exited")
            
    

get_numbers()
run_multiple_queries(561, 800)

# run_query(32055, 'my', path="queries/32055.my_query (min)",out_path="out/verification.txt")
