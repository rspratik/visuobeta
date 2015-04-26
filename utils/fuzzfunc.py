import numpy as np

def calcrang(ls,num):
  r=range(len(ls))
  diff = [abs(x) for x in ls-num] #if x >= ls[0] and x <= ls[-1]]
  temp = sorted(zip(r, diff), key=lambda x: x[1])
  #this assumes that the zeroth index is the minimal difference, instead
  #get the index with the smallest x-value
  i = temp[0][0]
  try:
    h=r[i-3]
  except IndexError:
    h=0
  if temp[0][1] == 0:
    try:
      j=r[i+3]
    except IndexError:
      j=r[-1]
  else:
    try:
      j=r[i+2]
    except IndexError:
      j=r[-1]
  return h, j

def fuzz(ls, num):
  i1, i3 = calcrang(ls, num)
  xp = [ls[i1], num, ls[i3]]
  fp = [0.0, 1.0, 0.0]
  return np.interp(ls, xp, fp)

def fuzzavg(i, old, new):
  return (i*old + new)/(i+1.0)

def defuzz(ls, probs):
  return np.dot(ls, probs)/np.sum(probs)

##Don't need these, really
def interp(low, up, val, rng):
  temp = [interpcalc(0.0, 1.0, low, x, val) if x < val else x for x in rng]
  temp = [interpcalc(1.0, 0.0, val, x, up) if x > val else x for x in temp]
  temp2 = [0.0 if x <= low or x >= up else temp[i] for i, x in enumerate(rng)]
  temp2 = [1.0 if x > 1 else x for x in temp2]
  return temp2

def fuzz2(ls, num):
  i1, i3 = calcrang(ls, num)
  return interp(ls[i1], ls[i3], num, ls)

