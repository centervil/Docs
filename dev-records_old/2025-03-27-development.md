# 2025-03-27 development

## 今日の開発テーマ

今日の開発テーマは、Diary-Converterのaction.ymlの改善です。

## 前日までの活動履歴
前日までの活動履歴は以下の通りです：
* 2025-03-26: Diary-ConverterのIssue #1「Zenn公開用日記のフォーマット最適化」の解決
* 2025-03-25: centervil/Diary-ConverterにIssueを発行
* 2025-03-24: Zenn公開用日記のフォーマット最適化

## 会話ログ

- ユーザー: 今日の開発を始めます。
まずは、 'Docs/dev-docs/Auto_Logging_Guide.md' (see below for file content) を読んで。
また、昨日の開発記録は、 'Docs/dev-records/2025-03-26-development.md' (see below for file content) です。
今日の開発テーマは、 Diary-Converter のaction.ymlの改善です。
準備が出来たら詳細を伝えます。

- LLM: Auto_Logging_Guide.mdと昨日の開発記録を確認しました。今日の開発テーマはDiary-Converterのaction.ymlの改善ですね。準備ができましたので、詳細をお聞かせください。

- ユーザー: やりたいことは、Diary-Converterのaction.yml により生成されたドキュメントに、不備があったので、修正するプロセスを追加してほしい。
具体的には、生成されたマークダウンファイルの冒頭に```markdown 、末尾に ``` と付いていて、全体がコードブロック化されていた。
これは、LLMが文書を生成する以上、完全に排除するのは難しい問題だと思っているので、パイプライン中でドキュメントを生成した後、文書をチェックしてこの問題を取り除くプロセスを追加してほしい。
なお、このプロセスは、今後他の問題も修正する機能を追加する可能性があるので、拡張性を考慮して設計して。また、このプロセスを直接action.ymlに書かず、pythonファイルに外出しして。

- LLM: 理解しました。LLMによって生成されたマークダウンファイルの問題（全体がコードブロック化されている）を修正するプロセスを追加します。拡張性を考慮して、Pythonファイルに外出しして実装します。

以下の改善を行いました：

1. ドキュメント処理用のPythonファイルの作成
   - `document_processor.py`という新しいファイルを作成
   - マークダウンファイル全体を囲むコードブロックを削除する機能を実装
   - 将来的に他の問題も修正できるよう、拡張性を考慮した設計
   - 処理関数をリスト化し、順番に適用する仕組み
   - デバッグモードのサポート

2. action.ymlの修正
   - ドキュメント生成後に`document_processor.py`を呼び出す新しいステップを追加
   - デバッグモードの引き継ぎ
   - 処理完了メッセージの追加

`document_processor.py`の主な機能：

```python
# 処理関数のリスト（順番に実行される）
self.processors: List[Callable[[str], str]] = [
    self.remove_markdown_code_block,
    # 将来的に他の処理関数を追加可能
    # self.fix_frontmatter_format,
    # self.normalize_headings,
    # self.fix_image_paths,
    # など
]

def remove_markdown_code_block(self, content: str) -> str:
    """
    マークダウンファイル全体を囲むコードブロックを削除する
    
    LLMが生成したマークダウンファイルでは、しばしば全体が```markdownと```で囲まれている
    この関数は、そのようなコードブロックを検出して削除する
    """
    # 文書全体がコードブロックで囲まれているかチェック
    if content.startswith('```') and content.endswith('```'):
        # 先頭行と末尾の```を削除
        ...
    
    # 先頭が```markdownで始まるケース
    if content.startswith('```markdown') or content.startswith('```Markdown'):
        # 先頭行と末尾の```を削除
        ...
    
    return content
```

この実装により、LLMによって生成されたマークダウンファイルの問題（全体がコードブロック化されている）を自動的に修正できるようになりました。また、将来的に他の問題も修正できるよう、拡張性を考慮した設計になっています。

- ユーザー: あなた、致命的な間違いをしてますよ。
昨日の開発日記に、今日の開発日記を混ぜてます。
今日の開発日記は今日のファイルとして作り直して。昨日の開発日記はGitの記録から後で手動で戻すから

- LLM: 申し訳ありません。ご指摘ありがとうございます。昨日の開発日記に今日の内容を混ぜてしまいました。今日の開発日記を新しく作成しました。昨日の開発日記はGitの記録から手動で戻していただけるとのこと、了解しました。
