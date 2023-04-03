bl_info = {
    "name": "Shapekey Warning",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Sidebar > Shapekey Warning",
    "description": "Displays a warning when editing non-Basis shapekeys",
    "category": "3D View",
}

import bpy
import blf
import bgl
from bpy.types import Panel
from bpy.app.handlers import persistent

addon_key = "shapekey_warning"

@persistent
def draw_shapekey_warning(scene):
    context = bpy.context
    if context.mode == 'EDIT_MESH':
        obj = context.active_object
        if obj and obj.type == 'MESH' and obj.data.shape_keys:
            shapekey = obj.active_shape_key
            if shapekey and shapekey.name != 'Basis':
                prefs = context.preferences.addons[addon_key].preferences
                font_id = 0
                blf.size(font_id, prefs.font_size, 72)
                bgl.glEnable(bgl.GL_BLEND)
                blf.color(font_id, prefs.text_color[0], prefs.text_color[1], prefs.text_color[2], prefs.text_color[3])
                blf.position(font_id, prefs.location_x, prefs.location_y, 0)
                blf.draw(font_id, prefs.warning_text)
                bgl.glDisable(bgl.GL_BLEND)

def draw_callback_px():
    draw_shapekey_warning(bpy.context.scene)

class ShapeKeyWarning_PT_Panel(Panel):
    bl_label = "Shapekey Warning"
    bl_idname = "SHAPEKEY_PT_warning_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shapekey Warning'

    def draw(self, context):
        layout = self.layout
        prefs = context.preferences.addons[addon_key].preferences
        layout.prop(prefs, "warning_text")
        layout.prop(prefs, "font_size")
        layout.prop(prefs, "location_x")
        layout.prop(prefs, "location_y")
        layout.prop(prefs, "text_color")

class ShapeKeyWarningPreferences(bpy.types.AddonPreferences):
    bl_idname = addon_key

    handle = None

    warning_text: bpy.props.StringProperty(
        name="Warning Text",
        description="Text to display when editing a non-Basis shapekey",
        default="YOU ARE EDITING A SHAPEKEY"
    )

    font_size: bpy.props.IntProperty(
        name="Font Size",
        description="Size of the warning text",
        default=24,
        min=10,
        max=100
    )

    location_x: bpy.props.IntProperty(
        name="Location X",
        description="X position of the warning text",
        default=15,
        min=0
    )

    location_y: bpy.props.IntProperty(
        name="Location Y",
        description="Y position of the warning text",
        default=80,
        min=0
    )

    text_color: bpy.props.FloatVectorProperty(
        name="Text Color",
        description="Color of the warning text",
        subtype='COLOR',
        size=4,
        min=0,
        max=1,
        default=(1, 1, 1, 1)
    )

    def draw(self, context):
            layout = self.layout
            prefs = context.preferences.addons[addon_key].preferences
            layout.prop(prefs, "warning_text")
            layout.prop(prefs, "font_size")
            layout.prop(prefs, "location_x")
            layout.prop(prefs, "location_y")
            layout.prop(prefs, "text_color")


def register():
    bpy.utils.register_class(ShapeKeyWarningPreferences)
    bpy.utils.register_class(ShapeKeyWarning_PT_Panel)
    if bpy.app.version >= (2, 81, 0):
        bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, (), 'WINDOW', 'POST_PIXEL')
    else:
        bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, (), 'WINDOW')

def unregister():
    bpy.utils.unregister_class(ShapeKeyWarning_PT_Panel)
    bpy.utils.unregister_class(ShapeKeyWarningPreferences)


if addon_key == "__main__":
    register()
