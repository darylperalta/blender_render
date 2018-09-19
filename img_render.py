
camera_params_tuple = [0,45,2]
# da = 360/views
reso_tuple = [448,448]
# stepsize =
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
scene.render.alpha_mode = 'TRANSPARENT'
# model_identifier = os.path.split(os.path.split(obj)[0])[1]
# model_folder = os.path.split(os.path.split(os.path.split(obj)[0])[0])[1]
#print (model_folder)
image_path = "/home/daryl/"
fp = image_path
r = 1
print(fp)
scene.render.image_settings.file_format = 'PNG'  # set output format to .png
# for output_node in [depth_file_output]:
    # output_node.base_path = ''
#render and save image
# print("Rotation {}, {}".format((stepsize * n), radians(stepsize * n)))
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
