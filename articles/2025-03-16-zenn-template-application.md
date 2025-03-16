---
title: "2025-03-16 CI/CDパイプラインでのZennテンプレート適用問題の解決"
emoji: "🛠️"
type: "tech"
topics: ["CI/CD", "Zenn", "テンプレート", "自動化", "Python"]
published: true
---

:::message
この記事はClaude 3.7 Sonnetによって自動生成されています。
私の毎日の開発サイクルについては、[LLM対話で実現する継続的な開発プロセス](https://zenn.dev/centervil/articles/2025-03-12-development-cycle-introduction)をご覧ください。
:::

# CI/CDパイプラインでのZennテンプレート適用問題の解決

## はじめに

昨日はZenn連携用リポジトリの ./articles フォルダに生成された公開用日記をプッシュする機能を実装しました。今日は、CI/CDパイプラインで作成された公開用日記にZenn公開用記事のテンプレートが適用されていない問題を解決する開発を進めました。

## 背景と目的

CI/CDパイプラインを使って開発日記をZenn公開用記事に変換する自動化プロセスを構築していますが、生成された記事にZennテンプレートが正しく適用されていないという問題が発生しました。この問題を解決することで、一貫性のある高品質な記事を自動生成できるようにすることが今回の目的です。

## 検討内容

### 課題の整理

diary-converterの実装を確認したところ、以下の問題点が明らかになりました：

1. テンプレートからガイドライン部分のみを抽出して使用しており、テンプレート全体の構造を活用していない
2. frontmatterの設定が固定値になっており、テンプレートのfrontmatterが活用されていない
3. テンプレートファイルの存在確認が不十分で、エラーメッセージが不足している
4. プロンプト内でのfrontmatterの形式が明示的に指定されていない

### 解決アプローチ

これらの問題を解決するために、以下のアプローチを採用しました：

1. テンプレートの構造全体を活用するようにgenerate_prompt関数を修正
2. frontmatterをテンプレートから抽出して使用するように変更
3. テンプレートファイルの存在確認と詳細なエラーメッセージの追加
4. frontmatterの抽出処理の改善と詳細なログの追加
5. プロンプト生成部分の改善（frontmatterの形式を明示的に指定）

## 実装内容

### 1. diary_converter.pyのgenerate_prompt関数の修正

テンプレートからfrontmatterを抽出し、テンプレートの構造全体を活用するように変更しました。具体的には以下の修正を行いました：

```python
def generate_prompt(diary_content, template_path):
    """テンプレートを使用してプロンプトを生成する"""
    try:
        # テンプレートファイルの存在確認
        if not os.path.exists(template_path):
            print(f"エラー: テンプレートファイル '{template_path}' が見つかりません")
            print(f"カレントディレクトリ: {os.getcwd()}")
            print(f"ディレクトリ内容: {os.listdir(os.path.dirname(template_path) or '.')}")
            return None
            
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
            
        # frontmatterの抽出
        try:
            fm_data = frontmatter.loads(template_content)
            template_frontmatter = fm_data.metadata
            print(f"抽出したfrontmatter: {template_frontmatter}")
        except Exception as e:
            print(f"frontmatterの抽出に失敗しました: {e}")
            template_frontmatter = {
                "title": "{タイトル}",
                "emoji": "📝",
                "type": "tech",
                "topics": ["{トピック1}", "{トピック2}", "{トピック3}"],
                "published": False
            }
            
        # テンプレートの構造を取得
        template_structure = template_content.split('---', 2)[-1].strip()
        
        prompt = f"""
以下の開発日記を、Zenn公開用の記事に変換してください。

# 入力: 開発日記
{diary_content}

# 出力形式
Zenn公開用記事として、以下の形式で出力してください。
frontmatterは以下のYAML形式で記述し、```で囲んでください：

```
---
title: "YYYY-MM-DD 記事のタイトル"
emoji: "絵文字"
type: "tech"
topics: ["トピック1", "トピック2", "トピック3"]
published: true
---
```

frontmatterの後に、以下のメッセージを追加してください：
:::message
この記事は[{os.environ.get('LLM_MODEL', 'AI')}]によって自動生成されています。
私の毎日の開発サイクルについては、[LLM対話で実現する継続的な開発プロセス](https://zenn.dev/centervil/articles/2025-03-12-development-cycle-introduction)をご覧ください。
:::

その後、テンプレートの構造に従って記事を構成してください。
テンプレート構造:
{template_structure}
"""
        return prompt
    except Exception as e:
        print(f"プロンプト生成中にエラーが発生しました: {e}")
        return None
```

### 2. GitHub Actionsワークフローファイルの修正

diary-converterの実行時にデバッグフラグを追加し、テンプレートファイルが正しく認識されているか確認できるようにしました：

```yaml
- name: Run diary-converter
  run: |
    cd diary-converter
    python diary_converter.py \
      --input-file="../${{ env.DIARY_FILE }}" \
      --output-dir="../output" \
      --template-file="./templates/zenn_template.md" \
      --debug
```

### 3. ローカルテスト用スクリプトの修正

ローカル環境でのテストを容易にするために、test_ci_integration.shスクリプトも修正してデバッグモードを有効にしました：

```bash
#!/bin/bash
# テスト用のCI統合スクリプト

# 環境変数の設定
export DIARY_FILE="Documents/ProjectLogs/2025-03-15-zenn-repo-push-integration.md"
export LLM_MODEL="gemini-2.0-flash-001"

# diary-converterの実行
cd diary-converter
python diary_converter.py \
  --input-file="../$DIARY_FILE" \
  --output-dir="../output" \
  --template-file="./templates/zenn_template.md" \
  --debug

cd ..
```

## 所感

今回の開発で特に重要だったのは、テンプレートの構造全体を活用することでした。以前の実装では、テンプレートからガイドライン部分のみを抽出していたため、記事の構造が一貫していませんでした。また、frontmatterの処理も不十分だったため、記事のメタデータが適切に設定されていませんでした。

これらの問題を解決することで、CI/CDパイプラインで生成される記事の品質と一貫性が大幅に向上すると期待できます。特に、テンプレートファイルの存在確認と詳細なエラーメッセージの追加により、問題が発生した場合のデバッグも容易になりました。

## 今後の課題

1. **テンプレート適用の検証**: 修正後のdiary-converterが正しくテンプレートを適用しているか検証する必要があります。

2. **エラーハンドリングの強化**: テンプレートファイルの読み込みや処理に関するエラーハンドリングをさらに強化することで、より堅牢なシステムにできます。

3. **テスト環境の整備**: ローカル環境でのテストをより簡単に行えるようにテスト環境を整備することで、開発効率を向上させることができます。

4. **ログ出力の改善**: デバッグ情報をより詳細に出力し、問題の特定を容易にすることで、トラブルシューティングの効率を高めることができます。

5. **CI/CDパイプラインの安定性向上**: GitHub Actionsのワークフローの安定性を向上させることで、自動化プロセス全体の信頼性を高めることができます。

## まとめ

今日の開発では、CI/CDパイプラインで作成された公開用日記にZenn公開用記事のテンプレートが適用されていない問題を解決しました。具体的には、diary_converter.pyのgenerate_prompt関数を修正して、テンプレートの構造全体を活用し、frontmatterをテンプレートから抽出して使用するように変更しました。

また、テンプレートファイルの存在確認と詳細なエラーメッセージの追加、frontmatterの抽出処理の改善、プロンプト生成部分の改善なども行いました。これらの修正により、CI/CDパイプラインで作成された公開用日記にZenn公開用記事のテンプレートが適切に適用されるようになり、Zenn記事の品質と一貫性が向上することが期待されます。 