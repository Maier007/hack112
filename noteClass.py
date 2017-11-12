import midi

#SPECIFY WHICHEVER NOTE (duration) YOU WANT
#DO NOT USE THE *NOTE* CLASS ALONE
class Note(object):
    fullNoteDuration = 500
    def __init__(self, pitch=midi.C_5,dot=False,noteSign=0):
        self.pitch = pitch
        #self.image = image
        self.loudness = 80
        self.dot = dot
        self.noteSign = noteSign
    def playNote(self, track):
        # play audio file *pitch* for self.duration time
        # if the note is dotted, the duration is extended by half
        if self.dot:
            duration = int(self.duration*1.5)
        else:
            duration = self.duration
        on = midi.NoteOnEvent(tick=0, velocity=self.loudness, pitch=self.pitch)
        track.append(on)
        off = midi.NoteOffEvent(tick=duration, pitch=self.pitch)
        track.append(off)

    def getRest(self):
        for rest in Rests:
            if self.duration == rest.duration:
                return rest(self.dot)

    def __repr__(self):
        return str((self.pitch,type(self)))
    
    def getDuration(self):
        return self.duration


class WholeNote(Note):
    duration = Note.fullNoteDuration

class HalfNote(Note):
    duration = Note.fullNoteDuration//2
    
class QuarterNote(Note):
    duration = Note.fullNoteDuration//4
    
class EighthNote(Note):
    duration = Note.fullNoteDuration//8

    
class Rest(Note):
    def __init__(self, dot=False):
        super().__init__(midi.C_5,dot)
        self.loudness = 0

class WholeRest(Rest):
    duration = Note.fullNoteDuration
    image = 'whole_rest.png'

class HalfRest(Rest):
    duration = Note.fullNoteDuration//2
    image = 'half_rest.png'
    
class QuarterRest(Rest):
    duration = Note.fullNoteDuration//4
    image = 'quarter_rest.png'
    
class EighthRest(Rest):
    duration = Note.fullNoteDuration//8
    image = 'eighth_rest.png'

Rests = [WholeRest,HalfRest,QuarterRest,EighthRest]

#Test, this generates a harmonic minor scale
"""
pattern = midi.Pattern()
track = midi.Track()
pattern.append(track)
noteList = []
noteList.append(QuarterNote(midi.C_5+1))
noteList.append(QuarterNote(midi.D_5+1))
noteList.append(QuarterNote(midi.Eb_5+1))
noteList.append(QuarterNote(midi.F_5+1))
noteList.append(QuarterNote(midi.G_5+1))
noteList.append(QuarterNote(midi.Ab_5+1))
noteList.append(QuarterNote(midi.B_5+1))
noteList.append(WholeNote(midi.C_6+1))
for note in noteList:
    note.playNote(track)
eot = midi.EndOfTrackEvent(tick=1)
track.append(eot)
midi.write_midifile("testNoteClass.mid", pattern)
"""
