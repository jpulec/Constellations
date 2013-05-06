import Image
import ImageDraw
import operator
import networkx as nx
from UnionFind import UnionFind


class Star:
    def __init__(self, x, y):
        self.left = x
        self.top = y
        self.right = x
        self.bottom = y
        self.in_constellation = False

    def has_pixel(self, x, y):
        return x >= self.left and x <= self.right and y >= self.top and y <= self.bottom

    def add_pixel(self, x, y):
        if x < self.left:
            self.left = x
        if x > self.right:
            self.right = x
        if y < self.top:
            self.top = y
        if y > self.bottom:
            self.bottom = y

    def __repr__(self):
        return str((self.left, self.top, self.right, self.bottom))


    def __str__(self):
        return str((self.left, self.top, self.right, self.bottom))

def kruskal(graph, iterations):
    subtrees = UnionFind()
    tree = []
    edge_set = [(graph[v1][v2]["weight"], v1,v2) for v1 in graph for v2 in graph[v1]]
    edge_set.sort(cmp=lambda x,y: cmp(x[0], y[0]), reverse=True)
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
    THRESH = 125
    sky = Image.open("night-sky.jpeg")
    pixels = sky.load()

    width = sky.size[0]
    height = sky.size[1]
    for col in xrange(width):
        for row in xrange(height):
            G.add_node((col,row))
            if row-1 > 0 and col-1 > 0:
                if pixels[col,row][0] > THRESH and pixels[col,row][1] > THRESH and pixels[col,row][2] > THRESH:
                    weight = tuple(map(operator.abs, (map(operator.sub, pixels[col,row], pixels[col-1, row-1]))))
                    G.add_edge((col,row),(col-1, row-1), weight=weight)
            if row-1 > 0 and col+1 < width:
                if pixels[col,row][0] > THRESH and pixels[col,row][1] > THRESH and pixels[col,row][2] > THRESH:
                    weight = tuple(map(operator.abs, (map(operator.sub ,pixels[col,row], pixels[col+1, row-1]))))
                    G.add_edge((col,row), (col+1, row-1), weight=weight)
            if row+1 < height and col-1 > 0:
                if pixels[col,row][0] > THRESH and pixels[col,row][1] > THRESH and pixels[col,row][2] > THRESH:
                    weight = tuple(map(operator.abs, (map(operator.sub ,pixels[col,row], pixels[col-1, row+1]))))
                    G.add_edge((col, row), (col-1, row+1), weight=weight)
            if row+1 < height and col+1 < width:
                if pixels[col,row][0] > THRESH and pixels[col,row][1] > THRESH and pixels[col,row][2] > THRESH:
                    weight = tuple(map(operator.abs, (map(operator.sub ,pixels[col,row], pixels[col+1, row+1]))))
                    G.add_edge((col, row), (col+1, row+1), weight=weight)
            if row-1 > 0:
                if pixels[col,row][0] > THRESH and pixels[col,row][1] > THRESH and pixels[col,row][2] > THRESH:
                    weight = tuple(map(operator.abs, (map(operator.sub, pixels[col,row], pixels[col, row-1]))))
                    G.add_edge((col,row),(col, row-1), weight=weight)
            if col+1 < width:
                if pixels[col,row][0] > THRESH and pixels[col,row][1] > THRESH and pixels[col,row][2] > THRESH:
                    weight = tuple(map(operator.abs, (map(operator.sub ,pixels[col,row], pixels[col+1, row]))))
                    G.add_edge((col,row), (col+1, row), weight=weight)
            if row+1 < height:
                if pixels[col,row][0] > THRESH and pixels[col,row][1] > THRESH and pixels[col,row][2] > THRESH:
                    weight = tuple(map(operator.abs, (map(operator.sub ,pixels[col,row], pixels[col, row+1]))))
                    G.add_edge((col, row), (col, row+1), weight=weight)
            if col-1 > 0:
                if pixels[col,row][0] > THRESH and pixels[col,row][1] > THRESH and pixels[col,row][2] > THRESH:
                    weight = tuple(map(operator.abs, (map(operator.sub ,pixels[col,row], pixels[col-1, row]))))
                    G.add_edge((col, row), (col-1, row), weight=weight)
            #if pixels[row, col][0] > THRESH and pixels[row,col][1] > THRESH and pixels[row,col][2] > THRESH:
            #    image_pixels[(row,col)] = []
            #    for x in [row - DIST, row + DIST]:
            #        for y in [col - DIST, col + DIST]:
            #            if (x, y) in image_pixels and (x,y) != (row, col):
            #                image_pixels[(row, col)].append((x,y))
    for num_stars in [100000, 1000000]: #[100, 1000, 10000, 100000, 1000000, 1000000000000]:
        sky_copy = sky.copy()
        tree = kruskal(G, num_stars)
        pixels = sky_copy.load()
        for v1, v2 in tree:
            pixels[v1[0], v1[1]] = (128,0,0)
            pixels[v2[0], v2[1]] = (128,0,0)
        #sky_copy.show()
        #first need to identify stars in image from red 
        stars = []
        for col in xrange(width):
            for row in xrange(height):
                if pixels[col, row] == (128,0,0):
                    already = False
                    for s in stars:
                        if s.has_pixel(col, row):
                            already = True
                            break
                    if already:
                        continue
                    #found a star pixel
                    star = Star(col, row)
                    x = 0
                    y = 0
                    dx = 0
                    dy = -1
                    while row + y < height and row + y > 0 and col + x < width and col + x > 0 and pixels[col + x, row + y] == (128,0,0):
                        star.add_pixel(col + x, row + y)
                        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
                            dx, dy = -dy, dx
                        x, y = x + dx, y + dy
                    stars.append(star)
        for star in stars:
            for x in xrange(star.left, star.right):
                for y in xrange(star.top, star.bottom):
                    pixels[x, y] = (0, 128, 0)
        sky_copy.show()
        #print stars
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

