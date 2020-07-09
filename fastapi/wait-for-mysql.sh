#!/bin/sh
# wait-for-mysql.sh
# CMD sh /wait-for-mysql.sh HOST USER PASSWORD
# cf. https://qiita.com/shiena/items/47437f4f7874bf70d664

set -e

host="$1"
user="$2"
password="$3"

cmd="from MySQLdb import _mysql; \
  db = _mysql.connect( \
    host='$host', \
    user='$user', \
    passwd='$password' \
  ); \
  print(db)"

echo "Due to mysql sleeping(unhealthy or starting), this container is unavailable. - [wait-for-mysql.sh]"
echo -n "Waiting for mysql container ..."

# -q　オプション: マッチした行を出力させない（quiet） cf. https://it-ojisan.tokyo/grep-q/
until python -c "$cmd" 2>/dev/null | grep -q '_mysql.connection open'
do
        >&2 echo -n "."
        sleep 1
done

>&2 echo " Mysql is starting up! - [wait-for-mysql.sh]"
