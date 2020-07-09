#!/bin/sh
# wait-for-kibana.sh

# `-e`: "errexit" = パイプやサブシェルで実行したコマンドが1つでもエラーになったら直ちにシェルを終了する
# cf. https://bit.ly/37IF4pS
set -e

host="$1"

echo "Due to Kibana sleeping(unhealthy or starting), this container is unavailable. - [wait-for-kibana.sh]"
echo -n "Waiting for Kibana ..."

# until + curlでの繰り返し試行 cf. https://bit.ly/3fu3eXI
# `>&2`: 標準エラー出力（ファイルディスクリプタ） cf. https://bit.ly/3hE1Qns
until curl --silent --output /dev/null --write-out 'HTTP %{http_code}' http://$host/api/status | grep "HTTP 200"
do
  >&2 echo -n "."
  sleep 5
done

>&2 echo " Kibana is starting up! - [wait-for-kibana.sh]"
