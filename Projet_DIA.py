import time

me = 1 if input("Quelle coulleur je doit jouer ? ") == "noir" else -1
vectorsQuick = [(0,1),(1,1),(1,0),(1,-1)]
vectors = [(0,1),(1,1),(1,0),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
coup = 0
etat = 1
lettres = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
range15 = range(15)
range5 = range(1,5)

tempClean = 0
tempFit = 0

def initialisation_map() :
  grille = [[0 for k in range15] for k in range15]
  return grille

carteDeJeux = initialisation_map()

def game_over(state):
  for i in range15:
    for j in range15:
      stateij = state[i][j]
      if stateij != 0:
        for w in vectorsQuick:
          for k in range5:
            nx,ny = j+k*w[1],i+k*w[0]
            if not (0 <= nx < 15 and 0 <= ny < 15):
              break
            elif state[ny][nx] != state[i][j]:
              break
            elif k == 4: return True
  return False

class SimplePlayer:
    def __init__(self,playerId,depthG):
        self.playerId = playerId
        self.depth = depthG
        self.alpha = -2000
        self.beta = 2000
        self.start = 0
    def predict(self,state):
        self.start = time.time()
        a = self.internPredict(state,self.depth,self.playerId,self.alpha,self.beta)[:2]
        if a == [-1,-1]:
          print("Rien trouvé")
          return None
        return(a)
    def internPredict(self,state,depth,player,alpha,beta):
        best = [-1, -1, -500000000] if player == self.playerId else [-1, -1, 500000000]
        if depth == 0 or game_over(state): return [-1, -1, fitness(state,self.playerId)]
        if((time.time()-self.start > 4.3 and depth <= 2)):
          return [-1, -1, fitness(state,self.playerId)]
        if((time.time()-self.start > 4.9 and depth <= 3)):
          return [-1, -1, fitness(state,self.playerId)]
        for cell in empty_cells(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = self.internPredict(state,depth-1,-player,alpha,beta)
            state[x][y] = 0
            score[0], score[1] = x, y
            best2 = best[2]
            if player == self.playerId:
                best = score if score[2] > best2 else best
                if best2 >= beta: return best
                alpha = alpha if alpha > best2 else best2
            else:
                best = score if score[2] < best2 else best
                if best2 <= alpha: return best
                beta = beta if beta < best2 else best2
        return best

def fitness(x,player):
  c = 0
  s1 = 0
  s2 = 0
  for i in range15:
    for j in range15:
      vvx = x[i][j]
      if vvx == player:
        c += 1
        for w in vectors:
          wx,wy = w
          if (0 <= i+4*wx < 15 and 0 <= j+4*wy < 15):
            tempS = 0
            prof = 0
            for k in range5:
              vx = x[i+k*wx][j+k*wy]
              if(vx == 0):
                prof += 1
                if(prof == 1): tempS+= k*k
              elif(vx == player):
                k2 = k+1 if k != 1 else 2.5
                tempS+= k2*k2*k2*k*(1 if prof == 0 else (0.3 if prof == 1 else 0))
              else:
                tempS = 0
                break
            s1 += tempS
      elif vvx == -player:
        c += 1
        for w in vectors:
          wx,wy = w
          if (0 <= i+4*wx < 15 and 0 <= j+4*wy < 15):
            tempS = 0
            prof = 0
            for k in range5:
              vx = x[i+k*wx][j+k*wy]
              if(vx == 0):
                prof += 1
                if(prof == 1): tempS+= k*k
              elif(vx == -player):
                k2 = k+1 if k != 1 else 2.5
                tempS+= k2*k2*k2*k2*(1 if prof == 0 else (0.3 if prof == 1 else 0))
              else:
                tempS = 0
                break
            s2 += tempS
  fit = (s1-1.5*s2)/c
  return fit

def empty_cells(state):
    cells = []
    if coup == 2:
        for x in range(8):
            for y in range(8):
                if max(x,y) == 7: cells.append([4+x,4+y])
        return cells
    for i in range15:
        for j in range15:
            if state[i][j] == 0:
                if coupPossible(state,i,j): cells.append([i, j])
    return cells

def coupPossible(state,i,j):
  for x in range(-1,2):
      for y in range(-1,2):
          if(15 > i+x > 0 and 15 > j+y > 0 and state[i+x][j+y] != 0): return True
  return False

myself = SimplePlayer(me,4)
myselftest = SimplePlayer(-me,3)
def prettyPrint(state):
    print("".join(["-" for k in range(15*3)]))
    print("".join([(" " if k < 10 else "") + str(k) + " " for k in range(1,16)]))
    for x in range(len(state)):
        txt = ""
        for i in range(len(state[0])):
            j = state[x][i]
            txt += " O " if j == 1 else (" X " if j == -1 else " ● ")
        print(txt + " " + lettres[x])
l = []
vpx,vppx,px,py,ppx,ppy = None,None,None,None,None,None
while not game_over(carteDeJeux):
  if(etat == me):
    if(coup == 0):
      print("Je joue H8")
      carteDeJeux[7][7] = me
      prettyPrint(carteDeJeux)
    else:
      start = time.time()
      [x,y] = myself.predict(carteDeJeux)
      vpx,vppx,px,py,ppx,ppy= carteDeJeux[x][y],vpx,ppx,ppy,x,y
      end = time.time()
      print("Je joue " + lettres[x]+str(y+1) + " en " + str(end - start) + "s")
      l+= [end - start]
      tempFit = 0
      carteDeJeux[x][y] = me
      prettyPrint(carteDeJeux)
  else:
    nextcoup = input("Quell est votre coup ? ")
    if(nextcoup == "cancel"):
      carteDeJeux[px][py] = vppx
      carteDeJeux[ppx][ppy] = vpx
      print("Coup annulé")
      prettyPrint(carteDeJeux)
      continue
    valid = False
    while not valid:
        try:
            x,y = lettres.index(nextcoup[0].upper()),int(nextcoup[1:])-1
            valid = True
            break
        except ValueError:
            print("Veuillez reessayer")
            nextcoup = input("Quell est votre coup ? ")
    vpx,vppx,px,py,ppx,ppy= carteDeJeux[x][y],vpx,ppx,ppy,x,y
    carteDeJeux[x][y] = -me
    prettyPrint(carteDeJeux)
  coup += 1
  etat = -etat
print(sum(l)/len(l))
print(max(l))
