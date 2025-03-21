---
title: "2025-03-21 Diary-Converterのリポジトリ移行"
emoji: "🚚"
type: "idea"
topics: ['GitHub Actions', 'リポジトリ移行', 'コンポーザブルアクション']
published: false
---

:::message
この記事はgemini-2.0-flash-001によって自動生成されています。
私の毎日の開発サイクルについては、[LLM対話で実現する継続的な開発プロセス](https://zenn.dev/centervil/articles/2025-03-12-development-cycle-introduction)をご覧ください。
:::

# Diary-Converterのリポジトリ移行

## はじめに

昨日はDiary-Converterを独立したリポジトリにする準備を行いました。今日は、いよいよそのリポジトリ移行を実行し、GitHub Actionsのコンポーザブルアクションとして利用できるように設定していきます。

## 背景と目的

これまで、Diary-ConverterはSiteWatcherプロジェクトの一部として存在していました。しかし、より汎用的に利用できるようにするため、独立したリポジトリとして公開することにしました。これにより、他のプロジェクトからも簡単に利用できるようになり、再利用性とメンテナンス性が向上します。特に、GitHub Actionsのコンポーザブルアクションとして提供することで、CI/CDパイプラインへの組み込みが容易になることを期待しています。

## 検討内容

### 課題の整理

リポジトリ移行にあたり、以下の課題を整理しました。

1.  **ファイルの移動**: SiteWatcherリポジトリからDiary-Converter関連のファイルを安全かつ確実に移動する必要がある。
2.  **CI/CDパイプラインの修正**: SiteWatcher側のCI/CDパイプラインを修正し、新しいDiary-Converterリポジトリを参照するように変更する必要がある。
3.  **コンポーザブルアクション化**: Diary-ConverterをGitHub Actionsのコンポーザブルアクションとして利用できるように設定する必要がある。

### 解決アプローチ

これらの課題を解決するために、以下のアプローチを検討しました。

1.  **ファイルの移動**: `cp -r`コマンドを使用して、SiteWatcher内のDiary-Converter関連ファイルを新しいリポジトリにコピーする。
2.  **CI/CDパイプラインの修正**: SiteWatcherの`deploy.yml`ファイルを修正し、`uses`キーワードで新しいDiary-Converterリポジトリを参照するように変更する。
3.  **コンポーザブルアクション化**: Diary-Converterリポジトリに`action.yml`ファイルを作成し、コンポーザブルアクションとしてのメタデータを定義する。

## 実装内容

実際に行った作業内容は以下の通りです。

1.  **ファイルの移動**:

    ```bash
    cp -r SiteWatcher/tools/diary-converter /home/centervil/Diary-Converter
    mv /home/centervil/Diary-Converter/INDEPENDENT_README.md /home/centervil/Diary-Converter/README.md
    ```

    SiteWatcher内の`diary-converter`ディレクトリの内容を、事前に作成しておいた`/home/centervil/Diary-Converter`にコピーしました。また、`INDEPENDENT_README.md`を正式な`README.md`としてリネームしました。

2.  **移行先リポジトリの更新**:

    ```bash
    cd /home/centervil/Diary-Converter
    git add .
    git commit -m "Initial commit"
    git push origin main
    ```

    コピーしたファイルをステージングし、初期コミットを作成してGitHubにプッシュしました。

3.  **SiteWatcherリポジトリの更新**:

    ```yaml
    # .github/workflows/deploy.yml
    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
          - name: Run diary-converter
            uses: centervil/Diary-Converter@main
            with:
              source_file: path/to/source.md
              destination_file: path/to/output.md
              api_key: ${{ secrets.GOOGLE_API_KEY }}
              model: gemini-2.0-flash-001
              template: path/to/template.md
              debug: 'true'
    ```

    SiteWatcherの`deploy.yml`ファイルを修正し、`uses`キーワードで新しいDiary-Converterリポジトリを参照するように変更しました。これにより、CI/CDパイプライン内でDiary-Converterのコンポーザブルアクションを利用できるようになりました。

    ```bash
    rm -rf SiteWatcher/tools/diary-converter
    git add .
    git commit -m "Update CI/CD pipeline to use composable action"
    git push origin main
    ```

    元の`diary-converter`ディレクトリを削除し、変更をコミットしてGitHubにプッシュしました。

## 技術的なポイント

今回の実装で特に重要だった技術的なポイントは、GitHub Actionsのコンポーザブルアクションの利用方法です。コンポーザブルアクションを使用することで、処理を再利用可能な形にカプセル化し、複数のリポジトリやワークフローで共有できます。

### GitHub Actionsのコンポーザブルアクション解説

今回の開発で学んだGitHub Actionsのコンポーザブルアクションについて、以下に詳細を記録します：

#### コンポーザブルアクションとは

コンポーザブルアクションは、複数のステップをまとめて再利用可能な形にパッケージ化するGitHub Actionsの機能です。通常のワークフロー（`.github/workflows/*.yml`）が単一のリポジトリ内で定義・実行されるのに対し、コンポーザブルアクションは異なるリポジトリ間で共有・再利用できます。

#### 主な利点

1.  **再利用性**: 同じ処理を複数のリポジトリやワークフローで再利用できる
2.  **カプセル化**: 複雑な処理をシンプルなインターフェースで提供できる
3.  **メンテナンス性**: 実装の変更を一箇所で行い、利用側は参照を更新するだけでよい
4.  **バージョン管理**: タグやリリースを通じてバージョン管理ができる

#### コンポーザブルアクションの定義方法

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

#### 他のリポジトリからの利用方法

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

#### 仕組みと動作原理

1.  **アクションの取得**:
    *   ワークフローの実行時、GitHubはアクションリポジトリを指定された参照（ref）で取得
    *   アクションのコードは一時的にワークフロー実行環境にダウンロードされる

2.  **パラメータの受け渡し**:
    *   `with`で指定した入力値が`inputs`として渡される
    *   アクション内では`${{ inputs.input_name }}`で参照できる

3.  **実行コンテキスト**:
    *   アクションは呼び出し元のワークフローコンテキスト内で実行される
    *   `${{ github.workspace }}`は呼び出し元リポジトリのチェックアウトパス

#### diary-converterでの実装例

今回実装したdiary-converterのコンポーザブルアクションは以下のように使用できます：

```yaml
- name: Run diary-converter
  uses: centervil/Diary-Converter@main
  with:
    source_file: path/to/source.md
    destination_file: path/to/output.md
    api_key: ${{ secrets.GOOGLE_API_KEY }}
    model: gemini-2.0-flash-001
    template: path/to/template.md
    debug: 'true'
```

この実装により、diary-converterの機能を他のプロジェクトから簡単に利用できるようになりました。

## 所感

今回のリポジトリ移行作業は、思った以上にスムーズに進めることができました。特に、GitHub Actionsのコンポーザブルアクションについて深く理解できたことが大きな収穫です。これまでは、CI/CDパイプライン内でスクリプトを直接実行していましたが、コンポーザブルアクションを使うことで、コードの再利用性が高まり、メンテナンスも容易になります。

最初は、コンポーザブルアクションの設定に少し手間取りましたが、GitHubのドキュメントやサンプルコードを参考にしながら、なんとか実装することができました。実際に動くようになったときは、達成感がありましたね。

## 今後の課題

今回のリポジトリ移行は完了しましたが、まだいくつかの課題が残っています。

1.  **ドキュメントの整備**: Diary-Converterの利用方法や設定方法について、より詳細なドキュメントを作成する必要があります。
2.  **テストの追加**: コンポーザブルアクションとしての動作を検証するためのテストを追加する必要があります。
3.  **バージョン管理**: タグやリリースを活用して、Diary-Converterのバージョン管理を適切に行う必要があります。

## まとめ

今回は、Diary-Converterを独立したリポジトリに移行し、GitHub Actionsのコンポーザブルアクションとして利用できるように設定しました。これにより、Diary-Converterの再利用性とメンテナンス性が向上し、他のプロジェクトからも簡単に利用できるようになりました。今後は、ドキュメントの整備やテストの追加を行い、より使いやすいツールとして成長させていきたいと思います。