from __future__ import unicode_literals

from django.db import models

# Create your models here.

class HangmanWord(models.Model):
  key = models.CharField(max_length=32)
  word = models.CharField(max_length=200)
  word_so_far = models.CharField(max_length=200)
  wrong_letters = models.CharField(max_length=200)
  
  def guess(self, guess):
    if len(self.wrong_letters) >= 8:
      self.reset()

    index = 0
    for letter in self.word:
      if letter == guess:
        self.word_so_far = self.setCharN(self.word_so_far, index, guess)
      index += 1
      
    if guess not in self.word:
      if guess not in self.wrong_letters:
        self.wrong_letters = self.wrong_letters + guess
        #if len(self.wrong_letters) >= 8:
        #  self.reset()
    return
    
  def reset(self):
    hidden_word = ''
    for letter in self.word:
      if letter == ' ': hidden_word += ' '
      else: hidden_word += '-'
    self.word_so_far = hidden_word
    self.wrong_letters = ""
  
  def attemptsLeft(self):
    return 8 - len(self.wrong_letters)
  
  def setCharN(self, subject, index, char):
    return subject[:index] + char + subject[index+1:]
