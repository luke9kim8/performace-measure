wget https://www.sqlite.org/2020/sqlite-src-3330000.zip
unzip sqlite-src-3330000.zip
mv sqlite-src-3330000 sqlite333
cd sqlite333
./configure --enable-unicode=ucs4
make -j 4

cp .libs/libsqlite3.so.0.8.6 ./libsqlite3.so.3.33
cp libsqlite3.so.3.33 /usr/lib/x86_64-linux-gnu/
cd ..

wget https://www.sqlite.org/2017/sqlite-src-3180000.zip
unzip sqlite-src-3180000.zip
mv sqlite-src-3180000 sqlite318
cd sqlite318
./configure --enable-unicode=ucs4
make -j 4

cp .libs/libsqlite3.so.0.8.6 ./libsqlite3.so.3.18
cp libsqlite3.so.3.18 /usr/lib/x86_64-linux-gnu/libsqlite3.so.0.8.6
cd ..