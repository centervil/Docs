# 情報セキュリティマネジメント試験 30日間学習計画Day 4

この記事の内容はPodCastとしても配信しています。
<!-- PodCastのURLを載せる -->

## 📚 今日の学習テーマ：パスワード・認証攻撃と基本的なウェブ攻撃

### 📝 学習の目標

* パスワード攻撃の種類と仕組みを理解する。
* SQLインジェクション、XSS、CSRFの基本的な概念と対策を理解する。
* 認証情報の適切な管理方法と多要素認証の重要性を認識する。

### 🔍 カバーする範囲

本日は、パスワードに対する攻撃手法（辞書攻撃、ブルートフォース攻撃、クレデンシャルスタッフィングなど）と、代表的なウェブアプリケーションへの攻撃手法（SQLインジェクション、クロスサイトスクリプティング、CSRF）について学習します。また、これらの攻撃からシステムを守るための認証管理の重要性についても触れます。

## 📖 解説パート

### パスワード攻撃

パスワード攻撃は、不正にアカウントへのアクセス権限を得るために、パスワードを特定しようとする攻撃の総称です。主な手法には以下のようなものがあります。

* **辞書攻撃 (Dictionary Attack)**：よく使われる単語やフレーズ、過去に漏洩したパスワードのリスト（辞書）を用いて、パスワードを試行する攻撃です。単純なパスワードや推測しやすいパスワードが設定されている場合に有効です。
* **ブルートフォース攻撃 (Brute-force Attack)**：考えられるすべての文字の組み合わせを総当たりで試行する攻撃です。時間と計算資源が必要ですが、十分に短いか単純なパスワードであれば解読される可能性があります。
* **リバースブルートフォース攻撃 (Reverse Brute-force Attack)**：一つのパスワードを固定し、多数のユーザーIDに対して試行する攻撃です。特定のパスワード（例："password123"）が多くのユーザーに使われている場合に有効です。
* **クレデンシャルスタッフィング (Credential Stuffing)**：他のサービスから漏洩したIDとパスワードのリストを利用して、別のサービスへの不正ログインを試みる攻撃です。多くのユーザーが複数のサービスで同じ認証情報を使い回していることを悪用します。
* **パスワードスプレー攻撃 (Password Spraying Attack)**：少数のよく使われるパスワード（例："Password@1"、"Qwerty1234"）を、多数のアカウントに対して試行する攻撃です。アカウントロックアウトを避けるために、試行回数を低く抑え、時間をかけて行われることがあります。

これらの攻撃から保護するためには、推測されにくい複雑なパスワードの使用、定期的なパスワード変更、そして多要素認証の導入が不可欠です。

### 基本的なウェブ攻撃手法

ウェブアプリケーションは常に様々な攻撃の標的となります。ここでは特に重要な3つの攻撃手法について解説します。

* **SQLインジェクション (SQL Injection)**：ウェブアプリケーションがデータベースと連携する際に、入力フォームなどに不正なSQL文を注入（インジェクション）することで、データベースを不正に操作する攻撃です。情報の窃取、改ざん、削除などが行われる可能性があります。対策としては、プレースホルダの使用（プリペアドステートメント）、入力値の検証（バリデーション）、エスケープ処理、ウェブアプリケーションファイアウォール（WAF）の導入などがあります。

* **クロスサイトスクリプティング (Cross-Site Scripting, XSS)**：攻撃者が悪意のあるスクリプトをウェブページに埋め込み、それを閲覧したユーザーのブラウザ上で実行させる攻撃です。ユーザーのクッキー情報（セッションIDなど）の窃取、ウェブサイトの改ざん、マルウェアの配布などに悪用されます。対策としては、入力値のサニタイジング（無害化）、出力時のエスケープ処理、Content Security Policy (CSP) の設定、WAFの導入などが挙げられます。

* **CSRF (Cross-Site Request Forgery)**：ユーザーがログイン状態のサービスに対して、攻撃者が用意した罠サイトなどを経由して、ユーザーの意図しないリクエストを送信させる攻撃です。パスワード変更、商品購入、退会処理などが不正に行われる可能性があります。対策としては、トークン（CSRFトークン）の使用、重要な操作の前に再認証を求める、SameSite Cookie属性の設定などがあります。

#### 重要ポイント

* パスワード攻撃は多様であり、単純なパスワードは容易に破られる危険性がある。
* SQLインジェクションはデータベースへの不正操作を可能にし、情報漏洩の主要な原因となる。
* XSSはユーザーのブラウザを悪用し、セッションハイジャックやフィッシングに繋がる。
* CSRFはユーザーの意図しない操作を強制実行させる。
* 適切な入力検証、エスケープ処理、多要素認証、WAFの導入がこれらの攻撃に対する基本的な防御策となる。

## 🏢 ケーススタディ

### ケース：大手ECサイトにおけるクレデンシャルスタッフィング被害

ある大手ECサイトで、多数のユーザーアカウントへの不正ログインが発生しました。調査の結果、攻撃者は他のサービスから漏洩したと思われる大量のIDとパスワードのリストを使用し、自動化ツールでログイン試行を繰り返していたことが判明しました（クレデンシャルスタッフィング）。被害に遭ったアカウントでは、登録されていたクレジットカード情報が悪用され、不正な商品購入が行われました。同サイトでは、パスワードの複雑性要件は設定されていたものの、多要素認証はオプションであり、多くのユーザーが利用していませんでした。

#### 問題点

* ユーザーが複数のサービスで同じパスワードを使い回していた。
* ECサイト側で多要素認証が必須化されていなかった。
* 不正なログイン試行を検知し、アカウントを一時的にロックする仕組みが不十分だった。

#### 対応策

* 全ユーザーに対してパスワードリセットを強制し、より複雑なパスワードの設定を推奨する。
* 多要素認証の利用を強く推奨、あるいは重要な操作（購入、個人情報変更など）では必須化する。
* 短時間に多数のログイン失敗があったIPアドレスやアカウントを検知し、一時的にアクセスを制限するレートリミット機能を強化する。
* ユーザーに対して、パスワードの使い回しを避けるよう啓発活動を行う。
* 漏洩した認証情報が自社サービスで使われていないか定期的にチェックする仕組みを導入する。

#### ケースから学ぶ教訓

* パスワードの使い回しは、一つのサービスからの情報漏洩が他のサービスにも波及するリスクを高める。
* 多要素認証は、パスワードが漏洩した場合でも不正アクセスを防ぐための非常に有効な手段である。
* サービス提供者は、不正アクセスを早期に検知し対応するための監視体制と、ユーザーを保護するためのセキュリティ機能を継続的に強化する必要がある。

## 📝 理解度チェックテスト

以下の問題を解いて、今日の学習内容の理解度をチェックしましょう。

### 問題1

パスワード攻撃の一つで、事前に用意された単語やフレーズのリスト（辞書）を用いてパスワードを試行する攻撃手法は何ですか。

1. ブルートフォース攻撃
2. 辞書攻撃
3. クレデンシャルスタッフィング
4. リバースブルートフォース攻撃

### 問題2

ウェブアプリケーションの入力フォームに不正なSQL文を注入し、データベースを不正に操作する攻撃手法は何ですか。

1. クロスサイトスクリプティング (XSS)
2. CSRF (Cross-Site Request Forgery)
3. SQLインジェクション
4. DDoS攻撃

### 問題3

クロスサイトスクリプティング (XSS) の対策として適切でないものはどれですか。

1. 入力値のサニタイジング
2. Content Security Policy (CSP) の設定
3. プレースホルダの使用
4. 出力時のエスケープ処理

### 問題4

ユーザーがログインしているサービスに対し、本人の意図しないリクエストを送信させる攻撃手法は何ですか。

1. SQLインジェクション
2. フィッシング
3. CSRF (Cross-Site Request Forgery)
4. 中間者攻撃

### 問題5

クレデンシャルスタッフィング攻撃が成功する主な原因として最も適切なものはどれですか。

1. ユーザーが推測しやすい単純なパスワードを使用している。
2. ユーザーが複数のオンラインサービスで同じIDとパスワードを使い回している。
3. ウェブサイトがSSL/TLSによる暗号化通信を導入していない。
4. 攻撃者が高度なソーシャルエンジニアリング技術を使用している。

## 📋 今日のまとめ

* パスワード攻撃には辞書攻撃、ブルートフォース攻撃、クレデンシャルスタッフィングなどがあり、複雑なパスワードと多要素認証が対策の基本です。
* SQLインジェクションはデータベースを標的とし、入力検証やプレースホルダの使用で防ぎます。
* XSSはユーザーのブラウザで悪意のあるスクリプトを実行させ、サニタイジングやエスケープ処理で対策します。
* CSRFはユーザーに意図しない操作を強制し、CSRFトークンや再認証で対策します。
* 認証情報の適切な管理と、ウェブアプリケーションの脆弱性対策は、情報セキュリティにおいて非常に重要です。

### 次回予告

明日は「中間者・セッション攻撃 – MITM、フィッシング、リプレイ」について学習します。

## ✅ テスト回答・解説

### 問題1 正解：2. 辞書攻撃

解説：辞書攻撃は、パスワードとしてよく使われる単語やフレーズ、あるいは過去に漏洩したパスワードのリスト（辞書）を利用してログインを試みる手法です。ブルートフォース攻撃は総当たり、クレデンシャルスタッフィングは他サービスからの漏洩情報、リバースブルートフォースはパスワード固定でIDを試行します。

### 問題2 正解：3. SQLインジェクション

解説：SQLインジェクションは、アプリケーションのセキュリティ上の不備を意図的に利用し、アプリケーションが想定しないSQL文を実行させることにより、データベースシステムを不正に操作する攻撃方法です。XSSはスクリプト埋め込み、CSRFは意図しないリクエスト送信、DDoSはサービス妨害攻撃です。

### 問題3 正解：3. プレースホルダの使用

解説：プレースホルダの使用（プリペアドステートメント）は、SQLインジェクションの対策として非常に有効な手段です。XSSの対策としては、入力値のサニタイジング、出力時のエスケープ処理、CSPの設定などが挙げられます。

### 問題4 正解：3. CSRF (Cross-Site Request Forgery)

解説：CSRFは、ユーザーが特定のウェブサイトにログインした状態で、攻撃者が用意した別のウェブサイトのリンクをクリックするなどして、意図しないリクエスト（商品の購入、退会処理など）をログイン中のウェブサイトに送信させられてしまう攻撃です。

### 問題5 正解：2. ユーザーが複数のオンラインサービスで同じIDとパスワードを使い回している

解説：クレデンシャルスタッフィング攻撃は、あるサービスから漏洩した認証情報（IDとパスワードの組み合わせ）をリスト化し、それを他のサービスに対して試行する攻撃です。そのため、ユーザーが複数のサービスで同じ認証情報を使い回している場合に成功しやすくなります。

## 📚 参考資料・リソース

* 情報処理推進機構 (IPA) - 安全なウェブサイトの作り方: [https://www.ipa.go.jp/security/vuln/websecurity.html](https://www.ipa.go.jp/security/vuln/websecurity.html)
* OWASP Japan - OWASP Top 10: [https://owasp.org/www-project-top-ten/](https://owasp.org/www-project-top-ten/) (主に開発者向けですが、攻撃手法の理解に役立ちます)
* JPCERT/CC - 注意喚起情報: [https://www.jpcert.or.jp/at/](https://www.jpcert.or.jp/at/)
