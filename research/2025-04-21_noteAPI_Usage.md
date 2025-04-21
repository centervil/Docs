## noteAPIで下書きを作成するためのコマンド例

noteの非公式APIを利用して「下書き記事」をAPI経由で作成したい場合、直接的なREST APIエンドポイントとしては `/v1/text_notes/draft_save` が知られています。ただし、このAPIは完全な公式ドキュメントが存在せず、認証やパラメータの詳細も非公開です。  
一方、Pythonライブラリ（例：`Note_Client`）を使うことで、ログイン認証を含めて比較的簡単に下書き投稿が可能です[2][5]。

---

### Pythonライブラリを使った下書き作成コマンド例

#### 1. 必要な準備
- `Note_Client` ライブラリをインストール（PyPIやGitHubから入手）
- 投稿内容を記載したテキストファイル（例：`content.txt`）を用意

#### 2. サンプルコード

```python
from Note_Client import Note

EMAIL = 'your email'
PASSWORD = 'your password'
USER_ID = 'your user_id'
TITLE = 'APIテスト下書き'
CONTENT_PATH = 'content.txt'
TAG_LIST = ['api_test']

# 下書き保存の場合、POST_SETTINGをFalseにする（省略時も下書き）
POST_SETTING = False

note = Note(email=EMAIL, password=PASSWORD, user_id=USER_ID)
result = note.create_article(
    title=TITLE,
    file_name=CONTENT_PATH,
    input_tag_list=TAG_LIST,
    post_setting=POST_SETTING
)
print(result)
```
- `POST_SETTING=False` または省略 → 下書き保存
- `POST_SETTING=True` → 公開投稿

#### 3. content.txt の例

```
# これはAPI経由で作成した下書き記事です
テスト投稿です。
```

#### 4. 実行結果例

```json
{'run':'success','title':'APIテスト下書き','file_path':'content.txt','tag_list':['api_test'],'post_setting':'Draft'}
```


---

### 参考：非公式APIエンドポイント

REST APIとして直接リクエストを送る場合、以下のようなエンドポイントが知られていますが、認証情報（クッキーやトークン）が必須です。

```
POST https://note.com/api/v1/text_notes/draft_save?id=xxxxxxx
```
- パラメータや認証の詳細は公開されていません[5]。

---

## 注意事項

- 非公式APIの利用はnoteの利用規約やシステム変更により動作しなくなる場合があります。
- アカウントへの影響や規約違反リスクも考慮してください[2][5]。

---

### まとめ

- Pythonライブラリ（`Note_Client`など）を使えば、簡単にAPI経由で下書き記事が作成できます。
- REST APIエンドポイントの直接利用は認証やパラメータ仕様が不明なため、基本的にはライブラリ経由が安全です[2][5]。

Citations:
[1] https://note.com/ego_station/n/n85fcb635c0a9
[2] https://note.com/naokun_gadget/n/naf129cb5f34b
[3] https://docs.strapi.io/cms/api/document-service/status
[4] https://note.com/kiyo_ai_note/n/n4d7f8b9bd84a
[5] https://note.com/masuyohasiri/n/n1e8161d81866
[6] https://note.com/ego_station/n/n1a0b26f944f4
[7] https://note.com/nanashi2025/n/ne8cd329b045e
[8] https://note.com/kitahara_note/n/n42731ca085b6
[9] https://www.arch.info.mie-u.ac.jp/gitlab/help/api/draft_notes.md
[10] https://gitlab-docs.creationline.com/ee/api/draft_notes.html
[11] https://note.com/m_d_log/n/n3e68b8ad4e80
[12] https://note.com/plusjam/n/ndd5c7061e9b2
[13] https://note.com/suzuki_reiko/n/n757e453a1c0a
[14] https://note.com/fukugyou3/n/n4cb7614a9523
[15] https://zenn.dev/centervil/articles/2025-04-05_036_dev-diary
[16] https://forum.ghost.org/t/how-to-get-all-drafts-data-using-content-api/44538
[17] https://qiita.com/kai_kou/items/b5757ec6b58d52ac0815
[18] https://note.egg-glass.jp/%E6%8A%80%E8%A1%93/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0/2023/05/30/2023%E5%B9%B4%E5%BA%A6-note%E3%81%AE%E9%9D%9E%E5%85%AC%E5%BC%8FAPI%E4%B8%80%E8%A6%A7.html
[19] https://python-gitlab.readthedocs.io/en/stable/gl_objects/draft_notes.html
[20] https://docs.gitlab.com/api/draft_notes/

---
Perplexity の Eliot より: pplx.ai/share