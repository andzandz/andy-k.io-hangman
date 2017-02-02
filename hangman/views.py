from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import random, string
from hangman.models import HangmanWord

# Create your views here.

def all(request):
  resp = "all words: | "
  words = HangmanWord.objects.all()
  for word in words:
    resp = resp + word.word + " | " + word.key + " ||| "
  return HttpResponse(resp)

def create(request):
  key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))

  word = request.GET.get('word', None)
  #hidden_word = ''
  #for letter in word:
  #  if letter == ' ': hidden_word += ' '
  #  else: hidden_word += '-'
  
  #return JsonResponse({"1":hidden_word})
  #return JsonResponse( { "spaced":spaced(hidden_word).replace('-', '_') } )
  w = HangmanWord(word=word, key=key, word_so_far="", wrong_letters="")
  w.reset()
  w.save()
  return JsonResponse({"created_word": word, "key": key}, json_dumps_params={'indent':4})

def spaced(word):
  return ' '.join(word)

def index(request):
  return JsonResponse({"message":"Welcome to andy-k.io/hangman! Ask for a valid game key."}, json_dumps_params={'indent':4})

def play(request, key):
  words = HangmanWord.objects.all()
  word = None
  for thisword in words:
    if thisword.key == key:
      word = thisword
  if word == None:
    return HttpResponse('game not found')
  
  if request.GET.get('guess') != None:
    if(len(request.GET.get('guess')) > 1):
      if(request.GET.get('guess') == 'reset'):
        word.reset()
        word.save()
        return JsonResponse({
          'word_so_far': word.word_so_far,
          'word_so_far_spaced': ' '.join( word.word_so_far.replace('-', '_') )
        }, json_dumps_params={'indent':4})
      return JsonResponse({"error":"guess must be one letter"}, json_dumps_params={'indent':4})
    word.guess(request.GET.get('guess'))
    word.save()
  
  response_data = {
    'word_so_far': word.word_so_far,
    'word_so_far_spaced': ' '.join( word.word_so_far.replace('-', '_') )
  }
  response_data['guess'] = request.GET.get('guess')
  
  if request.GET.get('guess') == None:
    response_data['message'] = 'put ?guess=x on the end of the URL above to guess the letter X'
  
  if(word.wrong_letters != ''): response_data['wrong_letters'] = word.wrong_letters
  if(word.attemptsLeft() <= 4): response_data['attempts_left'] = word.attemptsLeft()
  if(word.attemptsLeft() == 0): response_data['message'] = "Try again! Request the URL again"
  
  if(word.attemptsLeft() <= 5): response_data['man'] = getMan( 8-word.attemptsLeft() )
  
  return JsonResponse(
    response_data,
    json_dumps_params={'indent':4}
  )
  
ascii_man = [
  "                               ____      ____      ____      ____      ____      ____     ",
  "                    |         |         |    |    |    |    |    |    |    |    |    |    ",
  "                    |         |         |         |    o    |    o    |    o    |    o    ",
  "                    |         |         |         |         |    |    |   ~|~   |   ~|~   ",
  "                    |         |         |         |         |    |    |    |    |    |    ",
  "                    |         |         |         |         |         |         |   /\   ",
  "                    |         |         |         |         |         |         |         ",
  "          ================================================================================"
]

def getMan(state):
  global ascii_man
  width = 10
  return [
    ascii_man[0][(state)*10 : (state+1)*10],
    ascii_man[1][(state)*10 : (state+1)*10],
    ascii_man[2][(state)*10 : (state+1)*10],
    ascii_man[3][(state)*10 : (state+1)*10],
    ascii_man[4][(state)*10 : (state+1)*10],
    ascii_man[5][(state)*10 : (state+1)*10],
    ascii_man[6][(state)*10 : (state+1)*10],
    ascii_man[7][(state)*10 : (state+1)*10],
  ]
