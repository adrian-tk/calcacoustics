How-to guides are directions that take the reader through the steps 
required to solve a real-world problem. How-to guides are goal-oriented.
# How To install CalcAcoustics

CalcAcoustics is written in Python using Kivy as GUI, so  it shall work in many place You can install Python.
Especially PC on Linux or Windows, IOS, Android. Rpi or other ARM shall also work.
At this time no binaries are available, so only the Python scripts are avaiable.
## Python scripts
1. Download files using git:
`git clone git@github.com:adrian-tk/calcacoustics.git`
2. In calcacoustic directory create a virtual environment and activate it:
`python3 -m venv env`
`source env/bin/activate`
3. Install all requirements with pip:
`pip install -r requirements.txt`
4. Run script:
`./calcacoustics.py` or click it in windows manager
## Android
### Build from script
At this time there is no ready binaries, You can build them using buildozer
1. Get all Python script as in Python scirpts section
2. export path
`export PATH=$PATH:~/.local/bin/`
3. build:
`buildozer -v android`
Binaries shall be in ./bin directory

# How To Calculate EBP?
TODO
In Speaker part put a xx and axx
EBP will be in EBP label

# How To decide which enclosure is the best for the speaker
TODO
EBP and stuff

