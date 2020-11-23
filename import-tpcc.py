import os

# os.system("sudo docker-compose exec mysql-legacy mysql > ALTER USER 'mysql'@'localhost' IDENTIFIED BY 'mysql'")
# os.system("sudo docker-compose exec mysql-legacy mysql -uroot -ppassword -e 'create database mysqltest'")
# os.system("sudo docker-compose exec mysql-legacy mysql -uroot -ppassword mysqltest -e 'CREATE TABLE recipes (recipe_id INT NOT NULL, recipe_name VARCHAR(30) NOT NULL, PRIMARY KEY (recipe_id), UNIQUE (recipe_name));'")
# os.system("sudo docker-compose exec mysql-legacy mysql -uroot -ppassword mysqltest -e 'INSERT INTO recipes (recipe_id, recipe_name) VALUES (1,\"Tacos\"), (2,\"Tomato Soup\"), (3,\"Grilled Cheese\");'")
# os.system("sudo docker-compose exec mysql-legacy mysql -uroot -ppassword mysqltest -e 'select * from recipes'")
# os.system("sudo docker-compose exec mysql-legacy mysql -uroot -ppassword -e 'drop database mysqltest'")
"""
mysql -u mysql -pmysql -e 'drop database mysqldb;'
mysql -u mysql -pmysql -e 'create database mysqldb;'

cat tpcc_mysql.sql|grep -v "TRANSACTION\|COMMIT" > tpcc_mysql2.sql
mysql -u mysql -pmysql mysqldb < transform/sql_ex/tpcc_mysql2.sql
"""
# os.system("sudo docker-compose exec mysql-legacy mysql -uroot -ppassword -e 'drop database mysqldb;'")
# os.system("sudo docker-compose exec mysql-legacy mysql -uroot -ppassword -e 'create database mysqldb;'")
# os.system("cat tpcc/tpcc_my.sql|grep -v \"TRANSACTION\|COMMIT\" > tpcc/tpcc_my2.sql")
# os.system("sudo docker-compose exec -T mysql-legacy mysql -uroot -ppassword mysqldb < tpcc/tpcc_my.sql")
# os.system("sudo docker-compose exec mysql-new mysql -uroot -ppassword -e 'USE mysqldb; SHOW TABLES;'")
# os.system("sudo docker-compose exec mysql-new mysql -uroot -ppassword -e 'SHOW TABLES FROM mysqldb;'")
# os.system("sudo docker-compose exec mysql-new mysql -uroot -ppassword -e 'USE mysqldb; CREATE TABLE IF NOT EXISTS tasks (task_id INT AUTO_INCREMENT PRIMARY KEY);'")
os.system("sudo docker-compose exec mysql-legacy mysql -uroot -ppassword -e 'USE mysqldb; SHOW TABLES;'")
# os.system("sudo docker-compose exec mysql-new mysql -uroot -ppassword -e'USE mysqldb; SHOW TABLES'")
# os.system("sudo docker-compose exec mysql-new    mysql -uroot -ppassword -e 'SELECT TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = \"mysqldb\";'")
# os.system("sudo docker-compose exec mysql-legacy mysql -uroot -ppassword -e 'SELECT TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = \"mysqldb\";'")
# os.system("sudo docker-compose exec mysql-legacy mysql -uroot -ppassword -e 'USE mysqldb; CREATE TABLE IF NOT EXISTS chores (task_id INT AUTO_INCREMENT PRIMARY KEY);'")
# os.system("sudo docker-compose exec mysql-legacy mysql -uroot -ppassword -e'USE mysqldb; SHOW TABLES'")
# os.system("sudo docker-compose exec mysql-new mysql -uroot -ppassword -e'USE mysqldb; SHOW TABLES'")

# os.system("sudo docker-compose exec mysql-new mysql -uroot -ppassword -e 'drop database mysqldb;'")
# os.system("sudo docker-compose exec mysql-new mysql -uroot -ppassword -e 'create database mysqldb;'")
# os.system("sudo docker-compose exec -T mysql-new mysql -uroot -ppassword mysqldb < tpcc/tpcc_my2.sql")
"""
psql -c 'drop database postgresdb;'
psql -c 'create database postgresdb;'
psql -d postgresdb -f transform/sql_ex/tpcc_postgres.sql
"""

# os.system("sudo docker-compose exec postgreSQL-legacy psql -U postgres -c 'drop database postgresdb;'")
# os.system("sudo docker-compose exec postgreSQL-legacy psql -U postgres -c 'create database postgresdb;'")
# os.system("sudo docker-compose exec postgreSQL-legacy psql -U postgres -d postgresdb --file=-")





