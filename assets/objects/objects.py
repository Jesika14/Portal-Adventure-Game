import numpy as np
import random

def CreateCircle(center, radius, colour, points = 10, offset = 0, semi = False):
    vertices = [center[0], center[1], center[2], colour[0], colour[1], colour[2]]
    indices = []

    if semi == True:
        for i in range(points+1):
            vertices += [
                center[0] + radius * np.cos(float(i * np.pi)/points),
                center[1] + radius * np.sin(float(i * np.pi)/points),
                center[2],
                colour[0],
                colour[1],
                colour[2],
                ]
            
            ind1 = i+1
            ind2 = i+2 if i != points else 1
            indices += [0 + offset, ind1 + offset, ind2 + offset]
    else:
        for i in range(points):
            vertices += [
                center[0] + radius * np.cos(float(i * 2* np.pi)/points),
                center[1] + radius * np.sin(float(i * 2* np.pi)/points),
                center[2],
                colour[0],
                colour[1],
                colour[2],
                ]
            
            ind1 = i+1
            ind2 = i+2 if i != points-1 else 1
            indices += [0 + offset, ind1 + offset, ind2 + offset]

    return (vertices, indices)    

def CreateTriangle(center, size, color):
    half_size = size / 2
    vertices = [
        center[0], center[1] + half_size, center[2], color[0], color[1], color[2], 0.5, 1.0,
        center[0] - half_size, center[1] - half_size, center[2], color[0], color[1], color[2], 0.0, 0.0,
        center[0] + half_size, center[1] - half_size, center[2], color[0], color[1], color[2], 1.0, 0.0,
    ]
    indices = [0, 1, 2]
    return vertices, indices

def CreateRectangle(center, width, height, color):
    half_w = width / 2
    half_h = height / 2
    vertices = [
        center[0] - half_w, center[1] + half_h, center[2], color[0], color[1], color[2], 0.0, 1.0,
        center[0] + half_w, center[1] + half_h, center[2], color[0], color[1], color[2], 1.0, 1.0,
        center[0] + half_w, center[1] - half_h, center[2], color[0], color[1], color[2], 1.0, 0.0,
        center[0] - half_w, center[1] - half_h, center[2], color[0], color[1], color[2], 0.0, 0.0,
    ]
    indices = [0, 1, 2, 0, 3, 2]
    return vertices, indices

def CreatePlayer():

    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.0, [220/255, 183/255, 139/255], 50, 0)

    eye_verts1, eye_inds1 = CreateCircle([0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts1
    indices += eye_inds1

    eye_verts2, eye_inds2 = CreateCircle([-0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts2
    indices += eye_inds2

    eye_verts3, eye_inds3 = CreateCircle([-0.4, -0.5, 0.10], 0.12, [0,0,0], 10, len(vertices)/6)
    vertices += eye_verts3
    indices += eye_inds3

    eye_verts4, eye_inds4 = CreateCircle([0.4, -0.5, 0.10], 0.12, [0,0,0], 10, len(vertices)/6)
    vertices += eye_verts4
    indices += eye_inds4

    eye_verts5, eye_inds5 = CreateCircle([0.0, 0.0, 0.2], 1.0, [1,0,0], 25, len(vertices)/6, True)
    vertices += eye_verts5
    indices += eye_inds5

    eye_verts6, eye_inds6 = CreateCircle([0.0, 0.95, 0.3], 0.3, [0.9,0.9,0.9], 20, len(vertices)/6)
    vertices += eye_verts6
    indices += eye_inds6

    return vertices, indices

def CreateBackground():
    grassColour = [0,1,0]
    waterColour = [0,0,1]

    vertices = [
        -500.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -400.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -400.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -500.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],

        500.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        400.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        400.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        500.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],

        -400.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        400.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        400.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        -400.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
    ]

    indices = [
        0,1,2, 0,3,2,
        8,9,10, 8,11,10,
        4,5,6, 4,7,6
    ]

    return vertices, indices

def CreateBackgroundSpace():
    grassColour = [0,1,0]
    waterColour = [0,0,0]

    vertices = [
        
        -500.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        500.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        500.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        -500.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
    
    ]

    indices = [
        0,1,2, 0,3,2,
        # 8,9,10, 8,11,10,
        # 4,5,6, 4,7,6
    ]

    return vertices, indices

def CreateAlien():
    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.2, [100/255, 255/255, 100/255], 50, 0)

    eye_verts1, eye_inds1 = CreateCircle([0.5, -0.6, 0.05], 0.35, [1,1,1], 20, len(vertices)//6)
    vertices += eye_verts1
    indices += eye_inds1

    eye_verts2, eye_inds2 = CreateCircle([-0.5, -0.6, 0.05], 0.35, [1,1,1], 20, len(vertices)//6)
    vertices += eye_verts2
    indices += eye_inds2

    eye_verts3, eye_inds3 = CreateCircle([-0.5, -0.6, 0.10], 0.15, [0,0,0], 10, len(vertices)//6)
    vertices += eye_verts3
    indices += eye_inds3

    eye_verts4, eye_inds4 = CreateCircle([0.5, -0.6, 0.10], 0.15, [0,0,0], 10, len(vertices)//6)
    vertices += eye_verts4
    indices += eye_inds4

    antenna_base, antenna_base_inds = CreateCircle([0.0, 1.2, 0.05], 0.15, [100/255, 255/255, 100/255], 10, len(vertices)//6)
    vertices += antenna_base
    indices += antenna_base_inds
    
    antenna_tip, antenna_tip_inds = CreateCircle([0.0, 1.5, 0.05], 0.1, [255/255, 0, 0], 10, len(vertices)//6)
    vertices += antenna_tip
    indices += antenna_tip_inds

    return vertices, indices

def CreateFish():
    # Body of the fish
    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.0, [0.2, 0.6, 1.0], 30, 0)

    # Eye (White part)
    eye_verts, eye_inds = CreateCircle([0.4, 0.3, 0.05], 0.2, [1,1,1], 15, len(vertices)//6)
    vertices += eye_verts
    indices += eye_inds

    # Pupil (Black)
    pupil_verts, pupil_inds = CreateCircle([0.45, 0.3, 0.10], 0.1, [0,0,0], 10, len(vertices)//6)
    vertices += pupil_verts
    indices += pupil_inds

    # Tail (Triangle shape)
    tail_vertices = [
        -1.0, 0.0, 0.0,  0.2, 0.6, 1.0,  
        -1.3, 0.3, 0.0,  0.2, 0.6, 1.0,  
        -1.3, -0.3, 0.0,  0.2, 0.6, 1.0
    ]
    tail_indices = [
        len(vertices)//6, len(vertices)//6 + 1, len(vertices)//6 + 2
    ]

    vertices += tail_vertices
    indices += tail_indices

    return vertices, indices

def CreateStone():
    center = [0.0, 0.0, 0.0]
    base_radius = 1.5
    color = [105/255, 105/255, 105/255]  # Dark gray
    segments = 12
    start_index = 0
    
    vertices = []
    indices = []
    angle_step = 2 * np.pi / segments
    
    vertices.extend([*center, *color])
    
    for i in range(segments + 1):
        angle = i * angle_step
        radius_variation = random.uniform(-0.3, 0.3)
        radius = base_radius + radius_variation
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        z = center[2]
        vertices.extend([x, y, z, *color])
        if i > 0:
            indices.append(start_index + i)
            indices.append(start_index)
            indices.append(start_index + i + 1)
    
    return vertices, indices

def CreateAstronaut():
    # Astronaut body (suit)
    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.0, [220/255, 220/255, 220/255], 50, 0)

    # Helmet glass
    helmet_verts, helmet_inds = CreateCircle([0.0, 0.3, 0.1], 0.6, [50/255, 50/255, 70/255], 40, len(vertices)//6)
    vertices += helmet_verts
    indices += helmet_inds

    # Oxygen pack
    pack_verts, pack_inds = CreateCircle([-0.6, 0.0, -0.1], 0.3, [180/255, 180/255, 180/255], 30, len(vertices)//6)
    vertices += pack_verts
    indices += pack_inds

    # Gloves
    glove1_verts, glove1_inds = CreateCircle([-0.8, -0.5, 0.05], 0.2, [150/255, 150/255, 150/255], 20, len(vertices)//6)
    vertices += glove1_verts
    indices += glove1_inds

    glove2_verts, glove2_inds = CreateCircle([0.8, -0.5, 0.05], 0.2, [150/255, 150/255, 150/255], 20, len(vertices)//6)
    vertices += glove2_verts
    indices += glove2_inds

    return vertices, indices

def CreateAsteroid():
    # Asteroid body
    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.5, [100/255, 100/255, 100/255], 60, 0)

    # White spots (craters)
    for i, pos in enumerate([(-0.5, 0.8), (0.7, -0.5), (-0.9, -0.3), (0.2, 0.5)]):
        spot_verts, spot_inds = CreateCircle([pos[0], pos[1], 0.05], 0.3, [200/255, 200/255, 200/255], 20, len(vertices)//6)
        vertices += spot_verts
        indices += spot_inds

    return vertices, indices

def CreateMagicalMat():
    mat_color = [0.3, 0.1, 0.1]  # Dark red mystic mat
    glow_color = [0.8, 0.3, 0.1]  # Golden glow

    # Create mat base
    vertices, indices = CreateCircle([0.0, -0.5, 0.0], 1.5, mat_color, 60, 0)

    # Create glow
    glow_verts, glow_inds = CreateCircle([0.0, -0.5, -0.1], 1.7, glow_color, 60, len(vertices)//8)
    vertices += glow_verts
    indices += glow_inds

    return vertices, indices

def CreateWizard():
    robe_color = [0.2, 0.0, 0.5]  # Deep blue robe
    face_color = [1.0, 0.8, 0.6]  # Skin tone
    hat_color = [0.1, 0.0, 0.2]  # Darker blue hat

    # Create robe
    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.2, robe_color, 50, 0)

    # Create face
    face_verts, face_inds = CreateCircle([0.0, 1.3, 0.0], 0.6, face_color, 40, len(vertices)//8)
    vertices += face_verts
    indices += face_inds

    # Create hat
    hat_verts, hat_inds = CreateCircle([0.0, 2.0, 0.0], 0.4, hat_color, 30, len(vertices)//8)
    vertices += hat_verts
    indices += hat_inds

    return vertices, indices

def CreateBackgroundMystic():
    waterColour = [0.7, 0.3, 0.2]

    vertices = [
        
        -500.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        500.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        500.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        -500.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
    
    ]

    indices = [
        0,1,2, 0,3,2,
        # 8,9,10, 8,11,10,
        # 4,5,6, 4,7,6
    ]

    return vertices, indices

def CreateMysticPlayer():
    body_color = [0.5, 0.2, 0.1]  # Brownish robe
    head_color = [1.0, 0.8, 0.6]  # Skin tone
    hat_color = [0.2, 0.0, 0.5]  # Mystic deep purple hat

    # Create body
    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.0, body_color, 50, 0)

    # Create head
    head_verts, head_inds = CreateCircle([0.0, 1.2, 0.0], 0.5, head_color, 40, len(vertices)//8)
    vertices += head_verts
    indices += head_inds

    # Create hat
    hat_verts, hat_inds = CreateCircle([0.0, 1.8, 0.0], 0.3, hat_color, 30, len(vertices)//8)
    vertices += hat_verts
    indices += hat_inds

    return vertices, indices

playerVerts, playerInds = CreatePlayer()
playerProps = {
    'vertices' : np.array(playerVerts, dtype = np.float32),
    
    'indices' : np.array(playerInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'opacity': 1.0,

    'type': 'player'
}

def CreateKey():
    key_color = [0.9, 0.8, 0.1]  # Golden key
    ring_color = [0.8, 0.7, 0.0]  # Slightly darker gold for the ring

    # Create key head (ring)
    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 0.6, ring_color, 40, 0)

    # Create key shaft
    shaft_verts, shaft_inds = CreateCircle([0.0, -0.8, 0.0], 0.2, key_color, 30, len(vertices)//8)
    vertices += shaft_verts
    indices += shaft_inds

    # Create key teeth
    teeth_verts, teeth_inds = CreateCircle([-0.3, -1.2, 0.0], 0.15, key_color, 20, len(vertices)//8)
    vertices += teeth_verts
    indices += teeth_inds

    teeth_verts2, teeth_inds2 = CreateCircle([0.3, -1.2, 0.0], 0.15, key_color, 20, len(vertices)//8)
    vertices += teeth_verts2
    indices += teeth_inds2

    return vertices, indices

backgroundVerts, backgroundInds = CreateBackground()
backgroundProps = {
    'vertices' : np.array(backgroundVerts, dtype = np.float32),
    
    'indices' : np.array(backgroundInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'boundary' : [500.0, -500.0, 500.0, 500.0],

    'river_banks': [-400.0, 400.0],

    'opacity': 1.0,

    'type': 'background'
}

fishVerts, fishInds = CreateFish()
fishProps = {
    'vertices' : np.array(fishVerts, dtype = np.float32),
    
    'indices' : np.array(fishInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'opacity': 1.0,

    'type': 'enemy'
}

stoneVerts, stoneInds = CreateStone()
stoneProps = {
    'vertices' : np.array(stoneVerts, dtype = np.float32),
    
    'indices' : np.array(stoneInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'opacity': 1.0,

    'type': 'platform'
}

backgroundSpaceVerts, backgroundSpaceInds = CreateBackgroundSpace()
backgroundSpaceProps = {
    'vertices' : np.array(backgroundSpaceVerts, dtype = np.float32),
    
    'indices' : np.array(backgroundSpaceInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'boundary' : [500.0, -500.0, 500.0, 500.0],

    'river_banks': [-400.0, 400.0],

    'opacity': 1.0,

    'type': 'background'
}

asteroidVerts, asteroidInds = CreateAsteroid()
asteroidProps = {
    'vertices' : np.array(asteroidVerts, dtype = np.float32),
    
    'indices' : np.array(asteroidInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'opacity': 1.0,

    'type': 'platform'
}

alienVerts, alienInds = CreateAlien()
alienProps = {
    'vertices' : np.array(alienVerts, dtype = np.float32),
    
    'indices' : np.array(alienInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'opacity': 1.0,

    'type': 'enemy'
}

astronautVerts, astronautInds = CreateAstronaut()
astronautProps = {
    'vertices' : np.array(astronautVerts, dtype = np.float32),
    
    'indices' : np.array(astronautInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'opacity': 1.0,

    'type': 'player'
}

backgroundMysticVerts, backgroundMysticInds = CreateBackgroundMystic()
backgroundMysticProps = {
    'vertices' : np.array(backgroundMysticVerts, dtype = np.float32),
    
    'indices' : np.array(backgroundMysticInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'boundary' : [500.0, -500.0, 500.0, 500.0],

    'river_banks': [-400.0, 400.0],

    'opacity': 1.0,

    'type': 'background'
}

magicalMatVerts, magicalMatInds = CreateMagicalMat()
magicalMatProps = {
    'vertices' : np.array(magicalMatVerts, dtype = np.float32),
    
    'indices' : np.array(magicalMatInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'opacity': 1.0,

    'type': 'platform'
}

wizardVerts, wizardInds = CreateWizard()
wizardProps = {
    'vertices' : np.array(wizardVerts, dtype = np.float32),
    
    'indices' : np.array(wizardInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'opacity': 1.0,

    'type': 'enemy'
}

mysticPlayerVerts, mysticPlayerInds = CreateMysticPlayer()
mysticPlayerProps = {
    'vertices' : np.array(mysticPlayerVerts, dtype = np.float32),
    
    'indices' : np.array(mysticPlayerInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'opacity': 1.0,

    'type': 'player'
}

keyVerts, keyInds = CreateKey()
keyProps = {
    'vertices' : np.array(keyVerts, dtype = np.float32),
    
    'indices' : np.array(keyInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'opacity': 1.0,

    'type': 'key'
}