import requests
import random

possible_categories = [11496, 11497, 11498, 11499, 11500, 11501, 11508, 11510, 11520, 11521, 11522, 11523, 11529, 11530, 11531, 11532, 11534, 11535, 11542, 11543, 11544, 11546, 11548, 11549, 11550, 11562, 11570, 11571, 11576, 11578, 11579, 11580, 11581]

categories_for_this_game = random.sample(possible_categories, 6)
#print(categories_for_this_game)

all_questions = []
for x in range(6):
    all_questions.append(requests.get("http://jservice.io/api/clues?category=" + str(categories_for_this_game[x])).json())

# print(all_questions)

category_names = []
for x in range(6):
    if all_questions[x][0]['category']:
        category_names.append(all_questions[x][0]['category']['title'])

score = 0

print("One out of a total of six categories will be chosen for you. In each category, there is a total of five questions that range from 200 to 1000 points. You have the option of selecting a different category but you MUST answer the questions in the order given to you. \n")
play_again = input("Are you ready to play jeopardy?\n")
if play_again == "":
    play_again = "y"

def strip_answer(text):
  text = text.lower()
  return text.replace("a ", "").replace("the ", "")

while play_again[0].lower() == "y":

    user_screen_prompt = "\nChoose a category by number: \n"
    for x in range(6):
        user_screen_prompt = user_screen_prompt + str(x+1) + " -  " + category_names[x] + "      (" + str(len(all_questions[x])) + " questions remain)\n"
    
    category_chosen = input(user_screen_prompt + "\n")
    
    while str(category_chosen) not in [str(1), str(2), str(3), str(4), str(5), str(6)]:
        category_chosen = input("Please choose a valid number from 1 to 6.\n")
    while len(all_questions[int(category_chosen) - 1]) == 0:
        category_chosen = input("You have seen all the questions in this category.  Please choose another category.\n")
    
    question_chosen = all_questions[int(category_chosen) - 1][0]["question"]
    question_chosen_points = all_questions[int(category_chosen) - 1][0]["value"]
    question_chosen_answer = all_questions[int(category_chosen) - 1][0]["answer"]
    
    user_answer = input("For " + str(question_chosen_points) + " points, your question is:\n" + question_chosen + "\n")
    if strip_answer(user_answer) == strip_answer(question_chosen_answer):
        score = score + question_chosen_points
        print("Good job!  Your score is now " + str(score) + " points.")
    else:
        print("Sorry.  The correct answer was " + question_chosen_answer + ".  Your score is still " + str(score) + " points.")
    
    del all_questions[int(category_chosen) - 1][0]

    #check whether the game is over
    questions_left = 0
    for x in range(6):
        questions_left = questions_left + len(all_questions[x])
    if questions_left == 0:
        break
    
    play_again = input("Do you want another question?  ")
    if play_again == "":
        play_again = "y"

print("\nYour final score is " + str(score) + ".  Thank you for playing, and have a nice day!\n")

