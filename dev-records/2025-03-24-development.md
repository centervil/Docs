# 2025-03-24 development

## 今日の開発テーマ

今日の開発テーマは、Zenn公開用日記のフォーマット最適化です。

## 前日までの活動履歴

前日までの活動履歴は以下の通りです：
* 2025-03-23: 各リポジトリのドキュメントをZenn-Docsに集約
* 2025-03-22: Diary-Converterのリポジトリの整理（開発日記の移動、フォルダ構成の整理）
* 2025-03-21: diary-converterを独立したリポジトリとして移行、GitHub Actionsのコンポーザブルアクションとして設定
* 2025-03-20: diary-converter独立化の検討
* 2025-03-13: diary-converterのCI/CD組み込み

## 会話ログ

- ユーザー: 今日の開発を始めます。
まずは、 'dev-docs/Auto_Logging_Guide.md' (see below for file content) を読んでください。
昨日の開発記録は、'dev-records/2025-03-23-development.md' (see below for file content) です。
準備が出来たら、今日の開発テーマを伝えます。
- LLM: 今日の開発日記ファイルを作成します。Auto_Logging_Guideの指示に従い、前日までの活動履歴を含めます。
- LLM: Auto_Logging_Guide、昨日の開発記録、会話ログのフォーマット、Zenn記事のテンプレートを確認し、今日の開発日記ファイルを作成しました。前日までの活動履歴も記録しています。

準備ができましたので、今日の開発テーマをお聞かせください。
- ユーザー: 今日の開発テーマは、 centervil/Zenn-Docs リポジトリの Issue #1 の解決です
- LLM: Issue #1の内容を確認しました。タイトルは「[Improvement] Zenn公開用日記のフォーマット最適化」で、以下の改善点が挙げられています：

1. 関連するリポジトリ（開発プロジェクト）へのリンクを追加
2. 前日の開発日記へのリンクを追加
3. Zenn記事のタイトルのスタイルを統一化
   - 日付の付与は廃止。代わりに開発日記のプロジェクト毎の連番を付ける
   - 開発日記であることをわかるようにする

これらの改善点を実装するために、まずはZenn記事のテンプレートファイル（dev-docs/zenn_template.md）を確認し、必要な変更を加えていきます。

Zenn記事のテンプレートファイルを以下のように修正しました：

1. タイトルのスタイルを統一化：
   - 「[プロジェクト名] 開発日記 #[連番]: [テーマ]」という形式に変更
   - 日付の付与を廃止し、プロジェクト毎の連番を付ける形式に変更
   - 「開発日記」という文言を追加して、開発日記であることを明示

2. 関連リンクセクションを追加：
   - プロジェクトリポジトリへのリンク
   - 前回の開発日記へのリンク

3. その他の改善：
   - typeを「idea」から「tech」に変更
   - topicsのデフォルト値に「開発日記」を追加

次に、diary-converterツールのソースコードを確認しました。現在のツールは新しいテンプレートのフォーマットに完全には対応していないことがわかりました。特に以下の点が課題です：

1. タイトルのフォーマット：ツールは現在「{date} {theme_name}」形式のタイトルを生成しますが、新しいテンプレートでは「[プロジェクト名] 開発日記 #[連番]: [テーマ]」形式が必要です。
2. 関連リンクセクション：新しく追加されたセクションに対応していません。

これらの課題に対応するために、以下の暫定対応を行いました：

1. テンプレートのタイトル部分を修正：
   - 現在のdiary-converterツールが対応している「[日付] [テーマ]」形式を維持
   - コメントを追加して、実際のタイトルは「[プロジェクト名] 開発日記 #[連番]: [テーマ]」形式にすべきことを明記

2. 関連リンクセクションにコメントを追加：
   - diary-converterツールが対応するまでの暫定対応であることを明記
   - 実際の記事では手動で情報を追加する必要があることを説明

今後の対応策として、以下を検討しています：

1. diary-converterツールのリポジトリに対して、Issue #1の内容に対応するための修正をPull Requestとして提案
   - タイトルのフォーマット変更に対応
   - 関連リンクセクションの自動生成に対応
   - プロジェクト名と連番の管理機能の追加

2. GitHub Actionsワークフローの改善：
   - 変換後の記事を自動的に修正するステップの追加
   - プロジェクト名と連番を自動的に設定する機能の追加

diary-converterツールの修正案として、以下の変更を提案します：

```python
# diary_converter.pyの修正案

# 1. 新しいパラメータの追加
def __init__(self, model="gemini-2.0-flash-001", template_path="./templates/zenn_template.md", 
             debug=False, project_name=None, issue_number=None, prev_article_slug=None):
    """初期化"""
    self.model_name = model
    self.template_path = template_path
    self.debug = debug
    self.project_name = project_name  # プロジェクト名
    self.issue_number = issue_number  # 連番（Issue番号）
    self.prev_article_slug = prev_article_slug  # 前回の記事スラッグ
    self.setup_api()

# 2. frontmatterテンプレートの修正
frontmatter_template = f"""---
title: "{self.project_name or 'プロジェクト'} 開発日記 #{self.issue_number or '1'}: {theme_name}"
emoji: "{template_fm.get('emoji', '📝')}"
type: "{template_fm.get('type', 'tech')}"
topics: {template_fm.get('topics', ['開発日記', 'プログラミング'])!r}
published: {str(template_fm.get('published', False)).lower()}
---"""

# 3. 関連リンクセクションの生成
repo_link = f"https://github.com/centervil/{self.project_name}" if self.project_name else "https://github.com/centervil/[リポジトリ名]"
prev_article_link = f"https://zenn.dev/centervil/articles/{self.prev_article_slug}" if self.prev_article_slug else "https://zenn.dev/centervil/articles/[前回の記事スラッグ]"

related_links_section = f"""## 関連リンク

- **プロジェクトリポジトリ**: [{self.project_name or 'プロジェクト名'}]({repo_link})
- **前回の開発日記**: [前回のタイトル]({prev_article_link})
"""

# 4. プロンプトの修正
prompt = f"""以下の開発日記を、Zenn公開用の記事に変換してください。

# 入力された開発日記
{content}

# 変換ルール
1. 「会話ログ」セクションは、対話形式ではなく、ストーリー形式に書き直してください
2. 技術的な内容は保持しつつ、読みやすく整理してください
3. 「所感」セクションを充実させ、開発者の視点や感想を追加してください
4. マークダウン形式を維持し、コードブロックなどは適切に整形してください
5. 記事の先頭に以下のfrontmatterを追加してください：

{frontmatter_template}

6. frontmatterの直後に以下のメッセージボックスを追加してください：

{message_box_template}

7. メッセージボックスの直後に以下の関連リンクセクションを追加してください：

{related_links_section}

# テンプレート構造
以下のテンプレート構造に従って記事を作成してください。各セクションの目的と内容を理解し、開発日記の内容に合わせて適切に変換してください：

{template_structure}

# 記述ガイドライン
{guidelines}

# 出力形式
frontmatterを含むマークダウン形式の完全な記事を出力してください。テンプレートの構造に従いつつ、開発日記の内容を適切に反映させてください。
以下の点に注意してください：
1. コードブロックは必要な場合のみ使用し、記事全体をコードブロックで囲まないでください
2. 記事の先頭や末尾に余分なコードブロックマーカー（```）を付けないでください
3. 記事の先頭に```markdownなどの言語指定を付けないでください
"""

# 5. コマンドライン引数の追加
parser.add_argument("--project-name", default="", help="プロジェクト名")
parser.add_argument("--issue-number", default="", help="連番（Issue番号）")
parser.add_argument("--prev-article", default="", help="前回の記事スラッグ")

# 6. GitHub Actionsの入力パラメータの追加
converter = DiaryConverter(
    model=args.model,
    template_path=args.template,
    debug=args.debug,
    project_name=args.project_name,
    issue_number=args.issue_number,
    prev_article_slug=args.prev_article
)
```

また、GitHub Actionsワークフローファイル（diary-convert.yml）の修正案も作成します：

```yaml
# diary-convert.ymlの修正案

- name: Run diary-converter
  uses: centervil/Diary-Converter@main
  with:
    source_file: ${{ steps.find-diary.outputs.diary_file }}
    destination_file: ${{ steps.find-diary.outputs.output_file }}
    api_key: ${{ secrets.GOOGLE_API_KEY }}
    model: gemini-2.0-flash-001
    template: dev-docs/zenn_template.md
    debug: 'true'
    project_name: 'Zenn-Docs'  # プロジェクト名を指定
    issue_number: '1'  # 連番を指定（自動的にインクリメントする仕組みも検討）
    prev_article: '2025-03-23-dev-diary'  # 前回の記事スラッグを指定
```

これらの修正案をPull Requestとして提案するための手順は以下の通りです：

1. centervil/Diary-Converterリポジトリをフォーク
2. 新しいブランチを作成（例：feature/zenn-template-optimization）
3. 修正案に基づいてdiary_converter.pyファイルを修正
4. GitHub Actionsのワークフローファイルに新しいパラメータを追加
5. テストを実行して動作確認
6. コミットしてPull Requestを作成
7. Pull Requestの説明に、Issue #1の内容と修正内容を記載

## 今回の作業のまとめ

今日は、centervil/Zenn-Docs リポジトリの Issue #1「Zenn公開用日記のフォーマット最適化」に対応するための作業を行いました。

### 実施した作業

1. Zenn記事のテンプレートファイル（dev-docs/zenn_template.md）を修正
   - タイトルのスタイルを「[プロジェクト名] 開発日記 #[連番]: [テーマ]」形式に変更
   - 関連リンクセクションを追加（プロジェクトリポジトリと前回の開発日記へのリンク）
   - typeを「tech」に変更し、topicsのデフォルト値に「開発日記」を追加

2. diary-converterツールとの互換性を確保するための暫定対応
   - テンプレートにコメントを追加して、実際のタイトルフォーマットを明記
   - 関連リンクセクションにコメントを追加して、手動で情報を追加する必要があることを説明

3. diary-converterツールの修正案を作成
   - 新しいパラメータ（プロジェクト名、連番、前回の記事スラッグ）の追加
   - frontmatterテンプレートの修正
   - 関連リンクセクションの自動生成機能の追加
   - プロンプトの修正
   - コマンドライン引数の追加

4. GitHub Actionsワークフローファイルの修正案を作成
   - 新しいパラメータを指定するための設定を追加

### 今後の課題

1. diary-converterツールの修正をPull Requestとして提案し、マージしてもらう
2. 連番の自動インクリメント機能の実装
   - 最新の記事から連番を取得し、自動的にインクリメントする仕組み
   - プロジェクト毎に連番を管理する仕組み

3. 前回の記事スラッグの自動取得機能の実装
   - 最新の記事のスラッグを自動的に取得する仕組み
   - プロジェクト毎に前回の記事を管理する仕組み

これらの改善により、Zenn公開用日記のフォーマットが最適化され、より一貫性のある記事が生成されるようになります。また、関連リンクの追加により、プロジェクト間の関連性が明確になり、読者がプロジェクトの全体像を把握しやすくなります。
