from flask import Flask, render_template, request, redirect
from openai import OpenAI
from dotenv import load_dotenv
import datetime
import os

# .env読み込み
load_dotenv()

# Flaskアプリ作成
app = Flask(__name__)

# OpenAI APIクライアント作成
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/")
def index():
    prompt = """
AIについて、
あなたが思うことを短くコメントしてください。

1～2文だけでお願いします。
60文字以内。
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    mystery_text = response.output_text.strip()

    return render_template("index.html", mystery_text=mystery_text)


@app.route("/profile")
def profile():
    return render_template("profile.html")


# -------------------- 制作物 --------------------
@app.route("/works")
def works():
    return render_template("works.html")


@app.route("/works/python")
def works_python():
    return render_template("works_python.html")


@app.route("/works/php")
def works_php():
    return render_template("works_php.html")


@app.route("/works/javascript")
def works_javascript():
    return render_template("works_javascript.html")

# メモアシスト（Python）
@app.route("/works/memo_assist")
def work_memo_assist():
    return render_template("work_memo_assist.html")

# 文章変換（Python）
@app.route("/works/proofreading")
def work_proofreading():
    return render_template("work_proofreading.html")

# AI解読（Python）
@app.route("/works/explanation")
def work_explanation():
    return render_template("work_explanation.html")

# DBテーブル作成（Python）
@app.route("/works/dbcreate")
def work_dbcreate():
    return render_template("work_dbcreate.html")

# 電話アシスト（Python）
@app.route("/works/callassist")
def work_callassist():
    return render_template("work_callassist.html")

# 学習支援（Python）
@app.route("/works/studysupport")
def work_studysupport():
    return render_template("work_studysupport.html")

# ワード保存（Python）
@app.route("/works/wordkeep")
def work_wordkeep():
    return render_template("work_wordkeep.html")

# 日直日誌（新）（PHP）
@app.route("/works/php_diary_new")
def work_php_new():
    return render_template("work_php_diary_new.html")

# 日直日誌（旧）（PHP）
@app.route("/works/php_diary_old")
def work_php_old():
    return render_template("work_php_diary_old.html")

# APIで天気取得（JavaScript）
@app.route("/works/javascript_app_weather")
def work_js_weather():
    return render_template("work_javascript_app_weather.html")

# APIで祝日情報（JavaScript）
@app.route("/works/javascript_app_holiday")
def work_js_holiday():
    return render_template("work_javascript_app_holiday.html")

# APIで首都検索（JavaScript）
@app.route("/works/javascript_app_capital")
def work_js_capital():
    return render_template("work_javascript_app_capital.html")

# -------------------- プロフィール --------------------
@app.route("/profile/about")
def about():
    return render_template("profile_about.html")


@app.route("/profile/education")
def profile_education():
    return render_template("profile_education.html")


@app.route("/profile/career")
def career():
    return render_template("profile_career.html")


@app.route("/profile/skills")
def profile_skills():
    return render_template("profile_skills.html")


@app.route("/profile/status")
def profile_status():
    return render_template("profile_status.html")


# AI ASSISTANT
@app.route("/ai_suggest", methods=["POST"])
def ai_suggest():
    mode = request.form.get("mode", "works")
    keyword = request.form.get("keyword", "")

    import json
    import re

    # --------------------
    # プロフィール検索
    # --------------------
    if mode == "profile":
        routes = {
            "about": "/profile/about",
            "education": "/profile/education",
            "career": "/profile/career",
            "skills": "/profile/skills",
            "status": "/profile/status",
        }

        prompt = f"""
あなたはポートフォリオサイトのプロフィール案内AIです。
ユーザー入力に合うプロフィールページを最大3件提案してください。

【使用できるページ】
about（私について）
education（学歴）
career（職歴）
skills（スキル）
status（現在の状況）

【ルール】
・必ず上記のページから選ぶ
・「学歴」と入力されたら education を提案する
・「職歴」と入力されたら career を提案する
・「スキル」「技術」と入力されたら skills を提案する
・「現在」「状況」と入力されたら status を提案する
・説明は短く
・JSONだけを返す

【出力形式】
[
  {{
    "title": "学歴",
    "desc": "これまでの学習や経歴を確認できます。",
    "url_key": "education"
  }}
]

【ユーザー入力】
{keyword}
"""

    # --------------------
    # 制作物検索
    # --------------------
    else:
        routes = {
            "callassist": "/works/callassist",
            "memo_assist": "/works/memo_assist",
            "explanation": "/works/explanation",
            "dbcreate": "/works/dbcreate",
            "studysupport": "/works/studysupport",
            "wordkeep": "/works/wordkeep",
            "php_diary_new": "/works/php_diary_new",
            "php_diary_old": "/works/php_diary_old",
            "javascript_app_holiday": "/works/javascript_app_holiday",
        }

        prompt = f"""
あなたはポートフォリオサイトの制作物案内AIです。
ユーザー入力に合う制作物を最大3件提案してください。

【使用できる制作物】
callassist（Python / 電話取次ぎアシスタント）
memo_assist（Python / メモ整理システム）
explanation（Python / AI解読システム）
dbcreate（Python / DBテーブル作成システム）
studysupport（Python / 学習支援システム）
wordkeep（Python / ワード保存システム）
php_diary_new（PHP / 日直日誌システム新）
php_diary_old（PHP / 日直日誌システム旧）
javascript_app_holiday（JavaScript / 祝日取得アプリ）

【ルール】
・必ず上記の制作物から選ぶ
・存在しない制作物は作らない
・新しいアイデアは禁止
・「Python」と入力されたらPython作品から提案する
・「PHP」と入力されたらPHP作品から提案する
・「JavaScript」と入力されたらJavaScript作品から提案する
・「CSS」など該当作品がない場合は [] を返す
・説明は短く
・JSONだけを返す

【出力形式】
[
  {{
    "title": "電話取次ぎアシスタント",
    "desc": "PythonとAI連携を使った制作物です。",
    "url_key": "callassist"
  }}
]

【ユーザー入力】
{keyword}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    try:
        suggestions_raw = response.output_text.strip()

        # ```json が付いて返ってきた場合の保険
        suggestions_raw = re.sub(r"^```json", "", suggestions_raw)
        suggestions_raw = re.sub(r"^```", "", suggestions_raw)
        suggestions_raw = re.sub(r"```$", "", suggestions_raw).strip()

        suggestions_json = json.loads(suggestions_raw)

        suggestions = []
        for s in suggestions_json:
            url_key = s.get("url_key")

            if url_key in routes:
                suggestions.append({
                    "title": s.get("title", ""),
                    "desc": s.get("desc", ""),
                    "url": routes[url_key]
                })

        if not suggestions:
            suggestions = [
                {
                    "title": "関連する候補が見つかりませんでした",
                    "desc": "別の言葉で入力してみてください。",
                    "url": "/"
                }
            ]

    except:
        suggestions = [
            {
                "title": "案内候補を作成できませんでした",
                "desc": "もう一度、別の言葉で入力してみてください。",
                "url": "/"
            }
        ]

    return render_template("index.html", suggestions=suggestions)


# -------------------- AI回答 --------------------
@app.route("/ai_question", methods=["POST"])
def ai_question():
    question = request.form.get("question", "")

    with open("data/profile_info.txt", "r", encoding="utf-8") as f:
        profile_info = f.read()

    prompt = f"""
あなたはポートフォリオサイト内の案内AIです。
以下の大城将吾に関する情報をもとに、質問へ回答してください。

【回答ルール】
・資料に書かれている内容をもとに答える
・わからないことは推測しすぎない
・褒めすぎない
・採用担当者が読んでも違和感のない表現にする
・短めに答える

【大城将吾の情報】
{profile_info}

【質問】
{question}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    result = response.output_text.strip()

    return render_template("index.html", result=result)


# -------------------- AI案内 --------------------
def get_target_page(user_input):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"""
あなたはWebサイトのナビゲーターです。
ユーザーの入力に応じて、以下の中から最適なページを1つだけ選んでください。

【選択肢】
home
profile
works
about
education
career
skills
status
python
php
javascript

【ルール】
・必ず1単語だけ返す
・説明は不要
・迷った場合は広いカテゴリを選んでください

【ユーザー入力】
{user_input}
"""
    )

    return response.output_text.strip().lower()


@app.route("/ai_navi", methods=["POST"])
def ai_navi():
    user_input = request.form.get("keyword", "")

    target = get_target_page(user_input)

    routes = {
        "home": "/",
        "profile": "/profile",
        "works": "/works",
        "about": "/profile/about",
        "education": "/profile/education",
        "career": "/profile/career",
        "skills": "/profile/skills",
        "status": "/profile/status",
        "python": "/works/python",
        "php": "/works/php",
        "javascript": "/works/javascript",
    }

    return redirect(routes.get(target, "/"))


# -------------------- AIによる印象 --------------------
@app.route("/ai_feedback", methods=["POST"])
def ai_feedback():
    user_profile = """
    大城将吾。
    未経験からエンジニアを目指し、Python・Flask・PHP・JavaScriptを学習中。
    ChatGPT APIを活用したアプリ開発に取り組んでいる。
    ポートフォリオとして複数のWebアプリを制作中。
    完成度を上げながら、学習したことを形にしている段階。
    """

    prompt = f"""
以下の人物について、このサイトを見たAIとして印象をコメントしてください。

【条件】
・褒めすぎない
・少し親しみやすく、軽いユーモアを入れる
・企業の採用担当者が見ても違和感がない表現
・未完成な部分も「伸びしろ」として自然に触れる
・120文字前後
・辛辣すぎる表現は避ける

【人物情報】
{user_profile}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    result = response.output_text.strip()

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)