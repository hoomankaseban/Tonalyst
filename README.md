# Musician

Musician is a Python music-theory experiment that turns a root note and a scale form into:

- the scale notes,
- the interval distances between each note,
- the tertian triads built on every scale degree,
- many cadence patterns translated into real chord names,
- two different displays: a theoretical spelling and an enharmonic-simplified practical spelling.

The project is currently a command-line program in `TheMusic.py`. The long-term idea, noted in the source, is to use this theory engine as the base for a UI and eventually for mapping scales on the guitar fretboard.

## Part 1: Music Theory View

This section explains the musical idea behind the code.

### Core Idea

The program treats a scale as a chain of interval distances. Instead of hard-coding every scale in every key, it starts from the natural note order:

```text
C D E F G A B
```

and the natural major distance pattern:

```text
C-D = 1
D-E = 1
E-F = 0.5
F-G = 1
G-A = 1
A-B = 1
B-C = 0.5
```

Then it rotates that note order around the requested tonic and adjusts the accidentals until the distances match the chosen scale form.

In this project:

- `1` means Natural Major.
- `2` means Natural Minor.
- `3` means Harmonic Minor.
- `4` means Melodic Minor.
- `5` means Harmonic Major.
- `6` means Melodic Major.

The scale formulas used by the code are:

| Form | Name | Interval Pattern |
| --- | --- | --- |
| `1` | Natural Major | `1, 1, 0.5, 1, 1, 1, 0.5` |
| `2` | Natural Minor | `1, 0.5, 1, 1, 0.5, 1, 1` |
| `3` | Harmonic Minor | `1, 0.5, 1, 1, 0.5, 1.5, 0.5` |
| `4` | Melodic Minor | `1, 0.5, 1, 1, 1, 1, 0.5` |
| `5` | Harmonic Major | `1, 1, 0.5, 1, 0.5, 1.5, 0.5` |
| `6` | Melodic Major | `1, 1, 0.5, 1, 0.5, 1, 1` |

### Accidentals and Scale Spelling

The code tries to preserve correct theoretical spelling. For example, if the note letter should be some form of `E`, the theoretical display may keep `E#` instead of immediately replacing it with `F`.

That is why the program has two display modes:

- The theoretical display keeps the calculated note spelling.
- The practical display simplifies notes and chords enharmonically.

Example idea:

```text
Theoretical: E#
Practical:   F
```

This is useful because theory and instrumental practice sometimes prefer different spellings. A composer or theory student may care about the letter function of the note, while an instrumentalist may prefer the cleaner physical note name.

### Tertian Harmony

After building the scale, the program harmonizes it by stacking thirds inside the scale. For each scale degree, it measures:

- the third above the root,
- the fifth above the root.

Then it decides the triad quality:

| Third | Fifth | Chord Quality | Code Suffix |
| --- | --- | --- | --- |
| Major third | Perfect fifth | Major | empty suffix, for example `C` |
| Minor third | Perfect fifth | Minor | `m`, for example `Dm` |
| Major third | Augmented fifth | Augmented | `_aug`, for example `C_aug` |
| Minor third | Diminished fifth | Diminished | `_dim`, for example `B_dim` |

For example, C natural major becomes:

```text
C, Dm, Em, F, G, Am, B_dim
```

### Cadences

The cadence engine converts scale-degree patterns into chord progressions.

The code includes four basic cadence families:

- Authentic cadences.
- Plagal cadences.
- Half cadences.
- Deceptive cadences.

It also includes combined and borrowed-color cadence patterns. These patterns may alter a degree with an accidental or change the chord quality. Examples of the internal pattern notation:

| Pattern Token | Meaning |
| --- | --- |
| `4` | Use the fourth chord from the current harmonized scale |
| `7bM` | Take degree 7, lower it, and make it major |
| `4m` | Take degree 4 and make it minor |
| `2D` | Take degree 2 and make it diminished |
| `6bA` | Take degree 6, lower it, and make it augmented |
| `7NM` | Use degree 7 from the natural minor form |

For harmonic minor and melodic minor cadences, the code can also borrow chords from natural minor when the pattern explicitly asks for `NM`.

### Why This Matters

The main musical goal is to make theory programmable:

1. Choose a tonic.
2. Choose a scale form.
3. Build the correctly spelled scale.
4. Harmonize every degree.
5. Generate many cadence possibilities.
6. Show both the theoretical result and a practical simplified result.

This gives the project a foundation for future tools such as:

- chord-progression exploration,
- composition helpers,
- scale and cadence study,
- guitar fretboard mapping,
- a desktop or mobile UI.

## Part 2: Developer README

### Project Structure

```text
Musician/
+-- README.md
+-- TheMusic.py
```

### Requirements

- Python 3
- The third-party `regex` package

Install the dependency with:

```bash
pip install regex
```

### Running the Program

Run:

```bash
python TheMusic.py
```

The program asks for:

1. A root note, such as `C`, `D`, `F#`, or `Bb`.
2. A scale form number from `1` to `6`.

Example input:

```text
Please enter your desired note:
C
Please specify your desired scale:
1
```

For `C` and `1`, the program builds C natural major, harmonizes it, generates cadences, and prints both theoretical and practical displays.

### Function Reference

#### `scaler(scale, form)`

Builds the requested scale.

Parameters:

- `scale`: root note as a string, such as `C`, `F#`, or `Bb`.
- `form`: scale form code as a string from `1` to `6`.

Returns:

- `desired_scale`: a dictionary where each key is a pair of neighboring notes and each value is their distance.
- `scale_notes`: the seven notes of the generated scale.

Example return shape:

```python
{
    ("C", "D"): 1,
    ("D", "E"): 1,
    ("E", "F"): 0.5,
    ("F", "G"): 1,
    ("G", "A"): 1,
    ("A", "B"): 1,
    ("B", "C"): 0.5,
}
```

#### `update_scale(scale_dict, current_tuple, signature, tuples_priority_index, difference)`

Helper used by `scaler()`.

It applies `#` or `b` changes to the second note of the current interval and then updates the next interval so the scale remains connected. This is how the scale builder adjusts note spelling until the interval pattern matches the selected form.

#### `scale_harmonization(scale_distances, scale_notes)`

Builds one triad on each scale degree.

Parameters:

- `scale_distances`: the interval dictionary returned by `scaler()`.
- `scale_notes`: the note list returned by `scaler()`.

Returns:

- A list of chord names, such as:

```python
["C", "Dm", "Em", "F", "G", "Am", "B_dim"]
```

#### `chord_quality(octave)`

Calculates the quality of a triad.

It measures the distance from the chord root to the third and fifth, then returns the chord suffix:

- `""` for major,
- `"m"` for minor,
- `"_aug"` for augmented,
- `"_dim"` for diminished.

#### `chord_converter(chord, desired_form, signature)`

Changes a chord's root accidental and/or quality.

Examples from the source comments:

```python
chord_converter("C#_dim", "A", "b")  # "C_aug"
chord_converter("C#_dim", "", "b")   # "C_dim"
```

Accepted quality conversion codes:

| Code | Output Quality |
| --- | --- |
| `M` | Major |
| `m` | Minor |
| `D` | Diminished |
| `A` | Augmented |

#### `cadences(scale, scale_form)`

Generates cadence progressions for the selected scale.

It first builds the scale, harmonizes it, then maps cadence-degree patterns into actual chord names.

Returns:

- A nested dictionary:

```python
{
    "Cadence Name": {
        1: ["Chord", "Chord", "Chord"],
        2: ["Chord", "Chord", "Chord"],
    }
}
```

The function contains different cadence pattern sets for:

- natural major,
- natural minor,
- harmonic minor,
- melodic minor,
- harmonic major,
- melodic major,
- combined major cadences,
- combined minor cadences,
- Picardy-third cadences.

#### `theoretical_display(desired_scale, scale_notes, scale_name, form, scale_chords, cadence)`

Prints the full result using the theoretical note spellings produced by the scale engine.

This display is useful when the exact theoretical function of a note matters.

#### `enharmonics_simplifier(container)`

Simplifies a list of notes or chords by converting repeated sharps or flats to a cleaner enharmonic spelling.

It uses two chromatic maps:

```python
["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
```

#### `simplifier(desired_scale, scale_notes, scale_chords, cadence)`

Applies `enharmonics_simplifier()` to:

- scale notes,
- scale chords,
- cadence chords,
- the displayed scale-distance dictionary.

Returns simplified versions of all those structures.

#### `practical_display(desired_scale, scale_notes, scale_name, form, scale_chords, cadence)`

Prints the enharmonic-simplified result.

This display is useful for instrumentalists because the names are usually easier to read and play.

#### `interface()`

The command-line entry point.

It:

1. Reads the root note from the user.
2. Reads the scale form from the user.
3. Calls `scaler()`.
4. Calls `scale_harmonization()`.
5. Calls `cadences()`.
6. Prints the theoretical display.
7. Prints the practical display.

At the bottom of `TheMusic.py`, `interface()` is called directly, so the program starts immediately when the file is executed.

### Data Conventions

Notes are represented as strings:

```python
"C"
"F#"
"Bb"
```

Chord qualities are represented by suffixes:

```python
"C"      # C major
"Cm"     # C minor
"C_aug"  # C augmented
"C_dim"  # C diminished
```

Intervals are measured in tones:

```python
1    # whole step
0.5  # half step
1.5  # augmented-second-sized step
```

Cadence patterns are first written as scale-degree formulas, then converted into chord names.

### Current Limitations

- The program is currently interactive only.
- There is no separate test suite yet.
- `interface()` runs automatically on import, so importing `TheMusic.py` from another file will also start the command-line prompt.
- Input validation is minimal. Invalid note names or form codes may raise errors.
- The project currently focuses on seven-note scale forms and triads.

### Future Ideas

- Add automated tests for scales, chords, enharmonic simplification, and cadences.
- Move the `interface()` call behind `if __name__ == "__main__":`.
- Add stronger input validation and clearer error messages.
- Add a graphical UI.
- Add guitar fretboard mapping.
- Add more chord types, inversions, seventh chords, and modes.

## License

No license file is currently included. Add one before publishing or sharing the project publicly.
