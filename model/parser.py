import os
import re
import mido
from mido import MidiFile, MidiTrack, Message

def parse_chart(chart_path):
    """Parses a .chart file and extracts BPM and note data."""
    with open(chart_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    bpm_changes = []
    notes = []
    resolution = 192  # Default tick resolution
    tick_multiplier = resolution / 192  # Scales the chart's resolution properly

    in_sync_track = False
    in_expert_track = False

    for line in lines:
        line = line.strip()

        # Get resolution
        if "Resolution =" in line:
            resolution = int(re.findall(r'\d+', line)[0])
            tick_multiplier = resolution / 192
        
        # Start SyncTrack (BPM changes)
        if line == "[SyncTrack]":
            in_sync_track = True
            continue
        if line.startswith("[") and line != "[SyncTrack]":
            in_sync_track = False

        # BPM Change
        if in_sync_track and "= B " in line:
            match = re.match(r"(\d+) = B (\d+)", line)
            if match:
                tick, bpm = map(int, match.groups())
                bpm_changes.append((tick, bpm / 1000))  # Convert back from B * 1000

        # Start Expert Guitar Track
        if line == "[ExpertSingle]":
            in_expert_track = True
            continue
        if line.startswith("[") and line != "[ExpertSingle]":
            in_expert_track = False

        # Notes Parsing
        if in_expert_track and "N " in line:
            match = re.match(r"(\d+) = N (\d+) (\d+)", line)
            if match:
                tick, note, length = map(int, match.groups())
                note_midi = 60 + note  # Convert to MIDI pitch (Middle C = 60)
                notes.append((tick, note_midi, length))

    return bpm_changes, notes, resolution

def chart_to_midi(chart_path, midi_output):
    """Converts .chart data to MIDI format and saves it."""
    bpm_changes, notes, resolution = parse_chart(chart_path)

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Set default tempo (first BPM change)
    if bpm_changes:
        first_tick, first_bpm = bpm_changes[0]
        tempo = mido.bpm2tempo(first_bpm)
        track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=first_tick))

    # Add BPM changes
    for tick, bpm in bpm_changes:
        tempo = mido.bpm2tempo(bpm)
        track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=tick))

    # Add Notes
    for tick, note, length in notes:
        track.append(Message('note_on', note=note, velocity=64, time=tick))
        track.append(Message('note_off', note=note, velocity=64, time=tick + length))

    # Save MIDI file
    mid.save(midi_output)
    print(f"✅ Successfully converted '{chart_path}' to '{midi_output}'!")

def process_directory(input_directory, output_directory):
    """Processes all .chart files in a directory and converts them to .mid files."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file in os.listdir(input_directory):
        if file.endswith(".chart"):
            chart_path = os.path.join(input_directory, file)
            midi_output = os.path.join(output_directory, file.replace(".chart", ".mid"))
            chart_to_midi(chart_path, midi_output)

input_dir = "charts"
output_dir = "midis"  

process_directory(input_dir, output_dir)

