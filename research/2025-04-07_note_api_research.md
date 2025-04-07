### 直接の回答

- note.comには記事を公開するための非公式APIが存在するようですが、公式ドキュメントはなく、仕様は限定的です。
- Markdownで書かれた記事をAPIで公開するには、まずMarkdownをHTMLに変換する必要があります。
- ドラフト保存エンドポイントを使用して記事をドラフト状態で投稿し、その後ウェブサイト上で手動で公開する必要があります。

#### 手順

**MarkdownをHTMLに変換する**

- MarkdownコンテンツをHTMLに変換するために、Pythonの`markdown2`ライブラリなどのツールを使用できます。
  例: `import markdown2; html_content = markdown2.Markdown().convert(your_markdown_content)`

**認証**

- APIを使用するには認証が必要です。ログイン後にセッションクッキーや認証トークンを取得する方法を見つける必要がありますが、詳細は明確ではありません。

**ドラフトとして記事を投稿**

- ドラフト保存エンドポイント `[invalid url, do not cite]` を使用して、HTML形式のコンテンツを投稿します。
  リクエストボディはJSON形式で、`{"body": "your_html_content", "index": false}` のようになる可能性があります。

**記事を公開**

- ドラフトを投稿した後、note.comのウェブサイトにログインし、ドラフト記事を見つけて手動で公開する必要があります。
  公開用のAPIエンドポイントは現在のところ明確ではありません。

この方法は非公式APIに基づいており、仕様が変更される可能性があるため、note.comの利用規約を遵守し、サーバーに過度な負荷をかけないように注意してください。

---

### 詳細な調査報告

この調査では、note.comのAPIを使用してMarkdownで書かれた記事を公開する方法について、利用可能な情報に基づいて詳細に分析しました。以下に、調査の過程で得られた情報を整理し、ステップバイステップで説明します。

#### 背景とAPIの概要

note.comはクリエイターが文章やマンガ、写真、音声などを投稿できるプラットフォームであり、Markdown形式での記事作成をサポートしています ([note.com Markdown Support](https://note.com/guide))。しかし、公式のAPIドキュメントは提供されておらず、非公式APIの情報が主にコミュニティやブログ記事から得られる状況です。2023年および2024年の記事では、note.comの非公式APIについて詳細がまとめられており、特に記事の取得や操作に関するエンドポイントが記載されています ([2023年度 noteの非公式API一覧](https://note.com/ego_station/n/n85fcb635c0a9), [2024年版 note API 非公式一覧表](https://note.com/ego_station/n/n1a0b26f944f4))。

調査の結果、記事を直接公開するための明確なAPIエンドポイントは見つかりませんでしたが、ドラフト状態での記事投稿が可能なエンドポイントが存在することが確認されました。このエンドポイントは認証が必要であり、コンテンツはHTML形式で提供する必要があります。

#### MarkdownからHTMLへの変換

note.comのエディタはMarkdownをサポートしていますが、APIで記事を投稿する際にはHTML形式が要求されます ([note-APIで記事情報の取得](https://note.com/kiyo_ai_note/n/n4d7f8b9bd84a))。そのため、MarkdownコンテンツをHTMLに変換する必要があります。この変換には、プログラミング言語のMarkdownライブラリを使用できます。たとえば、Pythonでは`markdown2`ライブラリが便利です：

```python
import markdown2
html_content = markdown2.Markdown().convert(your_markdown_content)
```

他の言語でも同様のライブラリ（例：JavaScriptの`marked`、Rubyの`redcarpet`）が利用可能です。このステップは、APIリクエストの準備において必須となります。

#### 認証の必要性と方法

APIの使用には認証が必要です。特にドラフト保存エンドポイントは認証を必要とするため、セッションクッキーや認証トークンを取得する必要があります ([note APIの利用とユーザ認証について](https://note.com/takahiro_yazu/n/nf3477fbdf596))。しかし、note.comの公式ドキュメントや明確な認証フローは提供されておらず、コミュニティの情報によると、ログイン後のブラウザセッションから取得されるトークンやクッキーを利用する可能性が高いとされています。認証方法の詳細は不明確であり、ユーザーはネットワークリクエストを調査するか、ログイン後のAPI呼び出しを試行錯誤する必要があります。

#### ドラフト保存エンドポイントの使用

調査の結果、記事をドラフト状態で投稿するためのエンドポイントとして `[invalid url, do not cite]` が挙げられています ([note.muのAPIをざっくりと眺めてみた](https://qiita.com/kai_kou/items/b5757ec6b58d52ac0815))。このエンドポイントはPOSTメソッドを使用し、以下のようなリクエストボディを期待します：


| **API Function**          | **Description**                                     | **HTTP Method** | **Endpoint**                          | **Parameters**             | **Response Status Code** | **Authentication Required** |
| --------------------------- | ----------------------------------------------------- | ----------------- | --------------------------------------- | ---------------------------- | -------------------------- | ----------------------------- |
| Draft Save (Article Post) | Posts article in draft state, requires HTML in body | POST            | [invalid url, do not cite] id=xxxxxxx | {"body":"", "index":false} | 201                      | Yes                         |

ここで、`body`はHTML形式のコンテンツを指定し、`index`はインデックス化の設定（例：`false`）を意味します。IDパラメータ（`id=xxxxxxx`）の具体的な取得方法は不明ですが、ドラフト作成時に自動生成される可能性があります。

#### 記事の公開方法

ドラフトを投稿した後、記事を公開するための明確なAPIエンドポイントは見つかりませんでした。調査では、ドラフトの状態を「公開」に変更するエンドポイントの情報は提供されておらず、ユーザーはnote.comのウェブサイトにログインし、手動でドラフト記事を公開する必要があります ([noteのAPIを使用して、記事の詳細を取得する方法](https://qiita.com/app_js/items/78f3c63a7c8995fe3101))。将来的に公開用のエンドポイントが追加される可能性はありますが、現在のところ、手動操作が現実的な解決策です。

#### 注意事項

- 非公式APIは予告なく変更される可能性があり、サーバーに過度な負荷をかける行為は禁止されています ([noteの利用規約](https://note.com/terms))。
- APIの使用は自己責任で行い、note.comの規約を遵守してください。特に、認証情報やトークンの取り扱いには注意が必要です。
- ドラフト保存後の公開手順が手動であるため、完全自動化は難しい場合があります。

#### まとめ

この調査では、note.comの非公式APIを使用してMarkdown記事をドラフトとして投稿する方法を特定しました。MarkdownをHTMLに変換し、認証を取得した上でドラフト保存エンドポイントを使用することで、記事をドラフト状態で投稿できます。その後、ウェブサイト上で手動で公開する必要があります。APIの仕様は限定的であり、さらなる情報収集やコミュニティの動向に注意を払うことをお勧めします。

#### 主要引用

- [2023年度 noteの非公式API一覧](https://note.com/ego_station/n/n85fcb635c0a9)
- [2024年版 note API 非公式一覧表](https://note.com/ego_station/n/n1a0b26f944f4)
- [note-APIで記事情報の取得](https://note.com/kiyo_ai_note/n/n4d7f8b9bd84a)
- [note.muのAPIをざっくりと眺めてみた](https://qiita.com/kai_kou/items/b5757ec6b58d52ac0815)
- [note APIの利用とユーザ認証について](https://note.com/takahiro_yazu/n/nf3477fbdf596)
- [noteの利用規約](https://note.com/terms)
- [noteのAPIを使用して、記事の詳細を取得する方法](https://qiita.com/app_js/items/78f3c63a7c8995fe3101)
