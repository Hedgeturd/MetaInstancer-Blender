import bpy
import struct
import os
import mathutils

import re, random

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.types import Operator
from .convert import Header, Convert

def get_type_from_particle_system(psys):
    """Extracts type(s) from particle system name and returns a random value or the first value."""
    match = re.search(r'@TYPE\(([\d,\s]+)\)', psys.name)
    if match:
        values = [int(v) for v in match.group(1).split(',')]
        return random.choice(values) if len(values) > 1 else values[0]

    # If no match, return 0
    return 0

def get_particle_data():
    """Extracts particle system positions and rotations."""
    obj = bpy.context.object
    if obj is None or obj.type != 'MESH':
        print("No valid mesh object selected.")
        return []

    particles = []

    for psys in obj.particle_systems:
        for particle in psys.particles:
            posx, posy, posz = particle.location

            # Particle's rotation quaternion (includes normal alignment)
            normal_vector = particle.rotation @ mathutils.Vector((0, 0, 1))
            # Convert normal vector to Euler for pitch and yaw
            rotation_matrix = normal_vector.to_track_quat('X', 'Z').to_euler()

            # Extract pitch and yaw
            pitch = rotation_matrix.x
            yaw = rotation_matrix.z

            type = get_type_from_particle_system(psys)
            print(type)
            
            particles.append((posx, posy, posz, pitch, yaw, type))#roll, type))

    return particles

class ExportMtiFile(Operator, ExportHelper):
    """Export MTI File"""
    bl_idname = "export_mesh.mti_file"
    bl_label = "Export MTI File"

    filename_ext = ".mti"
    filter_glob: StringProperty(
        default="*.mti",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        # Run the export function
        return self.export_to_hex(context)

    def export_to_hex(self, context):
        """Exports particle system data to a hex file."""
        try:
            bpy.ops.object.mode_set(mode='PARTICLE_EDIT')
            particles = get_particle_data()
            if not particles:
                self.report({'ERROR'}, f"No Hair Particles in Object.")
                return {"CANCELLED"}
        except Exception as e:
            self.report({'ERROR'}, f"No valid mesh object selected. {str(e)}")
            return {"CANCELLED"}

        instance_count = len(particles)
        instance_size = Header.INSTANCE_SIZE
        instance_offset = Header.HEADER_SIZE  # Instances start after the header

        try:
            # Create a binary file
            if os.path.exists(self.filepath):
                os.remove(self.filepath)
                print(f"Existing file '{self.filepath}' deleted.")

            with open(self.filepath, "wb") as f:
                # Write header (signature, version, count, size, padding, instance_offset)
                header_data = struct.pack(
                    Header.HEADER_FORMAT, 
                    0x4D544920,  # Example signature
                    1,           # Version
                    instance_count,
                    instance_size,
                    0, 0, 0,     # Hidden unknown values
                    instance_offset
                )
                print(header_data)
                f.write(header_data)

                # Write each instance (particle)
                for particle in particles:
                    #print(particle)
                    posx, posy, posz, pitch, yaw, type = particle
                    
                    # Apply coordinate transformation
                    posx, posy, posz = posx, posz, -posy  # Invert Z and swap Y/Z

                    # Convert pitch and yaw to int16
                    pitch_uint8 = Convert.to_uint8(pitch)
                    yaw_uint8 = Convert.to_uint8(yaw)
                    pitch_int16 = Convert.to_int16(pitch)
                    yaw_int16 = Convert.to_int16(yaw)

                    # Other default values
                    sway = 255
                    A, R, G, B = 1,1,1,1

                    instance_data = struct.pack(
                        Header.INSTANCE_FORMAT,
                        posx, posy, posz,
                        type, sway,
                        pitch_uint8, yaw_uint8,
                        pitch_int16, yaw_int16,
                        A, R, G, B
                    )
                    f.write(instance_data)

            print(f"✅ Exported {instance_count} particle instances to {self.filepath}")
            self.report({'INFO'}, f"Successfully imported MetaInstance")
            bpy.ops.object.mode_set(mode='OBJECT')
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            bpy.ops.object.mode_set(mode='OBJECT')
            return {'CANCELLED'}