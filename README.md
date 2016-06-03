# NEUR325
Neuroscience Auditory Experiment
Materials designed to run neuroscience auditory memory experiment, using the OpenSesame experiment builder.

**Experiment**
  * The experiment folder contains two OpenSesame programs, behavioral and eeg. Both programs run the same experiment, but the eeg one contains an additional plug-in that sends information to the LabScribe EEG recording program, which must be running concurrently.
  * Main components of experiment are as follows:
    * Video (stimuli presented to subject)
    * Experimental task (nap or distractor task for 20 min., not in the program)
    * Multiple Choice content questions
    * Practice response rounds
    * Experimental response rounds
    * End

**Audio Files**
  * The experiment tests auditory memory of the previously presented stimuli, so audio files needed to be generated for the experiment
  * `practicelist.txt` and `pythonlist.txt` are the practice response and experimental response word lists respectively, and are taken into `gen_audio_files.py`, which uses gTTS to generate audio files of the word list. The audio files are stored into the folder `audio_files`.
   
**Data Extraction**
  * Data recorded by the OpenSesame experiment run is stored in csv files, but they contain far more data than is necessary. `data_analyzer.py` reads in the csv files from a folder containing all subject data files, extracts the relevant information, and prints out the results into a text file.
