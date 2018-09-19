from math import radians, pi, sin, cos
import bpy
import numpy as np
import os


'''
def getFiles(dir):
    models = []
    ctr = 0
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith("obj"):
                fullpath = os.path.join(root, file)
                models.append(fullpath)
                print(ctr, os.path.join(root, file))
                ctr += 1
            #if ctr == 10:
                #models.sort()
                #return models
    models.sort()
    return models
'''
def LoadMatrixFromFile(filename):

    tmp = []
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
        return lines

# obj = LoadMatrixFromFile(objlist)
# print("Start: ")
# start = int(input())
# print("End: ")
# end = int(input())
#
# print("Start with", start, "\nEnd with ", end)
#obj = np.array(getFiles(dir))

#print(obj)
#print(obj.shape)

def writePose(filename, pose):
    with open(filename, 'w') as f:
        pose_text = '{:6.6f} {:6.6f} {:6.6f} {:6.6f} {:6.6f} {:6.6f}'.format(pose[0], pose[1], pose[2], pose[3], pose[4], pose[5])
        f.write(pose_text)

def man_render_image(camera_params_tuple,obj, stepsize, image_path='/home/usr/Desktop/DataSet', reso_tuple= [448,448], n = 0, transparent=False):
    azimuth = camera_params_tuple[0]
    elevation = camera_params_tuple[1]
    distance = camera_params_tuple[2]
    if distance==0:
        raise ValueError("distance must be greater than 0.")
    azimuth=azimuth*(pi/180) #converting from degrees to radians
    elevation=elevation*(pi/180)
    p = pi/2
    #calculating translation coordinates
    tx = distance*sin(p-elevation)*cos(azimuth)
    ty = distance*sin(p-elevation)*sin(azimuth)
    tz = distance*cos(p-elevation)
    print("Translation coordinates(tx,ty,tz): {}, {}, {}".format(round(tx,2), round(ty, 2), round(tz, 2)))
    #calculating rotation coordinates
    ry = (p-elevation)
    rx = 0
    rz = azimuth
    rx_deg = rx*(180/pi)
    ry_deg = ry*(180/pi)
    rz_deg = rz*(180/pi)
    print("Rotation coordinates(rx,ry,rz): {}, {}, {}".format(round(rx_deg,2), round(ry_deg, 2), round(rz_deg, 2)))
    fov = 50.0
    scene = bpy.data.scenes["Scene"]
    # Set render resolution
    scene.render.resolution_x = reso_tuple[0]
    scene.render.resolution_y = reso_tuple[1]
    # Set camera fov in degrees
    scene.camera.data.angle = fov*(pi/180.0)
    # Set camera rotation in euler angles
    scene.camera.rotation_mode = 'XYZ'
    scene.camera.rotation_euler[0] = rx
    scene.camera.rotation_euler[1] = ry
    scene.camera.rotation_euler[2] = rz
    # Set camera translation
    scene.camera.location.x = tx
    scene.camera.location.y = ty
    scene.camera.location.z = tz
    if transparent == True:
        scene.render.alpha_mode = 'TRANSPARENT'
    # model_identifier = os.path.split(os.path.split(obj)[0])[1]
    # model_folder = os.path.split(os.path.split(os.path.split(obj)[0])[0])[1]
    #print (model_folder)
    fp = image_path
    print(fp)
    scene.render.image_settings.file_format = 'PNG'  # set output format to .png
    # for output_node in [depth_file_output]:
        # output_node.base_path = ''
    #render and save image
    print("Rotation {}, {}".format((stepsize * n), radians(stepsize * n)))
    print(scene.camera.location)
    scene.render.filepath = fp + '/' + str(r)
    #depth_file_output.file_slots[0].path = scene.render.filepath + "_depth.exr"
    bpy.ops.render.render(write_still=True)  # render still
    #pose = [rx,ry,rz,tx,ty,tz]
    #print("pose:",pose)
    #writePose(scene.render.filepath + "_pose.txt", pose)
    #image_path = image_path + '/image'+str(n)+'.png'
    #bpy.data.scenes['Scene'].render.filepath = scene.render.filepath + ".png"
    #bpy.ops.render.render(use_viewport=True,  write_still=True)
    #print('image rendered')

############## main

if __name__ == '__main__':

    dir ='/home/ndpmedina/ShapeNetCore'
    defaultfile = '/home/ndpmedina/untitled.blend'
    # objlist = '/home/ndpmedina/list.txt'
    # format = 'OPEN_EXR'
    #obj = ['/media/raimarc/airscan4/datasets/ShapeNetCore.v1/02691156/1a04e3eab45ca15dd86060f189eb133/model.obj',
    #y'/media/raimarc/airscan4/datasets/ShapeNetCore.v1/02691156/1a6ad7a24bb89733f412783097373bdc/model.obj'
    #output_folder = '/home/raimarc/Documents/AIRSCAN/stanford-shapenet-renderer/tmp2'
    #output_folder = '/home/ndpmedina/ShapeNetCore/DataSet'
    color_depth = '16'
    depth_scale = 1.4
    views = 25

    defaultfile = '/home/daryl/Downloads/blender_render/untitled.blend'
    path = "/home/daryl/Downloads/FBX_OBJ/airscanBuilding/Building.fbx"
    bpy.ops.wm.open_mainfile(filepath=defaultfile)

    bpy.ops.import_scene.fbx(filepath=path)
    #print('OBJ ')
    #print(obj[i])
    output_folder = path.strip('/model.obj')
    output_folder = output_folder + '/rendering'
    output_folder = output_folder.strip('home/daryl/Downloads')

    print(output_folder)
    for object in bpy.context.scene.objects:
        # if object.name in ['Camera', 'Lamp']:
        #     continue
        # elif object.name in ['Cube']:
        #     # Delete default cube
        #     bpy.data.objects['Cube'].select = True
        #     bpy.ops.object.delete()
        bpy.context.scene.objects.active = object
        '''
        if args.scale != 1:
            bpy.ops.transform.resize(value=(args.scale,args.scale,args.scale))
            bpy.ops.object.transform_apply(scale=True)
        if args.remove_doubles:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.remove_doubles()
            bpy.ops.object.mode_set(mode='OBJECT')
        if args.edge_split:
            bpy.context.object.modifiers["EdgeSplit"].split_angle = 1.32645
            bpy.ops.object.modifier_add(type='EDGE_SPLIT')
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="EdgeSplit")
        '''
    # Make light just directional, disable shadows.
    lamp = bpy.data.lamps['Lamp']
    lamp.type = 'SUN'
    lamp.shadow_method = 'NOSHADOW'
    # Possibly disable specular shading:
    lamp.energy = 1
    lamp.use_specular = False

    # Add another light source so stuff facing away from light is not completely dark
    bpy.ops.object.lamp_add(type='SUN')
    lamp2 = bpy.data.lamps['Sun']
    lamp2.shadow_method = 'NOSHADOW'
    lamp2.use_specular = False
    lamp2.energy = 1
    bpy.data.objects['Sun'].rotation_euler = bpy.data.objects['Lamp'].rotation_euler
    bpy.data.objects['Sun'].rotation_euler[0] += 180
    bpy.data.objects['Sun'].rotation_euler[1] += 180



    camera_params_tuple = [0,45,1.5]
    da = 360/views
    # reso_tuple = [448,448]
    reso_tuple = [640,480]
    for r in range(views):
        camera_params_tuple[0] = camera_params_tuple[0] + da
        # camera_params_tuple[0] = camera_params_tuple[0] + da + np.random.uniform(-0.2,0.2,1)[0]
        # camera_params_tuple[1] = 30 + np.random.uniform(-0.5,0.5,1)[0]
        # camera_params_tuple[2] = 1 + np.random.uniform(-0.05,0.05,1)[0]
        #print(r)
        man_render_image(camera_params_tuple, path, da, output_folder, reso_tuple, r)

        # Delete default cube
        #bpy.data.objects['Cube'].select = True
        #bpy.ops.object.delete()
