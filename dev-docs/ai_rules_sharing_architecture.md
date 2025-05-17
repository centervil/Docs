# AIエージェント間ルール共有アーキテクチャ

## 1. 概要

複数のAIエージェント（Cursor、Windsurf、Clineなど）間でルールファイルを効率的に共有するためのアーキテクチャです。このアーキテクチャは以下の目標を達成します：

- 複数プロジェクト間でのルール共有
- 複数AIエージェント間での知識ベース共有
- コンテキスト消費の最適化（必要な時に必要な知識のみ参照）
- メンテナンス性の向上（単一アダプターファイルのみ管理）

## 2. アーキテクチャ構成

### 2.1 全体構造

```
project-root/
├── .git/
├── .gitmodules                 # Gitサブモジュール定義
├── ai-rules/                   # サブモジュールとしてマウントされる中央リポジトリ
│   ├── knowledge/              # 知識ベース
│   ├── mode/                   # 動作モード定義
│   ├── references/             # 詳細参照資料
│   └── adapters/               # 各AIエージェント用アダプターテンプレート
│       ├── cursor_adapter.mdc  # Cursor用テンプレート
│       ├── windsurf_adapter.md # Windsurf用テンプレート
│       └── cline_adapter.yaml  # Cline用テンプレート
├── .cursor/                    # Cursor固有の設定ディレクトリ
│   └── rules/
│       └── cursor_rules_adapter.mdc  # Cursor用単一アダプター（シンボリックリンク）
├── .windsurf/                  # Windsurf固有の設定ディレクトリ
│   └── rules/
│       └── windsurf_rules_adapter.md # Windsurf用単一アダプター（シンボリックリンク）
└── .cline/                     # Cline固有の設定ディレクトリ
    └── rules/
        └── cline_rules_adapter.yaml  # Cline用単一アダプター（シンボリックリンク）
```

### 2.2 中央リポジトリ構造

中央リポジトリ（`ai-rules`）は以下のディレクトリ構造を持ちます：

```
ai-rules/
├── knowledge/              # 知識ベース
│   ├── knowledge_development_process.md
│   ├── knowledge_security_best_practices.md
│   └── ...
├── mode/                   # 動作モード定義
│   ├── mode_tdd_facilitator.md
│   ├── mode_github_flow_guide.md
│   ├── mode_threat_modeling_support.md
│   └── ...
├── references/             # 詳細参照資料
│   ├── reference_coding_standards.md
│   ├── reference_security_checklist.md
│   └── ...
└── adapters/               # 各AIエージェント用アダプターテンプレート
    ├── cursor_adapter.mdc  # Cursor用テンプレート
    ├── windsurf_adapter.md # Windsurf用テンプレート
    └── cline_adapter.yaml  # Cline用テンプレート
```

## 3. モード選択型単一アダプター

各AIエージェントは1つのアダプターファイルのみを使用し、これが「モード選択」と「必要な知識の参照ガイド」を担当します。

### 3.1 アダプターファイルの役割

- タスクに応じた適切なモードの選択をガイド
- 利用可能なモードの一覧と説明を提供
- モードファイルの参照方法を説明
- 必要に応じて知識ベースへの参照方法を提供

### 3.2 アダプターファイルの例（Cursor用）

```markdown
---
title: "Rules Adapter for Cursor"
description: "AIエージェント用ルール・モード選択アダプター"
---

# モード選択アダプター

このファイルはタスクに応じて適切なモードを選択し、必要な知識ベースを参照するためのアダプターです。

## 利用可能なモード一覧

以下のモードが利用可能です。タスクに応じて適切なモードをアクティブにしてください：

- `mode_tdd_facilitator`: TDD手法によるソフトウェア開発支援
- `mode_github_flow_guide`: GitHub Flowに基づくブランチ戦略支援
- `mode_threat_modeling_support`: セキュリティ脅威モデリング支援
- （他のモード一覧）

## モード選択方法

特定のモードを使用するには、以下のいずれかの方法でモードファイルを参照してください：

1. **直接参照**:
```
mode_tdd_facilitator Ruleを適用してテスト駆動開発を支援してください
```

2. **知識参照**:
各モードは必要に応じて以下の知識ベースを参照します：
- `knowledge_development_process.md`: 開発プロセスの知識
- `knowledge_security_best_practices.md`: セキュリティベストプラクティス
- （他の知識ベース）

## モードファイルの場所

実際のモードファイルは以下のディレクトリに格納されています：
- モード: `/path/to/ai-rules/mode/`
- 知識: `/path/to/ai-rules/knowledge/`
- 参考: `/path/to/ai-rules/references/`
```

## 4. Gitサブモジュールによる実装

### 4.1 中央リポジトリの準備

1. GitHub等に中央リポジトリを作成
```bash
# 新規リポジトリの作成
mkdir ai-rules
cd ai-rules
git init
# ディレクトリ構造の作成
mkdir -p knowledge mode references adapters
# 初期ファイルの作成
touch knowledge/knowledge_development_process.md
touch mode/mode_tdd_facilitator.md
touch references/reference_coding_standards.md
# アダプターテンプレートの作成
touch adapters/cursor_adapter.mdc
touch adapters/windsurf_adapter.md
touch adapters/cline_adapter.yaml
# 変更をコミット
git add .
git commit -m "Initial commit with directory structure"
# リモートリポジトリに接続（例：GitHub）
git remote add origin https://github.com/username/ai-rules.git
git push -u origin main
```

### 4.2 プロジェクトへのサブモジュール追加

```bash
# プロジェクトディレクトリに移動
cd /path/to/your/project

# サブモジュールとして中央リポジトリを追加
git submodule add https://github.com/username/ai-rules.git ai-rules

# サブモジュールの初期化と更新
git submodule init
git submodule update
```

### 4.3 アダプターファイルのシンボリックリンク作成

```bash
# 必要なディレクトリの作成
mkdir -p .cursor/rules
mkdir -p .windsurf/rules
mkdir -p .cline/rules

# シンボリックリンクの作成
# Cursor用
ln -s $(pwd)/ai-rules/adapters/cursor_adapter.mdc .cursor/rules/cursor_rules_adapter.mdc
# Windsurf用
ln -s $(pwd)/ai-rules/adapters/windsurf_adapter.md .windsurf/rules/windsurf_rules_adapter.md
# Cline用
ln -s $(pwd)/ai-rules/adapters/cline_adapter.yaml .cline/rules/cline_rules_adapter.yaml

# 変更をコミット
git add .
git commit -m "Add AI rules submodule and adapter symlinks"
```

### 4.4 サブモジュールの更新

```bash
# 中央リポジトリの最新変更を取得
git submodule update --remote ai-rules

# 変更をコミット
git add ai-rules
git commit -m "Update AI rules submodule"
```

## 5. プロジェクト間での共有

複数のプロジェクトで同じ中央リポジトリを共有するには、各プロジェクトで同様のサブモジュール設定を行います。

```bash
# 別のプロジェクトディレクトリに移動
cd /path/to/another/project

# 同じサブモジュールを追加
git submodule add https://github.com/username/ai-rules.git ai-rules
git submodule init
git submodule update

# アダプターファイルのシンボリックリンク作成（上記と同様）
```

## 6. 利用フロー

1. **初期状態**: ユーザーは単一アダプターファイルだけを参照
2. **モード選択**: ユーザーがタスクに応じて特定のモードを選択
3. **知識の参照**: 選択したモードが必要に応じて知識ベースを参照
4. **コンテキスト節約**: 必要な知識のみが参照されるため、コンテキスト消費を最小化

## 7. メリット

- **一元管理**: すべてのルールファイルが中央リポジトリで管理される
- **複数プロジェクト共有**: Gitサブモジュールにより複数プロジェクトで同じルールを共有
- **AIエージェント間共有**: 各AIエージェント用のアダプターを通じて同じ知識ベースを共有
- **コンテキスト最適化**: 必要な時に必要な知識のみを参照
- **メンテナンス性**: アダプターファイルは各AIエージェントごとに1つのみ
- **拡張性**: 新しいAIエージェントへの対応は新しいアダプターテンプレートの追加のみ

## 8. 注意点

- シンボリックリンクはWindows環境では制限がある場合があります
- Gitサブモジュールの操作に慣れていないチームメンバーには教育が必要
- 中央リポジトリの変更は各プロジェクトで明示的に更新する必要があります

## 9. 代替案

### 9.1 コピー方式

シンボリックリンクの代わりに、セットアップスクリプトを使用してアダプターファイルをコピーする方法：

```bash
#!/bin/bash
# setup_adapters.sh

# アダプターファイルのコピー
mkdir -p .cursor/rules
mkdir -p .windsurf/rules
mkdir -p .cline/rules

cp ai-rules/adapters/cursor_adapter.mdc .cursor/rules/cursor_rules_adapter.mdc
cp ai-rules/adapters/windsurf_adapter.md .windsurf/rules/windsurf_rules_adapter.md
cp ai-rules/adapters/cline_adapter.yaml .cline/rules/cline_rules_adapter.yaml

echo "Adapter files have been copied successfully."
```

### 9.2 テンプレート生成方式

アダプターファイルをテンプレートから動的に生成する方法：

```bash
#!/bin/bash
# generate_adapters.sh

# 設定ファイルの読み込み
source adapter_config.sh

# アダプターファイルの生成
mkdir -p .cursor/rules
cat > .cursor/rules/cursor_rules_adapter.mdc << EOF
---
title: "Rules Adapter for Cursor"
description: "AIエージェント用ルール・モード選択アダプター"
---

# モード選択アダプター

$(cat ai-rules/adapters/cursor_adapter_template.md)

## 利用可能なモード一覧

$(for mode in $(ls ai-rules/mode/); do
  echo "- \`${mode%.*}\`: $(head -n 1 ai-rules/mode/$mode | sed 's/^# //')"
done)

## モードファイルの場所

実際のモードファイルは以下のディレクトリに格納されています：
- モード: \`$(pwd)/ai-rules/mode/\`
- 知識: \`$(pwd)/ai-rules/knowledge/\`
- 参考: \`$(pwd)/ai-rules/references/\`
EOF

echo "Adapter files have been generated successfully."
```

## 10. まとめ

このアーキテクチャにより、複数のAIエージェント間でルールファイルを効率的に共有しながら、各AIエージェントの特性を活かした利用が可能になります。Gitサブモジュールを活用することで、複数プロジェクト間での一貫性も確保されます。
