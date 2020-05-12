# Ak-auto: Arknights Auto for global ver.


## Requirements
- python installed
- android debugging bridge installed


## Installing dependencies
Run the following command from the source directory
```bash
pip install requirements.txt
```

## How to use
Firstly, go to the stage you want to repeat and open the mission brief with the start button at the bottom right of the screen.

From your terminal run the following command from the source directory
```bash
python main.py
```

### Options available
- serial: your device id or remote adb endpoint
- cycles: number of times to repeat stage
- adb: path to adb executable

Can be also found using
```bash
python main.py --help
```
Example options usage
```bash
python main.py -c 20 -s abcdef --adb C:\..
```