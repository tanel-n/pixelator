from PIL import Image as pil_image
from PIL import ImageColor as pil_color
import math
import colour

class Pallette():
    def __init__(self):
        self.hex_pallette = []
        self.rgb_pallette = []
        self.load_pallete("apollo.hex")

    def load_pallete(self, filename):
        file_name = filename

        with open("palletes/" + file_name, "r") as pallete_file:
            lines = pallete_file.readlines()
            for line in lines:
                self.hex_pallette.append(line.replace("\n", ""))

            self.rgb_pallette = self.convert_hex_to_rgb_pallette(self.hex_pallette)

    def convert_hex_to_rgb_pallette(self, hex_pallette):
        rgb_pallette = []

        for hex in hex_pallette:
            rgb_pallette.append(pil_color.getcolor("#" + hex, "RGB"))

        return rgb_pallette

    def find_match_from_pallette(self, rgb):
        rgb_float1 = (rgb[0]/255, rgb[1]/255, rgb[2]/255)
        xyz1 = colour.sRGB_to_XYZ(list(rgb_float1))
        lab1 = colour.XYZ_to_Lab(xyz1)
        best_match = [100, None] # [delta_E, RGB]

        for pallette_colour in self.rgb_pallette:
            xyz2 = colour.sRGB_to_XYZ([pallette_colour[0]/255, pallette_colour[1]/255, pallette_colour[2]/255])
            lab2 = colour.XYZ_to_Lab(xyz2)

            delta_E = colour.delta_E(lab1, lab2, method="CIE 1976")
            if best_match[0] > delta_E:
                best_match = [delta_E, pallette_colour]
        
        print("RGB: " + str(rgb) + " best match: " + str(best_match[1]))
        return best_match[1]

class Image():

    def __init__(self, image_name, verbose=False):
        self.image_name = image_name
        self.image = self.open_image()
        self.image_x = self.image.size[0]
        self.image_y = self.image.size[1]
        
        self.verbose = verbose

        self.pallette = Pallette()

    def open_image(self):
        image = pil_image.open(self.image_name)
        print("Source image parameters: " + image.format, image.size, image.mode)

        return image

    def save_image(self, image):
        old_name = self.image_name.split(".")
        new_name = old_name[0] + "_new." + old_name[1]
        print("Saved pixel art image: " + new_name)

        image.save(new_name, "jpeg")

    def crop_to_last_sized_pixel(self, step, image_size:tuple, resolution):
        crop_x = image_size[0] % step // 2
        crop_y = image_size[1] % step // 2
        crop_x2 = image_size[0] - (image_size[0] % step) // 2
        crop_y2 = image_size[1] - (image_size[1] % step) // 2

        self.image = self.image.crop((crop_x, crop_y, crop_x2, crop_y2))

        # update size after cropping
        self.image_x = self.image.size[0]
        self.image_y = self.image.size[1]

        print("Step: " + str(step) + " size " + str(image_size))
        print("Cropped image " + str(crop_x) + ", " + str(crop_y) + ", " + str(crop_x2) + ", " + str(crop_y2))

    def draw_sized_pixel(self, rgb, size, xy, image):
        for y in range(size):
            for x in range(size):
                image.putpixel((xy[0]+x, xy[1]+y), rgb)

        if(self.verbose):
            print("Drew pixel " + str(rgb) + " size " + str(size) + " location " + str(xy))

        return image

    def find_sized_pixel_rgb(self, rgb_list:list, pallette, recolor=False):
        red = 0
        green = 0
        blue = 0
        n_rgb_values = len(rgb_list)

        for rgb in rgb_list:
            red += rgb[0]
            green += rgb[1]
            blue += rgb[2]

        red = int(red/n_rgb_values)
        green = int(green/n_rgb_values)
        blue = int(blue/n_rgb_values)

        rgb = (red, green, blue)
        if recolor:
            rgb = self.pallette.find_match_from_pallette(rgb)
        
        return rgb

    def generate_pixel_art_from_image(self, bit_depth=8, resolution=64):
        pallette = "apollo"

        step = int(math.sqrt(self.image_x**2 + self.image_y**2) // resolution)

        # crop image to fit integer number of pixels
        self.crop_to_last_sized_pixel(step, (self.image_x, self.image_y), resolution)
        
        image_px = self.image.load()
        color_probe = []

        new_image = pil_image.new(mode="RGB", size=(self.image_x, self.image_y), color=(0,0,0))

        for y in range(0, self.image_y, step):
            for x in range(0, self.image_x, step):
                for i in range(step):
                    color_probe.append(image_px[x+i, y+i])

                sized_pixel_rgb = self.find_sized_pixel_rgb(color_probe, pallette, recolor=True)
                new_image = self.draw_sized_pixel(sized_pixel_rgb, step, (x, y), new_image)
                color_probe.clear()

        self.save_image(new_image)    

def main():
    my_image = Image("harjus.jpg", verbose=True)
    my_image.generate_pixel_art_from_image(resolution=164)


if __name__ == "__main__":
    main()