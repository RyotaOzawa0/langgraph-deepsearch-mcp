# Langgraph Deep Search MCP Server

Langgraph Deep Search MCP Server。Google Gemini公式実装をベースにしたLangGraphのAIエージェントを使用して包括的な調査を実行します。

## 🎯 実装について

**Langgraph Implementation**
- 完全にGoogleの公式実装をベース
- Gemini 2.0 Flashのネイティブ検索機能使用
- LangGraphによる状態管理とワークフロー
- grounding metadataによる自動引用

## 🌟 機能

- **Deep Search**: 複数回の検索イテレーションによる包括的な調査
- **Quick Search**: 単発検索による迅速な結果取得
- **Gemini Native Search**: Gemini 2.0 Flashのネイティブ検索機能を使用した高品質な検索
- **AI Analysis**: Gemini 2.0を使用した結果の分析と統合
- **MCP Integration**: Model Context Protocolによる外部アプリケーションとの統合
- **自動引用**: grounding metadataによる自動的なソース情報取得

## 🚀 クイックスタート

### 方法1: uvx使用 (推奨)

```bash
# 1. プロジェクトのクローン
git clone <repository-url>
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

- **GEMINI_API_KEY**: Gemini API (必須) - [Google AI Studio](https://makersuite.google.com/app/apikey)から取得

## 🛠 使用方法

### Claude Desktopでの自然言語入力例

MCPサーバーがClaude Desktopに接続されると、以下のような自然言語でリサーチを依頼できます：

#### 包括的な調査 (deep_search)

```
「最新のAI技術の動向について詳しく調査してください。特に2024年の重要な進展に焦点を当ててください。」

「気候変動が日本の農業に与える影響について、最新の研究結果を含めて包括的に調べてください。」

「量子コンピューティングの商用化の現状と今後5年間の見通しについて研究してください。」
```

#### 迅速な検索 (quick_search)

```
「Gemini 2.0の新機能を簡単に教えてください」

「現在の日本の人口は何人ですか？」

「OpenAIの最新モデルの名前は何ですか？」
```

#### サーバー状態確認

```
「検索ツールの状態を確認してください」

「MCPサーバーの設定情報を教えてください」
```

### 実際の応答例

**入力**: 「2024年のAI業界の主要な動向について調査してください」

**応答**: 
```
## 2024年のAI業界主要動向

### 1. 大規模言語モデルの進化
- OpenAI GPT-4o、Anthropic Claude 3.5 Sonnetなどの新モデルがリリース
- マルチモーダル機能の大幅な向上...

### 2. AI エージェントの実用化
- 複数のタスクを自律的に実行するAIエージェントが注目
- ビジネス分野での実装例が増加...

[引用とソース情報を含む詳細な調査結果]
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

## 🏗 アーキテクチャ

```
src/deep_search_mcp/
├── __init__.py          # パッケージ初期化
├── models.py           # データモデル (Pydantic)
├── prompts.py          # プロンプトテンプレート (Gemini準拠)
├── state.py            # 状態管理クラス
├── graph.py            # LangGraphワークフロー
├── agent.py            # エージェントファサード
├── tools.py            # 検索ツール管理
└── server.py           # MCPサーバー (FastMCP)
```

### 主要コンポーネント

1. **GoogleSearchManager**: Google検索の統合管理
2. **DeepResearchGraph**: LangGraphによる調査ワークフロー
3. **FastMCP Server**: MCPプロトコルでのツール公開

### Gemini実装準拠構造

元のGemini DeepResearch実装に準拠：

- **専門化された状態クラス**: `OverallState`, `QueryGenerationState`, `WebSearchState`, `ReflectionState`
- **JSON構造化出力**: LLMからの応答をJSONでパース
- **並列検索処理**: `asyncio.gather`による複数検索の同時実行
- **分離されたプロンプト**: `prompts.py`でテンプレート管理

## 🔧 Claude Desktop連携

### Windows/Mac環境

#### uvxを使用した設定 (推奨)

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

#### uv run使用での設定 (推奨)

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

#### 直接実行での設定

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

### WSL環境

#### uvxを使用した設定 (推奨)

`claude_desktop_config.json`に以下を追加：

```json
{
  "mcpServers": {
    "langgraph-deep-search": {
      "command": "wsl",
      "args": ["-e", "bash", "-c", "cd /home/username/deep-search-mcp-server && uv run uvx --from . langgraph-deep-search"],
      "env": {
        "GEMINI_API_KEY": "your_gemini_api_key"
      }
    }
  }
}
```

#### uv run使用での設定 (推奨)

```json
{
  "mcpServers": {
    "langgraph-deep-search": {
      "command": "wsl",
      "args": ["-e", "bash", "-c", "cd /home/username/deep-search-mcp-server && uv run python gemini_server.py"],
      "env": {
        "GEMINI_API_KEY": "your_gemini_api_key"
      }
    }
  }
}
```

#### 直接実行での設定

```json
{
  "mcpServers": {
    "langgraph-deep-search": {
      "command": "wsl",
      "args": ["-e", "python", "/home/username/deep-search-mcp-server/gemini_server.py"],
      "env": {
        "GEMINI_API_KEY": "your_gemini_api_key"
      }
    }
  }
}
```

#### WSL環境でのパス例

- WSLパス: `/home/username/deep-search-mcp-server`
- Windowsパス: `\\wsl$\Ubuntu\home\username\deep-search-mcp-server`

## 🧪 開発

### テスト実行

```bash
# uvを使用
uv run pytest

# または直接
python -m pytest
```

### Linting

```bash
uv run black src/
uv run isort src/
uv run mypy src/
```

### 開発モード

```bash
# MCP Inspector付きで開発
mcp dev gemini_server.py
```

## 📦 デプロイメント

### ローカル配布

```bash
# パッケージビルド
uv build

# インストール
uv pip install dist/langgraph-deep-search-mcp-server-0.1.0.tar.gz
```

## 🔍 トラブルシューティング

### よくあるエラー

1. **ModuleNotFoundError: No module named 'mcp'**:
   - 解決策: `uv sync`で依存関係をインストール
   - または: `uv run python gemini_server.py`を使用

2. **Agent not initialized**:
   - 解決策: `GEMINI_API_KEY`環境変数を設定

3. **Gemini native search not available**:
   - 解決策: Gemini 2.0 Flash APIキーが正しく設定されているか確認

4. **Process exited with code 1**:
   - 解決策: 絶対パスと`uv run`を使用
   - WSLの場合: `uv run python gemini_server.py`を含むコマンドを使用

5. **Import errors**:
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