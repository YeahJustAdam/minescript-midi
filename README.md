# minescript-midi
A minescript script that converts midi files into noteblocks played by minecarts

## Prereqisities
1. Python - Python 3.9+ (recommended 3.10 or 3.11)
2. Minescript - developed om 1.21.8
3. Mido - install using pip install mido

## Usage
After the minescript mod is installed. Clone the repo straight into the minecript folder.
Make sure there arent any other jobs running. (do \jobs and if there are do \killjob <id>)
It should look something like this (*are the cloned things):

``minescript/
├── blockpacks
├── system
├── midis*
│   ├── clair.mid
│   ├── fur_elise.mid
│   ├── ...
├── config.txt
├── README.md*
├── stop_midi.py*
├── listen.py*
└── midi.py*``

Then pick a spot, and run "\midi list" or "\midi <the_full_name_of_the_midi> <speed>"
speed can be any number from (0;10>, if you put in zero it will default to one.
enjoy.

If for some reason you'd like to stop before the midi finishes, do "\stop_midi"

If youd like to download more midi's youre free to do so, just download them and pop them into the midis folder :D
