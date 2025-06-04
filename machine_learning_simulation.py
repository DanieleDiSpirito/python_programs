from random import randint
from danidisp import sprint, sinput

INTRODUCTION = '''Welcome to our Life Satisfaction Questionnaire!
This survey aims to gauge various aspects of your life and well-being, helping you reflect on your overall satisfaction and happiness.
Your honest responses will provide valuable insights into areas where you may feel content or areas that may need improvement.
Please answer each question thoughtfully, using a scale of 1 to 5 to indicate your level of agreement or satisfaction.
Remember, there are no right or wrong answers; this questionnaire is simply a tool to help you gain a deeper understanding of your life and how you perceive it.
Thank you for participating, and let's begin!'''

questions = [
    "How satisfied are you with your overall sense of purpose and meaning in life?",
    "Rate your level of contentment with your physical health and well-being.",
    "How fulfilled do you feel in your personal hobbies and interests?",
    "How financially secure do you feel?",
    "Rate your level of satisfaction with your sense of personal growth and development.",
    "How connected do you feel to your community and surroundings?",
    "How often do you experience moments of gratitude and appreciation?",
]

weights: list[list[float]] = [
    #  1  2  3  4  5  6  7
    [5, 0.2, 3.3, 1, 4, 3.5, 1.7],  # Purpose and Meaning
    [0.2, 5, 4, 3.5, 3, 2.5, 4.5],  # Physical Well-being
    [3.3, 4, 5, 2, 3.5, 3, 4],      # Personal Hobbies
    [1, 3.5, 2, 5, 2.5, 3, 3],      # Financial Security
    [4, 3, 3.5, 2.5, 5, 3.5, 3.8],  # Personal Growth
    [3.5, 2.5, 3, 3, 3.5, 5, 4],    # Community Connection
    [1.7, 4.5, 4, 3, 3.8, 4, 5],    # Gratitude
]

names: list[str] = [
    "Purpose and Meaning",
    "Physical Well-being",
    "Personal Hobbies",
    "Financial Security",
    "Personal Growth",
    "Community Connection",
    "Gratitude",
]

LEN = questions.__len__()
output: list[float] = [0] * LEN


def q_and_a(simulation: bool = False) -> None:
    if simulation:
        for j, q in enumerate(questions):
            ans = randint(1, 5)
            for i in range(LEN):
                output[i] += (ans/2 - 1.25) * weights[i][j]
    else:
        for j, q in enumerate(questions):
            while True:
                try:
                    ans = int(sinput(q + " "))
                    if ans < 1 or ans > 5:
                        sprint("Insert a valid integer value in [1, 5]")
                    else:
                        break
                except ValueError as Error:
                    sprint("Insert a valid integer value in [1, 5]")
            for i in range(LEN):
                output[i] += (ans/2 - 1.25) * weights[i][j]


def result() -> None:
    for name, out in zip(names, output):
        sprint(f'{name}: {out:.2f}', 0.02)


def main() -> None:
    print(INTRODUCTION)
    ans: str = input("Do you want simulation? [Y/n]")
    simulation = ans in ('', 'Y', 'y')
    q_and_a(simulation)
    result()


if __name__ == '__main__':
    main()

