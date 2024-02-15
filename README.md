# Mult-Monitor Background Image Resizer
This is meant for when you have 2,3 or more monitors with different resolutions but would like to place a multi-monitor image on them and have it displayed correctly.

## Install
* `poetry install`

## Run
* python main.py [image_file]
* for help `python main.py -h`
it defaults to a 3 monitor setup where the 2 side monitors are 1920x1080 and the center is 2560x1440.
the images can easily be found by searching google for `5760x1080 background [insert search terms here]`

## Package to Binary
`poetry install --with dev`
`pyinstaller --onefile main.py`
binary will be in dist/main[.exe]
