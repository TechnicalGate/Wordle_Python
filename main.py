import random
import sys

colors = {'c':'\033[32m', 'w':'\033[33m', 'n':'\033[30m', 'end':'\033[m'}#color codes for correct, wrong position, completely wrong, and normal text

def get_words():
    #read wordslist.txt and take words from there
    with open(r'wordslist.txt') as file:
        f = file.readlines()

    return f

def get_word():
    #take words from stored list of words
    #used list instead of reading from textfile as still need to check if input is a word later
    word = random.choice(all_words)
    word = word.replace('\n','')

    #make it a list
    word = list(word)
  
    return word

def input_word():
    word = input('Word: ').upper()
    
    if len(word) != 5:#check word length
        print(f'"{word}" is not 5 letters')
        return input_word()

    for i in word:#check if all are letters:
        if ord(i) < 65 or ord(i) > 90:#ASCII codes of A and Z
            print('Word should only contain letters')
            return input_word()

    if str(word+'\n') not in all_words:#check if real word
        print(f'"{word}" is not in the word list')
        return input_word()

    return list(word)

def check_word(word, correctword):
    right = []
    
    for n,i in enumerate(word):
        if i == correctword[n]:
            right.append('c')
        elif i in correctword:
            right.append('w')
        else:
            right.append('n')

    return word, right

def check_win(memo, correctword):
    #if most recent input is correct, return something
    #else return false
    if memo[-1] == correctword:
        return 'win'
    else:
        return False

def draw(memo):
    for part in memo:
        for e in range(5):#5 as 5 letters per word
            #make color also appear in python IDLE
            if python:
                sys.stdout.shell.write(part[0][e], colors[part[1][e]])
                sys.stdout.shell.write('',colors['end'])
            else:
                print(f'{colors[part[1][e]]} {part[0][e]} {colors["end"]}', end='')
        print('')#new words on new lines

def new_game():
    #setup
    memo = []#memory list that stores other previous words
    correctword = get_word()

    #gameplay
    for _ in range(6):#6 rounds of wordle
        memo.append(check_word(input_word(), correctword))
        draw(memo)
        win = check_win(memo, correctword)
        if win:
            print('YOU WIN!')
            break
    if not win:
        #print correct word
        print('The word was ',end='')
        for i in correctword:
            print(i,end='')
        print('')

#setup
all_words = get_words()
#setup colors so it works on python idle
python = False
if  'idlelib' in sys.modules:
    python = True
    colors = {'c':'STRING','w':'KEYWORD','n':'stdin','end':'DEFINITION'}#redo color codes to make my life easier

#game
while True:
    #play
    new_game()

    #quit
    if input('Press "Q" to quit, press any other key to play again: ').upper() == 'Q':
        break
