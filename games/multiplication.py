from time import time
import pyinputplus as inp
import random as rnd
import time

num_games = 10
correct_answers = 0

for i in range(num_games):
    num1 = rnd.randint(2,100)
    num2 = rnd.randint(2,100)

    prompt = f'{i+1}: {num1} x {num2}  =   '

    try:
        inp.inputStr(prompt, allowRegexes=['{}'.format(num1*num2)],
                #en block puse una tupla () el primer termino es .* que incluye todos los
                #caracteres posibles, el segundo término es el mensaje cuando se cumple
                             blockRegexes=[('.*', 'Incorrect')],
                             timeout = 10, limit = 3)
    except inp.TimeoutException:
            print('Out of time!')
    except inp.RetryLimitException:
            print('Out of tries!')
    else:
        print('Correct!')
        correct_answers += 1
    time.sleep(1.5)
    print('Score: %s / %s' % (correct_answers,num_games))