## OASIS：noteに記事を投稿できるPythonアプリケーションの概要

OASIS（Optimized Article Sorting Intelligent System）は、Markdownファイルからnoteをはじめとする複数のプラットフォーム（WordPress、Qiita、Zennなど）へ記事投稿を自動化できるPython製のアプリケーションです[^1_1][^1_2][^1_4]。

---

**主な特徴**

- Markdownファイルを元に、note・Qiita・WordPress・Zennへ記事を同時投稿可能[^1_2][^1_4]。
- コマンドライン操作だけでなく、Web UI（v0.8.0以降）からも直感的に操作可能[^1_4]。
- LLM（大規模言語モデル）を活用した自動タグ・カテゴリ提案や、サムネイル画像自動アップロードなどの便利機能も搭載[^1_1]。
- 投稿先のプラットフォームはオプションで柔軟に選択できる[^1_2][^1_4]。

---

## インストール方法

1. Python（3.7以上推奨）をインストール
2. 以下のコマンドでOASIS本体をインストール

```
pip install -U oasis-article
```

---

## 使い方

**コマンドラインからの投稿例**

Markdownファイルが入ったフォルダを指定し、投稿先プラットフォームをオプションで選択します。

```
oasis /path/to/your/folder --qiita --note --wp --zenn
```

この例では、指定フォルダ内のMarkdown記事をQiita、note、WordPress、Zennへ同時投稿します[^1_2]。

**主なコマンドオプション**

| オプション | 内容 |
| :-- | :-- |
| --qiita | Qiitaに投稿 |
| --note | noteに投稿 |
| --wp | WordPressに投稿 |
| --zenn | Zennに投稿 |
| --firefox-headless | ブラウザのヘッドレス実行 |

---

**Web UIからの投稿（v0.8.0～）**

1. Web UIを起動

```
oasis -app
```

または

```
oasis --streamlit-app
```

2. ブラウザが自動で開き、画面左でMarkdownフォルダのパス、右で投稿先プラットフォーム（note含む）を選択
3. 「🚀 処理開始」ボタンで投稿実行
4. 投稿結果が画面に表示される

---

**認証情報の設定**

- 初回利用時は、各プラットフォームの認証情報を`.env`ファイルで設定する必要があります（今後UI対応予定）[^1_4]。

---

## 注意点・補足

- note公式APIは記事投稿機能を公開していないため、OASISは非公式APIやブラウザ自動操作（Selenium等）を用いて投稿処理を実現しています[^1_3][^1_4]。
- 投稿するMarkdownの記法や画像ファイルの配置など、細かな仕様はOASISのドキュメントや公式GitHubリポジトリを参照してください[^1_1][^1_4]。
- Web UIは2024年7月時点でv0.8.0から利用可能となっています[^1_4]。

---

## まとめ

OASISは、noteを含む複数プラットフォームへの記事投稿を効率化したいユーザーにとって強力なPythonアプリケーションです。コマンドライン・Web UIの両方に対応し、Markdownベースでの一括投稿・管理が可能です[^1_2][^1_4]。今後も機能拡張が予定されており、より便利に進化していくことが期待されます。

<div style="text-align: center">⁂</div>

[^1_1]: <https://pypi.org/project/oasis-article/>

[^1_2]: <https://hamaruki.com/markdown-to-wordpress-qiita-note-zenn-quick-crosspost-oasis-v0-7-0-usage/>

[^1_3]: <https://note.com/naokun_gadget/n/naf129cb5f34b>

[^1_4]: <https://qiita.com/Maki-HamarukiLab/items/6aeb22c4ab60134986ac>














