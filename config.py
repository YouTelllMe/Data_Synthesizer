import os
from collections.abc import MutableSequence


CURR_DIR = os.getcwd()
DATA_PATH: str = os.path.join(CURR_DIR, "data", "Data_for_Synth_Data_Candidates.xlsx") # Path of data
TARGET_SHEET: str | int | None | MutableSequence = 0 # Sheet name of interest

SAVE_SYNTH_PATH: str = os.path.join(CURR_DIR, "models", "my_synthesizer.pkl")
SAVE_META_PATH: str = os.path.join(CURR_DIR, "models", "my_metadata_v1.json")


#==================================================================================================#
"EX USAGE"

"TARGET_SHEET"
#TARGET_SHEET = "Sheet1" -> sheet named "Sheet1"
#TARGET_SHEET = [0, 1, 2, 3] -> sheet index 0, 1, 2, 3
#TARGET_SHEET = [0, "Sheet1", 2, 3] -> sheet index 0, 2, 3 and sheet named "Sheet1"