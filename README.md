# Langgraph Deep Search MCP Server
Google Gemini公式実装をベースにしたLangGraphのAIエージェントを使用して包括的な調査を実行します。

## 🎯 実装について

**Langgraph Implementation**
- 完全にGoogleの[公式実装](https://github.com/google-gemini/gemini-fullstack-langgraph-quickstart/tree/main/backend)をベース
- Gemini 2.5 Flashのネイティブ検索機能使用
- LangGraphによる状態管理とワークフロー
- grounding metadataによる自動引用

## 🌟 機能

- **Deep Search**: 複数回の検索イテレーションによる包括的な調査
- **Quick Search**: 単発検索による迅速な結果取得
- **Gemini Native Search**: Gemini 2.5 Flashのネイティブ検索機能を使用した高品質な検索
- **AI Analysis**: Gemini 2.5 Proを使用した結果の分析と統合
- **MCP Integration**: Model Context Protocolによる外部アプリケーションとの統合
- **自動引用**: grounding metadataによる自動的なソース情報取得

## 🚀 クイックスタート

### 方法1: uvx使用 (推奨)

```bash
# 1. プロジェクトのクローン
git clone https://github.com/RyotaOzawa0/langgraph-deepsearch-mcp.git
cd deep-search-mcp-server

# 2. 環境変数設定
export GEMINI_API_KEY=your_gemini_api_key_here

# 3. MCPサーバー起動
uvx --from . langgraph-deep-search
```

### 方法2: 手動セットアップ

```bash
# 1. プロジェクトのクローン
git clone <repository-url>
cd deep-search-mcp-server

# 2. 依存関係インストール
uv sync

# 3. 環境変数設定
export GEMINI_API_KEY=your_gemini_api_key_here

# 4. MCPサーバー起動
python gemini_server.py
```

## 📋 詳細インストール手順

### 前提条件

- Python 3.10以上
- uv (推奨) または pip

### 手動インストール

```bash
# 1. リポジトリをクローン
git clone <repository-url>
cd deep-search-mcp-server

# 2. uvでプロジェクトセットアップ
uv sync
uv pip install -e .

# 3. 環境変数設定
cp .env.example .env
# .envファイルを編集してAPIキーを設定

# 4. テスト実行
uv run python gemini_server.py
```

### API キー

- **GEMINI_API_KEY**: Gemini API (必須) - [Google AI Studio](https://aistudio.google.com/app/apikey)から取得

## 🛠 使用方法

### 自然言語入力例

MCPサーバーがClaude DesktopなどのMCPホストに接続されると、以下のような自然言語でリサーチを依頼できます：

#### 包括的な調査 (deep_search)

```
「React状態管理ライブラリを包括的に比較調査して」

「Terraformベストプラクティスを深く調べて」
```

#### 迅速な検索 (quick_search)

```
「Claude Codeの使用感・評判を速攻で調査して」

「Devinの最新アプデをサクッと検索して」
```

#### サーバー状態確認

```
「検索ツールの状態を確認してください」

「MCPサーバーの設定情報を教えてください」
```

### MCP Tools (開発者向け)

#### `deep_search`

包括的な調査を実行します。

**パラメータ:**
- `query` (str): 調査したいトピック
- `max_iterations` (int, default=3): 最大イテレーション回数
- `max_results_per_query` (int, default=5): クエリごとの最大結果数
- `language` (str, default="en"): 検索言語

#### `quick_search`

単発検索による迅速な結果取得。

#### `get_search_tools`

利用可能な検索ツールの状態を確認。

### MCP Resources

#### `search-config`

サーバーの設定情報と利用可能なツールの状態を取得。


### 主要コンポーネント

1. **GoogleSearchManager**: Google検索の統合管理
2. **DeepResearchGraph**: LangGraphによる調査ワークフロー
3. **FastMCP Server**: MCPプロトコルでのツール公開

## 🔧 Claude Desktop連携

### uvxを使用した設定 

`claude_desktop_config.json`に以下を追加：

```json
{
  "mcpServers": {
    "langgraph-deep-search": {
      "command": "uvx",
      "args": ["--from", "/path/to/deep-search-mcp-server", "langgraph-deep-search"],
      "env": {
        "GEMINI_API_KEY": "your_gemini_api_key"
      }
    }
  }
}
```

### uv run使用での設定

```json
{
  "mcpServers": {
    "langgraph-deep-search": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/deep-search-mcp-server", "python", "gemini_server.py"],
      "env": {
        "GEMINI_API_KEY": "your_gemini_api_key"
      }
    }
  }
}
```

### 直接実行での設定

```json
{
  "mcpServers": {
    "langgraph-deep-search": {
      "command": "python",
      "args": ["/path/to/deep-search-mcp-server/gemini_server.py"],
      "env": {
        "GEMINI_API_KEY": "your_gemini_api_key"
      }
    }
  }
}
```

### 開発モード

```bash
# MCP Inspector付きで開発
mcp dev gemini_server.py
```


## 🔍 トラブルシューティング

### よくあるエラー

1. **ModuleNotFoundError: No module named 'mcp'**:
   - 解決策: `uv sync`で依存関係をインストール
   - または: `uv run python gemini_server.py`を使用

2. **Agent not initialized**:
   - 解決策: `GEMINI_API_KEY`環境変数を設定

3. **Process exited with code 1**:
   - 解決策: 絶対パスと`uv run`を使用
   - WSLの場合: `uv run python gemini_server.py`を含むコマンドを使用

4. **Import errors**:
   - 解決策: `uv sync`で依存関係をインストール

### ログ確認

サーバー実行時にコンソールに出力されるログで状態を確認できます。

### デバッグモード

```bash
# 詳細ログ付きで実行
mcp dev gemini_server.py
```

## 📄 ライセンス

MIT License

## 🤝 貢献

1. Forkしてfeatureブランチを作成
2. 変更をcommit
3. Pull Requestを作成

## 📚 参考

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - 公式Python SDK
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Gemini Fullstack LangGraph Quickstart](https://github.com/google-gemini/gemini-fullstack-langgraph-quickstart)
- [MCP Server Development Guide](https://modelcontextprotocol.io/quickstart/server)

---