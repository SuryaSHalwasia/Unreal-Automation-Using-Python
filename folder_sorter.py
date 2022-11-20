import unreal
import os
import sys
# instances of unreal classes
editor_util_lib = unreal.EditorUtilityLibrary()
system_lib = unreal.SystemLibrary()
string_lib = unreal.StringLibrary()

editor_asset_lib = unreal.EditorAssetLibrary()

#get input from command
try:
    checkbox1 = ((sys.argv[1]))
    if(string_lib.equal_equal_str_str(checkbox1,"true")):
        checkbox = True
    else:
        checkbox = False
except Exception as err:
    checkbox = False

# get the selected assets
assets = editor_util_lib.get_selected_assets()
count = len(assets)

if(checkbox):
    if(count is not 0):
        assetName = assets[0].get_name()
        assetPath = assets[0].get_path_name()
        path_len = len(assetName)
        path_len = (path_len*2)+1
        path = string_lib.left_chop(assetPath,path_len) # removing asset name from the path
    else:
        unreal.log_error("No asset selected. Please select an asset")
else:
    path = "\Game"

unreal.log("Path is {}".format(path))
if(count is 0):
    unreal.log_error("No asset selected. Please select an asset")
#iterate through the assets
with unreal.ScopedSlowTask(count, "Moving the assets") as ST:
    ST.make_dialog(True)
    for asset in assets:
        asset_class = asset.get_class()  # get the class
        asset_name = system_lib.get_object_name(asset) # get the asset name
        class_name = system_lib.get_class_display_name(asset_class)
        try:
            new_path = os.path.join(path,class_name,asset_name)
            editor_asset_lib.rename_loaded_asset(asset,new_path)
            unreal.log("Successfully moved {} to {}".format(asset_name,new_path))
        except Exception as exception:
            unreal.log("Encountered an error {}. Please try again".format(exception))
        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, asset_name)
