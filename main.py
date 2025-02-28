import re

def parse_hit_objects(osu_file):
    hit_objects = []
    parsing = False
    
    with open(osu_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line == '[HitObjects]':
                parsing = True
                continue
            if parsing and line == '':
                break
            if parsing:
                parts = line.split(',')
                if len(parts) >= 3:
                    x = int(parts[0])
                    y = int(parts[1])
                    time = int(parts[2])
                    hit_objects.append((x, y, time, line))
    return hit_objects

def detect_note_patterns(hit_objects):
    patterns = {}
    
    for x, y, time, original in hit_objects:
        if time not in patterns:
            patterns[time] = []
        patterns[time].append(original)
    
    categorized_patterns = {'single': [], 'double': [], 'triple': [], 'quad': []}
    
    for time, notes in patterns.items():
        count = len(notes)
        if count == 1:
            categorized_patterns['single'].extend(notes)
        elif count == 2:
            categorized_patterns['double'].extend(notes)
        elif count == 3:
            categorized_patterns['triple'].extend(notes)
        elif count >= 4:
            categorized_patterns['quad'].extend(notes)
    
    return categorized_patterns

def save_patterns_to_files(patterns):
    for pattern, notes in patterns.items():
        filename = f"{pattern}_notes.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("[HitObjects]\n")
            file.write("\n".join(notes) + "\n")
        print(f"Saved {pattern} notes to {filename}")

def main():
    osu_file = input("Enter the path to the osu!mania file: ")
    hit_objects = parse_hit_objects(osu_file)
    patterns = detect_note_patterns(hit_objects)
    save_patterns_to_files(patterns)
    
if __name__ == '__main__':
    main()
