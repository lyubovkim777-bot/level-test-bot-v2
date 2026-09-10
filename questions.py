"""
Данные теста: Straightforward Quick Placement & Diagnostic Test (Ruth Goodman, Macmillan).
50 вопросов: 1-40 грамматика, 41-50 лексика. Один правильный ответ на вопрос.

У каждого вопроса, помимо 4 вариантов a-d, бот дополнительно показывает кнопку
«Я не знаю» (callback_data оканчивается на ":idk"). Она не засчитывается как
правильный ответ (и не может им быть), но не даёт ученику гадать наугад —
он либо знает ответ, либо честно признаётся, что не знает.
"""

LEVEL_BANDS = [
    (0, 15, "Beginner", "Начальный"),
    (16, 24, "Elementary", "Элементарный"),
    (25, 32, "Pre-Intermediate", "Ниже среднего"),
    (33, 39, "Intermediate", "Средний"),
    (40, 45, "Upper Intermediate", "Выше среднего"),
    (46, 50, "Advanced", "Продвинутый"),
]


def get_level(score: int) -> tuple[str, str]:
    """Возвращает (уровень на английском, уровень на русском) по числу баллов."""
    for lo, hi, en, ru in LEVEL_BANDS:
        if lo <= score <= hi:
            return en, ru
    return LEVEL_BANDS[-1][2], LEVEL_BANDS[-1][3]


QUESTIONS = [
    {
        "id": 1,
        "question": "I ________________ from France.",
        "options": {
            "a": "is",
            "b": "are",
            "c": "am",
            "d": "be"
        },
        "answer": "c"
    },
    {
        "id": 2,
        "question": "This is my friend. _____________ name is Peter.",
        "options": {
            "a": "Her",
            "b": "Our",
            "c": "Yours",
            "d": "His"
        },
        "answer": "d"
    },
    {
        "id": 3,
        "question": "Mike is ______________.",
        "options": {
            "a": "my sister’s friend",
            "b": "friend my sister",
            "c": "friend from my sister",
            "d": "my sister friend’s"
        },
        "answer": "a"
    },
    {
        "id": 4,
        "question": "My brother is ______________ artist.",
        "options": {
            "a": "the",
            "b": "an",
            "c": "a",
            "d": "— (no article / nothing)"
        },
        "answer": "b"
    },
    {
        "id": 5,
        "question": "_______________ 20 desks in the classroom.",
        "options": {
            "a": "This is",
            "b": "There is",
            "c": "They are",
            "d": "There are"
        },
        "answer": "d"
    },
    {
        "id": 6,
        "question": "Paul ________________ romantic films.",
        "options": {
            "a": "likes not",
            "b": "don’t like",
            "c": "doesn’t like",
            "d": "isn’t likes"
        },
        "answer": "c"
    },
    {
        "id": 7,
        "question": "Sorry, I can’t talk. I _____________ right now.",
        "options": {
            "a": "driving",
            "b": "‘m driving",
            "c": "drives",
            "d": "drive"
        },
        "answer": "b"
    },
    {
        "id": 8,
        "question": "She _________________ at school last week.",
        "options": {
            "a": "didn't be",
            "b": "weren’t",
            "c": "wasn’t",
            "d": "isn’t"
        },
        "answer": "c"
    },
    {
        "id": 9,
        "question": "I _________________ the film last night.",
        "options": {
            "a": "like",
            "b": "likes",
            "c": "liking",
            "d": "liked"
        },
        "answer": "d"
    },
    {
        "id": 10,
        "question": "__________________ a piece of cake? No, thank you.",
        "options": {
            "a": "Do you like",
            "b": "Would you like",
            "c": "Want you",
            "d": "Are you like"
        },
        "answer": "b"
    },
    {
        "id": 11,
        "question": "The living room is ___________________ than the bedroom.",
        "options": {
            "a": "more big",
            "b": "more bigger",
            "c": "biggest",
            "d": "bigger"
        },
        "answer": "d"
    },
    {
        "id": 12,
        "question": "The car is very old. We’re going ____________________ a new car soon.",
        "options": {
            "a": "to buy",
            "b": "buying",
            "c": "to will buy",
            "d": "buy"
        },
        "answer": "a"
    },
    {
        "id": 13,
        "question": "Jane is a vegetarian. She ____________________ meat.",
        "options": {
            "a": "sometimes eats",
            "b": "never eats",
            "c": "often eats",
            "d": "usually eats"
        },
        "answer": "b"
    },
    {
        "id": 14,
        "question": "There aren’t ________________ buses late in the evening.",
        "options": {
            "a": "some",
            "b": "any",
            "c": "no",
            "d": "a"
        },
        "answer": "b"
    },
    {
        "id": 15,
        "question": "The car park is _________________ to the restaurant.",
        "options": {
            "a": "next",
            "b": "opposite",
            "c": "behind",
            "d": "in front"
        },
        "answer": "a"
    },
    {
        "id": 16,
        "question": "Sue ________________ shopping every day.",
        "options": {
            "a": "is going",
            "b": "go",
            "c": "going",
            "d": "goes"
        },
        "answer": "d"
    },
    {
        "id": 17,
        "question": "They _________________ in the park when it started to rain heavily.",
        "options": {
            "a": "walked",
            "b": "were walking",
            "c": "were walk",
            "d": "are walking"
        },
        "answer": "b"
    },
    {
        "id": 18,
        "question": "________________ seen fireworks before?",
        "options": {
            "a": "Did you ever",
            "b": "Are you ever",
            "c": "Have you ever",
            "d": "Do you ever"
        },
        "answer": "c"
    },
    {
        "id": 19,
        "question": "We’ve been friends ____________________ many years.",
        "options": {
            "a": "since",
            "b": "from",
            "c": "during",
            "d": "for"
        },
        "answer": "d"
    },
    {
        "id": 20,
        "question": "You _________________ pay for the tickets. They’re free.",
        "options": {
            "a": "have to",
            "b": "don’t have",
            "c": "don’t need to",
            "d": "doesn’t have to"
        },
        "answer": "c"
    },
    {
        "id": 21,
        "question": "Jeff was ill last week and he _________________ go out.",
        "options": {
            "a": "needn't",
            "b": "can’t",
            "c": "mustn’t",
            "d": "couldn’t"
        },
        "answer": "d"
    },
    {
        "id": 22,
        "question": "These are the photos ________________ I took on holiday.",
        "options": {
            "a": "which",
            "b": "who",
            "c": "what",
            "d": "where"
        },
        "answer": "a"
    },
    {
        "id": 23,
        "question": "We’ll stay at home if it _______________ this afternoon.",
        "options": {
            "a": "raining",
            "b": "rains",
            "c": "will rain",
            "d": "rain"
        },
        "answer": "b"
    },
    {
        "id": 24,
        "question": "He doesn’t smoke now, but he __________________ a lot when he was young.",
        "options": {
            "a": "has smoked",
            "b": "smokes",
            "c": "used to smoke",
            "d": "was smoked"
        },
        "answer": "c"
    },
    {
        "id": 25,
        "question": "Mark plays football ___________________ anyone else I know.",
        "options": {
            "a": "more good than",
            "b": "as better as",
            "c": "best than",
            "d": "better than"
        },
        "answer": "d"
    },
    {
        "id": 26,
        "question": "I promise I __________________ you as soon as I’ve finished this cleaning.",
        "options": {
            "a": "will help",
            "b": "am helping",
            "c": "going to help",
            "d": "have helped"
        },
        "answer": "a"
    },
    {
        "id": 27,
        "question": "This town ___________________ by lots of tourists during the summer.",
        "options": {
            "a": "visits",
            "b": "visited",
            "c": "is visiting",
            "d": "is visited"
        },
        "answer": "d"
    },
    {
        "id": 28,
        "question": "He said that his friends ____________ to speak to him after they lost the football match.",
        "options": {
            "a": "not want",
            "b": "weren’t",
            "c": "didn’t want",
            "d": "aren’t wanting"
        },
        "answer": "c"
    },
    {
        "id": 29,
        "question": "How about _________________ to the cinema tonight?",
        "options": {
            "a": "going",
            "b": "go",
            "c": "to go",
            "d": "for going"
        },
        "answer": "a"
    },
    {
        "id": 30,
        "question": "Excuse me, can you ___________________ me the way to the station, please?",
        "options": {
            "a": "give",
            "b": "take",
            "c": "tell",
            "d": "say"
        },
        "answer": "c"
    },
    {
        "id": 31,
        "question": "I wasn’t interested in the performance very much. ________________.",
        "options": {
            "a": "I didn’t, too.",
            "b": "Neither was I.",
            "c": "Nor I did.",
            "d": "So I wasn’t."
        },
        "answer": "b"
    },
    {
        "id": 32,
        "question": "Take a warm coat, _______________ you might get very cold outside.",
        "options": {
            "a": "otherwise",
            "b": "in case",
            "c": "so that",
            "d": "in order to"
        },
        "answer": "a"
    },
    {
        "id": 33,
        "question": "__________________ this great book and I can’t wait to see how it ends.",
        "options": {
            "a": "I don’t read",
            "b": "I’ve read",
            "c": "I’ve been reading",
            "d": "I read"
        },
        "answer": "c"
    },
    {
        "id": 34,
        "question": "What I like more than anything else ___________________ at weekends.",
        "options": {
            "a": "playing golf",
            "b": "to play golf",
            "c": "is playing golf",
            "d": "is play golf"
        },
        "answer": "c"
    },
    {
        "id": 35,
        "question": "She ________________ for her cat for two days when she finally found it in the garage.",
        "options": {
            "a": "looked",
            "b": "had been looked",
            "c": "had been looking",
            "d": "were looking"
        },
        "answer": "c"
    },
    {
        "id": 36,
        "question": "We won’t catch the plane _________________ we leave home now! Please hurry up!",
        "options": {
            "a": "if",
            "b": "providing that",
            "c": "except",
            "d": "unless"
        },
        "answer": "d"
    },
    {
        "id": 37,
        "question": "If I hadn’t replied to your email, I___________________ here with you now.",
        "options": {
            "a": "can’t be",
            "b": "wouldn’t be",
            "c": "won’t be",
            "d": "haven’t been"
        },
        "answer": "b"
    },
    {
        "id": 38,
        "question": "Do you think you ___________________ with my mobile phone soon? I need to make a call. Upper Intermediate Unit 7",
        "options": {
            "a": "finish",
            "b": "are finishing",
            "c": "will have finished",
            "d": "are finished"
        },
        "answer": "c"
    },
    {
        "id": 39,
        "question": "I don’t remember mentioning __________________ dinner together tonight.",
        "options": {
            "a": "go for",
            "b": "you going to",
            "c": "to go for",
            "d": "going for"
        },
        "answer": "d"
    },
    {
        "id": 40,
        "question": "Was it Captain Cook ______________ New Zealand?",
        "options": {
            "a": "who discovered",
            "b": "discovered",
            "c": "that discover",
            "d": "who was discovering"
        },
        "answer": "a"
    },
    {
        "id": 41,
        "question": "You may not like the cold weather here, but you’ll have to ________________, I’m afraid.",
        "options": {
            "a": "tell it off",
            "b": "sort itself out",
            "c": "put up with it",
            "d": "put it off"
        },
        "answer": "c"
    },
    {
        "id": 42,
        "question": "It’s cold so you should __________________ on a warm jacket.",
        "options": {
            "a": "put",
            "b": "wear",
            "c": "dress",
            "d": "take"
        },
        "answer": "a"
    },
    {
        "id": 43,
        "question": "Paul will look ______________ our dogs while we’re on holiday.",
        "options": {
            "a": "at",
            "b": "for",
            "c": "into",
            "d": "after"
        },
        "answer": "d"
    },
    {
        "id": 44,
        "question": "She ___________________ a lot of her free time reading.",
        "options": {
            "a": "does",
            "b": "spends",
            "c": "has",
            "d": "makes"
        },
        "answer": "b"
    },
    {
        "id": 45,
        "question": "Hello, this is Simon. Could I ___________________ to Jane, please?",
        "options": {
            "a": "say",
            "b": "tell",
            "c": "call",
            "d": "speak"
        },
        "answer": "d"
    },
    {
        "id": 46,
        "question": "They’re coming to our house ___________________ Saturday.",
        "options": {
            "a": "in",
            "b": "at",
            "c": "on",
            "d": "with"
        },
        "answer": "c"
    },
    {
        "id": 47,
        "question": "I think it’s very easy to ___________ debt these days.",
        "options": {
            "a": "go into",
            "b": "become",
            "c": "go down to",
            "d": "get into"
        },
        "answer": "d"
    },
    {
        "id": 48,
        "question": "Come on! Quick! Let’s get _____________!",
        "options": {
            "a": "highlight",
            "b": "cracking",
            "c": "massive",
            "d": "with immediate effect"
        },
        "answer": "b"
    },
    {
        "id": 49,
        "question": "I phoned her ____________ I heard the news.",
        "options": {
            "a": "minute",
            "b": "during",
            "c": "by the time",
            "d": "the moment"
        },
        "answer": "d"
    },
    {
        "id": 50,
        "question": "I feel very ____________. I’m going to go to bed!",
        "options": {
            "a": "nap",
            "b": "asleep",
            "c": "sleepy",
            "d": "sleeper"
        },
        "answer": "c"
    }
]
