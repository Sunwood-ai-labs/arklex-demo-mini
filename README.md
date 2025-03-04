# 🤖 Arklex デモ: カスタマーサービスエージェント

## 📋 プロジェクト概要
このプロジェクトは、Arklex フレームワークを使用した最小構成のカスタマーサービスエージェントデモです。

## 🚀 セットアップ

### 1. 依存関係のインストール
```bash
# 仮想環境の作成（推奨）
python3 -m venv venv
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 2. 環境変数の設定
1. `.env.example` ファイルを `.env` にコピーします：
```bash
cp .env.example .env
```

2. `.env` ファイルを編集し、必要なAPIキーを追加してください：
- `OPENAI_API_KEY`: OpenAI APIキー
- `GEMINI_API_KEY`: Gemini APIキー
- `ANTHROPIC_API_KEY`: Anthropic APIキー

### 3. APIキーの取得
- OpenAI: [OpenAI API](https://platform.openai.com/account/api-keys)
- Gemini: [Google AI Studio](https://makersuite.google.com/app/apikey)
- Anthropic: [Anthropic API](https://www.anthropic.com/api)

## 📂 プロジェクト構造
- `examples/customer_service/`
  - `config.json`: エージェントの設定ファイル
    - エージェントの役割、目的、ドメイン、ワーカー設定を定義
  - `task_documents.pkl`: タスク関連のドキュメントとリソース
  - `taskgraph.json`: タスクグラフの構造定義
  - `taskplanning.json`: タスク計画の詳細

## 📋 config.json の詳細
`config.json` は、エージェントの動作を定義する重要な設定ファイルです：
- `role`: エージェントの主な役割
- `user_objective`: ユーザーの目標
- `builder_objective`: システム側の追加目標
- `domain`: エージェントが対応する業界やドメイン
- `intro`: 企業や製品の背景情報
- `workers`: エージェントが使用するワーカーの設定
  - `FaissRAGWorker`: 検索拡張生成（RAG）
  - `MessageWorker`: メッセージ処理
  - `SearchWorker`: 情報検索
  - `DefaultWorker`: デフォルトの処理

## 🔧 使用方法

### タスクグラフの生成
```bash
python create.py --config ./examples/customer_service/config.json --output-dir ./examples/customer_service
```

### エージェントの起動
```bash
python run.py --input-dir ./examples/customer_service
```

### モデルAPIの起動
```bash
python model_api.py --input-dir ./examples/customer_service
```

### エージェントの評価
```bash
python eval.py \
  --model_api http://127.0.0.1:8000/eval/chat \
  --config ./examples/customer_service/config.json \
  --documents_dir ./examples/customer_service \
  --output-dir ./examples/customer_service
```

## 🛠️ トラブルシューティング
- APIキーが正しく設定されていることを確認してください
- 必要に応じて、`python-dotenv` を使用して環境変数を読み込みます

## 📝 ライセンス
[ライセンス情報を追加]

## 🤝 貢献
[貢献方法に関する情報を追加]