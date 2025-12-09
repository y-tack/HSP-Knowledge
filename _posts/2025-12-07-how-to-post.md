---
layout: post
title: 記事の投稿方法
date: 2000-01-01 12:00:00 +0900
lastupdate: 2099-12-31 23:59:59 +9:00
author: HSP-Knowledge運営
tags: [使い方, チュートリアル]
summary: HSP-Knowledgeに記事を投稿する方法を説明します。GitHubを使った投稿手順を分かりやすく解説。
---

HSP-Knowledgeへようこそ! このサイトでは、HSPに関する知識やTipsをみんなで共有できます。

## 📝 投稿の流れ

記事の投稿は以下の3ステップで完了します:

1. **リポジトリをFork**
2. **記事ファイルを作成・編集**
3. **Pull Requestを送信**

## 1. リポジトリをFork

まず、[GitHub リポジトリ](https://github.com/Velgail/HSP-Knowledge)にアクセスして、右上の「Fork」ボタンをクリックします。

これであなたのGitHubアカウントにリポジトリのコピーが作成されます。

## 2. 記事ファイルを作成

### ファイル名のルール

`_posts/`フォルダ内に、以下の形式でファイルを作成します:

```
YYYY-MM-DD-記事のタイトル.md
```

**例:** `2025-12-07-my-first-hsp-article.md`

### テンプレートを使う

`_posts/template.md`をコピーして使うと便利です:

```bash
cd _posts
cp template.md 2025-12-07-my-article.md
```

### 記事の構造

記事ファイルは以下の構造になっています:

```markdown
---
layout: post
title: 記事のタイトル
date: 2025-12-07 12:00:00 +0900
author: あなたの名前
tags: [小技, HSP3]
summary: 記事の概要を120文字以内で
---

ここに本文を書きます。

## 見出し

Markdown形式で自由に記述できます。

### コード例

```hsp
mes "Hello, HSP!"
```
```

## 3. タグの選び方

記事には適切なタグを付けると、他のユーザーが見つけやすくなります。

### 推奨タグ

以下のタグを積極的に使ってください:

- **小技** - ちょっとしたテクニックやTips
- **チュートリアル** - 初心者向けの解説記事
- **応用** - 高度な技術や実践的な内容

その他、自由にタグを追加できます。

## 4. Pull Requestを送信

記事を書き終えたら、以下の手順でPull Requestを送信します:

1. 変更をコミット
2. Forkしたリポジトリにプッシュ
3. GitHubでPull Requestを作成
4. レビュー後、マージされます

### GitHubのWeb UIで編集する場合

1. Forkしたリポジトリの`_posts/`フォルダを開く
2. 「Add file」→「Create new file」をクリック
3. ファイル名と内容を入力
4. 「Commit new file」をクリック
5. Pull Requestタブから「New pull request」を作成

## 💡 記事を書くコツ

### 見出しを活用する

```markdown
## 大見出し
### 中見出し
#### 小見出し
```

### コードブロックを使う

HSPコードには`hsp`言語指定をすると、シンタックスハイライトが適用されます:

````markdown
```hsp
#include "hsp3utf.as"

mes "日本語も使えます"
```
````
↓
```hsp
#include "hsp3utf.as"

mes "日本語も使えます"
```


### 画像を追加する

画像は`assets/images/`フォルダに配置し、以下のように参照します:

```markdown
![説明文]({{ "/assets/images/my-image.png" | relative_url }})
```

### リンクを追加する

```markdown
[HSP公式サイト](https://hsp.tv/)
```

## 🎨 プレビューする

ローカル環境でJekyllをインストールしている場合、以下のコマンドでプレビューできます:

```bash
bundle exec jekyll serve
```

ブラウザで`http://localhost:4000/HSP-Knowledge/`にアクセスすると、記事のプレビューが表示されます。

## ❓ 困ったときは

- [GitHub Discussions](https://github.com/Velgail/HSP-Knowledge/discussions) で質問する
- Issuesで問題を報告する
- HSPTV! 掲示板で相談する

## ⚖️ ライセンスについて

本サイトに投稿された記事は、以下のライセンス方針で公開されます。投稿をもってこれに同意したものとみなされます。

- **コードブロック・スニペット**: **[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) (パブリックドメイン)**
  - ユーザーは商用・非商用を問わず、クレジット表記なしで自由にコードを利用・改変できます。
- **記事本文**: **[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (クリエイティブ・コモンズ 表示 4.0)**
  - 記事を転載・引用する場合は、元の記事へのリンクや著者の表示が必要です。

## まとめ

記事の投稿は思ったより簡単です! あなたの知識をぜひ共有してください。

みんなで作るHSPナレッジベース、よろしくお願いします 🎉
