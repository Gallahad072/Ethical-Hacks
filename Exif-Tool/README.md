# EXIF Tool

This [program](exif.py) find or remove valuable EXIF data from images.

## Requirements

Install Pillow with pip:

`pip install Pillow`

I am using python 3.9.8

## Functions

`getExifData(all=False)`

> This is the main function.
>
> Prints EXIF data for every image in the images folder.
>
> If 'all' is set to True, all data will be displayed, otherwise only crucial data will be displayed.

`removeExifData()`

> Removes EXIF data from all the images in the image folder.

## Use

**Run the Main Program**

Type in the terminal:

`python exif.py`

**Run Specific Function**

Type in the terminal:

`python exif.py <function name> <all?>`

Only the function name is required but, if 'all' is put after 'getExifData', 'all' will be set to True.

For example:

`python exif.py getExifData all`
