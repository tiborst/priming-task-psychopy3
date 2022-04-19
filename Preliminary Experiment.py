#preliminary experiment for psychopy3 by Tibor Stöffel

#imports
from psychopy.visual import TextStim, Window, Circle, Rect
from psychopy.core import wait, Clock, CountdownTimer, getTime
from psychopy.event import waitKeys, getKeys
from random import shuffle, uniform
import numpy as np
import pandas as pd

#define window
mywin = Window([800, 600], color = 'black')

#number of trials (should be a multiple of 3)
nTrials = 6

#randomization vectors for primes, stimuli and stimuli location
rnd_primes = np.repeat(np.array([0,1,2]), [nTrials/3])  #0:left, 1:right, 2:Nan
rnd_loc = np.repeat(np.array([1,2]), [nTrials/2])   # 1:left 2:right
rnd_stim = np.repeat(np.array([1,2]), [nTrials/2])  # 1:red/left 2:right/green
shuffle(rnd_primes)
shuffle(rnd_loc)
shuffle(rnd_stim)

#empty list for getKeys output 
react_key = []
react_time = []

#instruction sreen and primes
prime = ['LEFT', 'RIGHT', 'KWARG']
instruction = "Insctructions:\nYou will see a series of 2 stimuli on either side of the screen.\n\nWhenever you see the red Stimulus please press 'd'. Whenever you see the green Stimulus press 'k'. Between Stimuli focus on the Fixationcross in the middle of the Screen.\n\nPress 'space' to continue."
too_slow = 'TOO SLOW!'
text = TextStim(mywin, font = 'Verdana')
def show_text(instr_text, wait_time = 0.1, buttonpress = True, color = 'White'):
    text.setText(instr_text)
    text.setColor(color)
    text.draw()
    mywin.flip()
    wait(wait_time)
    if buttonpress: 
        inst_resp = waitKeys(keyList = ['space'])

#primes
def show_prime(prime, prime_time = 0.15):
    text.setText(prime)
    text.draw()
    mywin.flip()
    wait(prime_time)

#stimuli
stim1 = Rect(mywin, width = 0.3, height = 0.3, fillColor = 'red') #left
stim2 = Circle(mywin, radius = 0.3, fillColor = 'green')    #right
def react_stim(stim, loc):
    if stim == stim1:
        if loc == 1:
            stim1.pos = (-0.5, 0)
        elif loc == 2:
            stim1.pos = (0.5, 0)    
        stim1.draw()
    elif stim == stim2:
        if loc == 1:
            stim2.pos = (-0.5, 0)
        elif loc == 2:
            stim2.pos = (0.5, 0)
        stim2.draw()
    mywin.flip()

#Fixation Cross
vert_line = Rect(mywin, width = 0.01, height = 0.2, fillColor = 'white')
horz_line = Rect(mywin, width = 0.2, height = 0.01, fillColor = 'white')
def FixationCross(interval):
    vert_line.draw()
    horz_line.draw()
    mywin.flip()
    wait(interval)


#experiment for loop
show_text(instruction)
for t in range(nTrials):
    
    FixationCross(uniform(0.4,2))
    show_prime(prime[rnd_primes[t]])
    
    if rnd_stim[t] == 1:
        react_stim(stim1, rnd_loc[t])
    else:
        react_stim(stim2, rnd_loc[t])
        
    time_1 = getTime()
    out = waitKeys(maxWait = 1, keyList = ['d', 'k'])
    time_2 = getTime()
    
    if out == None:
        show_text(too_slow, wait_time = 0.7, buttonpress = False, color = 'red')
        react_key.append('None')
        react_time.append('None')
    else: 
        react_key.append(out[0])
        react_time.append((time_2-time_1))

#creating dataFrame for the output file
data = {'Stim': rnd_stim, 'Loc': rnd_loc, 'Prime': rnd_primes, 'RT': react_time, 'Key': react_key}
data_df = pd.DataFrame(data)
print(data_df)
data_df.to_csv('Data.csv')

#calculations:
mean_rt = []
mean_rt_wr = []

for ind,val in enumerate(rnd_stim):
    if val == 1:
        if rnd_primes[ind] == 0 and react_time[ind] != 'None':
            mean_rt.append(react_time[ind])
        elif react_time[ind] != 'None':
            mean_rt_wr.append(react_time[ind])
    elif val == 2:
        if rnd_primes[ind] == 1 and react_time[ind] != 'None':
            mean_rt.append(react_time[ind])
        elif react_time[ind] != 'None':
            mean_rt_wr.append(react_time[ind])
            
mean_rt_correct = sum(mean_rt)/len(mean_rt)
mean_rt_wrong = sum(mean_rt_wr)/len(mean_rt_wr)

x = 0
for i,v in enumerate(rnd_stim):
    if v == 1 and react_key[i] == 'd':
            x += 1
    elif v == 2 and react_key[i] == 'k':
            x += 1

perc_corr = (x /len(react_key))*100

endtext = 'Thank you for participating. Here are some Results:\nRT mean with congruent prime: ' + str(round(mean_rt_correct, 2)) + '\nRT mean with incongruent prime: ' + str(round(mean_rt_wrong, 2)) + '\nOverall % correct: ' + str(round(perc_corr, 2))
show_text(endtext)
print('RT mean with congruent prime: ' + str(round(mean_rt_correct, 2)))
print('RT mean with incongruent prime: ' + str(round(mean_rt_wrong, 2)))
print('Overall % correct: ' + str(round(perc_corr, 2)))
            
            



