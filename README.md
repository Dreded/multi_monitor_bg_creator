# Mult-Monitor Background Image Resizer
Uses OpenCV to resize wallpaper for use on multimonitors.

This is meant for when you have 2,3 or more monitors with different(or same) resolutions
but would like to place a multi-monitor image on them and have it displayed correctly.
it defaults to a 3 monitor setup where the 2 side monitors are 1920x1080 and the center is 2560x1440.
the images can easily be found by searching google for `5760x1080 background [insert search terms here]`  
  
However any image size will work... see example at bottom for how it handles this.
  
Currently only for monitors arranged horizontally.(if you have a suggestion for vertical let me know)

## Install
* `poetry install`

## Run
* python main.py [image_file]
* * It will show you the output before it saves, simply press any key on preview to close it.(TODO: allow not saving)
* * image_file can be any size it will split into desired_resolution[x] images then resize/add borders to top/bottom as needed.
* for help `python main.py -h`  

```
usage: main.py [-h] [-dr DESIRED_RESOLUTION] [-o OUTPUT] image

positional arguments:
  image                 Image to split up

options:
  -h, --help            show this help message and exit
  -dr DESIRED_RESOLUTION, --desired_resolution DESIRED_RESOLUTION
                        An array of the desired resolutions
                        default=[[1920,1080],[2560,1440],[1920,1080]]
  -o OUTPUT, --output OUTPUT
                        Output filename eg '/tmp/image.jpg'
```

## Package to Binary
`poetry install --with dev`  
`pyinstaller --onefile main.py`  
binary will be in dist/main[.exe]

## Example Output
### Vertical res larger than all monitors...
```
Splitting into 3 images from 7680 x 2160
Image 0: Desired = [1920, 1080]  Current = [2560, 2160]
        Resizing...
        Resized to: [1920, 1080]
        Adding Border to Height(centered)

Image 1: Desired = [2560, 1440]  Current = [2560, 2160]
        Resizing...
        Resized to: [2560, 1440]

Image 2: Desired = [1920, 1080]  Current = [2560, 2160]
        Resizing...
        Resized to: [1920, 1080]
        Adding Border to Height(centered)
```
![Oversized](example/example_2560xoversize_6400x1440.jpg)

### Any Size image should work...
#### Here is a weirdly sized single monitor bg image(actually produces a neat result)
```
Splitting into 3 images from 1536 x 1024
Image 0: Desired = [1920, 1080]  Current = [512, 1024]
        Resizing...
        Resized to: [1920, 1080]
        Adding Border to Height(centered)
Image 1: Desired = [2560, 1440]  Current = [512, 1024]
        Resizing...
        Resized to: [2560, 1440]
Image 2: Desired = [1920, 1080]  Current = [512, 1024]
        Resizing...
        Resized to: [1920, 1080]
        Adding Border to Height(centered)
```
![Female_Hacker](example/female_hacker_6400x1440.jpg)



