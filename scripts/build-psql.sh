sudo apt-get install wget ca-certificates
sudo echo "hey"
sudo apt-get clean
sudo apt-get install gnupg -y
sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
sudo apt-get clean
sudo apt-get update

sudo apt-get install postgresql-12 postgresql-9.6 postgresql-contrib -y
sudo echo "check001"
sudo cat /etc/postgresql/12/main/postgresql.conf

sudo sed -i -e "s:port = 5434:port = 5435:g" /etc/postgresql/12/main/postgresql.conf
sudo cat /etc/postgresql/12/main/postgresql.conf
sudo echo "check002"
sudo pg_ctlcluster 9.6 main start
sudo echo "check003"
sudo pg_ctlcluster 12 main start
sudo echo "check004"
sudo netstat -napt |grep "5435\|5432"

sudo -u postgres createuser -p 5432 -s $(whoami); createdb -p 5432 $(whoami)
sudo -u postgres createuser -p 5435 -s $(whoami); createdb -p 5435 $(whoami)

sudo -u postgres psql -p 5432 -U postgres -d postgres -c "ALTER USER postgres PASSWORD 'mysecretpassword';"
sudo -u postgres psql -p 5435 -U postgres -d postgres -c "ALTER USER postgres PASSWORD 'mysecretpassword';"
