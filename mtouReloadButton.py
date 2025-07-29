
# this script will only run inside of Unreal as a startup script
import unreal


def create_mtou_toolbar():

    # Create a new toolbar section
    toolbar_name = "MtoU Loader"
    section_name = "MtoULoaderSection"

    # Register the toolbar
    menus = unreal.ToolMenus.get()
    toolbar = menus.find_menu("LevelEditor.LevelEditorToolBar.User")

    if toolbar:
        toolbar.add_section(section_name, label=toolbar_name)

        # Add button entry
        entry = unreal.ToolMenuEntry(
            name="StoreCurrentProjectPath",
            type=unreal.MultiBlockType.TOOL_BAR_BUTTON
        )
        entry.set_label("Store Project Path")
        entry.set_tool_tip("Save current project path for MtoU Exporter")
        entry.set_icon("EditorStyle", "GenericCommands.Redo")  # Use any existing icon

        # Set the action
        entry.set_string_command(
            type=unreal.ToolMenuStringCommandType.PYTHON,
            custom_type="",
            string="mtouLoader.py"  # Python function
        )
        
        toolbar.add_menu_entry("StoreCurrentProjectPath", entry)

        # Refresh the toolbar
        menus.refresh_all_widgets()


create_mtou_toolbar()
