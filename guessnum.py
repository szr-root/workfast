import random

Num_Digits = 3
Max_Guess = 0

def getsecretnum():
    numbers = list(range(10))
    random.shuffle(numbers)
    secretnum = ''
    for i in range(Num_Digits):
        secretnum += str(numbers[i])
    return secretnum


def getclues(guess, secretnum):
    if guess == secretnum:
        return '你赢了！'

    clues = []
    for i in range(len(guess)):
        if guess[i] == secretnum[i]:
            clues.append('有数字正确且位置正确 ')
        elif guess[i] in secretnum:
            clues.append('有数字正确但位置不对 ')
    if len(clues) == 0:
        return '没有猜中数字 '

    clues.sort()
    return ''.join(clues)


def isonlydigits(num):
    if num == '':
        return False

    for i in num:
        if i not in '0 1 2 3 4 5 6 7 8 9'.split():
            return False

    return True


print('这里有一个 %s 位数。猜猜它是什么 '%(Num_Digits))
print('你需要猜测每一位是什么。')



while True:
    print('选择游戏难度 1.10次猜测机会。 2.15次猜测机会。3.20次猜测机会。')
    x = int(input('请选择游戏难度: '))
    if x == 1:
        Max_Guess = 10

    elif x == 2:
        Max_Guess = 15

    elif x == 3:
        Max_Guess = 20
    else:
        print('输入无效！')
        continue
    secretnum = getsecretnum()
    print('你有 %s 次的猜测机会 '%(Max_Guess))

    guesstime = 1
    while guesstime <= Max_Guess:
        guess = ''
        while len(guess) != Num_Digits or not isonlydigits(guess):
            print('第#%s 次猜测'%(guesstime))
            guess = input('输入你的猜测：')
        print(getclues(guess, secretnum))
        print('')
        guesstime += 1

        if guess == secretnum:
            break
        if guesstime > Max_Guess:
            print('你超出猜测次数了，答案是 %s .'%(secretnum))

    print('还要玩吗？(yes or no)')
    if not input().lower().startswith('y'):
        break



