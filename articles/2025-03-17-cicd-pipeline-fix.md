---
title: "2025-03-17 Cicd Pipeline Fix"
emoji: "🛠️"
type: "idea"
topics: ['CI/CD', 'GitHub Actions', 'Zenn']
published: false
---

:::message
この記事はgemini-2.0-flash-001によって自動生成されています。

:::

# 2025-03-17 Cicd Pipeline Fix

## はじめに

昨日はZenn公開用記事のテンプレート適用問題を解決しました。今日は、その流れでCI/CDパイプラインの不具合を修正し、Zennリポジトリへの公開用日記のプッシュが正常に行われるようにします。

## 背景と目的

開発日記をZenn記事として自動公開するためのCI/CDパイプラインを構築しましたが、昨日の修正後、パイプラインが正常に動作せず、記事がZennリポジトリにプッシュされませんでした。この問題を解決し、スムーズなZenn公開フローを確立することが今回の目的です。

## 検討内容

### 課題の整理

今回の問題は、diary-converterジョブで生成された記事が、zenn-pushジョブに正しく引き継がれていないことです。具体的には、以下の点が課題として挙げられます。

1.  diary-converterジョブは正常に実行され、記事が生成されている
2.  zenn-pushジョブの実行時に、`main-repo/articles/` ディレクトリが空になっている
3.  環境変数 `GENERATED_ARTICLE_FILENAME` が空になっている

### 解決アプローチ

これらの課題を解決するために、以下の解決アプローチを検討しました。

1.  diary-converterジョブで生成されたファイルをアーティファクトとして保存し、zenn-pushジョブでダウンロードする
2.  GitHub Actionsのアーティファクト関連アクションのバージョンを確認し、最新の安定バージョンを使用する
3.  zenn-pushジョブでのファイルコピー処理を簡素化し、エラーハンドリングを強化する

## 実装内容

GitHub Actionsのワークフローファイル（deploy.yml）を修正し、以下の実装を行いました。

```yaml
# deploy.yml (一部抜粋)

jobs:
  diary-converter:
    # ...
    steps:
      - name: Generate article
        # ...

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: generated-article
          path: /app/articles/2025-03-16-zenn-template-application.md
          if-no-files-found: error

  zenn-push:
    # ...
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: generated-article
          path: main-repo/articles/

      - name: Copy article
        run: cp main-repo/articles/2025-03-16-zenn-template-application.md ./articles/2025-03-16-zenn-template-application.md
```

### 変更点1: diary-converterジョブの改善

diary-converterジョブで生成されたファイルをアーティファクトとして保存するように変更しました。`actions/upload-artifact` を使用してファイルを保存し、ファイルが見つからない場合のエラーハンドリングを追加しました。

### 変更点2: zenn-pushジョブの改善

`actions/download-artifact` を使用してファイルを取得するように変更しました。不要なメインリポジトリのチェックアウトを削除し、ファイルコピー処理のロジックを簡素化しました。また、Git操作（コミットメッセージとステージング処理）を改善しました。

### 変更点3: GitHub Actionsのバージョン更新

`actions/upload-artifact` と `actions/download-artifact` をv2からv4に更新しました。

## 技術的なポイント

今回の修正で特に重要だった技術的なポイントは、GitHub Actionsのアーティファクト機能の活用です。ジョブ間でファイルを共有する際に、アーティファクトを使用することで、ファイルの一貫性を保ち、ジョブ間の依存関係を明確にすることができます。また、エラーハンドリングを強化することで、パイプラインの安定性を向上させることができました。

## 所感

今回のCI/CDパイプラインの修正作業は、GitHub Actionsの理解を深める良い機会となりました。特に、アーティファクト機能の活用方法や、ジョブ間の依存関係の管理方法について学ぶことができました。また、パイプラインのエラーログを分析し、問題の原因を特定するプロセスは、デバッグスキルを向上させる上で非常に役立ちました。最初は単純なファイル共有の問題だと思っていましたが、実際にはGitHub Actionsのバージョン管理やエラーハンドリングなど、様々な要素が絡み合っていることを実感しました。

## 今後の課題

今回の修正で、Zennリポジトリへの公開用日記のプッシュは正常に行われるようになりましたが、以下の課題が残っています。

1.  パイプラインの実行時間の短縮
2.  エラーログの監視体制の強化
3.  自動テストの導入

## まとめ

今回は、CI/CDパイプラインの不具合を修正し、Zennリポジトリへの公開用日記のプッシュが正常に行われるようにしました。GitHub Actionsのアーティファクト機能を活用し、ジョブ間のファイル共有を確実に行うことができました。今回の修正を通じて、GitHub Actionsの理解を深め、パイプラインの安定性を向上させることができました。今後は、パイプラインの実行時間の短縮やエラーログの監視体制の強化など、さらなる改善に取り組んでいきたいと思います。