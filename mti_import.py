import bpy
import struct

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator

from .convert import Header

def read_header(f, file_path):
    with open(file_path, "rb") as f:
        header_data = f.read(Header.HEADER_SIZE)  # Read 32 bytes
        if len(header_data) != Header.HEADER_SIZE:
            print("Error: Header size mismatch")
            return None

        # Unpack the header data
        signature, version, instance_count, instance_size, unk0, unk1, unk2, instance_offset = struct.unpack(Header.HEADER_FORMAT, header_data)

        print(f"Signature: {hex(signature)}")
        print(f"Version: {version}")
        print(f"Instance Count: {instance_count}")
        print(f"Instance Size: {instance_size}")
        print(f"Instance Offset: {instance_offset} (ignoring hidden values)")

        return {
            "signature": signature,
            "version": version,
            "instance_count": instance_count,
            "instance_size": instance_size,
            "instance_offset": instance_offset
        }
        
def read_instances(f, instance_count):
    """Reads instance data and extracts only (x, y, z) positions."""
    vertices = []
    
    for i in range(instance_count):
        data = f.read(Header.INSTANCE_SIZE)
        if len(data) != Header.INSTANCE_SIZE:
            break  # Stop if EOF
        
        # Unpack full instance data
        posx, posy, posz, type, sway, pitchAfterSway, yawAfterSway, pitchBeforeSway, yawBeforeSway, A, R, G, B = struct.unpack(Header.INSTANCE_FORMAT, data)
        
        # Store only the position (x, y, z)
        vertices.append((posx, -posz, posy))
    
    return vertices
    
def create_mesh(instance):
    """Creates a new Blender mesh object from the given vertex positions."""
    mesh = bpy.data.meshes.new(name="ImportedMesh")
    obj = bpy.data.objects.new(name="ImportedObject", object_data=mesh)
    
    bpy.context.collection.objects.link(obj)

    # Assign vertices to the mesh (no faces for now)
    mesh.from_pydata(instance, [], [])
    mesh.update()

    print(f"Created mesh with {len(instance)} vertices.")

class ImportMtiFile(Operator, ImportHelper):
    """Import MTI File"""
    bl_idname = "import_mesh.mti_file"
    bl_label = "Import MTI File"

    filename_ext = ".mti"
    filter_glob: StringProperty(
        default="*.mti",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        return self.import_mti(context)

    def import_mti(self, context):
        # Open the file once and process everything sequentially
        try:
            with open(self.file_path, "rb") as f:
                header = read_header(f, self.file_path)

                # Move to the start of instance data
                f.seek(header["instance_offset"])

                # Read all instances
                vertices = read_instances(f, header["instance_count"])
                    
                # Create a mesh from these vertices
                create_mesh(vertices)

            self.report({'INFO'}, f"Successfully imported MetaInstance")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {str(e)}")
            return {'CANCELLED'}