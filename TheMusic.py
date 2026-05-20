# Programmer: Hooman Kaseban
# Step By Step of Goals...
# Cofrde a program which takes a simple (in further steps, signatured scales) Scale Name and generates Suitable notes for creating Major (all scale forms) scale. passed!
# ...takes the scale name, then generates all complete Cadances of it.passed!
# ...takes the scale neme, then gererates all types of Cadances of it.passed!
# finally, I can go for mapping the scales on guitar board.
import regex as re
import flet as ft
# This function takes a note and desired scale form then, returns its scale in the desired form. 
def scaler(scale,form):
    #scale:
    # 'C','C#','D',...
    #scale form:
    #'1':natural_major,'2':natural_minor_distance,'3':harmonic_minor_distance,
    #'4':melodic_minor,'5':harmonic_major_distance,'6':melodic_major_distance
    Cmaj=["C","D","E","F","G","A","B"] # Cmajor chord notes (using in making priorities).
    # Cmajor distances (natural distance between notes), crucial for finding distances in any scale.
    natural_pattern_prior={('C','D'):1 , ('D','E'):1 , ('E','F'):0.5 , ('F','G'):1 , ('G','A'):1 , ('A','B'):1 , ('B','C'):0.5 }
    # this dict will include the scale distances.
    natural_pattern={}
    # handling scales with signatures ('b's and '#'s).
    if len(scale)>1: 
        #Cmaj Update
        pure_note=scale[0]
        signature=scale[1]
        Cmaj[Cmaj.index(pure_note)]=scale    # a little trick :)
        # create a draft of scale distances based on standard distance pattern (Cmajor).
        # in further steps, it would be updated to the actual scale distances.
        for key,val in natural_pattern_prior.items():
            if key[0]==pure_note: # first note of tuple
                revised_scale_tuple=(key[0]+signature,key[1]) #create right appearence for that tuple
                # distance handling for signatures.
                if signature=='#': 
                    revised_tuple_distance=val-0.5
                else: # for 'b' signature...
                    revised_tuple_distance=val+0.5
                # fill the scale dict.
                natural_pattern[revised_scale_tuple]=revised_tuple_distance
            elif key[1]==pure_note: # second note of tuple
                revised_scale_tuple=(key[0],key[1]+signature) #create right appearence for that tuple
                if signature=='#': #distance handling for diez
                    revised_tuple_distance=val+0.5
                else: # for 'b' signature...
                    revised_tuple_distance=val-0.5
                # fill the scale dict.
                natural_pattern[revised_scale_tuple]=revised_tuple_distance
            else: #Nothings changed (exactly looks same as Cmaj distance)
                natural_pattern[key]=val
    else: #simple scale (without signatures)
        natural_pattern=natural_pattern_prior
    # specify patterns' form
    natural_major_distance=[1,1,0.5,1,1,1,0.5] 
    natural_minor_distance=[1,0.5,1,1,0.5,1,1] 
    harmonic_minor_distance=[1,0.5,1,1,0.5,1.5,0.5]
    melodic_minor_distance=[1,0.5,1,1,1,1,0.5]
    harmonic_major_distance=[1,1,0.5,1,0.5,1.5,0.5]
    melodic_major_distance=[1,1,0.5,1,0.5,1,1]

    # Decide which form should be used
    form_code={'1':natural_major_distance,'2':natural_minor_distance,'3':harmonic_minor_distance,'4':melodic_minor_distance,'5':harmonic_major_distance,'6':melodic_major_distance}
    desired_form_pattern=form_code[form]
    base_note_index=Cmaj.index(scale) 
    #Creating a draft of scale (sorted notes).
    scale_sorted_notes=Cmaj[base_note_index:].copy()
    scale_sorted_notes+=Cmaj[:base_note_index+1]
    #this loop works on finding the distance between the Note (it should be palced on the 1st location of the pattern) and the next one.
    #it finds the "Standard" distance pattern 
    #in further steps, code works on "actual" distance for desired form.in%20%7C%20
    natural_note_tuples=list(natural_pattern.keys())
    desired_scale={} # this is the answer! (wanted scale)
    for note_index in range(len(scale_sorted_notes)-1):
        current_note=scale_sorted_notes[note_index]
        next_note=scale_sorted_notes[note_index+1] #for further use in creating tuples...
        for pair_note in natural_note_tuples:
            #check if the note is 'lead' note in the tuple.
            if (current_note in pair_note) and (pair_note.index(current_note)==0):
                #create a draft of the scale distances based on the form pattern.
                desired_scale[(current_note,next_note)]=natural_pattern[pair_note] 
                break
    # Now I have a draft of scale distances based on the pattern on "desired_scale".
    # in the next step, I must adopt it...
    for tuples_priority_index in range(len(desired_form_pattern)):
        scale_note_tuples=list(desired_scale.keys()) # use list forms of dictionarys for making a loop on them. 
        current_tuple=scale_note_tuples[tuples_priority_index] # will be used for searching the scale distance in the dict    
        # "if" distances are equal : DO NOTHING
        # check wheather natural distance is equal with the form distance.
        if desired_scale[current_tuple] == desired_form_pattern[tuples_priority_index]: 
            continue
        else: # have to use signatures
        # the change (signature move) is always append on the 2nd note and influences next tuple!
            difference = abs(desired_scale[current_tuple] - desired_form_pattern[tuples_priority_index])
            # check for # or b.
            if desired_scale[current_tuple] < desired_form_pattern[tuples_priority_index]:
                # add '#' to the 2nd note.
                desired_scale=update_scale(desired_scale,current_tuple,'#',tuples_priority_index,difference)
                
            else:
                # add "b" to the 2nd note.
                desired_scale=update_scale(desired_scale,current_tuple,'b',tuples_priority_index,difference)
            
    scale_notes=[]
    for tup in list(desired_scale.keys()):
        scale_notes.append(tup[0])
    return desired_scale,scale_notes # Now, it's complete!!
    
# function using in 'scaler' for applying '#'s and 'b's.
# this function returns signatured scale based on a mentioned tuple change.
def update_scale(scale_dict,current_tuple,signature,tuples_priority_index,difference): 
    scale_keys=list(scale_dict.keys())
    next_tuple=scale_keys[tuples_priority_index+1]
    signatured_key='' #use for updating next tuple note
    updated_scale={} #the answer

    if signature=='#': #Update difference due to its signature
        difference=difference
    else:
        difference=(-1)*difference
    #first, update distances (signatures are considered)
    scale_dict[current_tuple]+=difference
    scale_dict[next_tuple]-=difference
    # second, add 'signature' to the note
    difference=int(abs(difference)/0.5) #due to multiplying the number in signature sings (char type), I have to use integer.
    
    # this loop works on signature signs and applying them.
    for key,val in scale_dict.items(): 
        # only current tuple and the next would be updated by signatures
        # reminder: the note with signature is placed in 2nd and 1st of the current tuple and the next tuple respectively.
        if key==current_tuple: # check if it's turn to apply signature on the current tuple. (to update 'key')
            # transform to 'list' type for making changes.
            key=list(key) 
            # allow to insert multiple 'signature' if it needs! example: D#major
            key[1]=key[1]+signature*difference 
            signatured_key=key[1]
            key=tuple(key)#transform again to tuple for using in Dict (list type can't be placed as "key" in dict).
        elif key==next_tuple: # check if it's turn to apply signature on the next tuple. (to update 'key')
            # just have to replace the shape of the note which it's calculated on the previous round.
            key=list(key)
            key[0]=signatured_key
            key=tuple(key)
        # at the end, fill the answer dict.
        updated_scale[key]=val 

    return updated_scale

# With this function, I can find all chords of the scale.
def scale_harmonization(scale_distances,scale_notes):
    # D major "scale_distances":
    # {('D', 'E'): 1, ('E', 'F#'): 1.0, ('F#', 'G'): 0.5, ('G', 'A'): 1, ('A', 'B'): 1, ('B', 'C#'): 1.0, ('C#', 'D'): 0.5}
    # D major "scale_notes":
    # ['D', 'E', 'F#', 'G', 'A', 'B', 'C#']

    # by a circular loop, I want to calculate third and fifth degree distances of all notes of the scale (tertian Harmony!)
    # then, get the signature of the chords
    scale_chords=[] # will contain all signatured chords of the scale
    for base_note in scale_notes:
        one_octave={} # it will contain an octave begain with the selected note. 
        #finding the starter tuple
        for key in scale_distances.keys():
            if base_note in key[0]:
                base_tup=key
                break
        # achieve the octave using circular loop
        tup_list=list(scale_distances.keys())
        i=tup_list.index(base_tup)
        while True:
            one_octave[tup_list[i]]=scale_distances[tup_list[i]]
            i = (i+1) % len(tup_list)
            if tup_list[i]==base_tup:
                break
        signature=chord_quality(one_octave)
        chord=base_note+signature
        scale_chords.append(chord)
    return scale_chords
      
#this function should return the quality of the chord(Major,minor,augmented,and diminished)
def chord_quality(octave):
    #tertian Harmony :
    # Major = major third + perfect fifth
    # Minor = minor third + perfect fifth
    # Augmented = major third + augmented fifth
    # Diminished = minor third + diminished 
    third={2:'major',2.5:'augmented',1.5:'minor',1:'diminished'}
    fifth={3.5:'perfect',3:'diminished',4:'augmented'}
    counter=1
    tone=0
    third_form=''
    fifth_form=''
    for dist in octave.values():
        tone+=dist
        #check for 'third degree'
        if counter==2:
            third_form=third[tone]
        #check for 'fifth degree'
        if counter==4:
            fifth_form=fifth[tone]
            break
        counter+=1
    # specify the quality of the chord
    quality={('major','perfect'):'',('minor','perfect'):'m',('major','augmented'):'_aug',('minor','diminished'):'_dim'}
    chord_signature=quality[(third_form,fifth_form)]     
    return chord_signature #e.g >>> '' or 'm' or '_aug' or '_dim'

#this function takes a chord, a desired form (optional) and signature ("optional" and could be null), then simply return the chord in that form
# example: chord_converter('C#_dim','A','b')>>> 'C_aug' .
# example: chord_converter('C#_dim','','b')>>> 'C_dim' .
def chord_converter(chord,desired_form,signature):
    if desired_form!='': # if desired form is requested
        base_chord_draft=str(re.findall('[A-Z]{1}[#,b]*',chord)[0])
        if desired_form=='M': #for Major
            form=''
        elif desired_form=='m':#for Minor
            form='m'
        elif desired_form=='D':# for Diminished
            form='_dim'
        elif desired_form=='A': #for Augmented
            form='_aug'
    else: #if there is not any desired form! (user want to convert on the same form)
        pattern=re.compile(r'([A-Z]{1}[b*#*]?)([_]*[A-Z]*[a-z]*?)') # pattern for regex it splits on chord+signature and form.
        base_chord_draft,form=list(pattern.fullmatch(chord).groups()) #exg: C#_dim >>> 'C#','_dim' other exg: C# >>>> 'C#',''
    # handling sugnatures
    if signature=='': # if there is no signatures to apply on chord
        base_chord=base_chord_draft
    else: # if there is signatures to apply on chord
        if len(base_chord_draft)>1: #signatured chord
            if base_chord_draft[1]=='#': # if chord original signature is '#'
                if signature=='b':# sharp bemol; "#b" >> move back to base
                    base_chord=base_chord_draft[:(len(base_chord_draft)-1)]    
                else:
                    base_chord= base_chord_draft+signature            
            else: # if chord original signature is 'b'
                if signature=='#':  # bemol sharp; "b#" >> move on to base
                    base_chord=base_chord_draft[:(len(base_chord_draft)-1)]
                else:
                    base_chord= base_chord_draft+signature
        else: #simple chord
            base_chord= base_chord_draft+signature
    new_chord=base_chord+form
    return new_chord

#this function takes scale and form number (e.g. cadences(G,6) )
# then, it returns all types of cadence for the selected scale form.
def cadences(scale,scale_form):
    scale_with_distance,scale_notes= scaler(scale,scale_form)
    scale_chords=scale_harmonization(scale_with_distance,scale_notes)
    if scale_form=='3' or scale_form=='4':
        scale_with_distance,scale_notes= scaler(scale,'2')
        natural_minor_chords=scale_harmonization(scale_with_distance,scale_notes)
    # there are 4 types of cadences: authentic, half, plagal and deceptive
    # there are 2 types of Cadence shape: 1.pure scale 2.combination of natural, harmonic and melodic
    # to start, I work on pure scale shape
    # defining the shapes of each scale's authentic cadence
    cadence_pattern={}
    if scale_form=='1': # Natural Major:
        cadence_pattern['Authentic Cadence (Natural Major)']=[[1,2,5,1],[1,4,5,1],[1,4,2,5],[1,6,2,5],[1,6,4,5],
                    [1,5,4,5],[1,3,4,5],[1,5,2,5],
                    [1,4,1,5],[1,4,6,5],[1,2,1,5]]
    elif scale_form=='2': # Natural Minor:
        cadence_pattern['Authentic Cadence (Natural Minor)']=[[1,4,5,1],[1,4,7,1],[1,6,7,1],[1,6,5,1],
                    [1,3,4,5],[1,3,6,7],[1,3,4,7],[1,3,6,5],
                    [1,5,4,5],[1,5,4,7],[1,5,6,7],[1,7,6,5]]
    elif scale_form=='3': # Harmonic Minor:
        # note: 'str' numbers are the same index in natural minor!
        cadence_pattern['Authentic Cadence (Harmonic Minor)']=[[1,4,5,1],[1,6,5,1],[1,4,7,1],[1,4,'7NM',7],[1,6,7,1],[1,6,'7NM',7],
                    [1,4,6,5],[1,4,6,7],[1,4,7,5],[1,4,'7NM',7],[1,6,7,5],[1,6,'7NM',7],
                    [1,3,4,5],[1,'3NM',4,5],[1,3,6,5],[1,'3NM',6,5],
                    [1,4,1,5],[1,6,1,5],[1,4,3,5],[1,6,3,5]]
    elif scale_form=='4': # Melodic Minor:
        # note: 'str' numbers are the same index in natural minor!
        cadence_pattern['Authentic Cadence Melodic Minor']=[[1,4,5,1],[1,6,7,1],[1,4,2,5],[1,4,'4NM',5],[1,3,2,5]]
    elif scale_form=='5' or scale_form=='6' : # Harmonic and Melodic Major:
        if scale_form=='5':
            s='Authentic Cadence (Harmonic Major)'
        else:
            s='Authentic Cadence (Melodic Major)'
        cadence_pattern[s]=[[1,4,5,1],[1,4,7,1],[1,2,5,1],[1,2,7,1],
                    [1,4,3,5],[1,4,3,7],[1,4,2,5],[1,4,2,7],
                    [1,6,4,5],[1,6,4,7],[1,4,1,5],[1,4,1,7],
                    [1,4,6,5],[1,4,6,7],[1,5,4,5],[1,7,4,7],
                    [1,3,4,5],[1,3,4,7],[1,3,2,5],[1,3,2,7]]
    # add pure shape of other types of Cadence (in further, work on combined forms)
    cadence_pattern['Simple Plagal Cadence']=[[1,5,1,4,1]]
    cadence_pattern['Simple Half Cadence']=[[1,4,5,5]]
    cadence_pattern['Simple Deceptive Cadence']=[[1,4,5,4],[1,4,5,1]]
     # Now it's turn to work on other types of Cadence (using Combined forms)
    if scale_form=='1' or scale_form=='5' or scale_form=='6': #for Majors
        cadence_pattern['Combined Major Authentic Cadence']=[[1,4,'7bM',5],[1,2,'7bM',5],[1,4,'4m',5],
        [1,2,'2D',5],[1,'6bA',4,5]]
        cadence_pattern['Combined Major Plagal Cadence']=[[1,5,1,'4m'],[1,5,6,'4m'],[1,3,'6bA',4],
        [1,'6bA','6m',4],[1,'6bA','6m','4m']]
        cadence_pattern['Combined Major Half Cadence']=[[1,4,'4m',5,5],[1,2,4,5,'7bM'],[1,'6bM',4,5,'5m'],
        [1,6,'2D',5,'7D'],[1,3,'7b',5,5]]
        cadence_pattern['Combined Major Deceptive Cadence']=[[1,4,'4m',5,4],[1,2,'7bM',5,6],[1,'6bA',4,5,6],
        [1,4,'2D',5,4],[1,3,'7b',5,6]]
    elif scale_form=='2' or scale_form=='3' or scale_form=='4': #for minors
        cadence_pattern['Picardi-Third Cadence']=[[1,4,5,'1M']]
        cadence_pattern['Combined Minor Authentic Cadence']=[[1,4,7,'5M'],[1,6,'7#D','5M'],[1,'4M',4,'5M'],
        [1,6,'6#D','5M'],[1,'3A','3M','5M']]
        cadence_pattern['Combined Minor Plagal Cadence']=[[1,'5M',1,4],[1,5,3,'4M'],[1,7,3,'4M'],
        [1,'3A','4M',4],[1,'7#D',1,4]]
        cadence_pattern['Combined Minor Half Cadence']=[[1,'4M',4,'5M','5M'],[1,6,4,5,'5M'],[1,3,'4M','5M','5M'],
        [1,'3A',6,5,5],[1,'6#D',4,'2D','5M']]
        cadence_pattern['Combined Minor Deceptive Cadence']=[[1,4,'2D','5M',4],[1,6,5,'5M',4],[1,'3A','4M','5M',6],
        [1,6,7,'5M',4],[1,6,'6#D','7#D',6]]

    cadences={} #a dict which stores all cadences by chords
    for cadence_name, all_patterns in cadence_pattern.items(): # a loop over all types of cadence
        cadence_shapes={} # a temporary dict which stores all patterns of a cadence by chords specified by numbers
        counter=0
        for pattern in all_patterns: # a loop over all patterns of the cadence
            counter+=1
            cadence_cycle=[]
            for chord_index in pattern: # a loop over all notes of the cadence's pattern
                if type(chord_index)==int: # if the chord is availibe on the scale and do not required converter.
                    cadence_cycle.append(scale_chords[chord_index-1]) # add the chord (based on the index) to the list
                else: # if the chord is not availible on the scale and should use the same degree on other forms or scales.
                    if 'NM' in chord_index: #should use "natural Minor" form? (use in Melodic and harmonic authentic cadence)
                        cadence_cycle.append(natural_minor_chords[int(chord_index[0])-1])
                    else: # should use chord_converter? (use in combined cadences)
                        # using regex for dicoding
                        pattern=re.compile(r'(\d*)([b*#*]?)([A*D*M*m*]?)')
                        # converting '7#A' to '7','#','A' and if one of them is null, it returns '' .
                        base_chord_index,signature,desired_form=list(pattern.fullmatch(chord_index).groups()) 
                        base_chord=scale_chords[int(base_chord_index)-1] # finding "base chord"
                        #should use chord_converter!
                        target_chord=chord_converter(base_chord,desired_form,signature)
                        #add to the cycle
                        cadence_cycle.append(target_chord)
            cadence_shapes[counter]=cadence_cycle # the cadence shape No.(counter)
        cadences[cadence_name]=cadence_shapes  # add all paterns of the cadence to the answer dict
    return cadences #e.g. {'Authentic Cadence (Melodic Major)': {1: ['G', 'Cm', 'Dm', 'G'], 2:...} , 'Simple Plagal Cadence':{...} }

#this way of display is purely theoretical and it doesn't include any simplification
def theoretical_display(desired_scale,scale_notes,scale_name,form,scale_chords,cadence):
    form_code={'1':'Major','2':'Natural Minor','3':'Harmonic Minor','4':'Melodic Minor','5':'Harmonic Major','6':'Melodic Major'}
    scale_form_name=form_code[form]
    print(f'"{scale_name}" {scale_form_name} notation is:\n {desired_scale}')
    #printing notes of the scale...
    print(f'{scale_name} {scale_form_name} notes would be:\n{scale_notes}')
    print(f'scale chords would be:\n{scale_chords}')
    #printing all types of cadence for the scale
    for name,pattern in cadence.items():
        print(f'{name} for {scale_name} {scale_form_name} :')
        for number,cadence_form in pattern.items():
            print(f'{number} : {cadence_form}')

#this function simplifies chords and notes by enharmonics rule and is used in "simplifier"
def enharmonics_simplifier(container):
    pattern=re.compile(r'([A-Z]{1})([b*#*]*)(_*[a-z]*)')
    sharp_notation=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    flat_notation=["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
    simplified=[]
    for chord in container:
                pure_note,signatures,quality=list(pattern.match(chord).groups())
                if signatures: #if it's not a simple note
                    indicator=1
                    if "#" in signatures:
                        notation=sharp_notation
                    else: # there are 'b's
                        notation=flat_notation
                        indicator=-1 #this helps to reverse moving in flat notation
                    leveler=notation.index(pure_note) + (indicator*len(signatures))
                    simplified_chord=notation[leveler % len(notation)]
                    chord=simplified_chord+quality
                simplified.append(chord)
    return simplified

#this function simplifies chords and notes by enharmonics rule and is used in "practical_display"
def simplifier(desired_scale,scale_notes,scale_chords,cadence):
    # "desired_scale" is a dict of tuple:number
    # "scale_notes" is a list of strings
    # "scale_chords" is a list of strings
    # "cadence" is a dict of string:dict2 (which dict2 is int:list)

    #simplify 'scale_notes'
    simplified_scale_notes=enharmonics_simplifier(scale_notes)
    #simplify 'scale_chords'
    simplified_scale_chords=enharmonics_simplifier(scale_chords)
    #simplify 'cadence_form'
    simplified_cadence={} # a dict of string(name):internal_dict(int:list)
    for name,shape in cadence.items():
        #simplify selected cadence
        internal_dict={} # a dict of int(number):list(cadence shape)
        for number,cadence_form in shape.items():
            # simplify selected cadence form
            simplified_cadence_form=enharmonics_simplifier(cadence_form)
            internal_dict[number]=simplified_cadence_form
        simplified_cadence[name]=internal_dict #the cadence dict

    # simplify desired_scale
    distances=list(desired_scale.values())
    simplified_scale={}
    # using simplified scale's notes for creating simplified scale
    for tup_index in range(len(distances)):
        simplified_note_tup=(simplified_scale_notes[tup_index],simplified_scale_notes[(tup_index+1) % len(distances)])
        simplified_scale[simplified_note_tup]=distances[tup_index]
    #return simplified results
    return simplified_scale,simplified_scale_notes,simplified_scale_chords,simplified_cadence

#this way of display includes all simplifications in notes and chords usefull for cleaner display and more practical for instrumentalists
def practical_display(desired_scale,scale_notes,scale_name,form,scale_chords,cadence):
    form_code={'1':'Major','2':'Natural Minor','3':'Harmonic Minor','4':'Melodic Minor','5':'Harmonic Major','6':'Melodic Major'}
    scale_form_name=form_code[form]
    simplified_scale,simplified_scale_notes,simplified_scale_chords,simplified_cadence_form = simplifier(desired_scale,scale_notes,scale_chords,cadence)
    print(f'enharmonic-simplified "{scale_name}" {scale_form_name} notation is:\n{simplified_scale}')
    print(f'enharmonic-simplified {scale_name} {scale_form_name} notes would be:\n{simplified_scale_notes}')
    print(f'enharmonic-simplified scale chords would be:\n{simplified_scale_chords}')
    for name,pattern in simplified_cadence_form.items():
        print(f'enharmonic-simplified {name} for {scale_name} {scale_form_name} :')
        for number,cadence_form in pattern.items():
            print(f'{number} : {cadence_form}')

def interface():
    scale_name= input('Please enter your desired note: \n')
    task= input('Please specify your desired scale: \n1-Major     2-Natural Minor\n3-Harmonic Minor     4-Melodic Minor  \n5-Harmonic Major     6-Melodic Major  \n')
    scale_with_distance,scale_notes= scaler(scale_name,task)
    scale_chords=scale_harmonization(scale_with_distance,scale_notes)
    cadence=cadences(scale_name,task)
    print('***************theoretical display:***************')
    theoretical_display(scale_with_distance,scale_notes,scale_name,task,scale_chords,cadence)
    print('\n***************practical display:***************')
    practical_display(scale_with_distance,scale_notes,scale_name,task,scale_chords,cadence)
    

SCALE_FORM_LABELS={
    '1':'Major',
    '2':'Natural Minor',
    '3':'Harmonic Minor',
    '4':'Melodic Minor',
    '5':'Harmonic Major',
    '6':'Melodic Major',
}

ROOT_NOTE_PATTERN=re.compile(r'^[A-G](#|b)?$')
QUICK_ROOT_NOTES=['C','D','E','F','G','A','B','C#','F#','Bb','Eb','Ab']
ENHARMONIC_ROOT_HINTS={
    'A#':'Bb',
    'B#':'C',
    'Cb':'B',
    'D#':'Eb',
    'E#':'F',
    'Fb':'E',
    'G#':'Ab',
}


def flet_interface(page):
    page.title='Musician'
    page.theme_mode=ft.ThemeMode.LIGHT
    page.bgcolor='#F5F7FA'
    page.padding=0
    page.scroll=ft.ScrollMode.AUTO

    result_area=ft.Column(spacing=18)

    root_field=ft.TextField(
        label='Root note',
        value='C',
        hint_text='C, F#, Bb',
        prefix_icon=ft.Icons.MUSIC_NOTE,
        border_radius=8,
        filled=True,
        fill_color='#FFFFFF',
        on_submit=lambda event: generate_results(),
        col={'xs':12,'md':4},
    )

    form_dropdown=ft.Dropdown(
        label='Scale form',
        value='1',
        options=[
            ft.DropdownOption(key=code,text=f'{code}. {label}')
            for code,label in SCALE_FORM_LABELS.items()
        ],
        leading_icon=ft.Icons.TUNE,
        border_radius=8,
        filled=True,
        fill_color='#FFFFFF',
        col={'xs':12,'md':5},
    )

    def set_root(note):
        root_field.value=note
        root_field.error=None
        generate_results()

    quick_root_row=ft.Row(
        controls=[
            ft.OutlinedButton(
                content=note,
                tooltip=f'Use {note}',
                on_click=lambda event,note=note: set_root(note),
            )
            for note in QUICK_ROOT_NOTES
        ],
        wrap=True,
        spacing=8,
        run_spacing=8,
    )

    def reset_inputs(event=None):
        root_field.value='C'
        root_field.error=None
        form_dropdown.value='1'
        generate_results()

    def generate_results(event=None):
        scale_name=_normalize_root_note(root_field.value)
        form=form_dropdown.value or '1'
        root_field.value=scale_name
        root_field.error=None

        if not ROOT_NOTE_PATTERN.fullmatch(scale_name):
            root_field.error='Use A-G with optional # or b.'
            result_area.controls=[_message_panel(
                'Invalid root note',
                'Examples: C, F#, Bb',
                ft.Icons.ERROR_OUTLINE,
                '#FEF2F2',
                '#991B1B',
            )]
            page.update()
            return

        try:
            result=_build_music_result(scale_name,form)
        except Exception as error:
            result_area.controls=[_message_panel(
                'Could not build that scale',
                _scale_error_message(scale_name,error),
                ft.Icons.ERROR_OUTLINE,
                '#FEF2F2',
                '#991B1B',
            )]
        else:
            result_area.controls=[_result_view(result)]
        page.update()

    input_panel=_panel(
        'Scale Builder',
        ft.Icons.PIANO,
        [
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    root_field,
                    form_dropdown,
                    ft.FilledButton(
                        content='Generate',
                        icon=ft.Icons.PLAY_ARROW,
                        bgcolor='#0F766E',
                        color='#FFFFFF',
                        height=48,
                        on_click=generate_results,
                        col={'xs':12,'md':2},
                    ),
                    ft.OutlinedButton(
                        content='Reset',
                        icon=ft.Icons.REFRESH,
                        height=48,
                        on_click=reset_inputs,
                        col={'xs':12,'md':1},
                    ),
                ],
                spacing=12,
                run_spacing=12,
            ),
            ft.Divider(height=1,color='#E2E8F0'),
            ft.Text('Quick roots',size=12,weight=ft.FontWeight.W_600,color='#64748B'),
            quick_root_row,
        ],
        col=12,
    )

    page.add(
        ft.Container(
            padding=ft.Padding(28,24,28,28),
            content=ft.Column(
                controls=[
                    _app_header(),
                    input_panel,
                    result_area,
                ],
                spacing=18,
            ),
        )
    )
    generate_results()


def _normalize_root_note(value):
    value=value.strip()
    if value=='':
        return ''
    return value[0].upper()+value[1:].replace('B','b')


def _build_music_result(scale_name,form):
    scale_with_distance,scale_notes=scaler(scale_name,form)
    scale_chords=scale_harmonization(scale_with_distance,scale_notes)
    cadence=cadences(scale_name,form)
    simplified_scale,simplified_scale_notes,simplified_scale_chords,simplified_cadence=simplifier(
        scale_with_distance,
        scale_notes,
        scale_chords,
        cadence,
    )
    return {
        'scale_name':scale_name,
        'form':form,
        'form_name':SCALE_FORM_LABELS[form],
        'theoretical':{
            'scale':scale_with_distance,
            'notes':scale_notes,
            'chords':scale_chords,
            'cadences':cadence,
        },
        'practical':{
            'scale':simplified_scale,
            'notes':simplified_scale_notes,
            'chords':simplified_scale_chords,
            'cadences':simplified_cadence,
        },
    }


def _scale_error_message(scale_name,error):
    hint=ENHARMONIC_ROOT_HINTS.get(scale_name)
    if hint:
        return f'The current theory engine could not simplify this spelling. Try {hint} instead of {scale_name}.'
    return f'The current theory engine could not simplify this spelling. Details: {error}'


def _app_header():
    return ft.Container(
        padding=ft.Padding(20,18,20,18),
        bgcolor='#111827',
        border_radius=8,
        content=ft.Row(
            controls=[
                ft.Container(
                    width=44,
                    height=44,
                    bgcolor='#F59E0B',
                    border_radius=8,
                    alignment=ft.Alignment(0,0),
                    content=ft.Icon(ft.Icons.LIBRARY_MUSIC,color='#111827',size=26),
                ),
                ft.Column(
                    controls=[
                        ft.Text('Musician',size=26,weight=ft.FontWeight.W_800,color='#FFFFFF'),
                        ft.Text('Scale notes, harmonized chords, and cadence patterns',size=13,color='#CBD5E1'),
                    ],
                    spacing=2,
                ),
            ],
            spacing=14,
        ),
    )


def _result_view(result):
    title=f"{result['scale_name']} {result['form_name']}"
    theoretical=result['theoretical']
    practical=result['practical']

    return ft.Column(
        controls=[
            _summary_panel(title,theoretical),
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    _spelling_panel('Theoretical Spelling',ft.Icons.AUTO_AWESOME,theoretical,'#EEF2FF','#3730A3',{'xs':12,'lg':6}),
                    _spelling_panel('Practical Spelling',ft.Icons.PIANO,practical,'#ECFDF5','#047857',{'xs':12,'lg':6}),
                ],
                spacing=16,
                run_spacing=16,
            ),
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    _cadence_panel('Theoretical Cadences',theoretical['cadences'],{'xs':12,'xl':6}),
                    _cadence_panel('Practical Cadences',practical['cadences'],{'xs':12,'xl':6}),
                ],
                spacing=16,
                run_spacing=16,
            ),
        ],
        spacing=18,
    )


def _summary_panel(title,data):
    cadence_count=sum(len(patterns) for patterns in data['cadences'].values())
    return _panel(
        title,
        ft.Icons.TUNE,
        [
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    _stat_tile('Notes',len(data['notes']),'#E0F2FE','#0369A1'),
                    _stat_tile('Chords',len(data['chords']),'#FEF3C7','#92400E'),
                    _stat_tile('Cadence sets',len(data['cadences']),'#FCE7F3','#9D174D'),
                    _stat_tile('Patterns',cadence_count,'#DCFCE7','#166534'),
                ],
                spacing=12,
                run_spacing=12,
            )
        ],
        col=12,
    )


def _spelling_panel(title,icon,data,pill_bg,pill_color,col):
    return _panel(
        title,
        icon,
        [
            _label('Scale Notes'),
            _pill_row(data['notes'],pill_bg,pill_color),
            _label('Triads'),
            _pill_row(data['chords'],'#FFF7ED','#9A3412'),
            _label('Intervals'),
            _distance_table(data['scale']),
        ],
        col=col,
    )


def _cadence_panel(title,cadences,col):
    tiles=[
        _cadence_tile(name,patterns)
        for name,patterns in cadences.items()
    ]
    return _panel(title,ft.Icons.LIBRARY_MUSIC,tiles,col=col)


def _cadence_tile(name,patterns):
    pattern_rows=[
        ft.Container(
            padding=ft.Padding(10,8,10,8),
            bgcolor='#FFFFFF',
            border=_border('#E5E7EB'),
            border_radius=8,
            content=ft.Column(
                controls=[
                    ft.Text(f'Pattern {number}',size=12,weight=ft.FontWeight.W_700,color='#475569'),
                    _pill_row(chords,'#F8FAFC','#0F172A'),
                ],
                spacing=8,
            ),
        )
        for number,chords in patterns.items()
    ]

    return ft.Container(
        bgcolor='#FFFFFF',
        border=_border('#E5E7EB'),
        border_radius=8,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.ExpansionTile(
            title=ft.Text(name,size=14,weight=ft.FontWeight.W_700,color='#0F172A'),
            subtitle=ft.Text(f'{len(patterns)} patterns',size=12,color='#64748B'),
            leading=ft.Icons.KEYBOARD_ARROW_RIGHT,
            tile_padding=ft.Padding(12,0,12,0),
            controls_padding=ft.Padding(12,0,12,12),
            collapsed_bgcolor='#FFFFFF',
            bgcolor='#F8FAFC',
            controls=pattern_rows,
        ),
    )


def _panel(title,icon,controls,col=12):
    return ft.Container(
        col=col,
        padding=ft.Padding(18,16,18,18),
        bgcolor='#FFFFFF',
        border=_border('#DDE4EE'),
        border_radius=8,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon,color='#0F766E',size=22),
                        ft.Text(title,size=18,weight=ft.FontWeight.W_800,color='#111827'),
                    ],
                    spacing=10,
                ),
                *controls,
            ],
            spacing=14,
        ),
    )


def _message_panel(title,message,icon,bgcolor,color):
    return ft.Container(
        padding=ft.Padding(18,16,18,16),
        bgcolor=bgcolor,
        border=_border('#FCA5A5'),
        border_radius=8,
        content=ft.Row(
            controls=[
                ft.Icon(icon,color=color,size=24),
                ft.Column(
                    controls=[
                        ft.Text(title,size=16,weight=ft.FontWeight.W_800,color=color),
                        ft.Text(message,size=13,color=color),
                    ],
                    spacing=2,
                ),
            ],
            spacing=12,
        ),
    )


def _stat_tile(label,value,bgcolor,color):
    return ft.Container(
        col={'xs':6,'md':3},
        padding=ft.Padding(14,12,14,12),
        bgcolor=bgcolor,
        border_radius=8,
        content=ft.Column(
            controls=[
                ft.Text(str(value),size=24,weight=ft.FontWeight.W_800,color=color),
                ft.Text(label,size=12,weight=ft.FontWeight.W_600,color=color),
            ],
            spacing=2,
        ),
    )


def _label(text):
    return ft.Text(text,size=12,weight=ft.FontWeight.W_700,color='#64748B')


def _pill_row(items,bgcolor,color):
    return ft.Row(
        controls=[
            ft.Container(
                padding=ft.Padding(10,6,10,6),
                bgcolor=bgcolor,
                border_radius=8,
                content=ft.Text(str(item),size=13,weight=ft.FontWeight.W_700,color=color,no_wrap=True),
            )
            for item in items
        ],
        wrap=True,
        spacing=8,
        run_spacing=8,
    )


def _distance_table(scale):
    return ft.DataTable(
        columns=[
            ft.DataColumn('Interval'),
            ft.DataColumn('Distance',numeric=True),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f'{left} - {right}',size=13,color='#0F172A')),
                    ft.DataCell(ft.Text(_distance_label(distance),size=13,color='#0F172A')),
                ]
            )
            for (left,right),distance in scale.items()
        ],
        border=_border('#E5E7EB'),
        border_radius=8,
        heading_row_color='#F8FAFC',
        show_bottom_border=True,
        column_spacing=28,
        horizontal_margin=12,
    )


def _distance_label(distance):
    if isinstance(distance,float) and distance.is_integer():
        return str(int(distance))
    return str(distance)


def _border(color):
    side=ft.BorderSide(1,color)
    return ft.Border(side,side,side,side)


if __name__=='__main__':
    ft.run(flet_interface)
#code is optimized and refactored
#I utilized 2 way of showcasing the features...
#one called "theoretical": it focuses for knowledge of music theory usefull for musician
#another called "Practical": it gives a clear and simplified version of notes and chord using enharmonics usefull for instrumentalists
#example: 
# "E#" in theoretical displays as "E#", but in practical displays as "F".

#I have to test the code to be prepared for UI section.
#for combined cadences, let's check the correctency of the knowledge.

#using Figma, I have to create a draft of UI section.
#Then, by using Kivy, create the section for PC and then, for Android.
#There's a lot of exciting sections...
#Hope to reach prefectly all of them.


