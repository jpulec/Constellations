import Image
import ImageDraw
import operator
import networkx as nx
from UnionFind import UnionFind

class Star:
    def __init__(self, x1, x2, y1, y2):
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.in_constellation = False
    
    def add_pixel(x,y):
        if x < self.x1:
            self.x1 = x
        if x > self.x2:
            self.x2 = x
        if y < self.y1:
            self.y1 = y
        if y > self.y1:
            self.y1 = y


    def contains_pixel(self, x, y):
        return (x >= self.x1 and x <= self.x2 and y >= self.y1 and y <= self.y2)

def kruskal(graph, iterations):
    subtrees = UnionFind()
    tree = []
    edge_set = [(graph[v1][v2]["weight"], v1,v2) for v1 in graph for v2 in graph[v1]]
    edge_set.sort(cmp=lambda x,y: cmp(x[0], y[0]))
    for index, edge in enumerate(edge_set):
        if index > iterations:
            break
        if subtrees[edge[1]] != subtrees[edge[2]]:
            tree.append((edge[1],edge[2]))
            subtrees.union(edge[1],edge[2])
    return tree

def run():
    G = nx.Graph()
    DIST = 10
    THRESH = 30
    sky = Image.open("night-sky.jpeg")
    pixels = sky.load()
    stars = []
    width = sky.size[0]
    height = sky.size[1]
    for col in range(width):
        for row in range(height):
            G.add_node((col,row))
            found = False
            for star in stars:
                if star.contains_pixel(col,row):
                    found = True
                    break
            if found:
                continue
            if pixels[col,row][0] > 30 and pixels[col,row][1] > 30 and pixels[col,row][2] > 30:
                star = Star(col, col, row, row)
                region = sky.crop((col-THRESH, row-THRESH, col+THRESH, row+THRESH))
                pixs = region.load()
                for x in range(THRESH*2):
                    for y in range(THRESH*2):
                        if pix[x,y][0] > 30 and pix[x,y][1] > 30 and pix[x,y][2] > 30:
                            star.add_pixel(col - x, row y)
                stars.append(star)
                
    #for node in G:
    #    if node
    #    for col in range(width):
    #        for row in range(height):
    #        
    #            if row-1 > 0 and col-1 > 0:
    #            if pixels[col,row][0] > 30 and pixels[col,row][1] > 30 and pixels[col,row][2] > 30:
    #                weight = tuple(map(operator.abs, (map(operator.sub, pixels[col,row], pixels[col-1, row-1]))))
    #                G.add_edge((col,row),(col-1, row-1), weight=weight)
    #        if row-1 > 0 and col+1 < width:
    #            if pixels[col,row][0] > 30 and pixels[col,row][1] > 30 and pixels[col,row][2] > 30:
    #                weight = tuple(map(operator.abs, (map(operator.sub ,pixels[col,row], pixels[col+1, row-1]))))
    #                G.add_edge((col,row), (col+1, row-1), weight=weight)
    #        if row+1 < height and col-1 > 0:
    #            if pixels[col,row][0] > 30 and pixels[col,row][1] > 30 and pixels[col,row][2] > 30:
    #                weight = tuple(map(operator.abs, (map(operator.sub ,pixels[col,row], pixels[col-1, row+1]))))
    #                G.add_edge((col, row), (col-1, row+1), weight=weight)
    #        if row+1 < height and col+1 < width:
    #            if pixels[col,row][0] > 30 and pixels[col,row][1] > 30 and pixels[col,row][2] > 30:
    #                weight = tuple(map(operator.abs, (map(operator.sub ,pixels[col,row], pixels[col+1, row+1]))))
    #                G.add_edge((col, row), (col+1, row+1), weight=weight)
            #if pixels[row, col][0] > THRESH and pixels[row,col][1] > THRESH and pixels[row,col][2] > THRESH:
            #    image_pixels[(row,col)] = []
            #    for x in [row - DIST, row + DIST]:
            #        for y in [col - DIST, col + DIST]:
            #            if (x, y) in image_pixels and (x,y) != (row, col):
            #                image_pixels[(row, col)].append((x,y))
    for num_stars in [100, 1000, 10000, 100000, 1000000, 1000000000000]:
        sky_copy = sky.copy()
        draw = ImageDraw.Draw(sky_copy)
        tree = kruskal(G, num_stars)
        for v1, v2 in tree:
            draw.line([(v1[0], v1[1]), (v2[0], v2[1])], fill=128)
        sky_copy.show()
    #new_img = Image.new("RGB", (1024,768))
    #new_pix = new_img.load()
    #draw = ImageDraw.Draw(new_img)
    #for col in range(width):
    #    for row in range(height):
    #        if (col, row) in image_pixels:
    #            new_pix[col,row] = (200,200,200)
    #            for connected in image_pixels[(col,row)]:
    #                if row < connected[0] or (row < connected[0] and col < connected[1]):
    #                    continue
    #                #draw.line([(row,col), connected], fill = 128)
    #new_img.show() 

if __name__ == "__main__":
    run()

