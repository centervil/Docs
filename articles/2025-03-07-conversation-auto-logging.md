---
title: "2025-03-07 会話の自動記録の仕組みを整える"
emoji: "🗒️"
type: "idea"
topics: ["LLM", "開発日記", "自動化", "プロンプトエンジニアリング"]
published: true
---

:::message
この記事はClaude 3.7 Sonnetによって自動生成されています。
私の毎日の開発サイクルについては、[LLM対話で実現する継続的な開発プロセス](https://zenn.dev/centervil/articles/2025-03-12-development-cycle-introduction)をご覧ください。
:::

## はじめに

昨日は、LLM APIを利用した開発日記自動加工スクリプトのプロトタイプを作成しました。今日は、その流れで「会話の自動記録の仕組みを整える」ことに取り組みます。

LLMとの対話形式での開発において、会話ログを正確に記録することは非常に重要です。しかし、LLMモデルの精度の違いやツールの性能問題により、会話ログがうまく取れないことが頻発していました。今回は、この問題を解決するための仕組みづくりに挑戦します。

## 検討事項

まず、現状の課題を整理しました：

1. LLMモデルによる精度の違いがある（料金の問題で安価なモデルを使うこともある）
2. Cline自身の性能問題により、会話ログの記録に問題が発生する
   - ループが発生する
   - 指示しないと記録されない
   - エラーが発生する

これらの課題に対して、以下の対策を検討しました：

1. **LLMに依存しない会話記録システム**の構築
2. **自動バックアップシステム**の導入
3. **会話ログ記録用の専用ツール開発**
4. **会話ログのフォーマット標準化**

検討の結果、まずは簡単に実装できる「会話ログのフォーマット標準化」から着手することにしました。また、Clineとの会話開始時に自動的に開発日記ファイルを作成し、会話ログを記録するためのプロンプトも作成することにしました。

## 実装内容

### 1. 会話ログのフォーマット標準化

会話ログの標準フォーマットを以下のように定義しました：

```markdown
## 会話ログ

- ユーザー: [ユーザーのメッセージ]
- LLM: [LLMの応答（コード出力は要約）]
- ユーザー: [ユーザーのメッセージ]
- LLM: [LLMの応答（コード出力は要約）]
...
```

このフォーマットでは、以下のルールを設定しました：

- ユーザーの指示は漏らさず完全に記録する
- コード出力は要約して記録する
- エラーメッセージや実行結果も要約して記録する
- 会話の本質的な内容は省略せずに記録する

### 2. Cline用の自動記録プロンプト

Clineとの会話開始時に使用するプロンプトを作成しました。このプロンプトには以下の機能があります：

1. 今日の日付を自動的に取得
2. 開発日記ファイルを自動的に作成
3. 会話ログを自動的に記録

プロンプトの内容は以下の通りです：

```
# Cline用自動記録プロンプト

こんにちは、Cline。今日の開発セッションを始めます。

以下の指示に従って作業を進めてください：

1. 今日の日付（YYYY-MM-DD形式）を取得し、開発日記ファイル「Documents/ProjectLogs/YYYY-MM-DD-[テーマ].md」を作成してください。テーマは私が最初に伝えます。

2. 開発日記ファイルには以下の構造を使用してください：
```markdown
# YYYY-MM-DD [テーマ]

## 今日の開発テーマ

今日の開発テーマは[テーマ]です。

## 会話ログ

- ユーザー: [最初のメッセージ]
- LLM: [あなたの応答]
...
```

3. 私たちの会話内容を自動的に「会話ログ」セクションに記録してください。各メッセージは「- ユーザー: 」または「- LLM: 」で始まる形式で記録してください。

4. 記録の際の重要なルール：
   - ユーザーの指示は必ず漏らさず完全に記録してください
   - コード全体を表示する場合は、「[コード出力: ファイル名と主な変更点の要約]」のように要約して記録してください
   - エラーメッセージや実行結果も同様に要約して記録してください
   - 会話の本質的な内容（質問、回答、議論）は省略せずに記録してください

それでは、今日のテーマは「[テーマを入力]」です。
```

このプロンプトを使用することで、会話開始時に自動的に開発日記ファイルを作成し、会話ログを記録することができます。

### 3. ファイルの作成

最終的に、以下の2つのファイルを作成しました：

1. `Documents/conversation_log_format.md` - 会話ログのフォーマット標準を定義
2. `Documents/cline_auto_logging_prompt.md` - Cline用の自動記録プロンプト

## 今後の課題

今回は会話ログのフォーマット標準化とCline用の自動記録プロンプトの作成を行いましたが、より堅牢な会話記録システムを構築するためには、以下の課題に取り組む必要があります：

1. LLMに依存しない会話記録システムの構築
2. 自動バックアップシステムの導入
3. 会話ログ記録用の専用ツール開発

## まとめ

今回の開発では、LLMとの対話形式での開発における会話ログの記録問題に対処するため、会話ログのフォーマット標準化とCline用の自動記録プロンプトを作成しました。これにより、異なるLLMモデルを使用する場合でも統一されたフォーマットで会話ログを記録できるようになり、開発プロセスの効率化と安定化が期待できます。

また、コード出力や実行結果を要約して記録することで、ログファイルのサイズを抑えつつ、重要な情報を漏らさず記録できるようになりました。今後は、より堅牢な会話記録システムの構築に取り組んでいきたいと思います。 