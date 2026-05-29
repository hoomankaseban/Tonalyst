# Tonalyst

Tonalyst is a Python music-theory application with a Flet UI. It turns a root note and a scale form into scale notes, interval distances, tertian triads, and cadence patterns.

I built this project as both a guitarist and a programmer, combining two of my real passions: music and coding. It started as a way to gather my basic music-theory knowledge and connect it with what I know in Python. I have been working on it in my spare time, including the travel time between home and work, as a way to make better use of that time and keep learning.

I also continued coding Tonalyst during wartime in Iran. Working on music and code gave me a place to focus my mind and step away, even for a while, from the heavy feelings caused by war. As my music-theory knowledge grows, I plan to keep improving and expanding the app.

The app shows each result in two ways:

- Theoretical spelling, which keeps the calculated note names.
- Practical spelling, which simplifies notes and chords enharmonically.

The visible app behavior and music logic are intentionally kept the same. The code has been separated into modules so the theory engine, UI, and launcher are easier to understand and maintain.

## Application First Page
<img width="1920" height="1909" alt="app view" src="https://github.com/user-attachments/assets/73b28413-476d-41b8-98f1-c4214029bfb5" />

## Project Structure

```text
Musician/
+-- README.md
+-- Tonalyst.py
+-- musician/
    +-- __init__.py
    +-- app.py
    +-- theory.py
```

- `Tonalyst.py` is the project launcher. Running it starts the Flet app.
- `musician/app.py` contains the Flet interface and UI-specific helpers.
- `musician/theory.py` contains the music-theory engine, enharmonic simplification, cadence generation, and the older command-line helper functions.

## Requirements

- Python 3
- `flet`
- `regex`

Install dependencies with:

```bash
pip install flet regex
```

## Running the App

Run:

```bash
python Tonalyst.py
```

The app opens as **Tonalyst** and lets you choose:

- a root note, such as `C`, `F#`, or `Bb`,
- a scale form from `1` to `6`.

Available scale forms:

| Form | Name |
| --- | --- |
| `1` | Major |
| `2` | Natural Minor |
| `3` | Harmonic Minor |
| `4` | Melodic Minor |
| `5` | Harmonic Major |
| `6` | Melodic Major |

## Music Theory Model

The theory engine starts from the natural note order:

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

It rotates that note order around the selected tonic, then adjusts accidentals until the interval distances match the selected scale form.

Scale formulas:

| Form | Name | Interval Pattern |
| --- | --- | --- |
| `1` | Natural Major | `1, 1, 0.5, 1, 1, 1, 0.5` |
| `2` | Natural Minor | `1, 0.5, 1, 1, 0.5, 1, 1` |
| `3` | Harmonic Minor | `1, 0.5, 1, 1, 0.5, 1.5, 0.5` |
| `4` | Melodic Minor | `1, 0.5, 1, 1, 1, 1, 0.5` |
| `5` | Harmonic Major | `1, 1, 0.5, 1, 0.5, 1.5, 0.5` |
| `6` | Melodic Major | `1, 1, 0.5, 1, 0.5, 1, 1` |

## Main Functions

The core functions live in `musician/theory.py`.

### `scaler(scale, form)`

Builds the requested scale.

- `scale`: root note as a string, such as `C`, `F#`, or `Bb`.
- `form`: scale form code as a string from `1` to `6`.

Returns:

- `desired_scale`: a dictionary of neighboring note pairs and their distances.
- `scale_notes`: the seven notes of the generated scale.

### `scale_harmonization(scale_distances, scale_notes)`

Builds one triad on each scale degree.

Example for C major:

```python
["C", "Dm", "Em", "F", "G", "Am", "B_dim"]
```

### `cadences(scale, scale_form)`

Generates cadence progressions for the selected scale. It maps scale-degree patterns into real chord names.

The returned shape is:

```python
{
    "Cadence Name": {
        1: ["Chord", "Chord", "Chord"],
        2: ["Chord", "Chord", "Chord"],
    }
}
```

### `simplifier(desired_scale, scale_notes, scale_chords, cadence)`

Creates enharmonic-simplified versions of:

- scale notes,
- scale chords,
- cadence chords,
- the scale-distance dictionary.

For example, the practical display may show `F` where the theoretical spelling is `E#`.

## Data Conventions

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



## Future Ideas

- Add more advanced and compositional features. 
- Add guitar fretboard mapping.
- Add more chord types and modes.
