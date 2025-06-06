# 主要ポイント

- 証券口座の乗っ取り被害が急増し、5ヶ月で5,200億円超の不正取引が発生
- Cisco ISEクラウド版に深刻な脆弱性が発見され、ホットフィクスが公開
- 中小企業のサイバーセキュリティ対策に認識と実装のギャップ、AIを活用した防御策の採用は11%にとどまる

## 金融セキュリティ

金融庁は2025年6月5日、証券口座の乗っ取り被害が急増していると発表しました。2025年1月から5月までの5ヶ月間で確認された不正アクセスは10,422件、不正取引は5,958件に上り、売却・買付金額は合計で5,200億円を超える規模となっています。特に4月の被害が顕著で、不正アクセス件数と被害金額が大きく増加しました。

## 脆弱性とセキュリティ対策

Cisco Systemsが提供するネットワーク認証管理製品「Cisco Identity Services Engine（ISE）」のクラウド版に深刻な脆弱性が明らかとなりました。「Amazon Web Services（AWS）」「Microsoft Azure」「Oracle Cloud Infrastructure（OCI）」において、同一のバージョン、クラウドプラットフォームで展開されたCisco ISE間で、共通の認証情報が生成される脆弱性「CVE-2025-20286」が判明しました。共通脆弱性評価システム「CVSSv3.1」のベーススコアは「9.9」、重要度は「クリティカル（Critical）」とレーティングされています。

## 企業のセキュリティ動向

クラウドストライクは「2025年版中小企業サイバーセキュリティ報告書」を発表し、中小企業におけるサイバーセキュリティに対する認識と対策との間のギャップが拡大していることを明らかにしました。中小企業の93%がサイバーセキュリティリスクについて知識があると考えており、83%が対策を立てていると報告されていますが、新しいツールに投資しているのはわずか36%で、AIを活用した防御策を採用しているのはわずか11%にとどまっています。

---

## ニュース詳細

### 1. 証券口座の乗っ取り、不正取引 金額は5,000億円近くに

金融庁は2025年6月5日、不正アクセスによる証券口座の乗っ取り被害が急増しているとして、改めて強い注意喚起を行いました。2025年1月から5月の5ヶ月間で確認された不正アクセスは10,422件、不正取引は5,958件に上り、売却・買付金額は合計で5,200億円を超えました。

被害の多くは、フィッシングサイトでログイン情報（IDやパスワード）を盗まれた後、不正に口座へアクセスされ、保有株式を勝手に売却、得た資金で小型株を買付けるという流れです。この結果、被害者の口座には価値の不明な小型株が残されることになります。

この攻撃の背景には、「CoGUI（コグイ）」というフィッシングキットが関係している可能性が指摘されており、日本のIPのみを標的にしたジオフェンシングや、ブラウザ・端末情報の事前取得、正規サイトへリダイレクトする手口、月1億通超の大量メール送信といった極めて洗練された攻撃手法が確認されています。

金融庁は証券会社の顧客に対し、ブックマークからのアクセス、多要素認証の活用、強固なパスワードの使用、口座の定期確認、OSやセキュリティソフトの更新などの対策を強く推奨しています。

[出典: セキュリティニュース - 証券口座の乗っ取り、不正取引 金額は5,000億円近くに](https://rocket-boys.co.jp/security-measures-lab/securities-account-hacks-reach-500-billion-yen/)

### 2. 「Cisco ISE」クラウド版に深刻な脆弱性 - ホットフィクスを公開

Cisco Systemsが提供するネットワーク認証管理製品「Cisco Identity Services Engine（ISE）」に深刻な脆弱性が明らかとなりました。実証コード（PoC）も確認されています。

「Amazon Web Services（AWS）」「Microsoft Azure」「Oracle Cloud Infrastructure（OCI）」において、同一のバージョン、クラウドプラットフォームで展開されたCisco ISE間で、共通の認証情報が生成される深刻な脆弱性「CVE-2025-20286」が判明しました。

「Primary Administrationノード」をクラウド上に構成している場合に影響し、クラウドに展開された「Cisco ISE」から認証情報を抽出し、ほかのクラウド環境に導入されている同製品にアクセスし、システム構成の変更、限定的な管理操作、機密データへのアクセスなどが可能となります。

共通脆弱性評価システム「CVSSv3.1」のベーススコアは「9.9」、重要度は「クリティカル（Critical）」とレーティングされています。オンプレミス環境では影響を受けません。同脆弱性の悪用は確認されていないが、概念実証（PoC）コードが利用できる状態にあるとのことです。

同社は「Cisco ISE 3.4」「同3.3」「同3.2」「同3.1」向けにホットフィクスを提供。また10月以降にリリースする「同3.4P3」「同3.3P8」で修正を予定しています。

[出典: Security NEXT - 「Cisco ISE」クラウド版に深刻な脆弱性 - ホットフィクスを公開](https://www.security-next.com/171040)

### 3. クラウドストライク、「2025年版中小企業サイバーセキュリティ報告書」を発表

クラウドストライク（NASDAQ: CRWD）は「2025年版中小企業サイバーセキュリティ報告書」を発表しました。これにより、中小企業 (SMB) におけるサイバーセキュリティに対する認識と対策との間のギャップが拡大していることが明らかになりました。中小企業の93%がサイバーセキュリティリスクについて知識があると考えており、83%が対策を立てていると報告されていますが、新しいツールに投資しているのはわずか36%で、AIを活用した防御策を採用しているのはわずか11%です。

報告書の要点として、従業員数が50人未満の中小企業では、セキュリティ計画を実施していると回答したのはわずか47%で、半数以上が年間予算の1%未満をサイバーセキュリティに割り当てていると報告されています。また、中小企業の67%がサイバーセキュリティソリューションを選択する際に手頃な価格を優先する一方、高度な脅威に対する保護を優先すると答えたのはわずか57%で、現在のサイバーセキュリティ予算で本当に十分であると考えているのはわずか6.5%でした。

過去1年間にサイバーインシデントを経験した従業員25人未満の中小企業のうち、29%がランサムウェアを報告したのに対し、大企業では19%でした。現在、AIを活用したセキュリティを使用している中小企業はわずか11%で、ほとんどの中小企業はまだ初期段階にあります。

[出典: PR TIMES - クラウドストライク、「2025年版中小企業サイバーセキュリティ報告書」を発表：高い認知度、遅れる保護](https://prtimes.jp/main/html/rd/p/000000115.000031049.html)

## 深掘り

### サイバーセキュリティ対策の新たな潮流

最新のサイバーセキュリティ対策では、AIを活用した先制的な防御が重要視されています。チェック・ポイント・ソフトウェア・テクノロジーズ（NASDAQ: CHKP）がVeriti Cybersecurity社の買収を発表したことからも、この傾向が顕著に表れています。Veritiは複雑なマルチベンダー環境において、業界初となる、完全に自動化されたマルチベンダー対応の先制的脅威エクスポージャーおよび緩和プラットフォームを提供します。

AIによってサイバーセキュリティは転換点を迎え、攻撃者は大規模な攻撃を容易に実行できるようになりました。同時に、企業はクラウド、データセンター、エンドポイントに資産が分散したハイパーコネクテッドな状態にあり、攻撃対象領域が大幅に拡大しています。従来のリアクティブなセキュリティでは、もはや対応が追いつきません。

キヤノンITソリューションズ株式会社も、ITインフラサービス「SOLTAGE」の新たなセキュリティラインアップとして、"セキュリティ対策診断サービス"を2025年6月5日より提供開始しました。このサービスでは、「サイバーセキュリティラボ」の専任エンジニアがヒアリングから報告までを行い、最新の世界標準「NIST Cybersecurity Framework 2.0」に基づき、セキュリティリスクを「識別/防御/検知/対応/復旧」の5つに「統治」を加えた6段階で体系的に診断/評価します。

SBテクノロジー株式会社も、BlueVoyant LLCと再販契約を締結し、AIを活用した包括的なセキュリティ運用プラットフォーム「Cyber Defense Platform」の販売を開始しました。このプラットフォームは、サプライチェーンのサイバーリスク評価、自組織のセキュリティアセスメント、脆弱性管理、ダークウェブの監視を一元的に管理できる統合セキュリティ運用ツールです。

### 多層防御の重要性

現代のサイバーセキュリティ対策では、単一の防御策に頼るのではなく、多層防御（Defense in Depth）の考え方が重要です。これは、複数の異なるセキュリティ対策を組み合わせることで、一つの対策が破られても別の対策で防御できるようにする戦略です。

具体的には、以下のような対策の組み合わせが効果的です：

1. **技術的対策**：ファイアウォール、アンチウイルスソフト、侵入検知システム、暗号化など
2. **管理的対策**：セキュリティポリシーの策定、従業員教育、インシデント対応計画など
3. **物理的対策**：入退室管理、監視カメラ、生体認証など

特に金融機関や証券会社などでは、多要素認証（MFA）の導入が急務となっています。パスワードだけでなく、ワンタイムパスワード（OTP）や生体認証などを組み合わせることで、不正アクセスのリスクを大幅に低減できます。

## 関連知識

### フィッシング攻撃とは

フィッシング攻撃とは、攻撃者が信頼できる組織や個人になりすまし、メールやSMS、偽のウェブサイトなどを通じて個人情報やログイン情報を盗み取る手法です。最近では、AIを活用した高度なフィッシング攻撃も増加しており、従来の対策では検知が困難になっています。

「CoGUI（コグイ）」のような高度なフィッシングキットは、以下のような特徴を持っています：

- 特定の地域のIPアドレスのみを標的にするジオフェンシング機能
- ブラウザや端末情報を事前に取得し、より説得力のある偽サイトを構築
- 正規サイトへのリダイレクト機能により、被害者に不審感を抱かせない
- 大量のメール送信能力により、広範囲に攻撃を仕掛ける

### 脆弱性管理の重要性

脆弱性管理とは、システムやソフトウェアの脆弱性を特定し、評価し、修正するプロセスです。効果的な脆弱性管理には以下の要素が含まれます：

1. **脆弱性の特定**：定期的なスキャンや脆弱性情報の収集
2. **リスク評価**：脆弱性の重大度や影響範囲の評価
3. **優先順位付け**：限られたリソースで最も重要な脆弱性から対処
4. **修正**：パッチ適用や設定変更などの対策実施
5. **検証**：対策の有効性の確認
6. **報告**：脆弱性管理の状況を関係者に報告

Cisco ISEの脆弱性のように、CVSSスコアが高い（9.9）脆弱性は、早急な対応が求められます。特にクラウド環境では、複数の組織が同じインフラを共有しているため、一つの脆弱性が多くの組織に影響を及ぼす可能性があります。

## 今後の展望

サイバーセキュリティの分野では、AIの活用がさらに進むと予想されます。攻撃側はAIを使ってより高度で大規模な攻撃を仕掛け、防御側もAIを活用した先制的な対策が求められるようになるでしょう。

特に中小企業においては、限られたリソースでいかに効果的なセキュリティ対策を実施するかが課題となります。クラウドストライクの報告書が示すように、多くの中小企業はサイバーセキュリティリスクを認識しているものの、実際の対策は不十分な状況です。今後は、使いやすく、手頃な価格で、かつ効果的なセキュリティソリューションの需要が高まると考えられます。

また、サプライチェーンセキュリティの重要性も増しています。大企業がセキュリティ対策を強化する中、攻撃者は比較的セキュリティが弱い取引先や関連会社を狙う傾向があります。SBテクノロジーが提供を開始した「Cyber Defense Platform」のようなサプライチェーンのサイバーリスク評価ツールの需要も高まるでしょう。

## 結論

2025年6月5日のサイバーセキュリティニュースからは、サイバー攻撃の高度化・大規模化と、それに対応するセキュリティ対策の進化が浮き彫りになりました。特に金融分野での被害の拡大は深刻で、個人投資家や一般ユーザーも含めた幅広い対策が求められています。

企業においては、AIを活用した先制的な防御策の導入や、多層防御の考え方に基づいた包括的なセキュリティ対策が重要です。また、中小企業においても、限られたリソースの中で効果的なセキュリティ対策を実施することが求められています。

サイバーセキュリティは、技術的な対策だけでなく、人的要素も含めた総合的なアプローチが必要です。今後も最新の脅威動向を把握し、適切な対策を講じることが、デジタル社会における安全・安心の確保につながるでしょう。

## 主要引用

- 「中小企業の93%がサイバーリスクの知識があり、83%が対策を立てていると報告されていますが、新しいツールに投資しているのはわずか36%で、AIを活用した防御策を採用しているのはわずか11%です。」- クラウドストライク 2025年版中小企業サイバーセキュリティ報告書
- 「AIによってサイバーセキュリティは転換点を迎え、攻撃者は大規模な攻撃を容易に実行できるようになりました。同時に、企業はクラウド、データセンター、エンドポイントに資産が分散したハイパーコネクテッドな状態にあり、攻撃対象領域が大幅に拡大しています。」- チェック・ポイント・ソフトウェア・テクノロジーズ
- 「2025年1月から5月の5ヶ月間で確認された不正アクセスは10,422件、不正取引は5,958件に上り、売却・買付金額は合計で5,200億円を超えました。」- 金融庁

