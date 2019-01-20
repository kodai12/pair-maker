# ペアプロ用のペア決めがめんどくさい時に使うといいかも?

## 注意点
- 6人以上に対応してません:pray:
- 個人用なので汎用的では全くありません:pray:

## pre-require
1. `settings.csv`を作成
```
ex.
id,name,skip_days
1,test1,"3,4"
2,test2,""
```
skip_days: 出張などで順番を飛ばしたい曜日が事前にわかってる場合は設定できる(0~6の間で)
2. `history.csv`を作成, 中身は何も書かなくて良い
3. `.envrc.template`を参考に`.envrc`を作成
  - SLACK_WEBHOOK_URL: `https://qiita.com/kakiuchis/items/1d9ade2ef83709209dc4`とか適当に参考して取得しておく
  - SETTINGS_CSV_FILE: 上で作った`settings.csv`を設定
  - INDEX_HISTORY_CSV_FILE: 上で作った`history.csv`を設定
4. `sh ./build.sh`を実行
