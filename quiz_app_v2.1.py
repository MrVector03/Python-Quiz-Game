"""
Quiz Game v2.1

I've started implementing the login/logout feature into the app.
There are a few minor bugs that need to be fixed but overall this feature works
well, with a lot less code and struggle while using the app than before. In this feature,
the user has an option to log in and stay logged in and use the app on his behalf
as much as he wants until he decides to log out. Therefore he doesn't need to log in again to
create quiz or quiz questions or anything like that. After he is finished using the program,
another user can come in, log into his account and use the program until he logs out.
"""

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="quiz_app"
)

cursor = db.cursor()


def create_account():  # creates account and puts it into the database
    #  checks if there is an another account using the username inputted by user
    while True:
        username = input("\nUsername: ")
        cursor.execute("SELECT username FROM Accounts WHERE username = %s", (username, ))
        u_n_l = [i for i in cursor]
        if u_n_l:
            if u_n_l[0][0] == username:
                print("\nThat username already exists, please try another one.")
                pass
            else:
                print("\nUsername available!")
                break
        else:
            print("\nUsername available!")
            break

    while True:
        password = input("\nPassword: ")
        conf_password = input("Confirm password: ")
        if password == conf_password:
            print("\nPassword created")
            break
        else:
            pass

    cursor.execute("INSERT INTO Accounts (username, password, rightAns, wrongAns, accuracy, cpl_q, score, is_logged) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, password, 0, 0, 0.0, 0, 0, 0))
    db.commit()

    print("\nAccount created successfully!")
    print("\nYour account information: ")
    cursor.execute("SELECT * FROM Accounts WHERE username = %s AND password = %s", (username, password))
    list_of_accounts = [i for i in cursor]
    account = list_of_accounts[len(list_of_accounts) - 1]
    print("\nAccount ID: " + str(account[0]) + "\nUsername: " + account[1])
    print("Password: " + account[2])


def display_account():
    username = input("Username: ")
    cursor.execute("SELECT * FROM Accounts WHERE username = %s", (username, ))
    for account in cursor:
        print(account)


def create_quiz():
    cursor.execute("SELECT * FROM Accounts WHERE is_logged = 1")
    for info in cursor:
        print("Logged in as:", info[1], "(ID:", str(info[0]) + ")")

    quiz_name = input("\nQuiz name: ")
    num_of_qs = int(input("Number of questions (Only 5 questions available for now, click 5): "))
    cursor.execute("INSERT INTO Quiz (created_by, created_id, q_name, num_quest, rating, t_comp, has_questions, has_answers) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (temporary_list[0][1], temporary_list[0][0], quiz_name, num_of_qs, 0.0, 0, 0, 0))
    db.commit()
    cursor.execute("SELECT * FROM Quiz WHERE q_name = %s AND created_by = %s", (quiz_name, temporary_list[0][1]))
    temp_list_quiz = [i for i in cursor]
    print("\nQuiz successfully created.")
    print("\nQuiz info:")
    print("\nQuiz name: " + temp_list_quiz[0][3] + "\nQuiz ID:" + temp_list_quiz[0][0] + "\nCreated by: " + temp_list_quiz[0][1] + "\nCreator ID: " + str(temp_list_quiz[0][2]))
    print("Number of questions: " + str(temp_list_quiz[0][4]))


def display_quiz_developer_tool():
    counter = 0
    cursor.execute("SELECT * FROM Quiz")
    for quiz in cursor:
        counter += 1
        print(counter, quiz)


def quiz_display():
    cursor.execute("SELECT * FROM Accounts WHERE is_logged = 1")
    ph_name = ""
    for info in cursor:
        print("Logged in as:", info[1], "(ID:", str(info[0]) + ")")
        ph_name = info[1]

    cursor.execute("SELECT * FROM Quiz WHERE created_by = %s", (ph_name, ))
    quiz_list = [i for i in cursor]
    print(quiz_list)
    q_count = 1
    for i in quiz_list:
        print('\n' + str(q_count) + '.')
        print("\nQuiz name:", i[3])
        print("Quiz ID:", i[0])
        print("Created by:", i[1])
        print("Creator ID:", i[2])
        print("Number of questions:", i[4])
        print("Rating: " + str(i[5]) + "/10")
        print("Times completed:", i[6])
        if i[7] == 1:
            print("\nQuestions: Yes")
        elif i[7] == 0:
            print("\nQuestions: No")
        if i[8] == 1:
            print("Answers: Yes")
        elif i[8] == 0:
            print("Answers: No")
        q_count += 1


def create_questions():
    cursor.execute("SELECT * FROM Accounts WHERE is_logged = 1")
    for info in cursor:
        print("Logged in as:", info[1], "(ID:", str(info[0]) + ")")

    quiz_name_check = input("Input the quiz name: ")
    cursor.execute("SELECT q_ID, created_by, created_id, q_name, num_quest, has_questions, has_answers FROM Quiz WHERE q_name = %s", (quiz_name_check, ))
    quiz_list = [i for i in cursor]
    if len(quiz_list) > 1:
        print("\nIt appears there are more quizzes with that name,")
        print("Please specify the quiz ID number.")

        #  User inputs ID number of the quiz to find his quiz from the database when there are two similar Quiz Names
        while True:
            quiz_id_temp = int(input("\nQuiz ID: "))
            for quiz in quiz_list:
                if quiz_id_temp == quiz[0]:
                    for i in quiz_list:
                        if i[0] != quiz_id_temp:
                            quiz_list.remove(i)

            if len(quiz_list) == 1:
                print("\nQuiz ID found!")
                break
            else:
                print("\nThere are no quizzes with that ID number, try another one.")
                print("If the Quiz ID is forgotten check the number with command 'display quiz'.")

    if quiz_list[0][5] == 1:
        print("This quiz already has questions")
    elif quiz_list[0][5] == 0:
        q1 = input("\nQuestion 1: ")
        q2 = input("Question 2: ")
        q3 = input("Question 3: ")
        q4 = input("Question 4: ")
        q5 = input("Question 5: ")
        cursor.execute("INSERT INTO Questions (quiz_link, q1, q2, q3, q4, q5) VALUES (%s, %s, %s, %s, %s, %s)", (int(quiz_list[0][0]), q1, q2, q3, q4, q5))
        db.commit()
        print("\nQuestions created")
        cursor.execute("UPDATE Quiz SET has_questions = 1 WHERE has_questions = %", (quiz_list[0][0],))
        db.commit()
        print("\ncommit successful...")
        print("\nhas_questions successfully changed from 0 to 1")


def display_questions():
    cursor.execute("SELECT * FROM Questions")
    for i in cursor:
        print(i)


def create_answers():
    cursor.execute("SELECT * FROM Accounts WHERE is_logged = 1")
    for info in cursor:
        print("Logged in as:", info[1], "(ID:", str(info[0]) + ")")

    quiz_name_check = input("Input the quiz name: ")
    cursor.execute("SELECT q_ID, created_by, created_id, q_name, num_quest, has_questions, has_answers FROM Quiz WHERE q_name = %s", (quiz_name_check,))
    quiz_list = [i for i in cursor]
    print(quiz_list)
    if len(quiz_list) > 1:
        print("\nIt appears there are more quizzes with that name,")
        print("Please specify the quiz ID number.")

        #  User inputs ID number of the quiz to find his quiz from the database when there are two similar Quiz Names
        while True:
            quiz_id_temp = int(input("\nQuiz ID: "))
            for quiz in quiz_list:
                if quiz_id_temp == quiz[0]:
                    for i in quiz_list:
                        if i[0] != quiz_id_temp:
                            quiz_list.remove(i)

            if len(quiz_list) == 1:
                print("\nQuiz ID found!")
                break
            else:
                print("\nThere are no quizzes with that ID number, try another one.")
                print("If the Quiz ID is forgotten check the number with command 'display quiz'.")

    print(quiz_list)
    cursor.execute("SELECT * FROM Questions WHERE quiz_link = %s", (quiz_list[0][0],))
    questions_list = [i for i in cursor]
    if quiz_list[0][6] == 1:
        print("This quiz already has answers")

    elif quiz_list[0][6] == 0:
        answers = []
        print("Type in 4 options for the answers with one of them being the right answer")
        #  for loop for shorter way to input answers automatically
        for i in range(5):
            print(str(i + 1) + '. ' + questions_list[0][i + 2])
            while True:
                a_one = input("First option: ")
                a_two = input("Second option: ")
                a_three = input("Third option: ")
                a_four = input("Fourth option: ")
                a_right = input("What's the right answer")
                if a_right == a_one or a_right == a_two or a_right == a_three or a_right == a_four:
                    answers.append(a_one + ',' + a_two + ',' + a_three + ',' + a_four + '|' + a_right)
                    break
                else:
                    print("There are no options matching with the right answer, please try again.")

        a1 = answers[0]
        a2 = answers[1]
        a3 = answers[2]
        a4 = answers[3]
        a5 = answers[4]
        cursor.execute("INSERT INTO Answers (questions_link, a1, a2, a3, a4, a5) VALUES (%s, %s, %s, %s, %s, %s)", (quiz_list[0][0], a1, a2, a3, a4, a5))
        db.commit()
        print("\nAnswers created")
        cursor.execute("UPDATE Quiz SET has_answers = 1 WHERE q_ID = %s", (quiz_list[0][0], ))
        db.commit()
        print("commit successful...")
        print("has_questions successfully changed from 0 to 1")
        cursor.execute("SELECT has_questions, has_answers FROM Quiz WHERE q_ID = %s", (quiz_list[0][0], ))
        list_has = [i for i in cursor]
        if list_has[0] and list_has[1]:
            print("Quiz fully created.")


def main_quiz():
    cursor.execute("SELECT * FROM Accounts WHERE is_logged = 1")
    for info in cursor:
        print("Logged in as:", info[1], "(ID:", str(info[0]) + ")")

    cursor.execute("SELECT * FROM Quiz")
    mq_quizzes = [i for i in cursor]
    chosen_one = []
    mq_quiz_library = {}
    print("\nAvailable quizzes:")
    for instance in range(len(mq_quizzes)):
        mq_quiz_library[mq_quizzes[instance][0]] = mq_quizzes[instance][3]
        print(str(mq_quizzes[instance][0]) + ". " + mq_quizzes[instance][3] + " [ID: " + str(mq_quizzes[instance][0]) + "] by " + mq_quizzes[instance][1])
    mq_quiz_choice = input("\nSelect an ID of the quiz you would like to do: ")
    if int(mq_quiz_choice) in mq_quiz_library:
        for i in range(len(mq_quizzes)):
            if int(mq_quiz_choice) == mq_quizzes[i][0]:
                chosen_one.append(mq_quizzes[i])
                print("Quiz found: " + mq_quizzes[i][3])
            else:
                cursor.execute("SELECT * FROM Quiz WHERE q_id = %s", (mq_quiz_choice,))
                abandoned_quiz = [i for i in cursor]
                if abandoned_quiz[0][7] == 0 or abandoned_quiz[0][8] == 0:
                    print("This quiz does not contain questions or answers, \nplease choose different quiz")
                    if abandoned_quiz[0][1] == username_login:
                        print("\nTo play this quiz, add questions or answers to it.")

    cursor.execute("SELECT * FROM Questions WHERE quiz_link = %s", (chosen_one[0][0], ))
    mq_questions = [i for i in cursor]
    cursor.execute("SELECT * FROM Answers WHERE questions_link = %s", (chosen_one[0][0], ))
    mq_answers = [i for i in cursor]
    total_score = 0
    right_answers = 0
    wrong_answers = 0
    print("Use capital letters in order to choose your answer")
    for i in range(5):
        scoring = 100
        while True:
            print(mq_questions[0][i + 2])
            answers = []
            ans = ""
            for j in mq_answers[0][i + 2]:
                if j != "," and j != "|":
                    ans += j
                elif j == ",":
                    answers.append(ans)
                    ans = ""
                elif j == "|":
                    answers.append(ans)
                    ans = ""
            answers.append(ans)
            print("A. " + answers[0] + "\nB. " + answers[1] + "\nC. " + answers[2] + "\nD. " + answers[3])
            answering_format = {}

            for k in range(4):
                letters = ["A", "B", "C", "D"]
                answering_format[letters[k]] = answers[k]
            while True:
                user_answer = input("Your answer: ")
                if answering_format[user_answer.upper()] == answers[4]:
                    total_score += scoring
                    right_answers += 1
                    print("\nCorrect!")
                    break
                else:
                    if scoring != 0:
                        scoring -= 20
                        wrong_answers += 1
                        print("\nIncorrect, try again.")
                    elif scoring == 0:
                        wrong_answers += 1
                        print("\nIncorrect, try again.")
            break

    print("\nQuiz completed!")
    print("Your final score: " + str(total_score))
    print("Congratulations")
    r_q = input("Would you like to rate the quiz? \n(yes/no): ")
    rate = 0.0
    if r_q == "yes":
        print("Rate the quiz from 1 to 10")
        while True:
            rate = input("\n>> ")
            if 1 <= float(rate) <= 10:
                print("\nThank you!")
                break
            else:
                print("Invalid input, try again")
    #  updating stats of the tables in database
    cursor.execute("SELECT score, rightAns, wrongAns, cpl_q FROM Accounts WHERE ID = %s", (id_for_account, ))

    score_for_acc = [i for i in cursor]
    cursor.execute("SELECT * FROM Quiz where q_ID = %s", (chosen_one[0][0], ))
    quiz = [i for i in cursor]
    mq_accuracy = 100 - ((score_for_acc[0][2] + wrong_answers) * 100 / (score_for_acc[0][1] + right_answers))

    cursor.execute("UPDATE Accounts SET score = %s WHERE ID = %s", (score_for_acc[0][0] + total_score, id_for_account, ))
    db.commit()
    cursor.execute("UPDATE Accounts SET rightAns = %s WHERE ID = %s", (score_for_acc[0][1] + right_answers, id_for_account, ))
    db.commit()
    cursor.execute("UPDATE Accounts SET wrongAns = %s WHERE ID = %s", (score_for_acc[0][2] + wrong_answers, id_for_account, ))
    db.commit()
    cursor.execute("UPDATE Accounts SET cpl_q = %s WHERE ID = %s", (score_for_acc[0][3] + 1, id_for_account, ))
    db.commit()
    cursor.execute("UPDATE Accounts SET accuracy = %s WHERE ID = %s", (mq_accuracy, id_for_account,))
    db.commit()
    if quiz[0][5] == 0:
        cursor.execute("UPDATE Quiz SET rating = %s WHERE q_ID = %s", (rate, chosen_one[0][0]))
        db.commit()
    elif quiz[0][5] > 0:
        rate = (float(rate) + float(quiz[0][5])) / 2
        cursor.execute("UPDATE Quiz SET rating = %s WHERE q_ID = %s", (rate, chosen_one[0][0]))
        db.commit()
    cursor.execute("UPDATE Quiz SET t_comp = %s WHERE q_ID = %s", (quiz[0][6] + 1, chosen_one[0][0]))
    db.commit()
    print("\nAccount stats updated.")
    print("\nProcess finished!")
    cursor.execute("SELECT * FROM Accounts WHERE username = %s", ("Viktor Milojevic", ))
    for i in cursor:
        print(i)


while True:
    print("1. Login\n2. Exit\n")
    q = input("Query >>> ")
    temp_id = 0
    if str(q).lower() == 'login':
        while True:
            username_login = input("\nUsername: ")
            cursor.execute("SELECT ID, username, password FROM Accounts WHERE username = %s", (username_login,))
            temporary_list = [i for i in cursor]
            id_for_account = temporary_list[0][0]
            temp_id = id_for_account
            if username_login == temporary_list[0][1]:
                break
            else:
                print("There was an error finding your account, please try again.")
                print("If you don't have one, create an account.")
        while True:
            password_login = input("Password: ")
            if password_login == temporary_list[0][2]:
                print("\nSuccessfully logged in!")
                break
            else:
                print("\nIncorrect password,\nplease try again.")
                pass
        cursor.execute("UPDATE Accounts SET is_logged = 1 WHERE is_logged = 0 AND ID = %s", (temp_id,))
        db.commit()
        cursor.execute("SELECT * FROM Accounts")
        for i in cursor:
            print(i)
        print("Logged account ID =", id_for_account)
        while True:
            print("\nOptions:")
            print("\n- Create account ('create account')")
            print("- Play a quiz ('play')")
            print("- Create a quiz ('create quiz')")
            print("- Create questions ('create questions')")
            print("- Create answers ('create answers')")
            print("- Logout ('logout')")
            print("\n- Display account ('display account')")
            print("- Display quiz ('display quiz')")
            print("- Display questions ('display questions')")
            print("- Exit the program ('quit', 'exit')")
            query = input("\nQuery >> ")
            if query == "create_account" or query == "create account":
                create_account()
            elif query == "display_account" or query == "display account":
                display_account()
            elif query == "create_quiz" or query == "create quiz":
                create_quiz()
            elif query == "display_quiz" or query == "display quiz":
                quiz_display()
            elif query == "create_questions" or query == "create questions":
                create_questions()
            elif query == "display_questions" or query == "display questions":
                display_questions()
            elif query == "create_answers" or query == "create answers":
                create_answers()
            elif query == "play":
                main_quiz()
            elif query == "logout":
                cursor.execute("UPDATE Accounts SET is_logged = 0 WHERE is_logged = 1 AND ID = %s", (temp_id,))
                db.commit()
                cursor.execute("SELECT * FROM Accounts")
                for i in cursor:
                    print(i)
                print("Successfully logged out")
                break
    elif str(q) == "quit" or str(q) == "exit":
        print("\nThank you for playing!")
        break
