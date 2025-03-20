---
title: "2025-03-20 Diary Converter Independence"
emoji: "🔄"
type: "tech"
topics: ["CI/CD", "GitHub Actions", "開発日記", "Python"]
published: false
---

:::message
この記事はgemini-2.0-flash-001によって自動生成されています。
私の毎日の開発サイクルについては、[LLM対話で実現する継続的な開発プロセス](https://zenn.dev/centervil/articles/2025-03-12-development-cycle-introduction)をご覧ください。
:::

# diary-converterの独立リポジトリ化

## はじめに

昨日まではCI/CDパイプラインの改善やZenn記事のフォーマット修正に取り組んでいました。今日は、開発日記をZenn公開用記事に変換するツール「diary-converter」を独立したリポジトリとして切り出し、他のプロジェクトからでも利用できるようにする作業を進めました。

## 背景と目的

開発日記をZenn用の記事に変換するツール「diary-converter」は現在SiteWatcherリポジトリの一部として実装されており、このリポジトリ内でのみ使用可能です。しかし、このツールは汎用性が高く、他のプロジェクトでも活用できる可能性があります。

独立したリポジトリとして切り出すことで、複数のプロジェクトから利用可能になり、メンテナンスもしやすくなります。また、GitHub Actionsのコンポーザブルアクションとして実装することで、CI/CDパイプラインへの組み込みも簡単になります。

## 検討内容

### 課題の整理

diary-converterを独立リポジトリ化するためには、以下の課題に対応する必要がありました：

1. 環境依存を解消し、異なる環境でも動作するよう調整
2. パス参照を相対パスに変更し、どこからでも実行可能に
3. テンプレートファイルの管理方法の見直し
4. GitHub Actionsから簡単に利用できる仕組みの構築
5. Docker環境での実行をより柔軟に

### 解決アプローチ

これらの課題を解決するために、以下のアプローチを採用しました：

1. 独立リポジトリ用の新しいREADMEと構成ファイルの作成
2. GitHub Actionsのコンポーザブルアクション設定の実装
3. テンプレートディレクトリの整理と相対パス対応
4. スクリプト自体の修正（パス解決ロジックの改善）
5. Docker関連ファイルの整備と柔軟な設定

複数のアプローチを検討した結果、GitHub Actionsのコンポーザブルアクションが最も柔軟性が高く、他のプロジェクトからの利用も簡単だと判断しました。

## 実装内容

独立リポジトリとしてdiary-converterを機能させるため、以下の変更を実装しました。

### 変更点1: 独立リポジトリ用のREADMEの作成

独立したリポジトリで使用するための新しいREADMEファイル（INDEPENDENT_README.md）を作成しました。このファイルには以下の内容を記載しています：

- ツールの概要と機能説明
- インストール方法と基本的な使用方法
- 詳細オプションと環境変数の設定方法
- Docker環境での実行手順
- CI/CDパイプラインでの利用方法（3つのアプローチ）
- テスト方法と開発への貢献方法

### 変更点2: GitHub Actionsのコンポーザブルアクション設定

`action.yml`ファイルを作成し、GitHub Actionsのコンポーザブルアクションとして利用できるようにしました：

```yaml
name: 'Diary Converter'
description: 'Convert development diary logs to Zenn articles'
inputs:
  source_file:
    description: 'Path to the source diary file'
    required: true
  destination_file:
    description: 'Path to the destination article file'
    required: true
  api_key:
    description: 'Gemini API Key'
    required: true
  model:
    description: 'Gemini model to use'
    required: false
    default: 'gemini-2.0-flash-001'
  # ... その他のパラメータ ...
runs:
  using: 'composite'
  steps:
    - name: Set up Python
      uses: actions/setup-python@v4
      # ... その他のステップ ...
```

これにより、他のリポジトリから以下のようにシンプルに呼び出すことができます：

```yaml
- name: Run diary-converter
  uses: username/diary-converter@v1
  with:
    source_file: Documents/ProjectLogs/latest.md
    destination_file: articles/output.md
    api_key: ${{ secrets.GOOGLE_API_KEY }}
```

### 変更点3: ディレクトリ構造の整理とテンプレートファイルの調整

テンプレートファイルを`templates`ディレクトリに配置し、独立リポジトリとして機能するように構造を整理しました：

```
diary-converter/
├── diary_converter.py
├── requirements.txt
├── action.yml
├── docker-compose.yml
├── Dockerfile
├── docker-entrypoint.sh
├── README.md
└── templates/
    └── zenn_template.md
```

### 変更点4: diary_converter.pyの修正

スクリプト自体にも複数の修正を加えました：

- デフォルトテンプレートパスを相対パス（`./templates/zenn_template.md`）に変更
- テンプレート読み込み処理を改善し、相対パスを正しく解決できるように
- 不要なパス調整コードを削除し、どの環境でも一貫して動作するように

```python
def read_template(template_path):
    """テンプレートファイルを読み込む"""
    try:
        # 相対パスを解決
        if not os.path.isabs(template_path):
            # スクリプトの実行ディレクトリからの相対パス
            script_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(script_dir, template_path)
        
        # テンプレートファイルの存在確認...
```

### 変更点5: Docker関連ファイルの整備

docker-compose.ymlファイルを作成・更新し、適切なボリュームマウントと環境変数設定を行いました：

```yaml
version: '3.8'

services:
  diary-converter:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: diary-converter
    volumes:
      - ./input:/app/input
      - ./output:/app/output
      - ./templates:/app/templates
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    entrypoint: ["/app/docker-entrypoint.sh"]
```

## 技術的なポイント

今回の実装で特に重要だったのは、GitHub Actionsのコンポーザブルアクションの活用です。これにより、複雑なセットアップや実行手順を単一のアクションにカプセル化し、他のリポジトリから簡単に利用できるようになりました。

コンポーザブルアクションのメリットは、複数のステップをまとめて再利用可能な形にパッケージ化できる点です。一度作成したアクションは、異なるリポジトリ間で共有・再利用できます。

```yaml
# action.ymlでの定義
runs:
  using: 'composite'
  steps:
    - name: Set up Python
      uses: actions/setup-python@v4
    - name: Install dependencies
      run: pip install -r requirements.txt
      shell: bash
    - name: Run converter
      run: python diary_converter.py ...
      shell: bash
```

また、パス解決のロジックも重要でした。独立したリポジトリでは、ハードコードされたパスは機能しないため、相対パスを適切に解決する仕組みを実装しました。

## 所感

diary-converterを独立リポジトリとして切り出す作業を通じて、モジュール化と再利用性の重要性を実感しました。最初は単純なタスクだと思っていましたが、実際に取り組んでみると、環境依存の解消やパス解決の問題など、意外と考慮すべき点が多かったです。

特にGitHub Actionsのコンポーザブルアクションについては、今回初めて深く学ぶ機会となりました。これまではワークフロー内に直接コマンドを記述していましたが、再利用可能なアクションとしてパッケージ化することで、メンテナンス性が大幅に向上することを実感しました。

ある意味で、このdiary-converterの独立リポジトリ化は「マイクロサービス化」に似ている面があります。単一の大きなシステムから機能を分離し、独立して進化できるようにすることで、全体の柔軟性が向上していきます。

## 今後の課題

今回の実装で残された課題としては以下が挙げられます：

1. 別リポジトリへの記事出力をよりスムーズにする機能の追加
2. テンプレートのカスタマイズ機能の強化
3. CI/CDパイプラインとの統合テストの実施
4. 変換品質のさらなる向上とエラーハンドリングの強化
5. GitHub Actionsのバージョン管理戦略の検討

また、重複したメッセージボックスが生成される問題については、diary_converter.pyのプロンプト生成部分かGemini APIからの応答処理部分での修正が必要です。

## まとめ

diary-converterを独立したリポジトリとして切り出し、GitHub Actionsのコンポーザブルアクションとして実装することで、より柔軟で再利用可能なツールに進化させることができました。特に、CI/CDパイプラインとの統合がシンプルになった点は大きな成果です。

今回学んだGitHub Actionsのコンポーザブルアクションの知識は、今後の開発でも活用していきたいと思います。共通機能をアクション化することで、コードの重複を減らし、メンテナンス性を高められることを実感しました。

次のステップとしては、実際に新しいGitHubリポジトリを作成し、diary-converterを移行した上で、既存プロジェクトのCI/CDパイプラインを更新して連携テストを行う予定です。 