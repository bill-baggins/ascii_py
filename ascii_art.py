
import PIL
import os
import sys

from PIL import Image
from math import floor
from typing import Generator


ASCII_NORMAL = u"█▓▒░$$░▒▓█"
ASCII_INVERT = ASCII_NORMAL[::-1]
CTA = 255//len(ASCII_NORMAL)


def ascii_matrix_of(image_name: str,
                    ascii_string: str,
                    new_width: int) -> Generator:
    """
    Generator function that turns the image into a 2d matrix of ASCII
    characters. To preprocess the image, it resizes it proportional to the
    user-given width. It then loops through the width and height of the image
    and yields an ASCII value.
    """

    filename = f"images/{image_name}"
    im = Image.open(filename)
    wpercent = (new_width / float(im.size[0]))
    hsize = int((float(im.size[1]) * float(wpercent)))
    im = im.resize((new_width, hsize), PIL.Image.ANTIALIAS)

    for y in range(im.size[1]):
        for x in range(im.size[0]):
            rgb = im.getpixel((x, y))
            if isinstance(rgb, int):
                continue
            rpixel, gpixel, bpixel = 0.330*rgb[0], 0.587*rgb[1], 0.083*rgb[2]
            rpixel = ascii_string[floor(rpixel / CTA)-1]
            gpixel = ascii_string[floor(gpixel / CTA)-1]
            bpixel = ascii_string[floor(bpixel / CTA)-1]
            yield f"{rpixel}{gpixel}{bpixel}"
        yield "\n"
    im.close()


def get_user_input(image_width: int, ascii_string: str) -> None:
    min_size = 50
    max_size = 340

    while ascii_string == "" and image_width == 0:
        try:
            image_width = int(input("Enter in the width for your image (default: 50; max 340):\n"))
            if image_width > max_size or image_width < min_size:
                print(f"Invalid input. Type a value between {min_size} and {max_size} next time.")
                continue
        except ValueError:
            print(f"Invalid input. Type a value between {min_size} and {max_size} next time.")
            continue

        ascii_string = input("Do you want your image(s) to be inverted? Y/N\n")
        if ascii_string.lower() == "y":
            ascii_string = ASCII_INVERT
        elif ascii_string.lower() == "n":
            ascii_string = ASCII_NORMAL
        else:
            continue


def main():
    image_width = 0     # User-inputted value.
    ascii_string = ""   # User-inputted value.

    relative_path = "./images"
    valid_file_types = (".jpg", ".png", ".bmp")
    image_names = os.listdir(relative_path)

    # Check for any invalid file type
    for i, image in enumerate(image_names):
        if image[len(image) - 4:len(image)].lower() not in valid_file_types:
            print("WARNING: There are files in your directory that are not of the following types:"
                  " .jpg, .png, .bmp, .gif.")
            print("Please remove these files.")
            input("Press the 'enter' key to exit...")
            sys.exit()
        print(f"Image {i}: {image}")

    print("Image to ASCII: Convert images into ASCII characters!")

    get_user_input(image_width, ascii_string)

    if "ascii_conversions" not in os.listdir():
        os.mkdir("ascii_conversions")

    for image in image_names:
        temp_name = image.split(".")[0]
        with open(f"{os.path.join('ascii_conversions', f'{temp_name}_ascii.txt')}", "w+", encoding="utf-8") as f:
            for v in ascii_matrix_of(image, ascii_string, image_width):
                f.write(v)

        print(f"Success! '{image}' converted to '{temp_name}_ascii.txt'!")


if __name__ == "__main__":
    main()
