import Image
import ImageDraw
import operator

image_pixels = {}

class UnionFind():
    def __init__(self):
        self.sets = []
        self.lookup = {}
    def make_set(self, item):
        new_set = [item]
        self.sets.append(new_set)
        self.lookup[item] = new_set
    def union(self, set1, set2):
        """Merges set1 into set2"""
        assert(set1 in self.sets)
        assert(set2 in self.sets)
        for (item, value) in self.lookup.iteritems():
            if value == set1:
                self.lookup[item] = set2
        self.sets.remove(set1)
        set2.extend(set1)

class Edge:
    def __init__(self, v1, v2, weight):
        self.v1 = v1 
        self.v2 = v2
        self.weight = weight


def kruskal(graph):
    subtrees = UnionFind()
    tree = []
    edge_set = [(edge.weight,edge.v1,edge.v2) for edge in edges for edges in graph.itervalues()]
    edge_set.sort()
    for w,v1,v2 in edge_set:
        if subtrees[v1] != subtrees[v2]:
            tree.append((v1,v2))
            subtrees.union(v1,v2)
    return tree

def run():
    DIST = 10
    THRESH = 30
    sky = Image.open("night-sky.jpeg")
    pixels = sky.load()

    width = sky.size[0]
    height = sky.size[1]
    edges = [[] for i in range(width)] 
    for col in range(width):
        for row in range(height):
            image_pixels[(col,row)] = []
            if row-1 > 0 and col-1 > 0:
                weight = tuple(map(operator.abs, (map(operator.sub, pixels[col,row], pixels[col-1, row-1]))))
                edges =
                image_pixels[(col,row)].append(Edge((col, row), (col-1, row-1), weight))
            if row-1 > 0 and col+1 < width:
                weight = tuple(map(operator.abs, (map(operator.sub ,pixels[col,row], pixels[col+1, row-1]))))
                image_pixels[(col,row)].append(Edge((col, row), (col+1, row-1), weight))
            if row+1 < height and col-1 > 0:
                weight = tuple(map(operator.abs, (map(operator.sub ,pixels[col,row], pixels[col-1, row+1]))))
                image_pixels[(col,row)].append(Edge((col, row), (col-1, row+1), weight))
            if row+1 < height and col+1 < width:
                weight = tuple(map(operator.abs, (map(operator.sub ,pixels[col,row], pixels[col+1, row+1]))))
                image_pixels[(col,row)].append(Edge((col, row), (col+1, row+1), weight))
            #if pixels[row, col][0] > THRESH and pixels[row,col][1] > THRESH and pixels[row,col][2] > THRESH:
            #    image_pixels[(row,col)] = []
            #    for x in [row - DIST, row + DIST]:
            #        for y in [col - DIST, col + DIST]:
            #            if (x, y) in image_pixels and (x,y) != (row, col):
            #                image_pixels[(row, col)].append((x,y))
    kruskal(image_pixels)
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

