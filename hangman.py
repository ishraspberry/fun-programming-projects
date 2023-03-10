import os
import string
import getpass

#this could be made a lost faster using dictionaries to point out values and indexes, but this is a good start!

ogWord = []
progressWord = []

def letterInput():
    global ogWord
    global progressWord
    
    word = str(getpass.getpass("please enter the word you would like for the other player to guess: ")).lower()
    #getpass.getpass encrypts any word you enter, so that the other player is unable to view your input
    if(len(word.split())!=1 or not word.isalpha()):
        print("invalid word, please ensure your word is ONE WORD")
        letterInput()
    else:
        print("thank you for your selection! Lets play!"+"\n")
        ogWord = list(word)
        progressWord = ["_" for x in ogWord]
        
def guessingTime():
    lives = 5
    lettersGuessed = set(string.ascii_lowercase)
    global progressWord
    global ogWord
    while(lives > 0):
        print(' '.join(progressWord))
        
        if progressWord == ogWord:
            print("congrats! you won <3 now go and gloat girl")
            break
        
        letterGuessed = str(input("\n"+"guess a letter <3: ")).lower()
        if(len(letterGuessed)!= 1 or not letterGuessed.isalpha()):
            print("please enter one letter")
            continue
        
        if letterGuessed not in lettersGuessed:
            print("You already guessed this letter!")
            continue
        
        lettersGuessed.remove(letterGuessed)
        
        countIfExist = ogWord.count(letterGuessed)
        
        if countIfExist == 0:
            lives -= 1
            print("WRONG LOL! You have ", lives, " lives left!")
            if lives == 0:
                print("You're all outta lives and luck~ try again next time")
            continue
    
        index = 0
        for x in ogWord:
            if letterGuessed == x:
                progressWord[index] = letterGuessed
            index += 1
        
def main():
    letterInput()
    guessingTime()

if __name__ == '__main__':
    main()