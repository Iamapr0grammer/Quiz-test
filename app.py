import random
from flask import Flask, render_template, request, redirect


questionCount = 0
randomMode = True

app = Flask(__name__)

# 0 - question, 1-3 answers, 4 ID of right answer, 5 ID of that question

question1 = ["Which Python libraries are commonly used for implementing artificial intelligence?",
             "numpy and matplotlib", "tensorflow and keras", "flask and django", "requests and beautifulsoup4", 2, 0]

question2 = ["What is the purpose of activation functions in neural networks?", "To initialize weights and biases",
             "To calculate the gradient descent", "To introduce non-linearities into the network",
             "To determine the learning rate", 3, 1]

question3 = ["What does the term (overfitting) refer to in machine learning?", "The model performs well on new, unseen data",
             "The model fails to capture the underlying patterns in the data", "The model learns noise or irrelevant details in the training data",
             "The model is too simple to understand complex patterns", 3, 2]

question4 = ["What is the primary purpose of cross-validation in machine learning?", "To prevent overfitting by penalizing complex models",
             "To evaluate a model's performance on the training data", "To assess how well a model generalizes to new data",
             "To optimize hyperparameters in a model", 3, 3]

question5 = ["In reinforcement learning, what does the term (exploitation) refer to?", "Exploring new actions to improve the agent's policy",
             "Maximizing immediate reward based on the current knowledge", " Balancing exploration and exploitation for optimal decision-making",
             "Adjusting the learning rate to avoid convergence to local optima", 2, 4]

question6 = ["What role does the (learning rate) play in gradient descent optimization algorithms?", "It determines the size of the model's parameters",
             "It sets the number of iterations for convergence", "It adjusts the step size to update model weights during training",
             "It defines the number of layers in a neural network", 3, 5]

question7 = ["What is the purpose of the term (dropout) in neural networks?", "To remove outliers from the dataset before training",
             "To reduce the dimensionality of the input data", "To prevent overfitting by randomly disabling neurons during training",
             " To adjust the learning rate dynamically based on model performance", 3, 6]

allQuestions = []


# add all questions
allQuestions.append(question1)
allQuestions.append(question2)
allQuestions.append(question3)
allQuestions.append(question4)
allQuestions.append(question5)
allQuestions.append(question6)
allQuestions.append(question7)

# print(allQuestions)
#
# answer = input("Submit Your answer: ")

listOfUsernames = ["Name1", "Name2"]
allAccounts = []
AccountID = 0
Myaccount = None
lastQuestionAskedID = None

# def CheckAnswer():
#     print(answer)
#
# CheckAnswer()

@app.route('/page')
def index():
    global questionCount
    template = render_template('quiz.html', question=allQuestions[questionCount])
    if not randomMode:
        if questionCount + 1 == len(allQuestions):
            questionCount = 0
        else:
            questionCount += 1
    else:
        questionCount = random.randint(0, len(allQuestions) - 1)

    return template

@app.route('/page', methods=['POST'])
def HandleSubmit():
    for x in request.form.items():
        print(x)
    return redirect('/page')

@app.route('/signup')
def HandleSignup():
    template = render_template('registration.html')
    return template

@app.route('/register', methods=['POST'])
def HandleRegister():
    username = request.form['username']
    password = request.form['password']
    didCreateAccount = CreateAccount(listOfUsernames, allAccounts, AccountID, username, password)
    if didCreateAccount:
        return render_template('registration.html', successRegistry="Account created!")
    else:
        return render_template('registration.html', failedRegistry="Couldn't create an account.")
    

def CreateAccount(listOfUsernames, allAccounts, AccountID, username, password):
        success = False
        if username in listOfUsernames:
            return success
        else:
            AccountID += 1
            newAccount = [username, password, AccountID, 0]  # Store username, password, AccountID, and score in a list, 0 is a score
            listOfUsernames.append(username)
            allAccounts.append(newAccount)
            success = True
            # print(username)
            # print(newAccount)
            # print(AccountID)
            return success  # Return the updated AccountID

@app.route('/login', methods=['POST'])
def Login():
    global allAccounts
    loginAccount = request.form['username']
    passwordAccount = request.form['password']
    # find that user
    for account in allAccounts:
        if account[0] == loginAccount:
            if account[1] == passwordAccount:
                print("Login succesfull")
                return redirect('/page')
    return render_template('registration.html', failedRegistry="That account doesn't exist.")


def AskQuestion(allQuestions, allAccounts, Myaccount, lastQuestionAskedID):

    questionAskedID = random.randint(0,len(allQuestions) - 1)

    # make sure, that the last question is not the same, as the previous question
    while lastQuestionAskedID == questionAskedID:
        questionAskedID = random.randint(0, len(allQuestions) - 1)

    MyQuestion = allQuestions[questionAskedID]
    lastQuestionAskedID = MyQuestion

    print(MyQuestion[0])
    print("A) ",MyQuestion[1])
    print("B) ",MyQuestion[2])
    print("C) ",MyQuestion[3])
    print("D) ",MyQuestion[4])
    answer = input("Choose Your answer: ")
    answerID = 0
    if answer == "A" or answer == "a":
        answerID = 1
    if answer == "B" or answer == "b":
        answerID = 2
    if answer == "C" or answer == "c":
        answerID = 3
    if answer == "D" or answer == "d":
        answerID = 4
    # print(int(MyQuestion[5]))
    # print(answerID)
    if answerID == int(MyQuestion[5]):
        print("Correct!")

        # increase the score of the player by 25
        for account in allAccounts:
            if account[2] == int(Myaccount): # search for the account of the player
                account[3] += 25 # inscrease the score by 25

                # Print score of the account of the player
                print(account[3])
                return allAccounts, lastQuestionAskedID # update the account and last question asked
    else:
        print("False!")

        #Decrease the score of the player by 25, untill 0
        for account in allAccounts:
            if account[2] == int(Myaccount):  # search for the account of the player
                account[3] -= 25 # descrease the score by 25
                if account[3] < 0: # not below 0
                    account[3] = 0

                # Print score of the account of the player
                print(account[2])
                return allAccounts, lastQuestionAskedID # update the account and last question asked





####################################           CHECKING BELOW          #################################################



app.run(debug=True)


# Checking if everything works fine

# listOfUsernames, allAccounts, AccountID = CreateAccount(listOfUsernames, allAccounts, AccountID) # create new account
# listOfUsernames, allAccounts, AccountID = CreateAccount(listOfUsernames, allAccounts, AccountID) # create new account
# listOfUsernames, allAccounts, AccountID = CreateAccount(listOfUsernames, allAccounts, AccountID) # create new account

# Myaccount = Login(listOfUsernames, allAccounts, AccountID, Myaccount) # Login and remember user ID in (Myaccount)

# allAccounts, lastQuestionAskedID = AskQuestion(allQuestions, allAccounts, Myaccount, lastQuestionAskedID) # Ask question and update score
# allAccounts, lastQuestionAskedID = AskQuestion(allQuestions, allAccounts, Myaccount, lastQuestionAskedID) # Ask question and update score