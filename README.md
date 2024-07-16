# textra-api-wrapper

本APIラッパーは、[みんなの自動翻訳＠TexTra®](https://mt-auto-minhon-mlt.ucri.jgn-x.jp/content/menu/)を利用してテキスト翻訳を行うためのPythonラッパーです。

## 特徴
- 簡単にAPIを利用して翻訳を実行できます。
- Wikipediaやオープンソースソフトウェアのドキュメントの翻訳に適しています。

## 注意事項
- 本APIラッパーは「みんなの自動翻訳＠TexTra®」の利用規約に基づき、商用目的での利用を禁止しています。
- 不適切な利用が発見された場合、APIの利用が制限されることがあります。
- 利用回数に上限が設けられる場合があります。
- サービス提供期間は保証されていません。
- 入力されたテキストや用語はNICTのサーバーに記録されることがあります。個人情報や機密情報を入力しないようお願いします。

## インストール

```bash
pip install textra-api-wrapper
```

## Usage

### 環境変数の設定

利用の前に以下の環境変数を設定してください。

- `TEXTRA_LOGIN_ID`: ログインID
- `TEXTRA_API_KEY`: API_KEY
- `TEXTRA_API_SECRET`: API_SECRET

ターミナルから設定する例を示します。

```bash
export TEXTRA_LOGIN_ID='your_login_id'
export TEXTRA_API_KEY='your_api_key'
export TEXTRA_API_SECRET='your_api_secret'
```

利用中のOSやシェルによって設定方法は異なりますのでご注意ください。

### 使用例

テストコードをご参照ください。

```python
from textra_api_wrapper import APIClient


def test_client():
    client = APIClient()
    text = "Hello everyone. My name is ｟John.｠"
    res = client.translate(text)

    expected = "皆さんこんにちは、John.と申します。"
    assert res.text == expected
    assert res.original_text == text
    assert res.information["text-s"] == text
    assert res.information["text-t"] == expected
    assert (
        res.request_url
        == "https://mt-auto-minhon-mlt.ucri.jgn-x.jp/"
    )
```

- `APIClient()`により生成されるインスタンスは、英語から日本語への翻訳となります。
- 翻訳不要記号で囲むことで原文をそのまま出力します。例: `｟John.｠`
- 言語の指定は`APIClient(source_lang="ja", target_lang="en")`などとします。

```python
def test_ja_to_en():
    client = APIClient(source_lang="ja", target_lang="en")
    text = "こんにちは、皆さん。私の名前は｟タロー｠です"
    res = client.translate(text)

    expected = "Hi everyone. My name is タロー."
    assert res.text == expected
    assert res.original_text == text
    assert (
        res.request_url
        == "https://mt-auto-minhon-mlt.ucri.jgn-x.jp/api/mt/generalNT_ja_en/"
    )
```

### ファイル翻訳

ファイル翻訳APIは3つのエンドポイントがあります。登録 (set)、確認 (status)、取得 (get) です。set を行うと API サーバで翻訳が実行されますが、ファイル単位なのである程度の時間がかかります。そのため、登録時には PID のみが返ります。status は翻訳状況の確認、get でファイルを取得できます。

#### `set_file(path)`

`path` で翻訳元のファイルパスを指定します。実行時点では処理が完了していない可能性があります。
APIResponseParserのインスタンスが返ります。

APIの仕様により、ファイルの拡張子は限定されています。サポート外の拡張子は内部で`.txt`に変換されます。

```python
client = APIClient()
original_filepath = "tests/example_file.cfg"
sample = client.set_file(original_filepath)

sample.get("pid") # 12345
sample.request["title"] # "example_file"
```

titleはファイル名から拡張子を除いたものになります。

#### `file_status()`

ファイル翻訳の状況を確認できます。`state` は状態を表します。

- -2: 失敗
- 0: 待機中
- 1: 処理中
- 2: 完了

```python
client = APIClient()
sample = client.file_status()
sample.get('list')
# Example
# [
#     {
#         'id': 71204,
#         'register': '2024-07-15 09:49:24',
#         'state': 2,
#         'title': 'test_file',
#     },
#     {
#         'id': 71181,
#         'register': '2024-07-14 15:19:50',
#         'state': 2,
#         'title': 'README_en_t',
#     },
# ]

sample.get_status({"id": 71204})
# {
#     'id': 71204,
#     'register': '2024-07-15 09:49:24',
#     'state': 2,
#     'title': 'test_file',
# }
```

#### `get_file(pid, encoding="utf-8", path=None)`

API サーバから翻訳済みのファイルを取得して内容を返します。`path` を指定すると保存します。

- `pid`: ファイル翻訳ID
- `encoding` (オプション): デフォルトでは `utf-8`
- `path` (オプション): 翻訳後のファイルを保存する場所

```python
def test_get_file():
    client = APIClient()
    path = "tests/test_file_result.txt"
    res = client.get_file(pid=71204, path=path)

# Example:
# "ハイテク大手、革新的なAIツールを発表"
```

## License

本APIラッパーはMITライセンスにより提供されますが、利用には[みんなの自動翻訳＠TexTra®](https://mt-auto-minhon-mlt.ucri.jgn-x.jp/content/policy/)の利用規約に従う必要がありますのでご注意ください。
