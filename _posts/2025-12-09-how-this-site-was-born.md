---
layout: post
date: 2025-12-09 00:58:00 +09:00
title: 【開発記録】HSP-Knowledgeができるまで ─ 72時間で作ったQiita風ナレッジ共有サイト
author: Velgail & Claude 4.5 Opus
tags: [Tips, 開発記録, GitHub Pages, Jekyll, 自動化, チュートリアル]
summary: 「Qiitaみたいなの欲しいよね」という掲示板の一言から始まり、72時間でGitHub Pages + Jekyll + Gemini自動レビューで維持費0円のナレッジ共有サイトを作った話。
---

## はじまりは深夜2時の掲示板

2025年12月5日、深夜2時39分。

HSP掲示板にこんな書き込みがありました。

> 変な時間に目覚めて考えたんですが😅
> Qiitaみたいなコンテンツはどうでしょうか😆
> ─ Y_repeat さん

この一言がすべての始まりでした。

## 🤔 HSPコミュニティの課題

掲示板での議論から浮かび上がった問題点をまとめると：

1. **情報の分散** - 公式Wiki、個人Wiki、ブログ、Qiita……あちこちに散らばっている
2. **Wikiの維持が大変** - 立ち上げた人にかなりの負担がかかる
3. **スパム対策の難しさ** - MediaWikiを放置したらスパムだらけに
4. **費用の問題** - サーバー代を誰が負担するのか

ABATBelieverさん（HSP Wiki運営者）のコメントが的を射ていました：

> 人手があれば、作ることはできます。問題は維持すること。

## 💡 「GitHub Pagesで頑張ってみる案」

私（Velgail）は12月7日の深夜に掲示板を見て、こう書き込みました：

> GitHub Pagesで頑張ってみる案もありますね。サーバー代とかを考えなくて済むので。

そして、その日のうちに実験場を公開：

> 一応頑張ればGithub Pagesでできるっぽいので、[実験場を作ってみました](https://velgail.github.io/HSP-Knowledge/)。

ここから怒涛の開発が始まります。

## 🛠️ 採用した技術スタック

### なぜこの構成なのか

| 課題 | 解決策 | 選んだ技術 |
|------|--------|------------|
| 維持費0円にしたい | 静的サイトホスティング | **GitHub Pages** |
| メンテナンス極小 | ビルド済みHTML配信 | **Jekyll** |
| 誰でも投稿可能 | PRベースの投稿システム | **GitHub Pull Request** |
| スパム防止 | AI自動レビュー | **Gemini Code Assist** |
| シンタックスハイライト | カスタム実装 | **HSP専用ハイライター** |

### GitHub Pagesを選んだ理由

```
✅ 完全無料（容量制限1GB、十分すぎる）
✅ セキュリティパッチ不要（GitHubが管理）
✅ CDN配信で高速
✅ 独自ドメイン対応可能
✅ HTTPS自動対応
```

## 📁 プロジェクト構成

最終的なディレクトリ構成はこうなりました：

```
HSP-Knowledge/
├── _config.yml           # Jekyll設定
├── _layouts/
│   ├── default.html      # ベースレイアウト
│   ├── post.html         # 記事ページ
│   └── tag.html          # タグページ
├── _posts/               # 記事置き場（Markdown）
│   ├── template.md       # 記事テンプレート
│   └── 2025-12-07-*.md   # 投稿記事
├── assets/
│   └── style.css         # スタイルシート
├── scripts/
│   └── check_pr.py       # 記事検証スクリプト
├── .github/
│   └── workflows/
│       └── pr-auto-review.yml  # 自動レビューワークフロー
└── .gemini/
    └── prompts.yaml      # Gemini用プロンプト
```

## 🎨 実装した機能

### 1. Qiita風デザイン

<img alt="image" src="https://github.com/user-attachments/assets/b108545c-2932-4a90-bfc7-a318ffdf3fc5" />

- 左サイドバー：タグ一覧
- メインコンテンツ：記事カード
- 右サイドバー：関連リンク、新着記事

### 2. HSP専用シンタックスハイライト

Copilotの力を借りて、**HSP専用のシンタックスハイライト**を実装しました。

```hsp
#include "hsp3dish.as"

*main
    redraw 0
    color 0, 0, 128
    boxf
    color 255, 255, 255
    pos 100, 100
    mes "Hello, HSP-Knowledge!"
    redraw 1
    await 16
    goto *main
```

既存のJavaScript構文ハイライターにはHSPがないので、独自にキーワードを定義：

- 命令（`mes`, `boxf`, `await` など）
- プリプロセッサ（`#include`, `#define` など）
- ラベル（`*main` など）
- コメント（`//` や `;`）

### 3. スマートフォン対応

名無しさんからの指摘を受けて、レスポンシブデザインを実装：

```css
@media (max-width: 768px) {
    .sidebar-left, .sidebar-right {
        display: none;
    }
    .main-content {
        margin: 0;
        padding: 1rem;
    }
}
```

### 4. コードブロックのコピー機能

これも名無しさんからの要望で実装。ただし、**行番号をコピーしない**ように工夫：

```javascript
// 行番号はCSSのcounter-incrementで生成
// コピー時はtextContentのみ取得
```

## 🤖 自動レビューシステム

ここからが本サイトの真骨頂です。

### 課題：人手によるレビューは持続不可能

Y_repeatさんの懸念：
> 定期的に見にいかなきゃいけないですし

ABATBelieverさんの経験：
> MediaWikiに沸くスパムについては、CloudflareとかのCDNを使えば緩和できますよ

### 解決策：Gemini + GitHub Actionsで完全自動化

```yaml
# .github/workflows/pr-auto-review.yml
name: PR Auto Review

on:
  pull_request:
    types: [opened, synchronize]
  issue_comment:
    types: [created]

jobs:
  validate-article:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run validation script
        run: python scripts/check_pr.py
        
      - name: Post review comment
        # 検証結果をPRにコメント
```

### 検証項目

`scripts/check_pr.py` で以下をチェック：

1. **ファイル名検証** - `YYYY-MM-DD-title.md` 形式か
2. **Front Matter検証** - 必須フィールド（title, author, tags）が存在するか
3. **テンプレート検証** - 「ここに本文を書きます」がそのまま残っていないか
4. **スパム判定** - HSP関連キーワードが含まれているか、外部リンクが多すぎないか
5. **更新時の検証** - 他人の記事のauthorを書き換えていないか

### /publish コマンド

検証に合格した記事は、PR作成者が `/publish` とコメントするだけで自動マージ！

```
ユーザー: /publish
↓
GitHub Actions: 検証OK？ → Approve → Auto Merge
```

**人間の手を介さずに記事が公開される**ので、管理者が寝ていても大丈夫です。

## 🔥 72時間の開発タイムライン

実際の掲示板の投稿時刻から振り返ると：

| 日時 | 出来事 |
|------|--------|
| 12/5 02:39 | Y_repeatさんが「Qiitaみたいなの」を提案 |
| 12/5 03:28 | nayaさんが賛同 |
| 12/6 22:14 | ABATBelieverさんが維持の難しさを指摘 |
| 12/7 00:42 | Velgailが「GitHub Pages案」を提案 |
| 12/7 15:24 | **実験サイト公開**（爆速） |
| 12/7 16:12 | Gemini自動レビュー機能を発見・実装開始 |
| 12/7 19:50 | Y_repeatさんが初PR投稿を試みる |
| 12/7 19:55 | HSPシンタックスハイライト実装完了 |
| 12/7 21:47 | コードコピー機能のバグ修正 |
| 12/8 00:24 | 投稿フロー改善案（GitHub Discussions活用）を提示 |
| 12/8 02:17 | スパム判定の自動化実装 |
| 12/8 03:59 | **自動検証・自動マージシステム完成** |

最初の提案から**約50時間**で、自動化されたナレッジ共有サイトが完成しました。

## 🚀 あなたもクローンできます

このサイトの仕組みは、**そのまま他のコミュニティでも使えます**。

### 1. リポジトリをFork

```bash
# GitHubでForkボタンを押すか、CLIで
gh repo fork Velgail/HSP-Knowledge
```

### 2. 設定を書き換え

```yaml
# _config.yml
title: あなたのナレッジサイト
description: あなたのコミュニティ向け説明
baseurl: "/your-repo-name"
url: "https://your-username.github.io"
```

### 3. GitHub Pagesを有効化

リポジトリ設定 → Pages → Source: `GitHub Actions`

### 4. 必要に応じてカスタマイズ

- `assets/style.css` - デザイン変更
- `_layouts/` - レイアウト変更
- `scripts/check_pr.py` - 検証ルール変更

## 📝 今後の展望

掲示板でいただいたフィードバックを元に、以下の機能を検討中：

- [ ] **GitHub Discussionsとの連携** - より気軽に投稿できる入口
- [ ] **記事の品質スコアリング** - 良い記事を見つけやすく
- [ ] **自動タグ提案** - Geminiによるタグ推薦
- [ ] **類似記事の検出** - 重複を防ぐ

## 🙏 謝辞

このサイトは、掲示板で議論に参加してくださった皆さんのおかげで生まれました：

- **Y_repeat さん** - 最初の提案と積極的なテスト参加
- **naya さん** - 賛同の声
- **ABATBeliever さん** - Wiki運営経験からの現実的な指摘
- **名無し さん** - 的確なUI/UXフィードバック

そして、72時間ほぼ寝ずにコードを書き続けた**GitHub Copilot**にも感謝します（本当に）。

---

> 「一気に作らなくても良い気がなきにしもあらず😅」
> ─ Y_repeat さん (12/8 12:45)

確かにその通りです（笑）。でも、勢いって大事ですよね。

---

## 📚 関連リンク

- [HSP-Knowledge GitHub リポジトリ](https://github.com/Velgail/HSP-Knowledge)
- [自動レビューシステムの詳細](https://github.com/Velgail/HSP-Knowledge/blob/main/docs/AUTO_REVIEW_SYSTEM.md)

## おわりに

「維持が大変」という問題に対して、「維持しなくていい仕組み」で答えを出せたのは、GitHub PagesとGemini Code Assistのおかげです。

もちろんこれが唯一の正解ではありませんが、**「叩き台としてまず動くものを作る」**ことで、議論が具体的になることを実感しました。

HSPコミュニティの情報共有が、少しでも活発になれば嬉しいです。

**Happy Hacking!** 🚀
