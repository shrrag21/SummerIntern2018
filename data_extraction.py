from music21 import *
import numpy as np
import pickle
from os import listdir
from os.path import isfile, join
batch_size=50;
random_data_size=1000
no_of_swaps=10000;
global data
data=np.zeros((1,(batch_size+1)))
def random_data_gerator():
    randomd=np.random.randint(30,high=100,size=(random_data_size,batch_size))
    zr=np.zeros((random_data_size,1))
    randomd=np.concatenate((zr,randomd),axis=1)    
    return randomd
def data_appender(i_fnotes):
    global data
    
#   print("data_shape")
#   print(np.shape(data))
#   print("f_notes")
#   print(np.shape(i_fnotes))
    data= np.concatenate((data,i_fnotes),axis=0)
#   print(data)
def split (renotes):
    fnotes=np.array([])
    l=int(len(renotes)/batch_size)
    for i in range(0,(batch_size*l)):
        fnotes=np.append(fnotes,[renotes[i]],axis=0)
#    print("lol")

    fnotes=fnotes.reshape(l,batch_size)
    op=np.ones((l,1), dtype=int)
    fnotes=np.concatenate((op,fnotes),axis=1)
#    print (fnotes)
    data_appender(fnotes)

def noteextractor(filelocation):
    keyboard_nstrument = ["KeyboardInstrument", "Piano", "Harpsichord", "Clavichord", "Celesta", ]
    midi = converter.parse(filelocation)
    notes_to_parse = None
    notes=[]
    renotes=[]
    lnotes=[]
    notes_to_parse = None
    try: # file has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse() 
    except: # file has notes in a flat structure
            notes_to_parse = midi.flat.notes
    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))
    offset = 0
    l=len(notes)
    print("     ",l,"\n")
#print("\nnotes\n")
##print(notes)
    for i in range (0,len(notes)):
        if (notes[i][0].isdigit()):
            lul=0;
#        renotes.append(notes[i])
        else:
#        print(notes[i])
            p1 = pitch.Pitch(notes[i])
            lnotes.append(notes[i])
            renotes.append(str(p1.midi))
#        if (p1.midi<30):
#            print("lol")
    output_notes = []
#print(renotes)
#print("\nlnotes\n")
#print(lnotes)
#print("\nrenotes\n")
#print(renotes)
    # create note and chord objects based on the values generated by the model
    for pattern in lnotes:
        # pattern is a chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        # pattern is a note
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)
        # increase offset each iteration so that notes do not stack
        offset += 0.4
    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp='E:\work\lol123.mid')
    split (renotes)
    
mypath='E:\work\lol'
midlen=12
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for i in range (0,len(onlyfiles)):
    lp=mypath+'\*'+onlyfiles[i]
    print("file     ",i)
    newstr = lp[:midlen] + lp[midlen+1:]
    noteextractor(newstr)
data = np.delete(data, (0), axis=0)
rdata=random_data_gerator()
np.around(rdata, decimals=0)
#print(rdata)
fdata=np.concatenate((rdata,data),axis=0)
h=np.shape(rdata)[0]
hd=np.shape(data)[0]
for i in range(0,no_of_swaps):
    ran_a=np.random.randint(0,high=h,size=1)
    ran_b=np.random.randint(h,high=h+hd,size=1)
    temp=fdata[ran_a[0]].copy()
    fdata[ran_a[0]]=fdata[ran_b[0]]
    fdata[ran_b[0]]=temp
#fdata=np.around(fdata, decimals=0)
pickle_out = open("E:\work\datafpickle2.pickle","wb")
pickle.dump(fdata, pickle_out)
pickle_out.close()
np.savetxt('E:\work\data\lollfdata2.txt', fdata,fmt='%5s',delimiter='    ')
np.savetxt('E:\work\data\lolldata2.txt', data,fmt='%5s',delimiter='    ')
np.savetxt('E:\work\data\lollrdata2.txt', rdata,fmt='%5s',delimiter='    ')
print("done")
