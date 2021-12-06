import os
import sys
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


def removeExifData():
    for root, _, files in os.walk(os.getcwd()):
        if root.split("/")[-1] == "images":
            root += "/"
            break
    for file_name in files:
        try:
            with Image.open(root + file_name) as img:
                img_no_exif = Image.new(img.mode, img.size)
                # Copy the pixel data from img_data.
                img_no_exif.putdata(list(img.getdata()))
                # Save without exif data.
                img_no_exif.save(root + file_name)
        except IOError:
            print("File format not supported!")


def convertDecimalDegrees(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    if direction == "S" or direction == "W":
        decimal_degrees *= -1
    return decimal_degrees


def getLocationUrl(gps_coords):
    dec_deg_lat = convertDecimalDegrees(
        float(gps_coords["GPSLatitude"][0]),
        float(gps_coords["GPSLatitude"][1]),
        float(gps_coords["GPSLatitude"][2]),
        gps_coords["GPSLatitudeRef"],
    )
    dec_deg_lon = convertDecimalDegrees(
        float(gps_coords["GPSLongitude"][0]),
        float(gps_coords["GPSLongitude"][1]),
        float(gps_coords["GPSLongitude"][2]),
        gps_coords["GPSLongitudeRef"],
    )
    return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"


def getExifData(all=False):
    gps_coords = dict()
    for root, _, files in os.walk(os.getcwd()):
        if root.split("/")[-1] == "images":
            root += "/"
            break
    for file_name in files:
        try:
            print(f"\n\n{file_name}\n{'-'*len(file_name)}")
            with Image.open(root + file_name) as image:
                if image._getexif() == None:
                    print("No Exif Data Found")
                    continue
                else:
                    for tag_num, value in image._getexif().items():
                        tag = TAGS.get(tag_num)
                        if tag == "GPSInfo":
                            for key, val in value.items():
                                gps_coords[GPSTAGS.get(key)] = val
                        elif tag in [
                            "Make",
                            "Model",
                            "Software",
                            "DateTime",
                        ]:
                            print(f"{tag}: {value}")
                        elif all:
                            print(f"{tag}: {value}")
                    if gps_coords:
                        location_url = getLocationUrl(gps_coords)
                        print(f"Location URL: {location_url}")
        except IOError:
            print("Error: File format not supported!")
    if len(files) == 0:
        print("Error: You don't have have files in the Images folder.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        getExifData()
    elif len(sys.argv) == 2:
        func = sys.argv[1]
        try:
            locals()[func]()
        except KeyError:
            print("Error: Function not found!")
    elif len(sys.argv) == 3:
        func = sys.argv[1]
        all = True if sys.argv[2] == "all" else False
        try:
            locals()[func](all)
        except TypeError:
            print("Error: Invalid arguments")
        except KeyError:
            print("Error: Function not found!")
    else:
        print("Usage: python tool.py <func>")
