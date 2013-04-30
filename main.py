import Image
import ImageDraw

image_pixels = {}

def run():
    DIST = 10
    THRESH = 30
    sky = Image.open("night-sky.jpeg")
    pixels = sky.load()
    pixel_count = 0
    for row in range(sky.size[0]):
        for col in range(sky.size[1]):
            if pixels[row, col][0] > THRESH and pixels[row,col][1] > THRESH and pixels[row,col][2] > THRESH:
                image_pixels[(row,col)] = []
                for x in [row - DIST, row + DIST]:
                    for y in [col - DIST, col + DIST]:
                        if (x, y) in image_pixels and (x,y) != (row, col):
                            image_pixels[(row, col)].append((x,y))
            pixel_count += 1
    new_img = Image.new("RGB", (1024,768))
    new_pix = new_img.load()
    draw = ImageDraw.Draw(new_img)
    for row in range(new_img.size[0]):
        for col in range(new_img.size[1]):
            if (row, col) in image_pixels:
                new_pix[row,col] = (200,200,200)
                for connected in image_pixels[(row,col)]:
                    if row < connected[0] or (row < connected[0] and col < connected[1]):
                        continue
                    draw.line([(row,col), connected])
    new_img.show() 

if __name__ == "__main__":
    run()

