import pixgen
import os, sys

logo = """
 ______   __     __  __     ______     __         ______     ______   ______     ______    
/\  == \ /\ \   /\_\_\_\   /\  ___\   /\ \       /\  __ \   /\__  _\ /\  __ \   /\  == \   
\ \  _-/ \ \ \  \/_/\_\/_  \ \  __\   \ \ \____  \ \  __ \  \/_/\ \/ \ \ \/\ \  \ \  __<   
 \ \_\    \ \_\   /\_\/\_\  \ \_____\  \ \_____\  \ \_\ \_\    \ \_\  \ \_____\  \ \_\ \_\ 
  \/_/     \/_/   \/_/\/_/   \/_____/   \/_____/   \/_/\/_/     \/_/   \/_____/   \/_/ /_/ 
                                                                                           
"""

flags = {"verbose": False}

def get_set_argv():
    for arg in sys.argv[1:]: 
        if arg == "-v":
            flags["verbose"] = True

def find_palettes():
    palettes = []
    # traverse whole directory
    for root, dirs, files in os.walk(r'palletes/'):
        # select file name
        for file in files:
            # check the extension of files
            if file.endswith('.hex'):
                # print whole path of files
                palettes.append(str(file))
    
    return palettes

def main():
    print(logo)

    if len(sys.argv) > 0:
        get_set_argv()

    image_name = input("Image name to pixelate: ")
    
    if input("Do you want to add a palette? (Y/N): ") == "Y":
        palettes = find_palettes()

        print("\nPalettes found:")
        for palette in palettes:
            print("\t" + str(palettes.index(palette) + 1) + ": " + str(palette))
        
        palette_index = int(input("\nChoose palette number: ")) - 1
        colorise = True
    
    resolution = int(input("Enter desired resolution: "))
    print("\n")

    pixelate = pixgen.Image(image_name)
    pixelate.verbose = flags["verbose"]
    if colorise:
        pixelate.set_palette(palettes[palette_index])

    print("Modifying image, this might take a couple of minutes")
    pixelate.generate_pixel_art_from_image(resolution=resolution)
    print("Image modified, exiting")

if __name__ == "__main__":
    main()