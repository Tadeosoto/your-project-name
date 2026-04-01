import os  # file path utilities

# Added: simple persistent high score using a text file in the project folder
_HIGHSCORE_FILENAME = "highscore.txt"  # file that stores the single best score

def _path() -> str:  # resolve absolute path for the score file
    # store alongside the game files
    return os.path.join(os.path.dirname(__file__), _HIGHSCORE_FILENAME)  # same folder as code

def load_high_score() -> int:  # read and parse the stored high score
    try:
        with open(_path(), "r", encoding="utf-8") as f:  # open file for reading
            return int(f.read().strip() or "0")  # parse integer; default 0 on empty
    except (FileNotFoundError, ValueError, OSError):  # if missing/corrupt/unreadable
        return 0  # treat as 0 so the game continues

def save_high_score(score: int) -> None:  # write the latest best score
    try:
        with open(_path(), "w", encoding="utf-8") as f:  # open file for writing
            f.write(str(max(0, int(score))))  # clamp to non-negative and persist
    except OSError:
        # fail silently; game should not crash if disk is not writable
        pass  # ignore write errors

