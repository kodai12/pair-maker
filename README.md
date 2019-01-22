# ペアプロ時のペア決めがめんどくさい時に使うといいかも?

## 概要
ペアプロの組み合わせをランダムに作成してslack通知してくれます

## 注意点
- 個人用なので汎用的では全くありません:pray:
- サーバーレスっぽいファイル構成ですが結果的にローカルで動かす形になりました

## pre-require
1. `settings.csv`を作成

ex.
```csv
id,name,skip_days
1,test1,"3,4"
2,test2,""
3,test3,"1"
```

- skip_days: 出張などで順番を飛ばしたい曜日が事前にわかってる場合は設定できる(0~6の間で)
  - NOTE: ダブルクォートで囲ってスキップしたい曜日の番号をカンマ区切りで入力する
  - 曜日の対応は以下
    - 0: 月曜
    - 1: 火曜
    - 2: 水曜
    - 3: 木曜
    - 4: 金曜
    - 5: 土曜
    - 6: 日曜

2. `history.csv`を作成, ここを参照して次のペアを作るが最初はなんでもよければ以下のように適当な順番で作っておく

ex.
```csv
id
1,
2,
3
```

3. `.envrc.template`を参考に`.envrc`を作成
  - PYTHONPATH: `プロジェクトまでのパス/pair_maker/lambdalayer`
  - SLACK_WEBHOOK_URL: [https://qiita.com/kakiuchis/items/1d9ade2ef83709209dc4](https://qiita.com/kakiuchis/items/1d9ade2ef83709209dc4)とか適当に参考にして取得しておく
  - SETTINGS_CSV_FILE: 上で作った`settings.csv`を設定
  - INDEX_HISTORY_CSV_FILE: 上で作った`history.csv`を設定
  - SLACK_NOTIFY_TITLE: お好みで
  - SLACK_NOTIFY_USERNAME: お好みで
  - SLACK_NOTIFY_ICON: お好みで

4. `sh ./build.sh`を実行

## 実行
`python handler.py`

cronとかで定期実行するようにすれば毎朝ペアプロの組み合わせを通知してくれます:muscle:
