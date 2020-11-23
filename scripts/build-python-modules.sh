# wget https://www.python.org/ftp/python/2.7.16/Python-2.7.16.tgz
# tar xzvf Python-2.7.16.tgz
file Python-2.7.16
cd Python-2.7.16
#vim Modules/_sqlite/module.c
sed -i -e "s:PyMODINIT_FUNC init_sqlite3(void):PyMODINIT_FUNC init_sqlite4(void):g" Modules/_sqlite/module.c
sed -i -e "s:Py_InitModule(\"_sqlite3\", module_methods):Py_InitModule(\"_sqlite4\", module_methods):g" Modules/_sqlite/module.c
echo "Checkpoint 001"
cat Modules/_sqlite/module.c

#   => modify
#     PyMODINIT_FUNC init_sqlite3(void)
#     Py_InitModule("_sqlite3", module_methods)
#      to
#     PyMODINIT_FUNC init_sqlite4(void)
#     Py_InitModule("_sqlite4", module_methods)

./configure --enable-unicode=ucs4
make -j 4
cp ./build/lib.linux-x86_64-2.7/_sqlite3_failed.so /usr/lib/python2.7/lib-dynload/_sqlite4.x86_64-linux-gnu.so
#hexedit /usr/lib/python2.7/lib-dynload/_sqlite4.x86_64-linux-gnu.so
sed -i -e "s:libsqlite3.so.0:libsqlite3.so.1:g" /usr/lib/python2.7/lib-dynload/_sqlite4.x86_64-linux-gnu.so
echo "Checkpoint 002"
# cat /usr/lib/python2.7/lib-dynload/_sqlite4.x86_64-linux-gnu.so
#  => modify "libsqlite3.so.0" to "libsqlite3.so.1"
#  => how to use hexedit? https://linux.die.net/man/1/hexedit

#make libsqlite3.so.1 link to /usr/lib/x86_64-linux-gnu/libsqlite3.so.3.27
cd /usr/lib/x86_64-linux-gnu/
ln -s libsqlite3.so.3.27 libsqlite3.so.1

cd /usr/lib/python2.7
cp -r sqlite3 sqlite4
cd sqlite4
sed -i -e "s:from _sqlite3:from _sqlite4:g" dbapi2.py

python /code/sqliteTest.py