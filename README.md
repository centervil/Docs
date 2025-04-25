# Docs リポジトリ

このリポジトリには、研究資料、開発記録、技術文書などが含まれています。

## 研究資料変換システム

研究資料をnote投稿用のMarkdownに自動変換するシステムを実装しています。

### 使用方法

1. 研究資料を `research/` ディレクトリに `.md` ファイルとして保存します
2. 変更をコミットしてプッシュします
3. GitHub Actionsによって自動的に変換処理が実行されます
4. 変換されたMarkdownファイルは `note-articles/` ディレクトリに保存されます
5. 手動でnoteにログインして、生成されたMarkdownファイルの内容をコピー＆ペーストして投稿します

### 手動での変換実行

ローカルで変換処理を実行することもできます：

```bash
# APIキーを設定（オプション、設定しない場合はモック処理になります）
export OPENROUTER_API_KEY=your_api_key_here

# 変換処理を実行
python note-converter/scripts/note_converter.py research/your_file.md
```

### CI/CDパイプライン

`research/` ディレクトリ内のMarkdownファイルが変更されると、GitHub Actionsワークフローが起動します：

1. 変更されたMarkdownファイルを検出
2. OpenRouter API（設定されている場合）を使ってLLMによる文章整形を実行
3. 整形されたMarkdownを `note-articles/` ディレクトリに保存
4. 変更をコミットしてリポジトリにプッシュ

## Zenn CLI

* [📘 使い方](https://zenn.dev/zenn/articles/zenn-cli-guide)