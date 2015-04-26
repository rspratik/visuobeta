
from fuzzfunc import fuzz, fuzzavg
from math import log
import numpy as np
import os

def parsetraindata(directory='H:\\VisuoData\\TrainData', test=False):
  output={}
  if test:
    files=['TrainDataTest.txt']
  else:
    files=os.walk(directory)
    files=list(files)[0]
    files=files[2]
  for j, fname in enumerate(files):
    percentcomplete=float(j)/len(files)*100
    if percentcomplete%10==0:
      print percentcomplete
    with open(os.path.join(directory, fname)) as f:
      lines=f.readlines()
    lines=list(lines)
    nameindexes=[(i, line) for i, line in enumerate(lines) if ' above ' in line]
    
    for i, line in nameindexes:
      try:
        inputs=[l.split('=')[1] for l in lines[i:i+4]]
      except IndexError:
        print fname, i, line
        return 'Fail'
      inputs=[inpt.strip().strip('"') for inpt in inputs]
      name1,name2=inputs[0].split(' above ')
      name1=name1.strip('[]')
      #distance, angle
      vals=(float(inputs[2]), float(inputs[3]))
      try:
        t=output[name1]
      except KeyError:
        output[name1]={name2:[vals]}
      else:
        try:
          t2=t[name2]
        except KeyError:
          t[name2]=[vals]
        else:
          t2.append(vals)
  return output

def fuzzparsetrainfiles(pdict, DIST, ANGL, symmetric=True):
  output={}
  for lbl in pdict:
    for lbl2 in pdict[lbl]:
      try:
        t=output[lbl]
      except KeyError:
        output[lbl]={lbl2:{'dist':np.zeros(8), 'angl':np.zeros(16), 'n':0}}
        t2=output[lbl][lbl2]
      else:
        try:
          t2=t[lbl2]
        except KeyError:
          t[lbl2]={'dist':np.zeros(8), 'angl':np.zeros(16), 'n':0}
          t2=t[lbl2]
      if symmetric:
        try:
          t3=output[lbl2]
        except KeyError:
          output[lbl2]={lbl:{'dist':np.zeros(8), 'angl':np.zeros(16), 'n':0}}
          t4=output[lbl2][lbl]
        else:
          try:
            t4=t3[lbl]
          except KeyError:
            t3[lbl]={'dist':np.zeros(8), 'angl':np.zeros(16), 'n':0}
            t4=t3[lbl]
      for dist, angl in pdict[lbl][lbl2]:
        d=fuzz(DIST, log(float(dist), 2))
        a=fuzz(ANGL, float(angl)-180.)
        t2['dist']=fuzzavg(t2['n'], t2['dist'], d)
        t2['angl']=fuzzavg(t2['n'], t2['angl'], a)
        t2['n']+=1
        if symmetric:
          t4['dist']=fuzzavg(t4['n'], t4['dist'], d)
          t4['angl']=fuzzavg(t4['n'], t4['angl'], a)
          t4['n']+=1
  return output

