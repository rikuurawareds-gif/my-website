# サイトの公開（無料で始めて、後で独自ドメインへ移す）

## 決定
- 当面は **Cloudflare Pages の無料のサブドメイン**（例: `afimakase.pages.dev`）で公開する（2026-11-25 オーナー決定）
- 独自ドメインが必要になったら、Cloudflare Pages に独自ドメインを追加するだけで移せる（URLが変わるので、XのプロフィールなどのリンクはPMが張り替える）

GitHub Pages ではなく Cloudflare Pages にする理由:
- サイトのフォルダ（`affiliate/site`）だけを公開でき、URLがきれい
- リポジトリを非公開にしても無料で使い続けられる
- 独自ドメインへの切り替えが簡単

## オーナーの作業（1回だけ・約10分）
1. https://dash.cloudflare.com/sign-up でアカウントを作る（無料）
2. 「Workers & Pages」→「作成」→「Pages」→「Git に接続」→ GitHub と連携し、`my-website` リポジトリを選ぶ
3. 設定:
   - プロジェクト名: `afimakase`（URLが `afimakase.pages.dev` になる。使われていたら `afimakase-jp` など）
   - 本番ブランチ: `main`（PR #1 をマージするまでは `claude/friendly-hawking-5k5ymh`）
   - フレームワーク: なし ／ ビルドコマンド: 空欄 ／ 出力ディレクトリ: `affiliate/site`
4. 「保存してデプロイ」→ 表示されたURLを PM に伝える

以後、PM がリポジトリを更新すると自動で公開される。

## 公開前に PM がやること
- `affiliate/site/assets/config.js` に GA4 の測定ID と、相談フォームの送信先（`automation/lead-capture.gs` のURL）を入れる
- プライバシーポリシーの運営者名・問い合わせ先・制定日を埋める（オーナーに確認）
- `compliance-reviewer` で LP の表現を確認する
