"""
Sample Japanese N3 exercises for testing
"""

SAMPLE_EXERCISES = [
    # Reading Comprehension
    {
        "title": "読解：短編小説",
        "exercise_type": "reading",
        "jlpt_level": "N3",
        "prompt": "この物語の主人公の最終的な決断は何ですか？",
        "context": """山田太郎は大企業の営業部長でした。毎日忙しく働いていましたが、ある日、
彼は自分の人生について深く考え始めました。子どもたちとの時間を失っていることに気づき、
会社を辞めて小さなカフェを開くことにしました。最初は大変でしたが、今、彼は毎日笑顔で仕事をしています。""",
        "correct_answers": ["会社を辞めてカフェを開いた", "小さなカフェを開く", "人生を変えた"],
        "explanation": "本文の最後の部分に、山田太郎がカフェを開いたと書いてあります。"
    },
    
    # Grammar
    {
        "title": "文法：接続詞",
        "exercise_type": "grammar",
        "jlpt_level": "N3",
        "prompt": "「雨が降っているので、___。」に最も適切な選択肢は？\nA) 中止になった\nB) 中止になってしまった\nC) 中止になっていた\nD) 中止になっているだろう",
        "context": "",
        "correct_answers": ["A", "中止になった"],
        "explanation": "「ので」（because）の後は、当然の結果が続くので、A) 中止になった が正解です。"
    },
    
    # Vocabulary
    {
        "title": "語彙：同義語",
        "exercise_type": "vocabulary",
        "jlpt_level": "N3",
        "prompt": "「勤務中に私語するのは迷惑です。」の「私語」の最も近い意味は？\nA) 私のことば\nB) 無駄な会話\nC) 秘密の話\nD) 外国語",
        "context": "",
        "correct_answers": ["B", "無駄な会話"],
        "explanation": "「私語」（しご）は、仕事中の不必要な会話を意味します。"
    },
    
    # Kanji Reading
    {
        "title": "漢字：読み方",
        "exercise_type": "kanji",
        "jlpt_level": "N3",
        "prompt": "「最近の天気予報は正確だ。」の「最近」の読み方は？",
        "context": "",
        "correct_answers": ["さいきん", "最近"],
        "explanation": "「最近」は「さいきん」と読みます。"
    },
    
    # Listening comprehension (text based)
    {
        "title": "聴解：会話の意図",
        "exercise_type": "listening",
        "jlpt_level": "N3",
        "prompt": "AさんはBさんに何をさせたいのですか？",
        "context": """A: 「最近、運動していますか？」
B: 「いいえ、忙しくて...」
A: 「そうですか。でも、健康のためには毎日少しは運動したほうがいいですよ。」""",
        "correct_answers": ["運動することを勧めている", "健康のために運動するよう勧めている", "毎日少し運動すること"],
        "explanation": "Aさんは、Bさんが運動することの重要性を説いており、運動することを勧めています。"
    },
    
    # More grammar examples
    {
        "title": "文法：受け身形",
        "exercise_type": "grammar",
        "jlpt_level": "N3",
        "prompt": "「この映画はアメリカで作られ___。」を完成させてください。",
        "context": "",
        "correct_answers": ["た", "ました"],
        "explanation": "受け身形の過去時制は「～られた/～られました」です。"
    },
    
    # Vocabulary
    {
        "title": "語彙：敬語",
        "exercise_type": "vocabulary",
        "jlpt_level": "N3",
        "prompt": "先生に失礼のないように話すには、「食べる」を___に変えるべきです。",
        "context": "",
        "correct_answers": ["召し上がる", "召し上がります"],
        "explanation": "「食べる」の最高敬語は「召し上がる」です。"
    },
]


def load_sample_exercises():
    """Load sample exercises into database"""
    from .models import JapaneseExercise
    
    created_count = 0
    for exercise_data in SAMPLE_EXERCISES:
        exercise, created = JapaneseExercise.objects.get_or_create(
            title=exercise_data['title'],
            defaults=exercise_data
        )
        if created:
            created_count += 1
    
    return created_count
