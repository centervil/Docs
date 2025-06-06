# 2025-03-07 会話の自動記録の仕組みを整える

## 今日の開発テーマ

今日の開発テーマは、会話の自動記録の仕組みを整えることです。

## 会話ログ

- ユーザー: では、今日の開発テーマをお伝えします。
（ここからは、会話ログを @ProjectLogs  以下に記載してください）
今日のテーマは、「会話の自動記録の仕組みを整える」です。

- Claude: 了解しました。今日のテーマは「会話の自動記録の仕組みを整える」ですね。会話ログを ProjectLogs 以下に記録していきます。

まず、今日の開発日記ファイルを作成しました。これから会話の自動記録の仕組みについて検討していきましょう。

現在の開発日記作成プロセスは2段階方式で、1) ProjectLogs に会話ログを記録し、2) それを元に Zenn 公開用の記事を articles に作成する流れになっています。

会話の自動記録の仕組みを整えるにあたり、どのような点を改善したいとお考えですか？例えば以下のような観点が考えられます：

1. 会話ログの記録を自動化する方法
2. 会話ログのフォーマットの標準化
3. 会話ログから Zenn 公開用記事への変換プロセスの効率化

具体的にどのような仕組みを整えたいかお聞かせいただけますか？

- ユーザー: まず、いま感じている課題を共有しましょう。
LLMによる対話形式の開発は、主には拡張機能のClineを通じて行っています。また、利用するLLMモデルは、料金上の問題から安価なものを利用したり、日によって変えたりします。
LLMモデルによる精度の違いや、Cline自身の性能の問題によって、うまく会話ログが取れない（ループしたり、こちらが指示しないと記録されなかったり、エラーが起きたり）ことが頻発しています。
これを是正し、毎日の開発をスムーズに効率よく進めとたいと思っています。

- Claude: ご共有いただきありがとうございます。Clineや異なるLLMモデルを使用する際の会話ログ記録の問題は重要な課題ですね。これらの問題を解決するために、以下のような対策が考えられます：

1. **LLMに依存しない会話記録システム**：
   - Clineの外部で会話を記録するシステムを構築する
   - 例えば、会話APIのリクエスト/レスポンスを直接ログとして保存する仕組み

2. **自動バックアップシステム**：
   - 定期的に会話内容をバックアップする仕組み
   - エラーやループが発生した場合でも、それまでの会話が失われないようにする

3. **会話ログ記録用の専用ツール開発**：
   - 昨日作成したGemini APIを使った開発日記変換スクリプトのように、会話ログを自動的に記録するツールを開発
   - このツールはClineやLLMモデルとは独立して動作させる

4. **会話ログのフォーマット標準化**：
   - どのLLMモデルを使用しても同じフォーマットでログを記録できるようにする
   - 例：`- ユーザー: [メッセージ]` と `- LLM: [レスポンス]` の形式を統一

これらの対策について、どれが最も優先度が高いとお考えですか？また、具体的な実装方法についてのご希望はありますか？

- ユーザー: まず簡単にできることから始めたいです。4が良さそうです。
また、Clineとの会話開始時に、今日の開発日記ファイルの作成や、その後の会話ログの記録をいちいち指示しなくても行ってくれるようなプロンプトを指示できればいいと思っています

- Claude: 承知しました。まずは会話ログのフォーマット標準化と、Clineとの会話開始時に自動的に開発日記ファイルを作成・記録するプロンプトの作成から始めましょう。

### 1. 会話ログのフォーマット標準化

標準的な会話ログのフォーマットを以下のように定義しましょう：

```markdown
## 会話ログ

- ユーザー: [ユーザーのメッセージ]
- LLM: [LLMの応答]
- ユーザー: [ユーザーのメッセージ]
- LLM: [LLMの応答]
...
```

### 2. Cline用の自動記録プロンプト

Clineとの会話開始時に使用するプロンプトを作成します。このプロンプトは以下の機能を持ちます：

1. 今日の日付を自動的に取得
2. 開発日記ファイルを自動的に作成
3. 会話ログを自動的に記録

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

4. 会話の途中で課題や解決策、所感などが明らかになった場合は、適宜それらのセクションに追記してください。

5. 会話の終了時に、その日の開発内容を簡潔にまとめてください。

それでは、今日のテーマは「[テーマを入力]」です。
```

このプロンプトをClineに提供することで、会話開始時に自動的に開発日記ファイルを作成し、会話ログを記録してくれるようになります。

これらの提案について、どう思われますか？何か修正や追加したい点はありますか？

- ユーザー: フォーマットについて、課題、解決策、所感の項目はいったん省きましょう。
これがあると出力がおかしくなることがある気がするので。
純粋な対話のみをロギングする形にしておきたいです。
また、途中でLLMがコード全体を表示することがあるのですが、それらをログに記載していると膨大になりすぎるので、変更点のみなど、出力結果はある程度まとめて記録することが現実的です。
ただし、私の指示は漏らさず記載してほしいです。

- Claude: 承知しました。フォーマットをシンプルにし、純粋な対話のみをロギングする形式に修正します。また、コード出力は要約して記録するようにします。

### 1. 修正した会話ログのフォーマット標準化

シンプルな会話ログのフォーマットを以下のように定義します：

```markdown
## 会話ログ

- ユーザー: [ユーザーのメッセージ]
- LLM: [LLMの応答（コード出力は要約）]
- ユーザー: [ユーザーのメッセージ]
- LLM: [LLMの応答（コード出力は要約）]
...
```

### 2. 修正したCline用の自動記録プロンプト

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

このプロンプトでは、課題、解決策、所感のセクションを省略し、純粋な対話のみをロギングする形式にしました。また、コード出力や実行結果は要約して記録するよう指示を追加しました。

この修正したフォーマットとプロンプトはいかがでしょうか？

- ユーザー: これでいいと思います。
ではフォーマットやプロンプトをファイルに切り出して、今日の開発を終わりましょう。

- Claude: 承知しました。フォーマットとプロンプトをファイルに切り出して保存します。

まず、会話ログのフォーマット標準を `Documents/conversation_log_format.md` として保存します：

[コード出力: Documents/conversation_log_format.md ファイルを作成し、会話ログのフォーマット標準を記述]

次に、Cline用の自動記録プロンプトを `Documents/cline_auto_logging_prompt.md` として保存します：

[コード出力: Documents/cline_auto_logging_prompt.md ファイルを作成し、修正したCline用の自動記録プロンプトを記述]

これで今日の開発は完了です。会話の自動記録の仕組みを整えるという目標に対して、以下の成果を得ることができました：

1. 会話ログのフォーマット標準を定義
2. コード出力などの長文を要約して記録するルールを設定
3. Clineとの会話開始時に使用する自動記録プロンプトを作成

これらの成果により、今後の開発セッションでは会話ログの記録がより効率的かつ確実に行えるようになります。お疲れ様でした。 