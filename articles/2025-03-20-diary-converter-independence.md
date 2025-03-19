---
title: "2025-03-20 Diary Converter Independence"
emoji: "🛠️"
type: "idea"
topics: ['開発日記', 'CI/CD', 'GitHub Actions']
published: false
---

:::message
この記事はgemini-2.0-flash-001によって自動生成されています。

:::

:::message
この記事はgemini-2.0-flash-001によって自動生成されています。
私の毎日の開発サイクルについては、[LLM対話で実現する継続的な開発プロセス](https://zenn.dev/centervil/articles/2025-03-12-development-cycle-introduction)をご覧ください。
:::

# Diary Converter の独立

## はじめに

昨日はdiary-converterを独立したリポジトリとして切り出すための準備を進めました。今日は、その成果を基に、diary-converterを他のプロジェクトからCI/CDパイプラインを通じて利用できるようにすることを目指します。

## 背景と目的

これまでdiary-converterは、ある特定の開発プロジェクトに組み込まれていました。しかし、このツールが他のプロジェクトでも有用であると考え、独立したリポジトリとして再利用可能にすることで、開発効率の向上を目指すことにしました。具体的には、diary-converterを独立したリポジトリとして切り出し、CI/CDパイプラインから利用できるようにすることで、開発日記の変換プロセスを自動化し、より多くのプロジェクトで活用できるようにします。

## 検討内容

### 課題の整理

diary-converterを独立したリポジトリとして利用可能にするためには、以下の課題を解決する必要がありました。

1. **依存関係の明確化**: 必要なライブラリや環境変数を明確にし、独立した環境でも動作するようにする。
2. **CI/CDパイプラインへの統合**: 既存のCI/CDパイプラインにdiary-converterを組み込むための方法を検討する。
3. **ドキュメントの整備**: 利用者が簡単に利用できるように、READMEやドキュメントを整備する。
4. **テストの実施**: 独立した環境でdiary-converterが正しく動作することを保証するためのテストを実施する。

### 解決アプローチ

これらの課題を解決するために、以下のアプローチを検討しました。

1. **GitHub Actionsのコンポーザブルアクションの活用**: diary-converterをGitHub Actionsのコンポーザブルアクションとして公開し、他のプロジェクトから簡単に利用できるようにする。
2. **Dockerコンテナの利用**: diary-converterをDockerコンテナとしてパッケージ化し、環境依存性の問題を解決する。
3. **READMEの充実**: diary-converterの概要、インストール方法、使用方法、CI/CDパイプラインへの統合方法などを詳細に記述したREADMEを作成する。

## 実装内容

実際に行った作業内容は以下の通りです。

### 変更点1: 独立リポジトリ用のREADME.mdの作成

diary-converterの概要、インストール方法、使用方法、CI/CDパイプラインでの利用方法などを詳細に記述したREADME.mdを作成しました。特に、CI/CDパイプラインでの利用方法については、以下の3つのアプローチを解説しました。

*   Gitリポジトリのクローンによるアプローチ
*   GitHubリリースからのダウンロードによるアプローチ
*   GitHub Actionsのコンポーザブルアクションによるアプローチ

### 変更点2: GitHub Actionsのコンポーザブルアクションの設定

diary-converterをGitHub Actionsのコンポーザブルアクションとして利用できるように、`action.yml`ファイルを作成しました。このファイルには、入力パラメータの定義、Pythonの設定、依存関係のインストール手順、テンプレートパスやデバッグモードなどのオプション対応などが記述されています。

```yaml
name: 'Diary Converter'
description: 'Convert diary files to Zenn articles'
inputs:
  source_file:
    description: 'Path to the source diary file'
    required: true
  destination_file:
    description: 'Path to the destination Zenn article file'
    required: true
  api_key:
    description: 'API key for the LLM'
    required: false
runs:
  using: 'composite'
  steps:
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      shell: bash
      run: |
        pip install -r requirements.txt
    - name: Run diary-converter
      shell: bash
      run: |
        python diary_converter.py ${{ inputs.source_file }} ${{ inputs.destination_file }} --api_key ${{ inputs.api_key }}
```

### 変更点3: テンプレートファイルの調整

テンプレートファイルを`templates`ディレクトリに配置し、独立リポジトリとして機能するように構造を整理しました。デフォルトテンプレートパスを相対パスに変更し、テンプレート読み込み処理を改善しました。

### 変更点4: diary_converter.pyの修正

diary\_converter.pyを修正し、デフォルトテンプレートパスを相対パスに変更しました。また、テンプレート読み込み処理を改善し、相対パスを正しく解決できるようにしました。独立リポジトリとして機能するために不要な特定のパス調整コードを削除しました。

### 変更点5: Docker関連ファイルの整備

独立リポジトリで使用するためのdocker-compose.ymlファイルを作成し、適切なボリュームマウントと環境変数設定を行いました。

## 技術的なポイント

今回の実装で特に重要だった技術的なポイントは、GitHub Actionsのコンポーザブルアクションの活用です。コンポーザブルアクションを使用することで、diary-converterを他のプロジェクトから簡単に利用できるようになり、CI/CDパイプラインへの統合も容易になりました。

コンポーザブルアクションは、複数のステップをまとめて再利用可能な形にパッケージ化するGitHub Actionsの機能です。通常のワークフロー（`.github/workflows/*.yml`）が単一のリポジトリ内で定義・実行されるのに対し、コンポーザブルアクションは異なるリポジトリ間で共有・再利用できます。

### コンポーザブルアクションの定義方法

1.  **action.yml ファイルの作成**: アクションのメタデータと実行内容を定義

```yaml
name: 'アクション名'
description: 'アクションの説明'
inputs:
  input_name:
    description: '入力の説明'
    required: true/false
    default: 'デフォルト値'
outputs:
  output_name:
    description: '出力の説明'
runs:
  using: 'composite'  # コンポジットアクションの場合
  steps:
    - name: 'ステップ1'
      run: 'コマンド'
      shell: bash
    - name: 'ステップ2'
      run: 'コマンド'
      shell: bash
```

2.  **実行方法の指定**: `runs`セクションで以下のいずれかを指定
    *   `composite`: シェルコマンドやアクションの組み合わせ
    *   `docker`: Dockerコンテナを使用
    *   `node16`/`node20`: JavaScriptアクション

### 他のリポジトリからの利用方法

アクションを利用するリポジトリのワークフロー（`.github/workflows/*.yml`）で以下のように参照します：

```yaml
jobs:
  job_name:
    runs-on: ubuntu-latest
    steps:
      - name: 'アクションを使用'
        uses: owner/repo-name@ref  # owner/repo-name@v1 など
        with:
          input_name: 'input value'
```

ここで重要なのは：

*   `owner/repo-name`: アクションが定義されているリポジトリ
*   `@ref`: ブランチ名、タグ、またはコミットSHA

### 仕組みと動作原理

1.  **アクションの取得**:
    *   ワークフローの実行時、GitHubはアクションリポジトリを指定された参照（ref）で取得
    *   アクションのコードは一時的にワークフロー実行環境にダウンロードされる

2.  **パラメータの受け渡し**:
    *   `with`で指定した入力値が`inputs`として渡される
    *   アクション内では`${{ inputs.input_name }}`で参照できる

3.  **実行コンテキスト**:
    *   アクションは呼び出し元のワークフローコンテキスト内で実行される
    *   `${{ github.workspace }}`は呼び出し元リポジトリのチェックアウトパス

4.  **ファイル操作の制約**:
    *   アクションは呼び出し元のワークスペース内のファイルにアクセス・操作できる
    *   別リポジトリへの書き込みは追加のチェックアウトやアクセス許可が必要

### コンポーザブルアクションでの別リポジトリとのファイル連携

別リポジトリへの出力ファイル生成など、リポジトリ間のファイル連携をする場合は、以下のパターンが一般的です：

```yaml
jobs:
  job_name:
    runs-on: ubuntu-latest
    steps:
      # ステップ1: メインリポジトリのチェックアウト
      - name: Checkout main repo
        uses: actions/checkout@v3

      # ステップ2: コンポーザブルアクションを実行して一時ファイルを生成
      - name: Run diary-converter
        uses: username/diary-converter@v1
        with:
          source_file: path/to/source.md
          destination_file: temp-output.md
          api_key: ${{ secrets.API_KEY }}

      # ステップ3: 別リポジトリをチェックアウト
      - name: Checkout target repo
        uses: actions/checkout@v3
        with:
          repository: username/target-repo
          path: target-repo
          token: ${{ secrets.TARGET_REPO_TOKEN }}

      # ステップ4: ファイルをコピーして変更をコミット
      - name: Copy and commit file
        run: |
          cp temp-output.md target-repo/path/to/destination.md
          cd target-repo
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add path/to/destination.md
          git commit -m "Update generated file"
          git push
```

### 今回の diary-converter で実装したコンポーザブルアクションの特徴

1.  **柔軟な入力パラメータ**:
    *   ソースファイル、出力先、APIキー、モデル名などを柔軟に設定可能
    *   オプションパラメータにはデフォルト値を設定

2.  **環境設定の自動化**:
    *   Pythonのセットアップ
    *   依存関係のインストール
    *   出力ディレクトリの準備

3.  **パス解決の工夫**:
    *   相対パスと絶対パスの両方に対応
    *   スクリプトディレクトリからの相対パスを正しく解決

4.  **エラーハンドリング**:
    *   出力ファイルの検証
    *   エラー時の適切な終了コード

これらの機能により、diary-converterのコンポーザブルアクションは再利用性が高く、様々なプロジェクトで簡単に利用できるようになっています。

## 所感

今回の開発作業を通じて、GitHub Actionsのコンポーザブルアクションについて深く理解することができました。これまで、GitHub Actionsはワークフローを定義するものという認識でしたが、コンポーザブルアクションを活用することで、よりモジュール化されたCI/CDパイプラインを構築できることを学びました。

また、diary-converterを独立したリポジトリとして切り出すことで、他のプロジェクトでの再利用性が高まり、開発効率の向上に貢献できることを実感しました。今後は、diary-converterの機能をさらに拡張し、より多くの開発者に利用してもらえるように、ドキュメントの整備やテストの拡充を進めていきたいと考えています。

## 今後の課題

今回の開発では、diary-converterを独立したリポジトリとして切り出し、GitHub Actionsのコンポーザブルアクションとして公開することができました。しかし、以下の課題が残っています。

1.  **テストの拡充**: 現在のテストは基本的な動作確認のみであるため、より多くのケースをカバーできるようにテストを拡充する必要があります。
2.  **ドキュメントの改善**: READMEは作成しましたが、より詳細なドキュメントやチュートリアルを作成する必要があります。
3.  **機能の拡張**: 現在のdiary-converterは基本的な変換機能のみであるため、より高度な変換機能やカスタマイズオプションを追加する必要があります。

## まとめ

今回は、diary-converterを独立したリポジトリとして切り出し、GitHub Actionsのコンポーザブルアクションとして公開することで、他のプロジェクトから簡単に利用できるようにしました。この取り組みにより、開発効率の向上やCI/CDパイプラインのモジュール化に貢献できると考えています。今後は、テストの拡充、ドキュメントの改善、機能の拡張を進め、より多くの開発者に利用してもらえるように、diary-converterを改善していきたいと考えています。