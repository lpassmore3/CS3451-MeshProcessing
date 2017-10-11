# Sample code for starting the mesh processing project
# Author: Luke Austin Passmore

rotate_flag = True    # automatic rotation of model?
time = 0   # keep track of passing time, for automatic rotation

geometry_table = []
vertex_table = []
opposite_table = []

white = False
rainbow = False
colors = []

per_vertex = False
normals = []

# initalize stuff
def setup():
    size (600, 600, OPENGL)
    noStroke()

# draw the current mesh
def draw():
    global time
    
    background(0)    # clear screen to black

    perspective (PI*0.333, 1.0, 0.01, 1000.0)
    camera (0, 0, 5, 0, 0, 0, 0, 1, 0)    # place the camera in the scene
    scale (1, -1, 1)    # change to right-handed coordinate system
    
    # create an ambient light source
    ambientLight (102, 102, 102)
  
    # create two directional light sources
    lightSpecular (204, 204, 204)
    directionalLight (102, 102, 102, -0.7, -0.7, -1)
    directionalLight (152, 152, 152, 0, 0, -1)
    
    pushMatrix();

    if (white == True):
        fill(255, 255, 255)
    else:
        fill (50, 50, 200)            # set polygon color
    ambient (200, 200, 200)
    specular (0, 0, 0)            # no specular highlights
    shininess (1.0)
  
    rotate (time, 1.0, 0.0, 0.0)

    # THIS IS WHERE YOU SHOULD DRAW THE MESH
    
    for i in range(0, len(vertex_table), 3):
        
        if (colors != [] and rainbow == True):
            fill(colors[i / 3][0], colors[i / 3][1], colors[i / 3][2])
        
        index0 = vertex_table[i]
        index1 = vertex_table[i + 1]
        index2 = vertex_table[i + 2]
        
        beginShape()
        
        if (normals != [] and per_vertex == True):
            normal(normals[index0][0], normals[index0][1], normals[index0][2])
        v0 = geometry_table[index0]
        vertex(v0[0], v0[1], v0[2]) 
        
        if (normals != [] and per_vertex == True):
            normal(normals[index1][0], normals[index1][1], normals[index1][2])
        v1 = geometry_table[index1]
        vertex(v1[0], v1[1], v1[2]) 
        
        if (normals != [] and per_vertex == True):
            normal(normals[index2][0], normals[index2][1], normals[index2][2])
        v2 = geometry_table[index2]
        vertex(v2[0], v2[1], v2[2]) 
        
        endShape()
           
    # beginShape()
    # normal (0.0, 0.0, 1.0)
    # vertex (-1.0, -1.0, 0.0)
    # vertex ( 1.0, -1.0, 0.0)
    # vertex ( 1.0,  1.0, 0.0)
    # vertex (-1.0,  1.0, 0.0)
    # endShape(CLOSE)
    
    popMatrix()
    
    # maybe step forward in time (for object rotation)
    if rotate_flag:
        time += 0.02

# process key presses
def keyPressed():
    global rotate_flag
    global white
    global rainbow
    global per_vertex
    
    if key == ' ':
        rotate_flag = not rotate_flag
    elif key == '1':
        read_mesh ('tetra.ply')
    elif key == '2':
        read_mesh ('octa.ply')
    elif key == '3':
        read_mesh ('icos.ply')
    elif key == '4':
        read_mesh ('star.ply')
    elif key == '5':
        read_mesh ('torus.ply')
    elif key == 'n':
        if (per_vertex == False):
            per_vertex = True
        elif (per_vertex == True):
            per_vertex = False
    elif key == 'r':
        if (rainbow == False):
            rainbow = True
            white = False
        elif (rainbow == True):
            rainbow = False
    elif key == 'w':
        if (white == True):
            white = False
        elif (white == False):
            white = True
            rainbow = False
    elif key == 'd':
        dual()
    elif key == 'q':
        exit()

# read in a mesh file (THIS NEEDS TO BE MODIFIED !!!)
def read_mesh(filename):
    global geometry_table
    global vertex_table
    global opposite_table
    global colors
    global normals
    
    geometry_table = []
    vertex_table = []
    opposite_table = []
    colors = []
    normals = []

    fname = "data/" + filename
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()
        
    # determine number of vertices (on first line)
    words = lines[0].split()
    num_vertices = int(words[1])
    # print "number of vertices =", num_vertices

    # determine number of faces (on first second)
    words = lines[1].split()
    num_faces = int(words[1])
    # print "number of faces =", num_faces

    # read in the vertices
    for i in range(num_vertices):
        words = lines[i+2].split()
        x = float(words[0])
        y = float(words[1])
        z = float(words[2])
        # print "vertex = ", x, y, z
        geometry_table.append([x, y, z])
    
    # read in the faces
    for i in range(num_faces):
        j = i + num_vertices + 2
        words = lines[j].split()
        nverts = int(words[0])
        if nverts != 3:
            print "error: this face is not a triangle"
            exit()
        
        index1 = int(words[1])
        index2 = int(words[2])
        index3 = int(words[3])
        # print "face =", index1, index2, index3

        vertex_table.append(index1)
        vertex_table.append(index2)
        vertex_table.append(index3)
        
        opposite_table.append(index1)
        opposite_table.append(index2)
        opposite_table.append(index3)
    
    # calculate opposite table and colors
    for a in range(len(vertex_table)):
        if (a % 3 == 0):
            r = random(255)
            g = random(255)
            b = random(255)
            colors.append([r, g, b])
        for b in range(len(vertex_table)):
            if (vertex_table[next(a)] == vertex_table[prev(b)] and vertex_table[prev(a)] == vertex_table[next(b)]):
                # print(str(a) + "  " + str(b))
                opposite_table[a] = b
                opposite_table[b] = a
    
    for g in range(len(geometry_table)):
        curr_corner = vertex_table.index(g)
        
        norm_x = 0.0
        norm_y = 0.0
        norm_z = 0.0
        numFaces = 1
        
        orig_corner = curr_corner
        looped = False   
        
        while (curr_corner != orig_corner or looped == False):
            looped = True
            numFaces += 1
            
            vertex0 = geometry_table[vertex_table[curr_corner]]
            vertex1 = geometry_table[vertex_table[next(curr_corner)]]
            vertex2 = geometry_table[vertex_table[next(next(curr_corner))]]
            
            side2 = [vertex1[0] - vertex0[0], vertex1[1] - vertex0[1], vertex1[2] - vertex0[2]]
            side1 = [vertex2[0] - vertex0[0], vertex2[1] - vertex0[1], vertex2[2] - vertex0[2]]
            
            norm_x += (side1[1] * side2[2]) - (side1[2] * side2[1])
            norm_y += (side1[2] * side2[0]) - (side1[0] * side2[2])
            norm_z += (side1[0] * side2[1]) - (side1[1] * side2[0])
            
            curr_corner = swing(curr_corner)
        
        normals.append([norm_x / numFaces, norm_y / numFaces, norm_z / numFaces])
        
# Returns the index of the next corner in the vertex table of a current corner      
def next(corner_index):
    triangle_number = corner_index // 3
    return (3 * triangle_number) + ((corner_index + 1) % 3)

# Returns the index of the previous corner in the vertex table of a current corner 
def prev(corner_index):
    triangle_number = corner_index // 3
    return (3 * triangle_number) + ((corner_index + 2) % 3)

# Returns the index of the adjacent swing corner in the vertex table of a current corner
def swing(corner_index):
    return next(opposite_table[next(corner_index)])

# Calculates the dual mesh
def dual():
    global geometry_table
    global vertex_table
    global opposite_table
    global colors
    global normals
    
    new_geometry_table = []
    new_vertex_table = []
    new_opposite_table = []
    new_colors = []
    new_normals = []
        
    for t in range(0, len(vertex_table), 3):
        vertex0 = geometry_table[vertex_table[t]]
        vertex1 = geometry_table[vertex_table[t + 1]]
        vertex2 = geometry_table[vertex_table[t + 2]]
        
        centroid_x = (vertex0[0] + vertex1[0] + vertex2[0]) / 3
        centroid_y = (vertex0[1] + vertex1[1] + vertex2[1]) / 3
        centroid_z = (vertex0[2] + vertex1[2] + vertex2[2]) / 3
        
        new_geometry_table.append([centroid_x, centroid_y, centroid_z])
    
    for v in range(len(geometry_table)):
        curr_corner = vertex_table.index(v)
        
        orig_corner = curr_corner
        looped = False 
        numFaces = 0   
        
        centroid_indecies = []
        super_centroid_x = 0.0
        super_centroid_y = 0.0
        super_centroid_z = 0.0
        
        while (curr_corner != orig_corner or looped == False):
            looped = True
            numFaces += 1
            
            triangle_number = curr_corner // 3
            centroid_indecies.append(triangle_number)
            
            super_centroid_x += new_geometry_table[triangle_number][0]
            super_centroid_y += new_geometry_table[triangle_number][1]
            super_centroid_z += new_geometry_table[triangle_number][2]
            
            curr_corner = swing(curr_corner)
            
        super_centroid = [super_centroid_x / numFaces, super_centroid_y / numFaces, super_centroid_z / numFaces]
        if (super_centroid not in new_geometry_table):
            new_geometry_table.append(super_centroid)
        
        # v_norm = [v_norm_x / numFaces, v_norm_y / numFaces, v_norm_z / numFaces]
        # new_normals.append(v_norm)
        
        for c in range(len(centroid_indecies)):
            new_vertex_table.append(centroid_indecies[c])
            new_vertex_table.append(centroid_indecies[(c + 1) % len(centroid_indecies)])
            new_vertex_table.append(new_geometry_table.index(super_centroid))
            
            new_opposite_table.append(centroid_indecies[c])
            new_opposite_table.append(centroid_indecies[(c + 1) % len(centroid_indecies)])
            new_opposite_table.append(new_geometry_table.index(super_centroid))
        
    for a in range(len(new_vertex_table)):
        if (a % 3 == 0):
            r = random(255)
            g = random(255)
            b = random(255)
            new_colors.append([r, g, b])
        for b in range(len(new_vertex_table)):
            if (new_vertex_table[next(a)] == new_vertex_table[prev(b)] and new_vertex_table[prev(a)] == new_vertex_table[next(b)]):
                new_opposite_table[a] = b
                new_opposite_table[b] = a
    
    geometry_table = new_geometry_table
    vertex_table = new_vertex_table
    opposite_table = new_opposite_table
    colors = new_colors
    
    for g in range(len(new_geometry_table)):
        curr_corner = new_vertex_table.index(g)
        
        norm_x = 0.0
        norm_y = 0.0
        norm_z = 0.0
        numFaces = 1
        
        orig_corner = curr_corner
        looped = False   
        
        while (curr_corner != orig_corner or looped == False):
            looped = True
            numFaces += 1
            
            vertex0 = new_geometry_table[new_vertex_table[curr_corner]]
            vertex1 = new_geometry_table[new_vertex_table[next(curr_corner)]]
            vertex2 = new_geometry_table[new_vertex_table[next(next(curr_corner))]]
            
            side2 = [vertex1[0] - vertex0[0], vertex1[1] - vertex0[1], vertex1[2] - vertex0[2]]
            side1 = [vertex2[0] - vertex0[0], vertex2[1] - vertex0[1], vertex2[2] - vertex0[2]]
            
            norm_x += (side1[1] * side2[2]) - (side1[2] * side2[1])
            norm_y += (side1[2] * side2[0]) - (side1[0] * side2[2])
            norm_z += (side1[0] * side2[1]) - (side1[1] * side2[0])
            
            curr_corner = swing(curr_corner)
        
        new_normals.append([norm_x / numFaces, norm_y / numFaces, norm_z / numFaces])
    
    normals = new_normals
    