import Image
import ImageDraw
import sys
import operator
import math
import random
import networkx as nx


class UnionFind:
    def __init__(self):
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):

        # check for previously unknown object
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root
        
    def __iter__(self):
        return iter(self.parents)

    def union(self, *objects):
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r],r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest


class Star:
    def __init__(self, x, y):
        self.left = x
        self.top = y
        self.right = x
        self.bottom = y
        self.constellation_count = 0

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

    def __eq__(self, other):
        return (self.left == other.left and self.right == other.right and self.top == other.top and self.bottom == other.bottom)

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
    THRESH = 20
    DIST = 50
    DENSITY = 1.2
    sky = Image.open("fuzzystars.jpg")
    pixels = sky.load()
    stars = []
    width = sky.size[0]
    height = sky.size[1]
    for col in xrange(width):
        for row in xrange(height):
            G.add_node((col,row))
            for x in xrange(col - 1, col + 1):
                for y in xrange(row - 1, row + 1):
                    if (x != col and y != row) and x > 0 and x < width and y > 0 and y < height:
                        if not (x, y) in G[(col, row)]:
                            lum1 = (0.2126 *  pixels[col,row][0]) + (0.7152 * pixels[col,row][1]) + (0.0722* pixels[col,row][2])
                            lum2 = (0.2126 *  pixels[x,y][0]) + (0.7152 * pixels[x,y][1]) + (0.0722* pixels[x,y][2])
                            G.add_edge((col,row),(x, y), weight=(lum1 + lum2) / 2)

            #if pixels[row, col][0] > THRESH and pixels[row,col][1] > THRESH and pixels[row,col][2] > THRESH:
            #    image_pixels[(row,col)] = []
            #    for x in [row - DIST, row + DIST]:
            #        for y in [col - DIST, col + DIST]:
            #            if (x, y) in image_pixels and (x,y) != (row, col):
            #                image_pixels[(row, col)].append((x,y))
    for num_stars in [5000, 10000, 25000, 50000]: #[4000, 4500, 5000, 5500, 6000]:
        sky_copy = sky.copy()
        tree = kruskal(G, num_stars)
        pixels = sky_copy.load()
        for v1, v2 in tree:
            pixels[v1[0], v1[1]] = (128,0,0)
            pixels[v2[0], v2[1]] = (128,0,0)
        sky_copy.save("KruskalVerticiesFuzzy%s.png" % str(num_stars))
        sky_copy.show()
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
                    while row + y < height and row + y > 0 and col + x < width and col + x > 0:
                        lum = (0.2126 *  pixels[col + x,row + y][0]) + (0.7152 * pixels[col + x,row + y][1]) + (0.0722* pixels[col + x,row + y][2])
                        if lum < THRESH:
                            break
                        star.add_pixel(col + x, row + y)
                        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
                            dx, dy = -dy, dx
                        x, y = x + dx, y + dy
                    stars.append(star)
        draw = ImageDraw.Draw(sky_copy)
        for star in stars:
            close_stars = []
            constell_count = 0
            star_center = ((star.right - star.left) / 2) + star.left, ((star.bottom - star.top) / 2) + star.top
            for other in stars:
                if other == star:
                    continue
                other_center = ((other.right - other.left) / 2) + other.left, ((other.bottom - other.top) / 2) + other.top
                dist = math.sqrt(pow(star_center[0] - other_center[0], 2) + pow(star_center[1] - other_center[1], 2))
                if dist < DIST:
                    close_stars.append(other)
                    constell_count += other.constellation_count
            constell_count += star.constellation_count
            if len(close_stars) > 0:
                if (float(constell_count) / len(close_stars)) < (DENSITY / len(close_stars)):
                    for close in close_stars:
                        close_center = ((close.right - close.left) / 2) + close.left, ((close.bottom - close.top) / 2) + close.top
                        draw.line([star_center, close_center], fill = (256, 256, 256), width=2)
                        close.constellation_count += 1
                        star.constellation_count += 1
                        constell_count += 2
                        if not (float(constell_count) / len(close_stars)) < (DENSITY / len(close_stars)):
                            break 
            
            #for x in xrange(star.left, star.right):
                #for y in xrange(star.top, star.bottom):
                    #pixels[x, y] = (0, 128, 0)
        sky_copy.save("ConstellationsFuzzy%s.png" % str(num_stars))
        sky_copy.show()
        #print stars
if __name__ == "__main__":
    run()

