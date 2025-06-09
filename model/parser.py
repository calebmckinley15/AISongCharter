import os
from pydub import AudioSegment


def generate_chart(song_metadata, bpm_changes, notes, output_path):
    """
    Generates a .chart file for Clone Hero based on song metadata, BPM changes, and notes.
    """
    with open(output_path, 'w', encoding='utf-8') as chart_file:
        # Write [Song] section
        chart_file.write("[Song]\n{\n")
        chart_file.write(f' Name = "{song_metadata['Name']}"\n')
        chart_file.write(f' Artist = "{song_metadata['Artist']}"\n')
        chart_file.write(f' Album = "{song_metadata['Album']}"\n')
        chart_file.write(f' Genre = "{song_metadata['Genre']}"\n')
        chart_file.write(f' Year = "{song_metadata['Year']}"\n')
        chart_file.write(f' Charter = ", {song_metadata['Charter']}"\n')
        chart_file.write(f" Resolution = {int(song_metadata['Resolution'])}\n")
        chart_file.write(f" Difficulty = {int(song_metadata['Difficulty'])}\n")
        chart_file.write(f" Offset = {float(song_metadata['Offset'])}\n")
        chart_file.write(f" Preview_start = {float(song_metadata['Preview_start'])}\n")
        chart_file.write(f" Preview_end = {float(song_metadata['Preview_end'])}\n")
        chart_file.write(f' MusicStream = "{song_metadata['MusicStream']}"\n')
        chart_file.write("}\n\n")

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

def generate_song_ini(song_metadata, output_path, song_length):
    """
    Generates a song.ini file for Clone Hero based on song metadata.
    """
    with open(output_path, 'w', encoding='utf-8') as ini_file:
        ini_file.write("[song]\n")
        ini_file.write(f"name = {song_metadata['Name']}\n")
        ini_file.write(f"artist = {song_metadata['Artist']}\n")
        ini_file.write(f"album = {song_metadata['Album']}\n")
        ini_file.write(f"genre = {song_metadata['Genre']}\n")
        ini_file.write(f"year = {song_metadata['Year']}\n")
        ini_file.write(f"song_length = {song_length}\n")
        ini_file.write(f"charter = {song_metadata['Charter']}\n")
        ini_file.write(f"diff_guitar = {song_metadata['Difficulty']}\n")
        ini_file.write(f"preview_start_time = {float(song_metadata['Preview_start']):.2f}\n")
        ini_file.write(f"delay = {float(song_metadata['Offset']):.2f}\n")
        ini_file.write("icon = Untitled\n")  # Default icon
        ini_file.write("playlist_track = \n")  # Empty by default
        ini_file.write("track = \n")  # Empty by default
        ini_file.write("album_track = \n")  # Empty by default
        ini_file.write("loading_phrase = \n")  # Empty by default
    print(f"✅ Successfully generated song.ini at '{output_path}'!")

def get_song_info():
    """
    Prompts the user to input song meta and returns it as a dictionary.
    """
    print("Please enter the song data (press Enter to use default values):")
    metadata = {
        "Name": input("Song Name (default: 'Unknown Song'): ") or "Unknown Song",
        "Artist": input("Artist Name (default: 'Unknown Artist'): ") or "Unknown Artist",
        "Album": input("Album Name (default: 'Unknown Album'): ") or "Unknown Album",
        "Genre": input("Genre (default: 'Unknown'): ") or "Unknown",
        "Year": input("Year (default: '0'): ") or "0",
        "Charter": input("Charter Name (default: 'Unknown Charter'): ") or "Unknown Charter",
        "Resolution": input("Resolution (default: '192'): ") or "192",
        "Difficulty": input("Difficulty (default: '0'): ") or "0",
        "Offset": input("Offset (default: '0'): ") or "0",
        "Preview_start": input("Preview Start (default: '0'): ") or "0",
        "Preview_end": input("Preview End (default: '0'): ") or "0",
        "MusicStream": input("Music Stream (default: 'song.ogg'): ") or "song.ogg"
    }
    return metadata

def process_song(song_path, output_directory, bpm_changes, notes):
    """
    Processes a song input and generates a .chart file and song.ini file.
    Supports both .ogg and .mp3 formats.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Detect file extension and extract song name
    file_extension = os.path.splitext(song_path)[1].lower()
    if file_extension not in ['.ogg', '.mp3']:
        raise ValueError("Unsupported file format. Please provide a .ogg or .mp3 file.")
    
    song_name = os.path.basename(song_path).replace(file_extension, "")

    if file_extension == ".mp3":
        print(f"Converting {song_name}.mp3 to .ogg format...")
        audio = AudioSegment.from_mp3(song_path)
        song_path = os.path.join(output_directory, f"{song_name}.ogg")
        audio.export(song_path, format="ogg")
        print(f"✅ Converted to '{song_path}'")

    # Get song length
    audio = AudioSegment.from_file(song_path)
    song_length = len(audio)

    # Song metadata
    song_metadata = get_song_info()
    song_metadata["MusicStream"] = "song.ogg"  # Reference the audio file in song.ini

    # Generate .chart file
    chart_output = os.path.join(output_directory, "notes.chart")
    generate_chart(song_metadata, bpm_changes, notes, chart_output)

    # Generate song.ini file
    ini_output = os.path.join(output_directory, "song.ini")
    generate_song_ini(song_metadata, ini_output, song_length)

    print(f"✅ Successfully processed song '{song_path}'!")

song_path = "song/song.ogg"
output_directory = "output_songs"

bpm_changes = [(0, 120), (480, 140)]  # Example BPM changes
notes = [(0, 60, 192), (192, 62, 192)]  # Example notes

process_song(song_path, output_directory, bpm_changes, notes)
