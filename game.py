import random


def drawBoard(board):
    print(board[7] + '|' + board[8] + '|' + board[9])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[1] + '|' + board[2] + '|' + board[3])


def inputPlayerLetter():
    letter = ' '
    while not (letter == 'X' or letter == 'O'):
        print('你想选 X 还是 O?')
        letter = input().upper()
    if letter == 'X':
        return['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def makeMove(board, letter, move):
    board[move] = letter


def isWinner(bo, le):
    return((bo[7] == le and bo[8] == le and bo[9] == le)or
(bo[4] == le and bo[5] == le and bo[6] == le)or
(bo[1] == le and bo[2] == le and bo[3] == le)or
(bo[7] == le and bo[4] == le and bo[1] == le)or
(bo[8] == le and bo[5] == le and bo[2] == le)or
(bo[9] == le and bo[6] == le and bo[3] == le)or
(bo[7] == le and bo[5] == le and bo[3] == le)or
(bo[9] == le and bo[5] == le and bo[1] == le))

def getBoardCopy(board):
    boardCopy = []
    for i in board:
        boardCopy.append(i)
    return boardCopy


def isSpaceFree(board, move):
    return board[move] == ' '


def getPlayerMove(board):
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('你下一步想下哪? (1-9)')
        move = input()
    # print('输入无效！')
    return int(move)


def chooseRandomMoveFromList(board, movesList):
    possibleMoves =[]
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
         return random.choice(possibleMoves)
    else:
        return None


def getComputerMove(board, computerLetter):
    for i in range(1, 10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, i):
            makeMove(boardCopy, computerLetter, i)
            if isWinner(boardCopy, computerLetter):
                return i
    for i in range(1, 10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, i):
            makeMove(boardCopy, playerLetter, i)
            if isWinner(boardCopy, playerLetter):
                return i

    if isSpaceFree(board, 5):
        return 5

    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    return chooseRandomMoveFromList(board, [2, 4, 6, 8])


def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


print('你好，来玩#字棋吧!')
while True:
    theBoard = [' '] * 10
    playerLetter, computerLetter = inputPlayerLetter()
    turn = whoGoesFirst()
    print(turn + ' 将先走第一步.')
    gameIsPlaying = True
    while gameIsPlaying:
        if turn == 'player':
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)

            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('你打败了电脑，真厉害（mdzz）!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('平局（你连智障电脑都下不赢）!')
                    break
                else:
                    turn = 'computer'
        else:
            move = getComputerMove(theBoard, computerLetter)
            makeMove(theBoard, computerLetter, move)
            if isWinner(theBoard,computerLetter):
                drawBoard(theBoard)
                print('电脑赢了，你这个垃圾! ')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('平局（你连智障电脑都下不赢）!')
                    break
                else:
                    turn = 'player'
    print('还想玩吗？只要998，让你爽到不能呼吸哟?(y or n)')
    if not input().lower().startswith('y'):
        break
