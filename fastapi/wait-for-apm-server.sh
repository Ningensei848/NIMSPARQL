#!/bin/sh
# wait-for-apm-server.sh

# `-e`: "errexit" = パイプやサブシェルで実行したコマンドが1つでもエラーになったら直ちにシェルを終了する
# cf. https://bit.ly/37IF4pS
set -e

host="$1"

echo "Due to APM-Server sleeping(unhealthy or starting), this container is unavailable. - [wait-for-apm-server.sh]"
echo -n "Waiting for APM-Server ..."

# `>&2`: 標準エラー出力（ファイルディスクリプタ） cf. https://bit.ly/3hE1Qns
until curl --silent --output /dev/null --write-out 'HTTP %{http_code}' http://$host/ | grep "HTTP 200"
do
  >&2 echo -n "."
  sleep 5
done

>&2 echo " APM-Server is starting up! - [wait-for-apm-server.sh]"
