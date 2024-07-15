# Change Log

### 0.2.0 (2024-07-15)

#### Added
- 🆕 ファイル翻訳APIの新機能を追加。
  - `set_file(path)` で翻訳元のファイルパスを指定し、PID を返す機能。
  - `file_status()` で翻訳状況を確認する機能。
  - `get_file(pid, encoding="utf-8", path=None)` で翻訳済みファイルを取得し、保存する機能。

#### Changed
- 📖 READMEにファイル翻訳APIの使用方法を追記。
  - 各エンドポイントの詳細な説明を追加。
  - 使用例のコードスニペットを含め、実際の利用方法を記述。
