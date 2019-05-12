from keras.models import load_model
import numpy as np

model = load_model('./20190512_2000')

from random import randrange
# None:何もない 0: 黒 1: 白
board = [[str(i+1)]+list('　　　　　　　　 ') for i in range(8)]
board = [list(' １２３４５６７８ ')] + board + [list('          ')]

board[4][4] = '●'
board[4][5] = '〇'
board[5][5] = '●'
board[5][4] = '〇'
dirs = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]

def predict(board, turn, opo):
  indata = np.array([
    [int(board[y][x] == turn) for x in range(1,9) for y in range(1,9)] +
    [int(board[y][x] == opo) for x in range(1,9) for y in range(1,9)]
  ]).reshape((1, 8, 8, 2), order='F')
  #print(str(indata[0][:,:,0]) +'\n\n'+str(indata[0][:,:,1]))
  pred = model.predict(indata)
  #print(pred)
  pred = pred[0]
  scores = sorted(list(enumerate(pred.tolist())), key=lambda x: -x[1])
  return [(i%8+1, i//8+1, s) for i, s in scores]

def process(t, o, x, y, dx, dy, turn=False):
  s = board[y][x]
  if s == '　' or not (1 <= x <= 8) or not (1 <= y <= 8):
    return False
  if s == t:
    return True
  ret = process(t, o, x+dx, y+dy, dx, dy, turn)
  if ret and turn:
    board[y][x] = t
  return ret

def is_available(t, o, x, y):
  if board[y][x] != '　':
    return False
  for dx, dy in dirs:
    tx, ty = x+dx, y+dy
    if board[ty][tx] != o:
      continue
    if process(t, o, tx, ty, dx, dy, False):
      return True

def candidate(t):
  o = '〇' if t == '●' else '●'
  ret = []
  for y in range(1, 9):
    for x in range(1, 9):
      if is_available(t, o, x, y):
        ret.append((y, x))
  return ret
board = [[str(i+1)]+list('　　　　　　　　 ') for i in range(8)]
board = [list(' １２３４５６７８ ')] + board + [list('          ')]

board[4][4] = '●'
board[4][5] = '〇'
board[5][5] = '●'
board[5][4] = '〇'
num = 4
turn = '●'
opo = '〇'
passes = 0
while num < 64 and passes <= 1:
  print("\n"+"\n".join(map("".join, board)))
  cands = candidate(turn)
  if len(cands) == 0:
    print('pass!')
    opo = turn
    turn = '〇' if turn == '●' else '●'
    passes += 1
    continue

  if turn == '●':
    y, x = map(int, input('候補手:%s:'%cands).split())
  else:
    preds = predict(board, turn, opo)
    print('\n'.join(list(map(str, preds[:5]))))
    input()
    for b, a, s in preds:
      if (b,a) in cands:
        y, x = b, a
        break
  if (y, x) in cands:
    for dx, dy in dirs:
      tx, ty = x+dx, y+dy
      if board[ty][tx] != opo:
        continue
      process(turn, opo, tx, ty, dx, dy, True)
    board[y][x] = turn
    num += 1
  else:
    print('候補手の中から入力してください')
    continue
  opo = turn
  turn = '〇' if turn == '●' else '●'
  passes = 0

print("\n"+"\n".join(map("".join, board)))
b, w = 0, 0
for y in range(1, 9):
  for x in range(1, 9):
    if board[y][x] == '●':
      b += 1
    else:
      w += 1
print('%s:%s'%(b,w))
