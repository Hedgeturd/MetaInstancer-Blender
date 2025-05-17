import bpy

from .mti_import import ImportMtiFile
from .export import ExportMtiFile

bl_info = {
    "name": "MetaInstancer",
    "description": "Import/Export MTI Data",
    "author": "Hedgeturd",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "warning": "",
    "wiki_url": "",
    "category": "Import-Export"
}

# Register addon classes
def menu_func_import(self, context):
    self.layout.operator(ImportMtiFile.bl_idname, text="Meta Instancer (.mti)")

def menu_func_export(self, context):
    self.layout.operator(ExportMtiFile.bl_idname, text="Meta Instancer (.mti)")

def register():
    bpy.utils.register_class(ImportMtiFile)
    bpy.utils.register_class(ExportMtiFile)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(ImportMtiFile)
    bpy.utils.unregister_class(ExportMtiFile)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()