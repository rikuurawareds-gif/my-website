# 引き継ぎ書：アフィまかせ（アフィリエイト運用支援サービス）

最終更新: 2026-11-28
新しい Claude のセッションは、**最初にこのファイルを読み、次に「1. 最初にやること」を実行する**。

---

## 0. 一言で
広告主・アフィリエイト代理店向けに、アフィリエイトの運用（ASP・メディア対応、成果承認、記事の表記チェック、月次レポート）を **月5万円から** まるごと引き受けるサービス「アフィまかせ」を、オーナーの手をほぼ使わずに立ち上げている。LP は公開済み、最初の顧客の獲得に向けて準備中。

- LP（本番）: https://afimakase.pages.dev/ ／ コラム: https://afimakase.pages.dev/column/
- GitHub: `rikuurawareds-gif/my-website`（**公開リポジトリ**）、作業ブランチ `claude/friendly-hawking-5k5ymh`（これが Cloudflare Pages の本番ブランチ。push すると自動で公開）、PR #1（下書き）
- Google Drive: 「アフィリエイト事業」フォルダ https://drive.google.com/drive/folders/15YjEuSvXCW638BGOe-8edyTtuCaG46Oi

---

## 1. 新しいセッションで最初にやること
1. リポジトリをクローンし、ブランチ `claude/friendly-hawking-5k5ymh` に切り替える（main ではない）
2. 次の順に読む: `CLAUDE.md`（ルート）→ `affiliate/CLAUDE.md`（運営ルール）→ `affiliate/docs/decisions.md`（決めたこと）→ `affiliate/knowledge/owner-insights.md`（オーナーの見立て・最優先）→ `affiliate/docs/launch-checklist.md`（リリースまでの全工程と状態）
3. Drive の「作業結果の受け渡し」（`1h3CYlzcAakR8DB2nmBx2qvGakh9Z7z5Zahi3_SNWSzM`）を読み、オーナーが Chrome・コワークで終えた作業の結果を反映する（いま反映済みは 01 のみ）
4. PC のフォルダ（下の 7）がつながっていれば、`list_computer_folders` で確認して接続する

---

## 2. オーナーの方針（必ず守る）
- **オーナーが作業しなければならないもの以外は、すべて Claude（PM）の判断で進める。** 経営判断・設計・サービス選定・料金なども PM が決めて `decisions.md` に記録する
- オーナーに聞くのは **得意領域だけ**: 顧客の悩み、決裁者と断る理由、ASP・メディアの力学（答えは `knowledge/owner-insights.md` に蓄積）
- オーナーの作業は **Claude in Chrome / コワークに貼るだけの指示文** にする。止まってよいのは ID・パスワード、認証コード、CAPTCHA、権限の許可、支払い、本人確認、ファイル選択だけ。指示文はスキル `/sagyo-bunsyo` で作る
- **最速でリリースし、後から上げる。** ただし ①自社の宣伝表現 ②契約・規約（最初の有料契約の前に弁護士確認）③個人情報の扱い は品質を下げない
- 外部サービスの費用は **月1〜2万円まで PM の判断で使ってよい**（費用対効果を考える）。テスト用アカウントやオーナーの Gmail（「+」付きアドレス）の利用も可
- オーナーは個人事業として立ち上げる。前職（アフィリエイト代理店）の資料の利用は会社の了承済み。ただし資料は機密として扱う

## 3. 守る線（変えない）
- **個人情報**: 顧客の会員（登録者）の氏名・連絡先は預からない（成果ID・属性だけ）。取引先の担当者・上長・ASP/メディア担当の情報は連絡のために保存してよい（`legal/privacy-standard.md`）
- **公開リポジトリ**: 顧客名・媒体名・個別の数字・元資料・オーナーのメールアドレス・秘密情報を書かない。機密は Drive だけ
- **表記チェック**: 法的な判断はしない一次チェック（弁護士法72条への配慮）。規約・申込書・レポートに明記
- **X**: 自動投稿は公式 API 経由だけ（ブラウザ操作での自動投稿は規約違反で凍結のおそれ）
- **ASP**: 顧客に CSV を送らせない。代理店権限 → ASP 担当からの定期送付 → 専用ログイン（同意のうえパスワード管理サービス）の順

---

## 4. 決まっていること（要点。全文は `docs/decisions.md`）
| 項目 | 内容 |
|---|---|
| サービス名 | アフィまかせ（屋号。運営者表示も「アフィまかせ」、代表者の氏名・住所は請求があれば回答） |
| 料金（税別・初期費用0円・最低3か月） | はじめて 月5万円／運用（媒体費 月100万円まで）月5万円／大規模 月15万円〜／代理店 1アカウント月5万円／表記チェックのみ 月3万円 |
| 主な顧客 | ASP・メディアへの支払いが月30〜100万円の広告主（担当者が月20時間・約10万円分かけている運用を半額で）、アフィリエイト代理店（1アカウント20時間→5時間）。最初の営業は人材分野から |
| 決裁者と断る理由 | 上長・経営者。断る理由は「チェックの質」と「メディアが増えるのか」→ 無料の表記チェックと無料の伸びしろ診断（メディア名は出さない）で答える |
| 管理画面 | 当面作らない。Chatwork とスプレッドシート・Drive で回す |
| 表記チェック・診断の実行 | コワーク（オーナーの PC）。AI の判定もコワークの Claude（API 費用なし） |
| 公開先 | Cloudflare Pages の無料サブドメイン。独自ドメインは必要になったら |
| X | サービスアカウント。平日12:13に自動投稿（初回 2026-12-01 予定・29本予約済み） |

---

## 5. いまの状態
### できているもの
- LP（工数診断・料金・FAQ・相談フォーム・代理店向け・構造化データ）、プライバシーポリシー（2022年改正対応）
- コラム7本（運用代行の費用、ステマ規制、始め方、成果承認、EPC、PR表記、代理店の選び方）＋ 30本の計画、`robots.txt`・`sitemap.xml`・`llms.txt`
- 表記チェック v0（16ルール、テスト5件）、月次レポート集計 v0（形の違う ASP の CSV を自動でそろえる、テスト4件）
- Apps Script: 相談フォーム受付、X 自動投稿（OAuth 署名は公式例で検証済み）、ASP レポートのメール取り込み、GA4 取り込み
- 契約・規約のたたき台5点、弁護士への依頼文、個人情報の扱いの標準
- 受注後の導入手順、ヒアリングシート、連絡先台帳、作業ログ
- ナレッジ（代理店の提案資料・定例資料8件から一般化）、11の担当エージェント定義、スキル `/sagyo-bunsyo`

### オーナーの作業待ち（指示文はスプレッドシート「オーナー作業の指示文」）
| # | 作業 | 状態 |
|---|---|---|
| 01 | サイトの公開（Cloudflare Pages） | ✅ 完了 |
| 03・12・10・05・06 | 相談フォーム、2段階認証、ASP 取り込み、ASP の CSV 形式、営業リスト | 未（今すぐ並行で可） |
| 02・04 | GA4、X アカウント | 未（01 の後） |
| 07 | X 自動投稿の設定 | 未（04 の後。12/1 の初回投稿に間に合わせたい） |
| 11・13・14 | Chatwork 運用アカウント、弁護士の候補、開業届・インボイス | 未（最初の顧客の前まで） |
| 08・09 | 無料表記チェック、無料伸びしろ診断 | 見込み客が来たら毎回 |

### 次に PM がやること
1. 受け渡しドキュメントに結果が来たら反映（02 → GA4 の測定IDを `site/assets/config.js` に、03 → 送信先URLを同ファイルに、04 → ユーザー名を `marketing/x-account.md` に など）
2. コラムを週2本（`marketing/content-plan.md` の順）
3. 最初の顧客の前に M1（Chatwork 窓口の自動化）を設計 → Superpowers の brainstorming → writing-plans → TDD で作る
4. ASP の CSV 形式（05）が来たら、`automation/asp-formats/<ASP名>.md` と変換表をテスト付きで作る
5. X の翌月分の投稿を `X投稿キュー_YYYYMM.csv` として Drive に置く（既存ファイルは書き換えない）。手順は `marketing/x-account.md` の「毎月の投稿づくり」（`x-researcher` → `x-post-writer` → チェック）。**次回は 2026-12-20 ごろ、2027-01-15 以降の分**
6. X: @afimakase 開設済み、07（自動投稿）も設定完了・本番稼働（初回 12/1 12:13）。**12/1 の午後に、投稿されたかを投稿ログのシートで確認し、初回投稿をプロフィールに固定する**（状態は `marketing/x-account.md`）

---

## 6. フォルダの構成
### GitHub リポジトリ（`rikuurawareds-gif/my-website`、ブランチ `claude/friendly-hawking-5k5ymh`）
```
CLAUDE.md                     リポジトリの概要（index.html はスマブラ賭けカウンターで無関係。触らない）
.claude/
  agents/                     担当エージェント 11（事業設計、サービス設計、開発、表記チェック、ASP対応、レポート、デザイン、コンテンツ、計測、CVR、社内法務）
  skills/sagyo-bunsyo/        オーナー作業を「貼るだけの指示文」にするスキル
affiliate/
  HANDOFF.md                  この引き継ぎ書
  CLAUDE.md                   運営ルール（全担当が読む。Superpowers の使い方、PM の道具の制約もここ）
  README.md                   事業の入口
  docs/                       decisions（決定ログ）、launch-checklist（全工程）、overall-design、business-plan、
                              workload-inventory（工数の棚卸し・モジュール M1〜M10）、architecture、roadmap、hosting、
                              industry-standards（料金・書類の業界標準）、drive（Drive の ID 一覧）、services/（モジュール仕様）ほか
  knowledge/                  owner-insights（最優先）、operations / proposal / report の型、指標辞書、工数の実データ
  playbooks/                  asp-pitch（ASP への連絡の6項目）、media-escalation（修正に応じないメディアの停止ルール）
  legal/                      利用規約・申込書・NDA・個人情報の覚書・委任範囲の合意書のたたき台、個人情報の標準、弁護士への依頼文
  site/                       公開サイト（Cloudflare Pages の出力ディレクトリ）
    index.html, privacy.html  LP とプライバシーポリシー
    content/*.md              コラムの原稿 → build.py で column/ と sitemap.xml・llms.txt を生成
    assets/                   config.js（GA4 の測定ID・フォームの送信先）、track.js（計測）
  checker/                    表記チェック v0（check.py、rules.json、テスト、サンプルレポート）
  reporting/                  月次レポート v0（report.py、テスト）
  automation/                 Apps Script: lead-capture / x-autopost / asp-intake / ga4-to-sheet、asp-formats/
  marketing/                  X の方針と投稿、営業の手順と文面、コンテンツ計画
  ops/                        onboarding（受注後の導入手順）、owner-tasks/（指示文 01〜14）
  lp/                         （旧）アフィリエイトメディア用の LP テンプレート。いまは使っていない
```

### Google Drive「アフィリエイト事業」（ID は `affiliate/docs/drive.md`）
```
00_PM・経営          オーナー作業の指示文（スプレッドシート）、作業結果の受け渡し、意思決定ログ、作業ログ
01_事業設計・リサーチ  提案資料（元データ）: 代理店の提案資料 PDF と読み込みノート（機密）
02_サービス設計
03_デザイン素材        X のアイコン・ヘッダー画像
04_コンテンツ・LP原稿
05_計測・KPI          KPI_週次、ASP管理画面_日次取込、ASP_CSV形式_収集メモ
06_ASP・契約          ASP案件管理（今は使わない）
07_法務・コンプライアンス
08_顧客              顧客管理、_顧客テンプレート（ASP成果CSV／月次レポート／表記チェックレポート／契約・レギュレーション／提携メディア台帳／連絡先台帳）、
                     ASP振り分け設定、ASPレポート_未振り分け、ヒアリングシート（テンプレート）
09_集客              リード管理、営業先リスト、X投稿キュー.csv、X投稿ログ
99_アーカイブ
```
オーナーが共有した代理店の定例資料（機密）: 共有フォルダ `1ctQ4sM21xUpkFp_9TtJIwcrNljABC-QV`

---

## 7. オーナーの PC のフォルダ
- 使いたいフォルダ: `C:\Users\rikuu\OneDrive\デスクトップ\Claude`、`C:\Users\rikuu\Downloads`
- 2026-11-27 時点: Remote Control に登録済みだが、クラウドのセッションには「not_available」（PC 側がまだ提供していない。Windows の Claude アプリの更新が必要な可能性）。**System32 が登録されていたので外すよう案内済み**
- 1つのセッションがつながれるのは1フォルダずつ。普段は `デスクトップ\Claude` を推奨
- つながらない場合の代替: Google ドライブ パソコン版で `デスクトップ\Claude` を同期 → Drive 経由で読む
- **2026-11-28: Windows の Claude アプリ（Code タブ）で、PC 上で直接セッションを動かせるようになった。** リポジトリは `デスクトップ\Claude\アフィリエイト運用\my-website` にクローン済み（ブランチ `claude/friendly-hawking-5k5ymh`）。PC には Python 3.12 を入れた（`%LOCALAPPDATA%\Programs\Python\Python312\python.exe`。`python` コマンドは Microsoft Store の別名が先に当たるので、フルパスで呼ぶ）。テストは `python checker\tests\test_check.py` のようにファイルを直接実行する

---

## 8. 道具の制約と注意
- Drive の道具は **新規作成と読み取りはできるが、既存ファイルの中身は書き換えられない**。追記が必要な仕組みは「フォルダ内の特定の名前で始まるファイルをすべて読む」形にしてある（X 投稿キュー、ASP 振り分けルール）。指示文シートを直すときは新しいシートを作り、古いものはゴミ箱へ
- クラウドの作業環境からは外部サイト（pages.dev、一部の官公庁サイトなど）に直接つながらないことがある。公開ページの確認はオーナーのブラウザかコワークで
- Claude（PM）が作業できるのは会話中だけ。オーナーには、作業が終わったら「終わった」と言ってもらう
- `git push` で LP・コラムは自動公開される。公開前に `checker/check.py` で自社の表現を確認し、LP はヘッドレスブラウザで動作を確認する
- Superpowers の使い方は `affiliate/CLAUDE.md` の表のとおり（大きい仕組みは brainstorming → writing-plans、コードは TDD、完了報告の前に検証）
