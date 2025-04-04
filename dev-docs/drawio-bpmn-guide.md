# draw.ioのBPMNをXML形式で直接記述するためのLLM向けガイド

このガイドは、LLMが人間の指示に基づいてdraw.ioで使用可能なBPMN図をXML形式で直接生成するための参照資料です。

## 1. 基本構造

draw.ioのXMLファイルは以下の基本構造を持ちます：

```xml
<mxfile host="app.diagrams.net" modified="TIMESTAMP" agent="Mozilla/5.0" version="VERSIONNUMBER">
  <diagram id="DIAGRAM_ID" name="DIAGRAM_NAME">
    <mxGraphModel dx="DELTA_X" dy="DELTA_Y" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- ここにBPMN要素を記述 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 2. BPMN基本要素のXML表現

### 2.1 セル要素の共通属性

各要素（mxCell）の共通属性：

- `id`: 要素の一意の識別子 - 数字または文字列（例: "2", "task1"）
- `value`: 要素に表示されるテキスト
- `style`: 要素のスタイル設定（色、線の太さなど）
- `vertex`: "1"の場合、この要素はノード（頂点）
- `edge`: "1"の場合、この要素はエッジ（接続線）
- `parent`: 親要素のID（通常は"1"）
- `source`: 接続線の始点となる要素のID
- `target`: 接続線の終点となる要素のID
- `geometry`: 位置とサイズの情報

### 2.2 イベント（Events）

#### 開始イベント（Start Event）
```xml
<mxCell id="start1" value="開始" style="shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=standard;symbol=general;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="50" height="50" as="geometry"/>
</mxCell>
```

#### 終了イベント（End Event）
```xml
<mxCell id="end1" value="終了" style="shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=end;symbol=general;" vertex="1" parent="1">
  <mxGeometry x="500" y="100" width="50" height="50" as="geometry"/>
</mxCell>
```

#### 中間イベント（Intermediate Event）
```xml
<mxCell id="intermediate1" value="中間イベント" style="shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=throwing;symbol=general;" vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="50" height="50" as="geometry"/>
</mxCell>
```

### 2.3 アクティビティ（Activities）

#### タスク（Task）
```xml
<mxCell id="task1" value="タスク" style="shape=ext;rounded=1;html=1;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="200" y="95" width="120" height="60" as="geometry"/>
</mxCell>
```

#### ユーザータスク（User Task）
```xml
<mxCell id="usertask1" value="ユーザータスク" style="shape=ext;rounded=1;html=1;whiteSpace=wrap;shape=mxgraph.bpmn.task;taskMarker=user;" vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="120" height="60" as="geometry"/>
</mxCell>
```

#### サービスタスク（Service Task）
```xml
<mxCell id="servicetask1" value="サービスタスク" style="shape=ext;rounded=1;html=1;whiteSpace=wrap;shape=mxgraph.bpmn.task;taskMarker=service;" vertex="1" parent="1">
  <mxGeometry x="200" y="300" width="120" height="60" as="geometry"/>
</mxCell>
```

#### サブプロセス（Subprocess）
```xml
<mxCell id="subprocess1" value="サブプロセス" style="shape=ext;rounded=1;html=1;whiteSpace=wrap;shape=mxgraph.bpmn.task;taskMarker=abstract;isLoopStandard=0;isLoopSub=0;isLoopStandard=0;" vertex="1" parent="1">
  <mxGeometry x="200" y="400" width="120" height="60" as="geometry"/>
</mxCell>
```

### 2.4 ゲートウェイ（Gateways）

#### 排他的ゲートウェイ（Exclusive Gateway）
```xml
<mxCell id="xgate1" value="排他的ゲートウェイ" style="shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=none;symbol=exclusiveGw;" vertex="1" parent="1">
  <mxGeometry x="400" y="95" width="50" height="50" as="geometry"/>
</mxCell>
```

#### 並列ゲートウェイ（Parallel Gateway）
```xml
<mxCell id="pargate1" value="並列ゲートウェイ" style="shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=none;symbol=parallelGw;" vertex="1" parent="1">
  <mxGeometry x="400" y="200" width="50" height="50" as="geometry"/>
</mxCell>
```

#### 包括的ゲートウェイ（Inclusive Gateway）
```xml
<mxCell id="incgate1" value="包括的ゲートウェイ" style="shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=none;symbol=inclusiveGw;" vertex="1" parent="1">
  <mxGeometry x="400" y="300" width="50" height="50" as="geometry"/>
</mxCell>
```

### 2.5 接続（Connections）

#### シーケンスフロー（Sequence Flow）
```xml
<mxCell id="flow1" value="" style="endArrow=block;endFill=1;endSize=6;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="start1" target="task1">
  <mxGeometry width="100" height="100" relative="1" as="geometry">
    <mxPoint x="100" y="200" as="sourcePoint"/>
    <mxPoint x="200" y="100" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

#### 条件付きシーケンスフロー（Conditional Sequence Flow）
```xml
<mxCell id="flow2" value="条件" style="endArrow=block;endFill=1;endSize=6;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="task1" target="xgate1">
  <mxGeometry width="100" height="100" relative="1" as="geometry">
    <mxPoint x="150" y="125" as="sourcePoint"/>
    <mxPoint x="200" y="125" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

#### メッセージフロー（Message Flow）
```xml
<mxCell id="msgflow1" value="" style="endArrow=block;endFill=1;endSize=6;html=1;dashed=1;dashPattern=1 4;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="task1" target="usertask1">
  <mxGeometry width="100" height="100" relative="1" as="geometry">
    <mxPoint x="340" y="125" as="sourcePoint"/>
    <mxPoint x="410" y="125" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

### 2.6 プールとレーン（Pools and Lanes）

#### プール（Pool）
```xml
<mxCell id="pool1" value="プール名" style="swimlane;html=1;horizontal=0;startSize=20;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="700" height="200" as="geometry"/>
</mxCell>
```

#### レーン（Lane）
```xml
<mxCell id="lane1" value="レーン1" style="swimlane;html=1;horizontal=0;startSize=20;" vertex="1" parent="pool1">
  <mxGeometry x="20" y="0" width="680" height="100" as="geometry"/>
</mxCell>

<mxCell id="lane2" value="レーン2" style="swimlane;html=1;horizontal=0;startSize=20;" vertex="1" parent="pool1">
  <mxGeometry x="20" y="100" width="680" height="100" as="geometry"/>
</mxCell>
```

## 3. 高度な要素とスタイリング

### 3.1 イベントの追加シンボル

イベントの `symbol` 属性を変更することで、異なるタイプのイベントを表現できます：

- メッセージイベント: `symbol=message`
- タイマーイベント: `symbol=timer`
- エラーイベント: `symbol=error`
- エスカレーションイベント: `symbol=escalation`
- 補償イベント: `symbol=compensation`
- 条件イベント: `symbol=conditional`
- リンクイベント: `symbol=link`
- シグナルイベント: `symbol=signal`
- 複数イベント: `symbol=multiple`
- 並列複数イベント: `symbol=parallelMultiple`
- 終了イベント: `symbol=terminate`

### 3.2 アクティビティのマーカー

アクティビティの `taskMarker` 属性を変更することで、異なるタイプのタスクを表現できます：

- ユーザータスク: `taskMarker=user`
- サービスタスク: `taskMarker=service`
- スクリプトタスク: `taskMarker=script`
- ビジネスルールタスク: `taskMarker=businessRule`
- 手動タスク: `taskMarker=manual`
- メッセージ送信タスク: `taskMarker=send`
- メッセージ受信タスク: `taskMarker=receive`

### 3.3 ループとマルチインスタンス

ループやマルチインスタンスを表現するには以下の属性を追加します：

- 標準ループ: `isLoopStandard=1`
- 並列マルチインスタンス: `isLoopMultiParallel=1`
- 順次マルチインスタンス: `isLoopMultiSequential=1`
- 補償: `isLoopCompensation=1`

### 3.4 色とスタイルのカスタマイズ

要素の `style` 属性に以下のプロパティを追加することで、色や線などをカスタマイズできます：

- 塗りつぶし色: `fillColor=#RRGGBB`
- 線の色: `strokeColor=#RRGGBB`
- 線の太さ: `strokeWidth=2`
- 点線: `dashed=1`
- 透明度: `opacity=50`
- フォントサイズ: `fontSize=12`
- フォントの色: `fontColor=#RRGGBB`
- 太字: `fontStyle=1`
- イタリック: `fontStyle=2`
- 下線: `fontStyle=4`

## 4. 実用的なヒント

### 4.1 ID命名規則

要素のIDは一意である必要があります。以下の命名規則を推奨します：

- 開始イベント: `start1`, `start2`, ...
- 終了イベント: `end1`, `end2`, ...
- タスク: `task1`, `task2`, ... または `task_登録`, `task_確認`, ...
- ゲートウェイ: `gw1`, `gw2`, ... または `gw_判断1`, `gw_並列1`, ...
- フロー: `flow1`, `flow2`, ... または `flow_開始_タスク1`, ...
- プール: `pool_顧客`, `pool_システム`, ...
- レーン: `lane_フロント`, `lane_バック`, ...

### 4.2 要素の配置

要素の位置は `mxGeometry` タグで指定します。座標系は左上が原点で、右に向かってx座標が増加し、下に向かってy座標が増加します。

```xml
<mxGeometry x="100" y="200" width="120" height="60" as="geometry"/>
```

要素を綺麗に配置するためには、以下のようなグリッドを意識するとよいでしょう：

- 水平方向: 100px間隔（x座標: 100, 220, 340, 460, ...）
- 垂直方向: 100px間隔（y座標: 100, 200, 300, 400, ...）
- タスクのサイズ: 120x60
- イベント/ゲートウェイのサイズ: 50x50

### 4.3 接続線の折れ曲がり

接続線に折れ曲がりを追加するには、`mxPoint` タグを使用します：

```xml
<mxCell id="flow3" value="" style="endArrow=block;endFill=1;endSize=6;html=1;" edge="1" parent="1" source="task2" target="end1">
  <mxGeometry width="100" height="100" relative="1" as="geometry">
    <mxPoint x="100" y="200" as="sourcePoint"/>
    <mxPoint x="200" y="100" as="targetPoint"/>
    <Array as="points">
      <mxPoint x="260" y="350"/>
      <mxPoint x="525" y="350"/>
    </Array>
  </mxGeometry>
</mxCell>
```

## 5. 完全なBPMN例

以下は、シンプルな注文処理プロセスのXML例です：

```xml
<mxfile host="app.diagrams.net" modified="2023-05-15T12:00:00.000Z" agent="Mozilla/5.0" version="21.0.0">
  <diagram id="order_process" name="注文処理プロセス">
    <mxGraphModel dx="1422" dy="798" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- プール -->
        <mxCell id="pool_customer" value="顧客" style="swimlane;html=1;horizontal=0;startSize=20;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="50" y="50" width="700" height="100" as="geometry"/>
        </mxCell>
        
        <mxCell id="pool_company" value="企業" style="swimlane;html=1;horizontal=0;startSize=20;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="50" y="150" width="700" height="200" as="geometry"/>
        </mxCell>
        
        <!-- レーン -->
        <mxCell id="lane_sales" value="営業部" style="swimlane;html=1;horizontal=0;startSize=20;" vertex="1" parent="pool_company">
          <mxGeometry x="20" y="0" width="680" height="100" as="geometry"/>
        </mxCell>
        
        <mxCell id="lane_warehouse" value="倉庫" style="swimlane;html=1;horizontal=0;startSize=20;" vertex="1" parent="pool_company">
          <mxGeometry x="20" y="100" width="680" height="100" as="geometry"/>
        </mxCell>
        
        <!-- 顧客プロセス -->
        <mxCell id="start_customer" value="開始" style="shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=standard;symbol=general;" vertex="1" parent="1">
          <mxGeometry x="100" y="75" width="50" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="task_order" value="注文送信" style="shape=ext;rounded=1;html=1;whiteSpace=wrap;" vertex="1" parent="1">
          <mxGeometry x="200" y="70" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="task_receive_confirm" value="注文確認受取" style="shape=ext;rounded=1;html=1;whiteSpace=wrap;" vertex="1" parent="1">
          <mxGeometry x="400" y="70" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="end_customer" value="終了" style="shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=end;symbol=general;" vertex="1" parent="1">
          <mxGeometry x="600" y="75" width="50" height="50" as="geometry"/>
        </mxCell>
        
        <!-- 営業部プロセス -->
        <mxCell id="start_sales" value="開始" style="shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=standard;symbol=message;" vertex="1" parent="1">
          <mxGeometry x="100" y="175" width="50" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="task_check_order" value="注文確認" style="shape=ext;rounded=1;html=1;whiteSpace=wrap;" vertex="1" parent="1">
          <mxGeometry x="200" y="170" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="gateway_stock" value="" style="shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=none;symbol=exclusiveGw;" vertex="1" parent="1">
          <mxGeometry x="370" y="175" width="50" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="task_send_confirm" value="確認送信" style="shape=ext;rounded=1;html=1;whiteSpace=wrap;" vertex="1" parent="1">
          <mxGeometry x="470" y="170" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="end_sales" value="終了" style="shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=end;symbol=general;" vertex="1" parent="1">
          <mxGeometry x="650" y="175" width="50" height="50" as="geometry"/>
        </mxCell>
        
        <!-- 倉庫プロセス -->
        <mxCell id="task_prepare" value="商品準備" style="shape=ext;rounded=1;html=1;whiteSpace=wrap;" vertex="1" parent="1">
          <mxGeometry x="335" y="270" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <!-- 接続 -->
        <!-- 顧客プロセスの接続 -->
        <mxCell id="flow_1" value="" style="endArrow=block;endFill=1;endSize=6;html=1;" edge="1" parent="1" source="start_customer" target="task_order">
          <mxGeometry width="100" height="100" relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow_2" value="" style="endArrow=block;endFill=1;endSize=6;html=1;" edge="1" parent="1" source="task_order" target="task_receive_confirm">
          <mxGeometry width="100" height="100" relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow_3" value="" style="endArrow=block;endFill=1;endSize=6;html=1;" edge="1" parent="1" source="task_receive_confirm" target="end_customer">
          <mxGeometry width="100" height="100" relative="1" as="geometry"/>
        </mxCell>
        
        <!-- 営業部プロセスの接続 -->
        <mxCell id="flow_4" value="" style="endArrow=block;endFill=1;endSize=6;html=1;" edge="1" parent="1" source="start_sales" target="task_check_order">
          <mxGeometry width="100" height="100" relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow_5" value="" style="endArrow=block;endFill=1;endSize=6;html=1;" edge="1" parent="1" source="task_check_order" target="gateway_stock">
          <mxGeometry width="100" height="100" relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow_6" value="在庫あり" style="endArrow=block;endFill=1;endSize=6;html=1;" edge="1" parent="1" source="gateway_stock" target="task_send_confirm">
          <mxGeometry width="100" height="100" relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow_7" value="" style="endArrow=block;endFill=1;endSize=6;html=1;" edge="1" parent="1" source="task_send_confirm" target="end_sales">
          <mxGeometry width="100" height="100" relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow_8" value="在庫確認" style="endArrow=block;endFill=1;endSize=6;html=1;" edge="1" parent="1" source="gateway_stock" target="task_prepare">
          <mxGeometry width="100" height="100" relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow_9" value="" style="endArrow=block;endFill=1;endSize=6;html=1;" edge="1" parent="1" source="task_prepare" target="task_send_confirm">
          <mxGeometry width="100" height="100" relative="1" as="geometry">
            <mxPoint x="350" y="300" as="sourcePoint"/>
            <mxPoint x="450" y="200" as="targetPoint"/>
            <Array as="points">
              <mxPoint x="530" y="300"/>
            </Array>
          </mxGeometry>
        </mxCell>
        
        <!-- メッセージフロー -->
        <mxCell id="msg_1" value="" style="endArrow=block;endFill=1;endSize=6;html=1;dashed=1;dashPattern=1 4;" edge="1" parent="1" source="task_order" target="start_sales">
          <mxGeometry width="100" height="100" relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="msg_2" value="" style="endArrow=block;endFill=1;endSize=6;html=1;dashed=1;dashPattern=1 4;" edge="1" parent="1" source="task_send_confirm" target="task_receive_confirm">
          <mxGeometry width="100" height="100" relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 6. LLMへの指示例

LLMにBPMN図のXMLを生成してもらう際の指示例：

```
以下の業務プロセスをdraw.ioで表示可能なBPMN図のXML形式で記述してください：

プロセス名: 与信申請処理

参加者:
- 営業担当者
- 与信管理部
- 財務部

プロセスフロー:
1. 営業担当者が顧客情報を入力して与信申請を開始する
2. 与信管理部が申請内容を確認する
3. 申請金額が100万円未満の場合、与信管理部で審査・承認を行う
4. 申請金額が100万円以上の場合、財務部へエスカレーションする
5. 財務部は詳細な信用調査を行い、結果を返す
6. 与信管理部は結果をもとに最終判断を行う
7. 承認された場合、営業担当者に通知され、取引が可能になる
8. 否認された場合、営業担当者に通知され、プロセスが終了する

XMLは以下の制約に従ってください：
- プールとレーンを適切に使用する
- ゲートウェイで分岐条件を表現する
- メッセージフローで部門間のコミュニケーションを表現する
- 各タスクには適切なタスクタイプを設定する
```

## 7. XMLの検証と修正のヒント

LLMが生成したXMLを検証する際のヒント：

1. ID値の一意性を確認する（重複がないこと）
2. 接続線の source と target が実在する要素のIDを参照していることを確認する
3. プールとレーンの親子関係が正しく設定されていることを確認する
4. 座標値が適切で、要素同士が重ならないように配置されていることを確認する
5. スタイル属性の構文が正しいことを確認する

共通のエラーと修正方法：
- `parent` 属性の参照先が存在しない → 正しいIDに修正
- `source` または `target` 属性の参照先が存在しない → 正しいIDに修正
- 要素のサイズや位置が不適切 → `mxGeometry` の値を調整
- スタイル属性の値が無効 → 正しい構文に修正（例：`fillColor=red` → `fillColor=#FF0000`）