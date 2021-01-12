
class Account:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.comp_quiz = 0
        self.score = 0
        self.accuracy = 0
        self.right_ans = 0
        self.false_ans = 0
        self.tries = 0

    def display(self):
        print("Name:", self.name)
        print("Surname:", self.surname)
        print("Total score:", self.score, "points")
        print("Completed quizzes:", self.comp_quiz)
        print("Accuracy:", str(100 * (self.right_ans / self.tries)) + "%")

    def add_score(self, score):
        self.score += score
        return score

    def right_answer(self):
        self.right_ans += 1

    def tried(self):
        self.tries += 1

    def wrong_answer(self):
        self.false_ans += 1

    def completed_quiz(self):
        self.comp_quiz += 1


questions = [3, ["Which year is it?", "2020", "2019", "2022", "2021", "4"], ["Which programming language is used to create this program?", "Java", "Python", "C", "C++", "2"], ["Who is the CEO of Apple", "Tim Cook", "Steve Jobs", "Bill Gates", "Larry Page", "1"]]


def quiz():
    username = Account(input("name: "), input("surname: "))
    for i in range(questions[0]):
        score_adder = 5

        print(questions[i + 1][0])
        print("1.", questions[i + 1][1])
        print("2.", questions[i + 1][2])
        print("3.", questions[i + 1][3])
        print("4.", questions[i + 1][4])

        while True:
            answer = input("Your answer: ")
            if answer == questions[i + 1][5]:
                username.right_answer()
                username.add_score(score_adder)
                username.tried()
                print("Correct")
                break

            else:
                username.wrong_answer()
                if score_adder <= 0:
                    score_adder = 0
                else:
                    score_adder -= 1
                username.tried()
                print("Wrong answer")

    username.completed_quiz()
    print("\nGood Job!")
    username.display()


quiz()
