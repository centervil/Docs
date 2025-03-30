# 2025-03-30 development

## 今日の開発テーマ

今日の開発テーマは、昨日に引き続きZenn公開用記事フォーマットの改善です。具体的には、昨日の成果物に見られたメッセージボックスの内容、前回の記事リンクURL、記事タイトルの問題を修正します。

## 前日までの活動履歴
前日までの活動履歴は以下の通りです：
* 2025-03-29: development
* 2025-03-28: development
* 2025-03-27: development

## 会話ログ

- ユーザー: 今日は、昨日の作業結果に不満があるため、昨日の開発テーマに引き続き取り組みたいです。具体的には、昨日の公開用日記の 'Docs/articles/2025-03-29-dev-diary.md' を見ると分かる通り、冒頭のメッセージboxに消したはずの 開発サイクルに関しての記述が含まれている点、前回の開発日記へのrリンクURLに仮文言が含まれている点、記事titleが指定通りでない点、です。
- LLM: 承知いたしました。昨日の開発テーマ「Zenn公開用記事フォーマット改善」に引き続き取り組み、指摘された問題点を修正します。まず、今日の開発テーマと最初のメッセージを開発日記に記録します。
- LLM: スクリプト `Diary-Converter/src/diary_converter/diary_converter.py` のプロンプト生成部分を修正しました。LLMに対して、提供された frontmatter とメッセージボックスのテンプレートをより厳密に使用するように指示を強化しました。次に、この修正を反映させるために、昨日の開発日記 (`Docs/dev-records/2025-03-29-development.md`) を再度変換し、対応する Zenn 記事 (`Docs/articles/2025-03-29-dev-diary.md`) を再生成します。
- ユーザー: 動作確認は置いておいて、CI/CDパイプラインにも問題がないか確認してください。Diary-Converterのパイプラインと、Docのパイプライン両方です
- LLM: CI/CDパイプラインの確認を行いました。問題点として、Docsリポジトリのテンプレート（`Docs/dev-docs/zenn_template.md`）とDiary-Converterのテンプレート（`Diary-Converter/templates/zenn_template.md`）の内容が異なっていること、GitHub Actionsワークフローで前回の記事スラッグが指定されていないことなどを特定しました。
- ユーザー: 'Diary-Converter/templates/zenn_template.md' と、 'Docs/dev-docs/zenn_template.md' があり、重複している。また、 'Diary-Converter/src/diary_converter/diary_converter.py' にもzenn_templateに書かれた内容と重複する部分があるのではと疑っている。下記の方針で、整理したうえで、GithunActionsワークフローを含めて修正を行って。・zennの公開日記用のフォーマットに関する情報は、zenn_template.mdにまとめる・重複して存在している zenn_templateは、'Diary-Converter/templates/zenn_template.md' を正として、'Docs/dev-docs/zenn_template.md' は削除する
- LLM: ご指示に従い、以下の修正を行いました：
  1. `Docs/dev-docs/zenn_template.md` を削除し、`Diary-Converter/templates/zenn_template.md` を正として使用するようにしました。
  2. GitHub Actionsワークフロー（`Docs/.github/workflows/diary-convert.yml`）を修正し、以下の変更を加えました：
     - テンプレートパスの指定を削除し、デフォルト値を使用するように変更
     - 前回の記事スラッグを自動的に検出するステップを追加
     - `project_name` と `issue_number` パラメータを削除
     - `prev_article` パラメータに自動検出した前回の記事スラッグを設定
  3. `Diary-Converter/action.yml` を修正し、以下の変更を加えました：
     - 不要な `cycle_article` 引数を削除
     - プロジェクト名を自動的に検出するロジックを追加
     - 連番（Issue番号）を自動的に検出するロジックを追加
  4. `diary_converter.py` を修正し、以下の変更を加えました：
     - 不要な `cycle_article` 関連のコードを削除
     - デフォルト値設定部分を修正し、テンプレートファイルとの重複を明確にするためのコメントを追加
