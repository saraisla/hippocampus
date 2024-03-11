import requests
import json
import random
import html

def get_trivia_question():
    while True:
        url = "https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=multiple"
        response = requests.get(url)
        data = json.loads(response.text)
        if 'results' in data and data['results'] and 'question' in data['results'][0] and 'correct_answer' in data['results'][0] and 'incorrect_answers' in data['results'][0]:
            question = data['results'][0]['question']
            correct_answer = data['results'][0]['correct_answer']
            incorrect_answers = data['results'][0]['incorrect_answers']
            options = incorrect_answers + [correct_answer]
            random.shuffle(options)  # Tilfeldig ordning av svaralternativene
            return question, options, correct_answer
        else:
            print("Ingen spørsmål tilgjengelig. Prøver igjen...")

def present_question(question, options):
    decoded_question = html.unescape(question)
    decoded_options = [html.unescape(option) for option in options]
    print("Spørsmål: " + decoded_question)
    for i, option in enumerate(decoded_options):
        print(f"{i+1}. {option}")

def validate_answer(selected_option, correct_answer):
    if selected_option == correct_answer:
        print("Du fikk riktig svar!")
        return True
    else:
        print("Svaret er dessverre feil... Det riktige svaret er:", correct_answer)
        return False

def play_quiz():
    score = 0
    question_count = 0
    previous_questions = []  # Liste for å lagre indeksene til tidligere spørsmål
    while question_count < 10:
        question, options, correct_answer = get_trivia_question()
        while question in previous_questions:  # Sjekk om spørsmålet allerede har blitt stilt
            question, options, correct_answer = get_trivia_question()
        previous_questions.append(question)  # Legg til indeksen til det nye spørsmålet
        present_question(question, options)
        selected_option = int(input("Velg riktig svaralternativ (1-4): "))
        selected_answer = options[selected_option - 1]
        if validate_answer(selected_answer, correct_answer):
            score += 1
        question_count += 1
    print("Resultatet ditt på dette spillet ble", score)

play_quiz()