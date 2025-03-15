---
title: "2025-03-15 Zenn連携リポジトリへの日記自動プッシュ機能の実装"
emoji: "🚀"
type: "tech"
topics: ["CI/CD", "GitHub Actions", "Zenn"]
published: false
---

:::message
この記事は[gemini-2.0-flash-001]によって自動生成されています。
私の毎日の開発サイクルについては、[LLM対話で実現する継続的な開発プロセス](https://zenn.dev/centervil/articles/2025-03-12-development-cycle-introduction)をご覧ください。
:::

# Zenn連携リポジトリへの日記自動プッシュ機能の実装

## はじめに

昨日はdiary-converterで生成されたZenn公開用日記を自動でZenn連携リポジトリにプッシュする機能を実装しました。今日は、その内容をZennの記事としてまとめます。

## 背景と目的

開発日記をZennで公開するプロセスを自動化するために、CI/CDパイプラインにZenn連携リポジトリへのプッシュ機能を追加しました。これにより、開発者は手動で記事をアップロードする手間を省き、より効率的に情報発信できるようになります。

## 検討内容

### 課題の整理

1.  diary-converterで生成された公開用日記を、別のZenn連携用リポジトリにプッシュする必要がある。
2.  リポジトリ間でのファイル共有が必要。
3.  GitHub Actionsから別のリポジトリにプッシュするための認証情報が必要。
4.  ジョブの実行順序を適切に設定する必要がある。

### 解決アプローチ

1.  GitHub Actionsワークフローに新しいジョブ「zenn-push」を追加。
2.  2つのリポジトリを別々のパスにチェックアウトする方法を採用。
3.  GitHub環境変数（$GITHUB_ENV）を使用してジョブ間でファイル情報を共有。
4.  GitHub Secretsに「ZENN_REPO」と「ZENN_REPO_TOKEN」を追加。
5.  zenn-pushジョブはdiary-converterジョブに依存するように設定。backend-deployジョブはzenn-pushジョブにも依存するように更新。

## 実装内容

GitHub Actionsワークフローファイルを修正して、生成された公開用日記を別のZenn連携用リポジトリにプッシュする機能を追加しました。具体的には、新しい「zenn-push」ジョブを作成し、diary-converterジョブで生成された記事ファイルをZennリポジトリの./articlesディレクトリにコピーしてプッシュする処理を実装しました。

```yaml
# deploy.yml
name: Deploy

on:
  push:
    branches:
      - main

jobs:
  diary-converter:
    # ... 既存のジョブ設定 ...

  zenn-push:
    needs: diary-converter
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Zenn Repo
        uses: actions/checkout@v3
        with:
          repository: ${{ secrets.ZENN_REPO }}
          token: ${{ secrets.ZENN_REPO_TOKEN }}
          path: ./zenn-repo

      - name: Copy Article
        run: |
          ARTICLE_PATH=$(echo ${{ needs.diary-converter.outputs.article_path }} | tr -d '\r')
          mkdir -p ./zenn-repo/articles
          cp $ARTICLE_PATH ./zenn-repo/articles/

      - name: Git Config
        run: |
          cd ./zenn-repo
          git config --global user.email "github-actions@github.com"
          git config --global user.name "GitHub Actions"
          git add .
          git commit -m "Add new article" || echo "No changes to commit"
          git push origin main

  backend-deploy:
    needs: zenn-push
    # ... 既存のジョブ設定 ...
```

### 変更点1: Zennリポジトリへのプッシュジョブの追加

GitHub Actionsのワークフローに、Zennリポジトリへのプッシュを行う新しいジョブを追加しました。このジョブでは、Zennリポジトリをチェックアウトし、生成された記事ファイルをコピーしてプッシュします。

### 変更点2: リポジトリ間のファイル共有

diary-converterジョブで生成されたファイル情報を、GitHub環境変数を使用してzenn-pushジョブに渡すようにしました。これにより、ジョブ間でファイル情報を共有し、スムーズな連携を実現しています。

## 技術的なポイント

GitHub Actionsで複数のリポジトリを扱うために、actions/checkoutアクションでrepositoryとtokenを指定して、Zennリポジトリをチェックアウトしています。また、GitHub SecretsにZENN\_REPOとZENN\_REPO\_TOKENを設定し、セキュアに認証情報を管理しています。

## 所感

今回の開発では、CI/CDパイプラインにZenn連携リポジトリへのプッシュ機能を組み込むことで、開発日記からZenn記事への変換と公開プロセスを完全に自動化することができました。これにより、手動操作によるミスを防止し、より効率的に情報発信できるようになりました。

## 今後の課題

1.  エラーハンドリングの強化
2.  重複記事の検出と処理
3.  記事メタデータの自動更新
4.  プッシュ結果の通知
5.  GitHub Secretsの設定方法のドキュメント整備
6.  テスト環境の構築
7.  記事の品質チェック

## まとめ

今回の開発では、diary-converterで生成された公開用日記をZenn連携用リポジトリにプッシュするための機能を実装しました。これにより、開発日記からZenn記事への変換と公開プロセスが完全に自動化され、手動操作によるミスを防止できるようになりました。今後は、エラーハンドリングの強化や重複記事の検出など、さらなる改善を進めていく予定です。