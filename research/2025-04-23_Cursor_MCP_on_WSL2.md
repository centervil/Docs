## CursorのMCP機能がWSL2接続でうまく使えない事例と解決策

Windows版CursorでWSL2上のUbuntu環境にRemote接続し、MCP（Model Context Protocol）機能が正常に動作しない、特に「Client closed」エラーなどでMCPサーバーが起動しない事例は多数報告されています[^1_1][^1_2][^1_4][^1_5][^1_6][^1_7]。

---

**よくある原因**

- MCPサーバー起動コマンドがWindows側で実行されてしまう
- Node.jsやnpxがWSL内にしかインストールされていない
- コマンドパスや環境変数の設定不備
- WSL拡張機能やCursor本体のバージョン不整合
- PowerShellのスクリプト実行ポリシー制限[^1_4]
- MCPサーバーの複数ファイル構成やTypeScript/ESM対応の問題[^1_2]

---

## 事例

- **Windowsのnpx/Node.jsが見つからず失敗**
CursorはWindowsアプリとして動作しているため、コマンドがWindows側で実行され、WSL内のNode.jsやnpxが使われない[^1_2][^1_7]。
- **wsl.exe経由でコマンドを実行していない**
MCPのコマンド設定で直接npxやnodeを指定すると、Windows側で実行されてしまう[^1_3][^1_7]。
- **拡張機能の不整合やアップデート後の接続不良**
WSL拡張機能の再インストールやCursor自体の再起動で解決する場合もある[^1_5][^1_6]。

---

## 解決方法

### 1. WSL経由でMCPサーバーを起動する

MCPサーバーの設定で、`wsl.exe`を明示的に利用し、WSL内のコマンドを実行させることで解決する事例が多いです。

**例：uvxコマンドをWSLで実行する場合**[^1_3]

```json
"mcpServers": {
  "awslabs.aws-documentation-mcp-server": {
    "command": "wsl.exe",
    "args": [
      "--",
      "/home/user/.local/bin/uvx",
      "awslabs.aws-documentation-mcp-server@latest"
    ],
    "env": {
      "FASTMCP_LOG_LEVEL": "ERROR"
    }
  }
}
```

**例：npxコマンドをWSLで実行する場合**[^1_7]

```json
"command": "wsl",
"args": [
  "bash",
  "-c",
  "/usr/bin/npx -y @modelcontextprotocol/server-filesystem /src/projects/test"
]
```

- `command`に`wsl.exe`または`wsl`を指定
- `args`でWSL内の絶対パスやbash -cでコマンドをラップ

---

### 2. Node.js・npxのインストール場所を確認

- WSL内だけでなく、Windows側にもNode.js/npxが必要な場合があるため、両方にインストールしてPATHが通っているか確認[^1_2][^1_4]。
- MCPサーバーの実行に失敗する場合、`node --version`や`npm --version`で確認。

---

### 3. PowerShellの実行ポリシーを確認

- PowerShellのスクリプト実行が`Restricted`だとコマンドが失敗することがあるため、`Set-ExecutionPolicy RemoteSigned`で許可[^1_4]。

---

### 4. WSL拡張機能のリセット

- CursorやWSL拡張機能の不整合が疑われる場合、拡張機能をアンインストール→再インストール[^1_5][^1_6]。

1. Windowsプロジェクトを開く
2. WSL拡張機能をアンインストール
3. Cursorを再起動
4. WSLプロジェクトを開き、拡張機能を再インストール

---

### 5. コマンド実行方式の工夫

- `cmd /c`や`cmd /k`を使ってバッチファイルとしてコマンドを実行することで解決する場合もある[^1_1][^1_2]。
- 例：`cmd /c npx @agentdeskai/browser-tools-mcp`

---

### 6. MCPサーバーを1ファイルにバンドル

- TypeScriptや複数ファイル構成の場合はesbuildなどで1ファイルにバンドルし、直接nodeで実行[^1_2]。

---

## まとめ

- **MCPサーバーのコマンドはWSL経由で実行する設定にする**
- **Node.js/npxはWindowsとWSLの両方にインストールしておく**
- **PowerShellの実行ポリシーやPATH設定も確認**
- **WSL拡張機能の再インストールやCursorの再起動も有効**
- **複雑なMCPサーバーは1ファイルにバンドルして実行**

これらを試しても解決しない場合は、CursorのバージョンやWSLの状態、MCPサーバーのログ出力内容を確認し、さらに詳細なトラブルシューティングを行うことが推奨されます[^1_1][^1_2][^1_5][^1_6][^1_7]。

<div style="text-align: center">⁂</div>

[^1_1]: https://forum.cursor.com/t/mcp-feature-client-closed-fix/54651?page=2

[^1_2]: https://apidog.com/blog/how-to-fix-cursor-ai-mcp-feature-client-closed-error/

[^1_3]: https://blog.spacecat.jp/archives/697

[^1_4]: https://qiita.com/yuki_s_14/items/18d7e3a7ed1b203e04e7

[^1_5]: https://github.com/getcursor/cursor/issues/1508

[^1_6]: https://www.reddit.com/r/cursor/comments/1izebnv/cursor_cant_connect_to_wsl_guide/

[^1_7]: https://qiita.com/takahashi-ry/items/ba8e9f329dad92a3ddd7

[^1_8]: https://github.com/microsoft/vscode-remote-release/issues/10826

[^1_9]: https://zenn.dev/torohash/scraps/42b16540421bee

[^1_10]: https://stackoverflow.com/questions/64125085/vs-code-connect-to-wsl-ubuntu-20-04-lts-fail-with-error-could-not-fetch-remote

[^1_11]: https://zenn.dev/sesere/articles/2faf1e24f65746

[^1_12]: https://github.com/mendableai/firecrawl-mcp-server/issues/18

[^1_13]: https://stackoverflow.com/questions/67017493/remote-desktop-connection-crashing-when-connecting-to-wsl-ubuntu-20-04-lts

[^1_14]: https://note.com/sojin25/n/nd50cb457d882

[^1_15]: https://forum.cursor.com/t/how-to-use-any-mcp-servers-in-wsl-with-nvm/50473

[^1_16]: https://code.visualstudio.com/docs/remote/wsl-tutorial

[^1_17]: https://note.com/norito_hiraoka/n/n0c782af7797f

[^1_18]: https://scottspence.com/posts/cursor-setup-for-wsl

[^1_19]: https://scottspence.com/posts/getting-mcp-server-working-with-claude-desktop-in-wsl

[^1_20]: https://zenn.dev/kudosho/articles/wsl2_cursor_performance

[^1_21]: https://forum.cursor.com/t/run-mcp-servers-in-wsl/55537

[^1_22]: https://qiita.com/takahashi-ry/items/ba8e9f329dad92a3ddd7

[^1_23]: https://forum.cursor.com/t/mcp-feature-client-closed-fix/54651

[^1_24]: https://github.com/getcursor/cursor/issues/870

[^1_25]: https://www.aise.ics.saitama-u.ac.jp/~gotoh/TroubleShootingAboutUbuntu2204OnWSL2.html

[^1_26]: https://github.com/getcursor/cursor/issues/1508

[^1_27]: https://github.com/modelcontextprotocol/servers/issues/891

[^1_28]: https://github.com/getcursor/cursor/issues/1457

[^1_29]: https://www.aise.ics.saitama-u.ac.jp/~gotoh/TroubleShootingAboutUbuntu2404OnWSL2.html

[^1_30]: https://forum.cursor.com/t/is-there-wsl2-support/97?page=2

[^1_31]: https://blog.spacecat.jp

[^1_32]: https://github.com/getcursor/cursor/issues/2833

[^1_33]: https://www.reddit.com/r/cursor/comments/1g2kp0l/cursor_setup_for_wsl_windows_subsystem_for_linux/

