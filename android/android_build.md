## General info
Version for Android is build using buildozer

## Preparing enviroment
 - linux
 - venv is not necessery but higly recommended
 - installed zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
 - buildozer need main.py as a main file

`ln -s calcacoustics.py main.py`

 - install ccache to save data from previous compilation

`sudo aptitude install ccache`

### build, copy on mobile, and run

in mobile turn on USB debugging and installing software via USB

`buildozer android debug deploy run`

### logging from terminal

`adb logcat -s "python"`
