import os
import re
import mido
from mido import MidiFile, MidiTrack, Message


def generate_chart(song_metadata, bpm_changes, notes, output_path):
    """
    Generates a .chart file for Clone Hero based on song metadata, BPM changes, and notes.
    """
    with open(output_path, 'w', encoding='utf-8') as chart_file:
        # Write [Song] section
        chart_file.write("[Song]\n")
        chart_file.write(f"Name = {song_metadata['name']}\n")
        chart_file.write(f"Artist = {song_metadata['artist']}\n")
        chart_file.write(f"Offset = {song_metadata['offset']}\n")
        chart_file.write(f"Resolution = {song_metadata['resolution']}\n")
        chart_file.write("\n")

        # Write [SyncTrack] section
        chart_file.write("[SyncTrack]\n")
        for tick, bpm in bpm_changes:
            bpm_value = int(bpm * 1000)  # Convert BPM to Clone Hero format
            chart_file.write(f"{tick} = B {bpm_value}\n")
        chart_file.write("\n")

        # Write [ExpertSingle] section
        chart_file.write("[ExpertSingle]\n")
        for tick, note, length in notes:
            chart_file.write(f"{tick} = N {note - 60} {length}\n")  # Convert MIDI pitch to Clone Hero note
        chart_file.write("\n")

    print(f"✅ Successfully generated chart at '{output_path}'!")

def generate_song_ini(song_metadata, output_path):
    """
    Generates a song.ini file for Clone Hero based on song metadata.
    """
    with open(output_path, 'w', encoding='utf-8') as ini_file:
        ini_file.write("[Song]\n")
        ini_file.write(f"Name = {song_metadata['name']}\n")
        ini_file.write(f"Artist = {song_metadata['artist']}\n")
        ini_file.write(f"Offset = {song_metadata['offset']}\n")
        ini_file.write(f"Resolution = {song_metadata['resolution']}\n")
        ini_file.write("MusicStream = song.ogg\n")  # Reference the audio file
    print(f"✅ Successfully generated song.ini at '{output_path}'!")

def process_song(song_path, output_directory, bpm_changes, notes):
    """
    Processes a song input and generates a .chart file and song.ini file.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Song metadata
    song_metadata = {
        "name": os.path.basename(song_path).replace(".ogg", ""),
        "artist": "Unknown Artist",  # Replace with actual artist if available
        "offset": "0",  # Replace with actual offset if available
        "resolution": "192"
    }

    # Generate .chart file
    chart_output = os.path.join(output_directory, song_metadata['name'] + ".chart")
    generate_chart(song_metadata, bpm_changes, notes, chart_output)

    # Generate song.ini file
    ini_output = os.path.join(output_directory, "song.ini")
    generate_song_ini(song_metadata, ini_output)

    print(f"✅ Successfully processed song '{song_path}'!")

input_dir = "charts"
output_dir = "midis"  

