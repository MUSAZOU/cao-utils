import bpy
from bpy.props import IntProperty, CollectionProperty
from bpy.types import Panel, UIList

# #########################################
# Register
# #########################################

def get_activeSceneObject():
    return bpy.context.scene.objects.active.name

class Uilist_actions_cylinder(bpy.types.Operator):
    bl_idname = "customcylinder.list_action"
    bl_label = "List Action"

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('DISABLE', "DISABLE", ""),
            ('ENABLE', "ENABLE", "")
        )
    )

    def invoke(self, context, event):

        scn = context.scene
        idx = scn.custom_cylinder_index

        try:
            item = scn.custom_cylinder[idx]
        except IndexError:
            pass

        else:
            if self.action == 'DOWN' and idx < len(scn.custom_cylinder) - 1:
                item_next = scn.custom_cylinder[idx+1].name
                scn.custom_cylinder_index += 1
                info = 'Item %d selected' % (scn.custom_cylinder_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.custom_cylinder[idx-1].name
                scn.custom_cylinder_index -= 1
                info = 'Item %d selected' % (scn.custom_cylinder_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item %s removed from list' % (scn.custom_cylinder[scn.custom_cylinder_index].name)
                scn.custom_cylinder_index -= 1
                self.report({'INFO'}, info)
                scn.custom_cylinder.remove(idx)
            elif self.action == 'DISABLE':
                for i in range(0,idx+1):
                    scn.custom_cylinder[i].enabled = False
            elif self.action == 'ENABLE':
                for i in range(0,idx+1):
                    scn.custom_cylinder[i].enabled = True
        return {"FINISHED"}

# #########################################
# Draw Panels and Button
# #########################################

class UL_items_cylinder(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(0.3)
        split.label("%d" % (index))
        split.prop(item, "name", text="%s" % (item.enabled), emboss=False, translate=False, icon='BORDER_RECT')

    def invoke(self, context, event):
        pass   

class UIListPanelExample_cylinder(Panel):
    """Creates a Panel in the Object properties window"""
    bl_idname = 'OBJECT_PT_my_panel_cylinder'
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "3D Cylinders"

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene

        rows = 2
        row = layout.row()
        row.template_list("UL_items_cylinder", "", scn, "custom_cylinder", scn, "custom_cylinder_index", rows=rows)

        col = row.column(align=True)
        col.operator("customcylinder.list_action", icon='ZOOMOUT', text="").action = 'REMOVE'
        col.separator()
        col.operator("customcylinder.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("customcylinder.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
        col.separator()
        col.operator("customcylinder.list_action", icon='VISIBLE_IPO_ON', text="Enable All").action = 'ENABLE'
        col.operator("customcylinder.list_action", icon='VISIBLE_IPO_OFF', text="Disable All").action = 'DISABLE'

        row = layout.row()
        col = row.column(align=True)
        col.operator("customcylinder.select_item", icon="UV_SYNC_SELECT")
        col.operator("customcylinder.clear_list", icon="X")

class Uilist_selectAllItems_cylinder(bpy.types.Operator):
    bl_idname = "customcylinder.select_item"
    bl_label = "Select List Item"
    bl_description = "Select Item in scene"

    def __init__(self):
        self._ob_select = None

    def execute(self, context):
        scn = context.scene
        bpy.ops.object.select_all(action='DESELECT')
        idx = scn.custom_cylinder_index

        try:
            item = scn.custom_cylinder[idx]
        except IndexError:
            pass

        else:
            self._ob_select = bpy.data.objects[scn.custom_cylinder[scn.custom_cylinder_index].name]
            self._ob_select.select = True
            scn.ignit_panel.vp_model_types = self._ob_select["vp_model_types"]

            scn.ignit_panel.vp_obj_Point1 = self._ob_select["vp_obj_Point1"]
            scn.ignit_panel.vp_obj_Point2 = self._ob_select["vp_obj_Point2"]
            scn.ignit_panel.vp_radius = self._ob_select["vp_radius"]
            scn.ignit_panel.vp_export_enable = self._ob_select["vp_export_enable"]

        return{'FINISHED'}

class Uilist_clearAllItems_cylinder(bpy.types.Operator):
    bl_idname = "customcylinder.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items in the list"

    def execute(self, context):
        scn = context.scene
        lst = scn.custom_cylinder
        current_index = scn.custom_cylinder_index

        if len(lst) > 0:
            for i in range(len(lst)-1,-1,-1):
                scn.custom_cylinder.remove(i)
            self.report({'INFO'}, "All items removed")

        else:
            self.report({'INFO'}, "Nothing to remove")   

        return{'FINISHED'}

class CustomProp_cylinder(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    id = IntProperty()
    enabled = bpy.props.BoolProperty()
    global_enable = bpy.props.BoolProperty(name = "Enable For Export", description = "True or False?", default = True)

# #########################################
# Register
# #########################################

classes = (
    CustomProp_cylinder,
    Uilist_actions_cylinder,
    Uilist_clearAllItems_cylinder,
    Uilist_selectAllItems_cylinder,
    UIListPanelExample_cylinder,
    UL_items_cylinder
)

if __name__ == "__main__":
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
