# Tabegle

## 概要

Googleと食べログのレビューを比較できるサービスです．

また，それぞれのサービスから総合的なおすすめ度を算出しています．

[Tabegle](https://tabegle.tk)
アクセスできない場合は
[こちら](https://tabegle.netlify.app)

## 機能

### 検索

エリアやジャンルからお店を検索することができます．

![https://user-images.githubusercontent.com/47177922/100213243-bde9ba80-2f51-11eb-8f76-e852606c7f72.png](https://user-images.githubusercontent.com/47177922/100213243-bde9ba80-2f51-11eb-8f76-e852606c7f72.png)

### 並び替え

食べログ，Google，総合おすすめ度それぞれで点数が高い順に並べ替えることができます．

![https://user-images.githubusercontent.com/47177922/100213366-de197980-2f51-11eb-8e51-c98ef8e32b52.png](https://user-images.githubusercontent.com/47177922/100213366-de197980-2f51-11eb-8e51-c98ef8e32b52.png)

### Keep

気になったお店は，Keepしてあとから見返すことができます．

![https://user-images.githubusercontent.com/47177922/100213456-fab5b180-2f51-11eb-8ef1-38be4957279d.png](https://user-images.githubusercontent.com/47177922/100213456-fab5b180-2f51-11eb-8ef1-38be4957279d.png)

### ログイン

Keepを使用するためのログイン機能です．

![https://user-images.githubusercontent.com/47177922/100213497-0acd9100-2f52-11eb-8f13-ffb5b6a0d5c1.png](https://user-images.githubusercontent.com/47177922/100213497-0acd9100-2f52-11eb-8f13-ffb5b6a0d5c1.png)

## ローカルでの実行
Google Places APIキーを取得し，`PLACE_API_KEY`として環境変数に設定してください．

ローカル用設定ファイルを作成してください`tabegle/local_settings.py`．
```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEBUG = True

```
```bash
# 依存関係の解決
$ pip install -r requirements.txt

# DBのマイグレーション
$ python manage.py migrate

# エリア・カテゴリ情報の登録
$ python manage.py update_place data/place.csv
$ python manage.py update_category data/category.csv

$ python manage.py runserver
```