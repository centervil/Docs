# 統合自動記録プロンプト (軽量版)

## 概要

このガイドは、LLMを用いた開発セッションの記録を自動化・軽量化するための指示です。コンテキスト量を削減しながら、効率的に開発記録を取得するための手順を示します。

## 基本設定

### クイックスタートコマンド

会話の最初に以下のコマンドを実行するだけで、自動記録が開始されます：

```
@dev-log-start テーマ="開発テーマ" records_path="/path/to/dev-records"
```

### パラメータ説明

- `テーマ`: 今日の開発テーマ（必須）
- `records_path`: 開発記録を保存するディレクトリの絶対パス（必須、初回のみ）

## 自動記録プロセス

1. **初期化処理**
   - 日付取得（YYYY-MM-DD形式）
   - 連番取得（最新ファイル番号+1）
   - 開発日記ファイル作成（`YYYY-MM-DD_NNN_development.md`）
   - 基本テンプレート適用
   - 前日の活動履歴自動取得

2. **自動記録機能**
   - 会話内容の自動記録（ユーザー・LLM双方）
   - コード出力・ツール実行結果の自動要約
   - 5回の対話ごとに自動保存チェックポイント

3. **コンテキスト最適化**
   - 外部パス参照によるワークスペース分離
   - MCPベースのファイル操作
   - 必要最小限のガイド参照

## ファイル構造

```markdown
# YYYY-MM-DD development

## 今日の開発テーマ

今日の開発テーマは[テーマ]です。

## 前日までの活動履歴
前日までの活動履歴は以下の通りです：
* YYYY-MM-DD: [活動内容] (ファイル名: YYYY-MM-DD_NNN_development.md)

## 会話ログ

- ユーザー: [最初のメッセージ]
- LLM: [応答]
...
```

## MCP活用による分離ワークスペース対応

### MCPベースのファイル操作

開発記録ファイルは、開発対象プロジェクトとは別のディレクトリ（`records_path`）に保存されます。ファイル操作には以下のMCP機能を利用します：

1. **ファイル読み込み**
   ```javascript
   fileSystem.readFile(records_path + "/latest_file.md")
   ```

2. **ファイル書き込み**
   ```javascript
   fileSystem.writeFile(records_path + "/YYYY-MM-DD_NNN_development.md", content)
   ```

3. **ディレクトリ一覧取得**
   ```javascript
   fileSystem.listDir(records_path)
   ```

### 軽量化されたワークスペース

- 開発対象のプロジェクトのみをワークスペースに含める
- 開発記録は外部ディレクトリに保存
- コンテキスト量の大幅削減
- プロジェクト切り替え時も同じ記録パスを使用可能

## 記録ルール

### 会話ログの自動記録

- 各対話を「- ユーザー: 」または「- LLM: 」で開始
- 完全な対話内容を記録
- コード出力は要約形式で記録
- ツール実行結果は重要部分のみ要約

### 記録の最適化

- 重要な対話は完全記録
- 大量出力は要約記録
- 自動保存ポイントで信頼性確保
- MCPによる外部ファイル操作で分離管理

## 実装例

```javascript
// 開発記録初期化関数の例
function initDevLog(theme, recordsPath) {
  const date = new Date().toISOString().split('T')[0];
  const files = fileSystem.listDir(recordsPath);
  const latestNum = getLatestFileNumber(files);
  const newNum = latestNum + 1;
  const fileName = `${date}_${String(newNum).padStart(3, '0')}_development.md`;
  
  // テンプレート作成
  const template = `# ${date} development\n\n## 今日の開発テーマ\n\n今日の開発テーマは${theme}です。\n\n## 前日までの活動履歴\n${getRecentActivity(recordsPath)}\n\n## 会話ログ\n\n`;
  
  // ファイル作成
  fileSystem.writeFile(recordsPath + "/" + fileName, template);
  
  return fileName;
}

// 会話記録追加関数の例
function appendConversation(recordsPath, fileName, role, content) {
  const currentContent = fileSystem.readFile(recordsPath + "/" + fileName);
  const newContent = currentContent + `\n- ${role}: ${summarizeIfNeeded(content)}`;
  fileSystem.writeFile(recordsPath + "/" + fileName, newContent);
}
```

## 移行ガイド

1. 従来の全プロジェクト含むワークスペースから、開発対象プロジェクトのみのワークスペースに移行
2. 開発記録は絶対パス指定で外部管理
3. `@dev-log-start` コマンドで簡単に記録開始
4. MCPベースのファイル操作で記録の一貫性を確保

## まとめ

この軽量版ガイドにより、以下のメリットが得られます：

1. コンテキスト量の大幅削減
2. 開発者の負担最小化（1コマンドのみ）
3. 自動化レベルの維持
4. 分離されたワークスペースによる効率向上
5. 柔軟性とパフォーマンスの両立 