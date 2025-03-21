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

昨日は、diary_converter.py を別リポジトリから利用できるようにするための準備を進めました。今日は、その具体的な実装と、GitHub Actionsのコンポーザブルアクションについて深掘りしていきます。

## 背景と目的

これまで、diary_converter.py は特定のリポジトリに依存していましたが、他のプロジェクトでも再利用できるように、独立したリポジトリとして切り出すことにしました。これにより、CI/CDパイプラインでの利用が容易になり、開発効率の向上が期待できます。

## 検討内容

### 課題の整理

diary_converter.py を独立させるにあたり、以下の課題が挙げられました。

1.  **依存関係の管理**: 独立したリポジトリとして、必要な依存関係を明確にする必要がある。
2.  **パスの調整**: テンプレートファイルのパスなどを、独立した環境に合わせて修正する必要がある。
3.  **CI/CD連携**: 既存のCI/CDパイプラインとの連携方法を確立する必要がある。
4.  **ドキュメント**: 他の開発者が利用しやすいように、詳細なドキュメントを作成する必要がある。

### 解決アプローチ

これらの課題を解決するために、以下のアプローチを検討しました。

1.  **依存関係の整理**: `requirements.txt` を見直し、必要なパッケージを明示的に記述する。
2.  **パスの調整**: 相対パスを使用し、環境に依存しないようにする。
3.  **CI/CD連携**: GitHub Actionsのコンポーザブルアクションを利用し、簡単に連携できるようにする。
4.  **ドキュメント**: README.md を充実させ、利用方法やCI/CD連携について詳しく解説する。

## 実装内容

### 1. 独立リポジトリ用のREADME.mdの作成

独立したリポジトリで使用するための新しいREADMEファイルを作成しました。このファイルにはツールの概要、インストール方法、使用方法、CI/CDパイプラインでの利用方法など、詳細な情報を記載しています。特に、CI/CDパイプラインでの利用方法については、以下の3つのアプローチを解説しました。

*   Gitリポジトリのクローンによるアプローチ
*   GitHubリリースからのダウンロードによるアプローチ
*   GitHub Actionsのコンポーザブルアクションによるアプローチ

### 2. GitHub Actionsのコンポーザブルアクションの設定

`action.yml`ファイルを作成し、GitHub Actionsのコンポーザブルアクションとして利用できるようにしました。このアクションは以下のような形式で簡単に利用できます。

```yaml
- name: Run diary-converter
  uses: [username]/diary-converter@v1
  with:
    source_file: Documents/ProjectLogs/latest.md
    destination_file: articles/output.md
    api_key: ${{ secrets.GOOGLE_API_KEY }}
```

`action.yml` の中身は以下のようになっています。

```yaml
name: 'Diary Converter'
description: 'Convert diary entries to various formats.'
inputs:
  source_file:
    description: 'Path to the source diary file.'
    required: true
  destination_file:
    description: 'Path to the destination file.'
    required: true
  api_key:
    description: 'API key for external services.'
    required: false
  template_path:
    description: 'Path to the template file.'
    default: './templates/zenn_template.md'
  debug_mode:
    description: 'Enable debug mode.'
    default: 'false'
runs:
  using: "composite"
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
        python diary_converter.py "${{ inputs.source_file }}" "${{ inputs.destination_file }}" --api_key "${{ inputs.api_key }}" --template_path "${{ inputs.template_path }}" --debug_mode "${{ inputs.debug_mode }}"
```

### 3. テンプレートファイルの調整

テンプレートファイルを`templates`ディレクトリに配置し、独立リポジトリとして機能するように構造を整理しました。テンプレートファイルは `templates/zenn_template.md` に配置し、内容は変更していません。

### 4. diary_converter.pyの修正

- デフォルトテンプレートパスを相対パスに変更しました。
- テンプレート読み込み処理を改善し、相対パスを正しく解決できるようにしました。
- 独立リポジトリとして機能するために不要な特定のパス調整コードを削除しました。

### 5. Docker関連ファイルの整備

独立リポジトリで使用するためのdocker-compose.ymlファイルを作成し、適切なボリュームマウントと環境変数設定を行いました。

## 技術的なポイント

今回の実装で特に重要だったのは、GitHub Actionsのコンポーザブルアクションの理解と、それを利用したCI/CD連携の実装です。コンポーザブルアクションを利用することで、diary_converter.py を他のリポジトリから簡単に利用できるようになりました。

また、パスの調整も重要なポイントでした。相対パスを使用することで、環境に依存しないようにし、独立したリポジトリとしての可搬性を高めました。

## 所感

今回の開発を通じて、GitHub Actionsのコンポーザブルアクションの強力さを改めて実感しました。これまで、CI/CDパイプラインは複雑になりがちでしたが、コンポーザブルアクションを利用することで、よりシンプルで再利用可能なパイプラインを構築できるようになりました。

また、diary_converter.py を独立したリポジトリとして切り出すことで、他のプロジェクトでの利用が容易になり、開発効率の向上に貢献できることを期待しています。

最初はコンポーザブルアクションの仕組みを理解するのに苦労しましたが、実際に手を動かして実装することで、そのメリットを実感することができました。特に、`action.yml` の書き方や、入力パラメータの受け渡し方など、実践的な知識を得ることができました。

## 今後の課題

今後の課題としては、以下の点が挙げられます。

1.  **テストの自動化**: 独立したリポジトリとして、テストの自動化を強化する必要がある。
2.  **ドキュメントの充実**: より詳細なドキュメントを作成し、利用者の利便性を向上させる必要がある。
3.  **機能の拡張**: さまざまな形式の出力に対応するなど、機能の拡張を検討する必要がある。

## まとめ

今回は、diary_converter.py を独立したリポジトリとして切り出し、GitHub Actionsのコンポーザブルアクションを利用してCI/CD連携を実現しました。これにより、diary_converter.py の再利用性が向上し、開発効率の向上に貢献できることを期待しています。

今回の開発を通じて、GitHub Actionsのコンポーザブルアクションの強力さを改めて実感することができました。今後は、この知識を活かして、よりシンプルで再利用可能なCI/CDパイプラインを構築していきたいと思います。