import requests
from bs4 import BeautifulSoup

#THIS IS AN EXTREMELY SLOW PROCESS OF GETTING THE WORDS (~4 MINUTES)
#RUN TO GET A NEW wordslist.txt IF IT HAS BROKEN
#REQUIRES INTERNET

#==========BASIC WORD GETTING CODE==================
def get_words(link):
    site = requests.get(link)#website domain data
    everything = BeautifulSoup(site.content, 'html.parser')#ALL the stuff from the website
    bitmorespecific = everything.find('div', class_ = 'browse-words')#stuff ignoring the buttons n stuff up top
    words = bitmorespecific.find_all('a', class_ = 'pb-4 pr-4 d-block')#the words + formating html in a list

    wordslist = []

    for i in words:
        word = clean_word(i)
        if word != False:#if word is valid
            wordslist.append(clean_word(i))#add word to list of words

    return wordslist

def clean_word(w):
    word = str(w)
    #removing parts that are not the word
    word = word.replace('<a class="pb-4 pr-4 d-block" href="/thesaurus/','')
    word = word.replace('"><span>','')
    word = word.replace('</span></a>','')

    #do this as the thing has 2 words per line
    word = word[int(len(word)/2):]

    word = check_word(word)#validation check
    return word

def check_word(w):
    w = w.upper()

    if len(w) != 5:#check if word is 5 letters for wordle
        return False

    for i in w:
        if ord(i) < 65 or ord(i) > 90:#if there are letters that are not capital regular alphabet letters, fail validation
            return False
    return w
#===================================================

#==========MULTIPLE PAGES OF WORDS==================
def get_page_nums(link):
    site = requests.get(link)#website domain data
    everything = BeautifulSoup(site.content, 'html.parser')#ALL the stuff from the website
    num = everything.find('li', class_ = 'last')#counter data

    #cleaning data (not big enough to have its own function)
    num = str(num)
    num = num[49:51]#2 digits

    #1 or 2 digit numbers
    try:
        int(num)
    except:
        num = num[:1]
    #if no pages
    try:
        int(num)
    except:
        num = 1

    return int(num)#added as sometimes the imt in the except does not trigger

def initial_words(letter, end):#gets all words of one initial
    wordslist = []
    
    for i in range(end):
        link = f"https://www.merriam-webster.com/browse/thesaurus/{letter}/{i+1}"
        wordslist += get_words(link)

    return wordslist

def all_words():
    wordslist = []
    
    for i in range(97,123):#all the letters of the alphabet in ord() [97 to 123]
        letter = chr(i)
        pages = get_page_nums(f"https://www.merriam-webster.com/browse/thesaurus/{letter}/1")

        wordslist += initial_words(letter, pages)

    return wordslist
#===================================================

#==========ADD WORDS TO TEXT FILE===================
def add_to_txtfile(what):
    w = ''
    for i in what:
        w += str(i) + '\n'#1 word every line

    with open('wordslist.txt','w') as file:#create a new textfile called wordslist or replace the old one
        file.write(w)

def generate():
    add_to_txtfile(all_words())
