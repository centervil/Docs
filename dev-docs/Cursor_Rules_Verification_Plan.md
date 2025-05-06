# Cursor Rules 高度活用 検証計画

## 1. 目的

以下の方法を用いた Cursor Rules の管理・活用が実現可能か、また実用的かを検証する。

- **Rules の分類**:
  - **背景知識 Rules**: 常に適用させたい共通知識 (例: コーディング規約、ログガイド)。`alwaysApply: true` で定義。
  - **役割（モード） Rules**: タスクに応じて切り替えたい特定の役割 (例: デバッグ、レビュー)。`manual: true` または `agentRequested: true` で定義。
- **管理方法**:
  - 上記2種類の Rules を単一の専用 Git リポジトリ (`my-cursor-rules`) で管理する。
  - 各プロジェクトでは、`my-cursor-rules` リポジトリを Git Submodule (`.cursor/rules-common`) として追加する。
  - 各プロジェクトの `.cursor/rules` ディレクトリから、`.cursor/rules-common` 内の Rules ファイルへのシンボリックリンクを作成する。

## 2. 前提条件

- Git がインストールされ、基本的な操作 (リポジトリ作成, add, commit, push, submodule add/update) が可能であること。
- Cursor がインストールされ、プロジェクトを開けること。
- シンボリックリンクを作成・利用できる環境であること (Linux, macOS, または Git Bash など Windows の対応環境)。

## 3. 検証手順

### 3.1. Rules 専用リポジトリの準備

1. **リポジトリ作成**: GitHub などに `my-cursor-rules` という名前で新しいプライベートリポジトリを作成する (公開リポジトリでも可)。
2. **ローカルクローン**: 作成したリポジトリをローカルにクローンする。

    ```bash
    git clone <your-repo-url>/my-cursor-rules.git
    cd my-cursor-rules
    ```

3. **背景知識 Rules の作成**: 常に適用させたい共通ルールを作成する。
    - ファイル名: `knowledge_base_rule.mdc`
    - 内容例:

        ```mdc
        ---
        description: 共通の背景知識と開発ガイドラインを適用するルール
        alwaysApply: true
        ---

        開発中は以下のドキュメントの内容を常に考慮してください。
        - @Docs/dev-docs/Overall_Development_Guidelines.md
        - @Docs/dev-docs/Coding_Standards.md
        - @Docs/dev-docs/Auto_Logging_Guide.md

        特に `Auto_Logging_Guide.md` に従い、会話ログは `Docs/dev-records/` 内の日次開発日記に記録してください。
        不明点や選択肢がある場合は、勝手に判断せず質問してください。
        ```

4. **役割（モード） Rules の作成**: 切り替えて使いたい役割ルールを作成する。
    - ファイル名: `debug_mode_rule.mdc`
    - 内容例 (`manual`):

        ```mdc
        ---
        description: デバッグ支援モード (手動適用)
        manual: true
        ---

        あなたはデバッグのエキスパートです。
        コードの問題点を特定し、具体的な修正案をステップバイステップで提示してください。
        ```

    - ファイル名: `review_mode_rule.mdc`
    - 内容例 (`agentRequested`):

        ```mdc
        ---
        description: コードレビューモード (キーワード起動)
        agentRequested: レビュー|review request
        ---

        あなたは経験豊富なレビュアーです。
        提供されたコードについて、保守性、可読性、規約 (@Docs/dev-docs/Coding_Standards.md) の観点からレビューしてください。
        ```

5. **コミット & プッシュ**: 作成した Rules ファイルをリポジトリに追加し、プッシュする。

    ```bash
    git add *.mdc
    git commit -m "Add initial common and mode rules"
    git push origin main
    ```

### 3.2. 検証用プロジェクトへの適用

1. **検証用プロジェクト**: 既存の Cursor プロジェクト、または新規プロジェクトを用意する。
2. **サブモジュール追加**: プロジェクトのルートディレクトリで、Rules 専用リポジトリをサブモジュールとして追加する。

    ```bash
    # プロジェクトルートに移動
    cd <path/to/your/project>
    # サブモジュールを追加 (ディレクトリ名を指定)
    git submodule add <your-repo-url>/my-cursor-rules.git .cursor/rules-common
    git commit -m "Add common cursor rules submodule"
    ```

3. **シンボリックリンク作成**: `.cursor/rules` ディレクトリを作成し、サブモジュール内の Rules へのシンボリックリンクを作成する。

    ```bash
    # .cursor/rules ディレクトリがなければ作成
    mkdir -p .cursor/rules
    # シンボリックリンク作成 (相対パス推奨)
    ln -s ../rules-common/knowledge_base_rule.mdc .cursor/rules/knowledge_base_rule.mdc
    ln -s ../rules-common/debug_mode_rule.mdc .cursor/rules/debug_mode_rule.mdc
    ln -s ../rules-common/review_mode_rule.mdc .cursor/rules/review_mode_rule.mdc
    # シンボリックリンクを Git に追加 (環境によっては .gitattributes が必要かも)
    git add .cursor/rules/*
    git commit -m "Link common cursor rules"
    ```

### 3.3. Cursor での動作確認

1. **プロジェクトを開く**: Cursor で検証用プロジェクトを開く。
2. **背景知識 Rule 確認**: 新しい会話を開始し、特にルールを指定せずに質問する。Cursor が `knowledge_base_rule.mdc` で参照されているドキュメント（例: `Auto_Logging_Guide.md`）の内容を考慮した応答をするか確認する。（例：「開発日記を記録してください」などと指示せずに記録を始めるか）
3. **Manual モード Rule 確認**:
    - `Cmd + Shift + P` を押し、"Apply Cursor Rule" を選択する。
    - リストに `debug_mode_rule` が表示されることを確認する。
    - それを選択し、デバッグに関する質問をする。Cursor がデバッグモードの指示に従った応答をするか確認する。
4. **Agent Requested モード Rule 確認**:
    - プロンプトにトリガーキーワード（例: 「このコードをレビューしてください」）を含めて質問する。
    - Cursor が `review_mode_rule.mdc` の指示に従ったレビュー応答をするか確認する。

### 3.4. 共通 Rules の更新テスト

1. **専用リポジトリ更新**: `my-cursor-rules` リポジトリのローカルコピーで、いずれかの `.mdc` ファイルを編集し、コミット＆プッシュする。
2. **サブモジュール更新**: 検証用プロジェクトのルートディレクトリで、サブモジュールを更新する。

    ```bash
    git submodule update --remote --merge
    git add .cursor/rules-common
    git commit -m "Update common cursor rules submodule"
    ```

3. **Cursor で再確認**: Cursor で再度プロジェクトを開き、更新された Rule が適用されているか確認する。

## 4. 期待される結果

- すべての手順が問題なく実行できる。
- 背景知識 Rule が自動的に適用される。
- Manual モード Rule が手動で選択・適用でき、指定した役割として動作する。
- Agent Requested モード Rule がキーワードによって起動され、指定した役割として動作する。
- 専用リポジトリで Rules を更新した後、各プロジェクトでサブモジュールを更新すれば、変更が反映される。

## 5. 検証結果記録

(ここに検証日時、実施者、各ステップの結果、問題点などを記録する)

---
