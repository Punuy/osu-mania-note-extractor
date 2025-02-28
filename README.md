# osu!mania Notes Explanation

## Overview
This Python program processes osu!mania `.osu` files by:
- **Parsing hit objects** from the `[HitObjects]` section.
- **Grouping notes** by how many occur at the same time (single, double, triple, or quad patterns).
- **Saving categorized notes** into separate text files.

---

## Code Breakdown

### **`parse_hit_objects(osu_file)`**

**Purpose:** Reads the `.osu` file and extracts hit objects (notes).

```python
hit_objects = []
parsing = False
```
- Initializes an empty list to store notes.
- A flag `parsing` starts `False` and turns `True` once `[HitObjects]` is found.

**File reading:**

```python
with open(osu_file, 'r', encoding='utf-8') as file:
```
- Opens the file with UTF-8 encoding for safe character handling.

**Parsing logic:**

```python
if line == '[HitObjects]':
    parsing = True
    continue
```
- Skips all lines until it reaches `[HitObjects]`.

```python
parts = line.split(',')
if len(parts) >= 3:
    x = int(parts[0])
    y = int(parts[1])
    time = int(parts[2])
    hit_objects.append((x, y, time, line))
```
- Splits the line into columns.
- Extracts **x** (column position), **y** (always 192 for osu!mania), and **time** (when the note occurs).
- Saves the original line for later.

**Result:**
Returns a list of tuples:

```python
[(64, 192, 3634, '64,192,3634,1,0,0:0:0:0:'), ...]
```

---

### **`detect_note_patterns(hit_objects)`**

**Purpose:** Groups hit objects by time and categorizes them by note pattern.

**Grouping notes:**

```python
patterns = {}
for x, y, time, original in hit_objects:
    if time not in patterns:
        patterns[time] = []
    patterns[time].append(original)
```
- Uses a dictionary `patterns` where:
  - **Key**: time (when the note happens)
  - **Value**: list of note lines occurring at that time

**Counting notes:**

```python
categorized_patterns = {'single': [], 'double': [], 'triple': [], 'quad': []}
```
- Initializes empty lists for each note pattern.

```python
if count == 1:
    categorized_patterns['single'].extend(notes)
elif count == 2:
    categorized_patterns['double'].extend(notes)
elif count == 3:
    categorized_patterns['triple'].extend(notes)
elif count >= 4:
    categorized_patterns['quad'].extend(notes)
```
- Checks how many notes occur at the same time and assigns them to the correct category.

**Result:**
Returns a dictionary:

```python
{
  'single': ['64,192,3634,1,0,0:0:0:0:'],
  'double': ['64,192,3934,1,0,0:0:0:0:', '192,192,3934,1,0,0:0:0:0:'],
  ...
}
```

---

### **`save_patterns_to_files(patterns)`**

**Purpose:** Saves note patterns into separate text files.

**File creation:**

```python
filename = f"{pattern}_notes.txt"
```
- Creates file names like:
  - `single_notes.txt`
  - `double_notes.txt`

**Writing to files:**

```python
with open(filename, 'w', encoding='utf-8') as file:
    file.write("[HitObjects]\n")
    file.write("\n".join(notes) + "\n")
```
- Each file starts with `[HitObjects]`.
- Writes all notes for that pattern, one per line.

**Result:**
- **single_notes.txt**:

```plaintext
[HitObjects]
64,192,3634,1,0,0:0:0:0:
```

- **double_notes.txt**:

```plaintext
[HitObjects]
64,192,3934,1,0,0:0:0:0:
192,192,3934,1,0,0:0:0:0:
```

---

### **`main()`**

**Purpose:** Runs the whole process.

```python
osu_file = input("Enter the path to the osu!mania file: ")
```
- Prompts the user for the `.osu` file path.

```python
hit_objects = parse_hit_objects(osu_file)
patterns = detect_note_patterns(hit_objects)
save_patterns_to_files(patterns)
```
- Extracts notes, categorizes them, and saves them to files.

**Result:**
When run, it asks for the file path and generates the output files:

```
Enter the path to the osu!mania file: path/to/your/file.osu
Saved single notes to single_notes.txt
Saved double notes to double_notes.txt
...
```

---

## How to Run
1. Save the program as `osu_mania_parser.py`.
2. Run it in the terminal:

```bash
python osu_mania_parser.py
```
3. Enter the path to your `.osu` file.
4. Check the generated `single_notes.txt`, `double_notes.txt`, etc.

---

## Next Steps
- **Add hold note support:** Extend the parser to handle `endTime` for long notes.
- **Customize output:** Allow the user to specify output folder or filenames.
- **Visualization:** Display note patterns in a simple terminal graphic.
