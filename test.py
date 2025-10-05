SOUND_FILE = "scary_sound.mp3"

def play_sound():
    """Play scary sound via mpg123 command-line player."""
    subprocess.run(["mpg123", "-q", SOUND_FILE])

if __name__ == "__main__":
    play_sound()