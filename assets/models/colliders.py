import bpy
from mathutils import Quaternion

print("")
print("")
print("")
print("        pos = [")
for child in bpy.data.objects["Colliders"].children:
    loc = child.location
    x = round(loc.x, 4)
    y = round(loc.y, 4)
    z = round(loc.z, 4)
    print("            [" + str(x) + ", " + str(z) + ", " + str(-y) + "]" + ", ")
print("        ]")

print("")
print("        rot = [")
for child in bpy.data.objects["Colliders"].children:
    quat = child.rotation_quaternion
    rx = round(quat.x, 4)
    ry = round(quat.y, 4)
    rz = round(quat.z, 4)
    rw = round(quat.w, 4)

    print("            [" + str(rx) + ", " + str(rz) + ", " + str(-ry) + ", " + str(rw) + "]" + ", ")
print("        ]")

print("")
print("        scale = [")
for child in bpy.data.objects["Colliders"].children:
    scale = child.scale
    sx = round(scale.x / 2, 4)
    sy = round(scale.y / 2, 4)
    sz = round(scale.z / 2, 4)
    print("            [" + str(sx) + ", " + str(sz) + ", " + str(sy) + "]" + ", ")
print("        ]")
