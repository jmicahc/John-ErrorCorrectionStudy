#!/usr/bin/env python
from __future__ import print_function
# SUPPLIED WITH NO GUARANTEES!!
import re
from psychopy import visual, core, event
#my lazy way of keeping time NB can be relatively inaccurate
import time
from nltk.corpus import brown
from nltk.book import gutenberg

sents = gutenberg.sents()

sents = brown.sents() + sents
sents = list(sents)
#sentences = nltk.book.gutenberg.sents()
sentences = os.open('/home/john/nltk_data/corpora/words/en', os.O_WRONLY | os.O_CREAT | os.O_EXCEL)



def mkSnts(sents, a, b):
    stimuli=[]
    append=True
    for i in range(len(sents)-1,0,-1):
        if (len(sents[i])>a and len(sents[i])<b):
            for j in range(len(sents[i])-1,0,-1):
                if sents[i][j] in ['.',';',':']:
                    sents[i][j-1] += sents[i].pop()
                elif len(re.sub("[\W\d]", "", sents[i][j].strip()))==0:
                    sents[i][j-1] += sents[i].pop()
                    append=False
                    break
            if append: 
                word = sents[i][0]
                if (word.isalpha()):
                    print(' '.join(sents[i]), file=sentences)
            else: 
                append=True

    return stimuli    
           



 #empty for now.. this is a string of zero length that 
                                 # we will append our key presses to in sequence

#a routine to save responses to file anytime we want to
def saveThisResponse(captured_string):
    outfile = "./myResponses.txt"
    f = open(outfile, 'a') #open our results file in append mode so we don't overwrite anything
    f.write(captured_string) #write the string they typed
    f.write('; typed at %s' %time.asctime()) #write a timestamp (very course)
    f.write('\n') # write a line ending
    f.close() #close and "save" the output file
 

#a routine to update the string on the screen as the participant types
def updateTheResponse(captured_string):
    CapturedResponseString.setText(captured_string)
    CapturedResponseString.draw()
    The_stimulus.draw()
     
    myWin.flip()

# set up a stimulusantsindow
myWin = visual.Window((800.0,800.0),allowGUI=False,winType='pyglet',
            monitor='testMonitor', units ='deg', screen=0)

#will be used to show the text they are typing: will update every 
# time they type a letter
sans = ['Gill Sans MT', 'Arial','Helvetica','Verdana'] #use the first font found on this list
CapturedResponseString = visual.TextStim(myWin, 
                        units='norm',height = 0.1,
                        pos=(0, 0.0), text='',
                        font=sans, 
                        alignHoriz = 'center',alignVert='center',
                        color='BlanchedAlmond')
#set up some fonts. If a list is provided, the first font found will be used.
#setup done, now start doing stuff!
stimuli = mkSnts(sents, 4, 7)
#for sent in stimuli:
    #print sent
captured_string = ''
while (len(stimuli)>0):
    sent = stimuli.pop(0)
    #print sent, "..."
    #print stimuli[0], "..."
    #keep going forever
    #draw the stimulus .. this can be anything but here it is text
    sentNum = 0
    for word in sent:
        The_stimulus = visual.TextStim(myWin, 
                            units='norm',height = 0.1,
                            pos=(0, 0.5), text=word,
                            font=sans, 
                            alignHoriz = 'center',alignVert='center',
                            color='BlanchedAlmond')
        The_stimulus.draw()  # draw it
        myWin.flip() # show it
        firstWord = word
        # now we will keep tracking what's happening on the keyboard
        # until the participant hits the return key
        subject_response_finished = 0 # only changes when they hit return
        
        #check for Esc key / return key presses each frame
        while subject_response_finished == 0:
        
            for key in event.getKeys():
                #quit at any point
                if key in ['escape']: 
                    myWin.close()
                    core.quit()
                    
                #if the participant hits return, save the string so far out 
                #and reset the string to zero length for the next trial
                elif key in ['space']:
     #               print 'participant typed %s' %captured_string #show in debug window
                    saveThisResponse(captured_string) #write to filen
                    if (captured_string!=word.lower()):
           #             print 'error found!', captured_string, "!=", word.lower()
                        stimulus = modifyFuture(stimuli, sent, word)
                    captured_string = '' #reset to zero length 
                    subject_response_finished = 1 #allows the next trial to start
                    
                #allow the participant to do deletions too , using the 
                # delete key, and show the change they made
                elif key in ['delete','backspace']:
                    captured_string = captured_string[:-1] #delete last character
                    updateTheResponse(captured_string)
                #handle spaces
                elif key in ['period']:
                    captured_string = captured_string+'.'
                    updateTheResponse(captured_string)
                elif key in ['colon']:
                    captured_string = captured_string+':'
                    updateTheResponse(captured_string)
                elif key in ['comma']:
                    captured_string = captured_string+','
                    updateTheResponse(captured_string)
                elif key in ['minus']:
                    captured_string += '-'
                    updateTheResponse(captured_string)
                elif key in ['apostrophe']:
                    captured_string += '\''
                    updateTheResponse(captured_string)
                elif key in ['lshift','rshift']:
                    pass #do nothing when some keys are pressed
                #etc ...
                # if any other key is pressed, add it to the string and 
                # show the participant what they typed
                else: 
                    captured_string = captured_string+key
                    #show it
                    updateTheResponse(captured_string)
                