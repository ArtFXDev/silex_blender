bl_info = {
    "name": "Silex Blender",
    "author": "ArtFX TDs",
    "description": "Silex pipeline integration (Conform, Publish, Submit...)",
    "version": (1, 0, 0),
    "blender": (2, 93, 0),
    "location": "3D View -> N -> Silex",
    "url": "https://github.com/ArtFXDev/silex_blender",
    "wiki_url": "https://github.com/ArtFXDev/silex_blender",
    "tracker_url": "https://github.com/ArtFXDev/silex_blender/issues",
    "category": "Pipeline",
}

import bpy
import os
from silex_client.action.action_query import ActionQuery
from silex_client.resolve.config import Config

# Stores the icon previews
preview_collections = {}

action_operators = []

for action_config in Config().actions:
    action_name = action_config["name"]
    action = ActionQuery(action_name)

    name = f"{action_name.capitalize()}ActionOperator"

    def action_execute(self, context):
        ActionQuery(action_name).execute()
        return {"FINISHED"}

    ActionOperator = type(
        name,
        (bpy.types.Operator,),
        {
            # Attributes
            "bl_idname": f"silex_blender.{action_name}_action",
            "bl_label": action.buffer.label,
            # Methods
            "execute": action_execute,
        },
    )

    action_operators.append(ActionOperator)


class SilexActionsPanel(bpy.types.Panel):
    bl_category = "Silex"
    bl_label = "Silex actions"
    bl_idname = "SILEX_PT_actions"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        for action_config in Config().actions:
            action_name = action_config["name"]
            icon = preview_collections["icons"][f"{action_name}.png"]

            layout.operator(
                f"silex_blender.{action_name}_action",
                text=action_name.capitalize(),
                icon_value=icon.icon_id,
            )


classes = action_operators + [SilexActionsPanel]


def register():
    import bpy.utils.previews

    # Load the action icons as previews
    pcoll = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    icon_files = os.listdir(icons_dir)

    for icon_file in icon_files:
        pcoll.load(icon_file, os.path.join(icons_dir, icon_file), "IMAGE")

    preview_collections["icons"] = pcoll

    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    # Remove icon previews
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)

    preview_collections.clear()

    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
