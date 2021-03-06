#!/usr/bin/env python3

"""
Author: Haitham Gad
Date: Feb 4, 2014
Description: Hangman game using Python Curses.
"""

import random
import sys
import os
import curses


# Hangman model
class Model():
  def __init__(self, filename):
    self.readWords(filename)
    self.reset()

  def readWords(self, filename):
    # file is assumed to contain one word per line
    with open(filename) as f:
      self.words = f.readlines()

  def validWord(self, word):
    return (len(word) > 2 and word.find('-') == -1)

  def pickWord(self):
    index = random.randint(0, len(self.words) - 1)
    word = self.words[index].rstrip()
    while not self.validWord(word):
      index = random.randint(0, len(self.words) - 1)
      word = self.words[index].rstrip()
    return word.lower()

  def reset(self):
    self.word = self.pickWord()
    self.guessWord = "-" * len(self.word)

  def updateGuessWord(self, c):
    self.guessWord = ''.join(
      [(lambda x, y: x if x == c else y)(a, b) for (a, b) in
               zip(self.word, self.guessWord)])

  def wordHas(self, c):
    return (self.word.find(c) != -1)

  def guessWordHas(self, c):
    return (self.guessWord.find(c) != -1)


# Curses view
class View():
  def __init__(self, scr):
    self.scr    = scr
    self.scr.leaveok(True) # hide the cursor
    self.initColorPairs()
    self.theme1 = curses.color_pair(1)
    self.theme2 = curses.color_pair(2)
    self.theme3 = curses.color_pair(3)
    self.theme4 = curses.color_pair(4)
    self.wrongGuesses = 0
    self.height, self.width = self.scr.getmaxyx()
    self.height = min(self.height, 25)
    self.steps = [self.leftLeg, self.rightLeg, self.body,
                  self.leftArm, self.rightArm, self.head, self.rope]

  def initColorPairs(self):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLUE,  curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_RED,   curses.COLOR_WHITE)

  def rect(self, ch, y1, x1, y2, x2):
    for i in range(y1, y2):
      for j in range(x1, x2):
        self.scr.addch(i, j, ch, self.theme1)

  def gallows(self):
    brick = curses.ACS_CKBOARD
    self.rect(brick, 0, self.width // 2 - 5, 5, self.width)
    self.rect(brick, 5, self.width - 11, self.height - 1, self.width)
    self.rect(brick, self.height - 4, 0, self.height - 1, self.width)

  def leftLimb(self, startY, startX, erase = False):
    ch = ' ' if erase else '/'
    for i in range(2):
      self.scr.addch(startY + i, startX - i, ch, self.theme1)

  def rightLimb(self, startY, startX, erase = False):
    ch = ' ' if erase else '\\'
    for i in range(2):
      self.scr.addch(startY + i, startX + i, ch, self.theme1)

  def leftLeg(self, erase = False):
    self.leftLimb(11, self.width // 2, erase)

  def rightLeg(self, erase = False):
    self.rightLimb(11, self.width // 2 + 2, erase)

  def leftArm(self, erase = False):
    self.leftLimb(9, self.width // 2, erase)

  def rightArm(self, erase = False):
    self.rightLimb(9, self.width // 2 + 2, erase)

  def body(self, erase = False):
    ch = ' ' if erase else curses.ACS_VLINE
    for i in range(2):
      self.scr.addch(9 + i, self.width // 2 + 1, ch, self.theme1)

  def head(self, erase = False):
    ch = ' ' if erase else 'O'
    self.scr.addch(8, self.width // 2 + 1, ch, self.theme1)

  def rope(self, erase = False):
    ch1 = ' ' if erase else curses.ACS_VLINE
    ch2 = ' ' if erase else 'O'

    for i in range(3):
      self.scr.addch(5 + i, self.width // 2 + 1, ch1, self.theme1)

    self.scr.addch(8, self.width // 2 + 1, ' ', self.theme1)
    self.scr.addch(8, self.width // 2, ch2, self.theme1)

  def hideCursor(self):
    # the only way I found to hide the cursor is to set the the last char in
    # the screen to something different, refresh, then reset it back to its
    # old value
    lastY = self.height - 2
    lastX = self.width  - 1
    self.scr.addch(lastY, lastX, ' ', self.theme1)
    self.scr.refresh()
    self.scr.addch(lastY, lastX, curses.ACS_CKBOARD, self.theme1)

  def updateGuessWord(self, word):
    self.scr.addstr(self.height - 8, 2, "Guess Word: " + word, self.theme1)
    self.hideCursor()

  def eraseBody(self):
    self.leftLeg(True)
    self.rightLeg(True)
    self.leftArm(True)
    self.rightArm(True)
    self.body(True)
    self.head(True)
    self.rope(True)

  def message(self, msg, theme = None):
    self.scr.addstr(self.height - 6, 2, msg,
                    theme if theme is not None else self.theme1)
    self.hideCursor()

  def clearMessage(self):
    self.message(" " * 32)
    self.hideCursor()

  def wrongGuess(self):
    if self.wrongGuesses > 6:
      return False

    self.steps[self.wrongGuesses]()
    self.wrongGuesses += 1
    self.hideCursor()

    if self.wrongGuesses == 7:
      return False

    return True

  def reset(self, guessWord):
    self.wrongGuesses = 0
    self.scr.bkgd(' ', self.theme1)
    self.gallows()
    self.updateGuessWord(guessWord + " " * 10)
    self.message(" " * 32)
    self.eraseBody()
    self.hideCursor()

  def getch(self):
    self.scr.refresh()
    c = self.scr.getch()
    while c > 255:
      c = self.scr.getch()
    return chr(c).lower()

  def repeatedChar(self, c):
    self.message("Repeated Character: " + c, self.theme2)

  def youWon(self):
    self.message("You Won :-), Play again? [y/n]", self.theme3)

  def gameOver(self):
    self.message("Game Over :-(, Play again? [y/n]", self.theme4)


# Hangman controller
class Controller():
  def __init__(self, model):
    self.model = model
    self.view = None
    self.usedChars = set()
    self.couldTakeStep = True

  def reset(self):
    self.model.reset()
    self.view.reset(self.model.guessWord)
    self.usedChars.clear()
    self.couldTakeStep = True

  def readAnswer(self):
    c = 'a'
    while True:
      if c == 'y':
        self.reset()
        break
      elif c == 'n':
        raise KeyboardInterrupt
      c = self.view.getch()

  def hangman(self, stdscr):
    self.view = View(stdscr)
    self.reset()

    while True:
      c = self.view.getch()
      self.view.clearMessage()
      if c in self.usedChars:
        self.view.repeatedChar(c)
        continue

      self.usedChars.add(c)
      if not self.model.wordHas(c):
        self.couldTakeStep = self.view.wrongGuess()
        if not self.couldTakeStep:
          self.view.gameOver()
      else:
        self.model.updateGuessWord(c)
        self.view.updateGuessWord(self.model.guessWord)
        if not self.model.guessWordHas("-"):
          self.view.youWon()

      if not (self.couldTakeStep and self.model.guessWordHas("-")):
        self.view.updateGuessWord(self.model.word)
        self.readAnswer()


def main():
  filepath = "/usr/share/dict/words"
  try:
    if not os.path.isfile(filepath):
      filepath = input("Please enter a newline-delimited words file path: ")

    controller = Controller(Model(filepath))
    curses.wrapper(controller.hangman)
  except KeyboardInterrupt:
    print("Good Bye!", file=sys.stdout)
    return 0
  except IOError:
    print("Cannot open file: " + filepath + ". Exiting.", file=sys.stderr)
    return 1


if __name__ == "__main__":
  sys.exit(main())

