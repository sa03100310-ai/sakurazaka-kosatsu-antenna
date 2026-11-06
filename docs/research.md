# 調査と設計判断

確認日：2026年11月6日（日本時間）。記載は確認時点の公式資料と公開サイトに基づきます。サービスの条件は変更されることがあります。

## 類似サイト

| サイト | 確認できた主な対象 | 今回との違い |
|---|---|---|
| [坂道46days・櫻坂46](https://sakamichi46-days.net/sakurazaka46) | ニュース・まとめ・特集 | 個人の考察ブログだけを登録対象にする構成ではない |
| [櫻坂46メンバーブログ紹介サイト](https://skr46.com/) | 公式メンバーブログの更新紹介 | ファンが書いた個人批評の集約ではない |
| [サクラノート](https://sakura46note.com/) | セットリスト等のデータ・ファン向けツール | 個人書き手の考察を中心にした入口とは目的が異なる |
| [坂道データベース](https://sakamichidb.anosaka.com/blog_stats/) | 公式メンバーブログの統計・検索 | 対象がメンバー自身のブログ |

検索した範囲では、今回と同じ対象・理念・機能を揃えたサイトは確認できませんでした。「存在しない」と断定する調査ではありません。まとめサイトのタイトル構成や広告密度は踏襲せず、記事タイトルと筆者への導線を中心にしました。

## 無料構成

採用：GitHub Pages + GitHub Actions + Python標準ライブラリ + JSON + HTML/CSS/JavaScript。

- GitHub Freeでも公開リポジトリでPagesを利用可能。公開サイト1GB、月100GBのソフト転送量上限等があります。[Pagesの制限](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- 公開リポジトリの標準GitHub-hosted runnerは無料。larger runnerは別であり採用しません。保存容量にも制限があるため、Pages用一時成果物の保持期間は1日にしています。[Actionsの課金条件](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- 予定実行は遅延や欠落があり、既定ブランチでのみ動きます。公開リポジトリで60日間活動がない場合、定期実行が無効になる条件があります。毎時0分を避け、6時間おきの17分にしています。[scheduleの公式説明](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- 公開方法はSettings → PagesでGitHub Actionsを指定する方式です。[公開元の設定](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)、[カスタムワークフロー](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

Pythonに追加パッケージを必要としないため、インストール失敗と依存関係の維持負担を抑えています。読者のブラウザから各RSSを直接取得せず、サーバー側の定期取得で作った静的データを配信します。

## RSSと利用条件

- noteは一般機能としてRSSを提供し、サーバー側で取り込んだうえでサイトに埋め込む方法を案内しています。通常アカウントは最新25件、独自ドメインを使うnote proは50件という案内です。[公式RSS案内](https://www.help-note.com/hc/ja/articles/4402395202841)
- noteの通常RSS本文は冒頭のみです。記事全文による判定ではありません。[全文RSSについて](https://www.help-note.com/hc/ja/articles/900001001246)
- はてなブログの更新フィードはAtomとRSS 2.0に対応し、通常は最新30件、本文全文が含まれます。全文が届いても転載や保存はせず、一時的な判定のみに使います。[更新フィードの公式説明](https://help.hatenablog.com/entry/feed)
- noteではコンテンツの著作権がクリエイターに帰属することが示されています。[note利用規約](https://note.com/terms)
- はてなの規約も知的財産権侵害などを禁止しています。[はてな利用規約](https://policies.hatena.ne.jp/rule)

RSSの提供は、画像や本文のあらゆる再利用を包括的に許す意味ではありません。この実装ではリンク一覧に必要なタイトル・筆者・日付・URLに絞っています。サムネイル、本文抜粋、歌詞を配信しません。各筆者への個別許諾取得はしていません。個別サイトの転載禁止表記や掲載拒否が判明した場合は停止します。サイト全ページの利用条件を精査した法的保証ではありません。

## クリックランキング

| 方法 | 得られるもの | 初期版への判断 |
|---|---|---|
| ブラウザのlocalStorage | その端末のクリックだけ | 全訪問者のランキングにならないので不採用 |
| GA4の離脱クリック | 元記事URLごとのクリックイベント | 無料で始めやすいが設定・集計API・公開ランキングへの反映が別途必要。広告ブロックなどによる欠測もあり、完全計測ではない |
| Cloudflare Web Analytics | PV・訪問等 | 公式FAQではカスタムイベント非対応。今回のクリックランキングにそのまま使えない |
| Cloudflare Workers + D1 のリダイレクト | 当サイトから元記事に転送したリクエスト数 | 有力な将来案。無料枠で小規模運用可能だが、アカウント・データベース・Bot対策・集計の維持が増える |

結論：初期版は未実装。最初は発見・検索・書き手の公平な扱いを優先します。ランキングを導入するときは「24時間・7日・30日の当サイト経由クリック」であり、note等のPV、読了者数、ユニーク人数とは違うことを表示します。

サーバー側の転送方式でも、Bot・先読み・連打があるため「人間の実クリックを100%正確に測れる」とは言えません。記事IDを許可リストで管理し、任意の外部URLへ転送できるオープンリダイレクトを作らない設計が必要です。日次集計にする場合、直近24時間を暦日合計と取り違えないよう時間窓も設計します。

出典：

- [GA4拡張計測・離脱クリック](https://support.google.com/analytics/answer/9216061?hl=ja)
- [Cloudflare Web Analytics FAQ（カスタムイベント）](https://developers.cloudflare.com/web-analytics/faq/)
- [Workersの料金](https://developers.cloudflare.com/workers/platform/pricing/)
- [D1の料金](https://developers.cloudflare.com/d1/platform/pricing/)

## 収集の公平性と限界

登録時に知名度やフォロワー数の閾値を設けていません。運営者も同じルールです。初期候補は検索で見つかった範囲なので、検索されにくい書き手は未発見のままです。批判的な見方を理由に除外していませんが、記事の真偽・質・執筆方法を保証しているわけではありません。

最新順は高頻度更新者が目立ちます。そこで「書き手を交互に」を用意し、各筆者の最新記事を1本ずつ取り出してから次の周回に進めます。記事単位でランダム抽選して、投稿数の多い筆者に有利にする方式ではありません。
