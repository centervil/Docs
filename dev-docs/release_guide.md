## リリースガイド

### 1. バージョン番号の更新

`setup.py` の `version` フィールドを更新します。

### 2. 変更履歴の更新

`CHANGELOG.md` にリリース内容を記載します。

### 3. リリースブランチの作成

```bash
git checkout -b release/vX.Y.Z
git add .
git commit -m "Prepare release vX.Y.Z"
git push origin release/vX.Y.Z
```

### 4. リリースの作成

1. GitHubのリポジトリページに移動
2. "Releases" → "Draft a new release"
3. タグバージョン（例：v1.0.0）を指定
4. リリースタイトルと説明を入力
5. "Publish release"をクリック

### 5. PyPIへの公開

GitHub Actionsが自動的にパッケージをビルドし、PyPIにアップロードします。

### 6. リリース後の確認

- [PyPI](https://pypi.org/project/content-converter/)でパッケージが公開されているか確認
- ドキュメントが更新されているか確認
- リリースノートが正しいか確認

### 7. メンテナンスブランチの更新

```bash
git checkout main
git merge --no-ff release/vX.Y.Z
git push origin main
```

### 8. 次の開発サイクルの準備

```bash
git checkout develop
git merge main
git push origin develop
```

## 注意事項

- リリース前に必ずテストを実行
- 依存パッケージのバージョンが適切か確認
- セキュリティチェックを実施
