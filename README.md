# NIMSPARQList

## TODO:

- syntax ハイライトをどうにかしたい
- debounce from lodash
- 登録フォームの実装（SPARQLet）
- 登録フォームの実装（keyword？）
- ORMをDjangoで置き換え
- MySQL client を「mysql connector/python」に変更
- MySQLコンテナのSSL通信を確立
- clientの通信プラグインを「caching_sha2_password」に変更（よりセキュアに）
- MySQLのログを永続化（コンテナ外部に吐き出させる）
- es の操作について，`curd.py` に移動させる
- `create` なのか `edit`なのか，そしてそれを同一コンポーネントで識別して対応する
-  submitSparqletにてエラーが帰ったときの例外処理，およびその場合の挙動を変更する
