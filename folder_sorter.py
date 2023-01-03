import unreal
import os
import sys

# instances of unreal classes
editor_util_lib = unreal.EditorUtilityLibrary()
system_lib = unreal.SystemLibrary()
string_lib = unreal.StringLibrary()

editor_asset_lib = unreal.EditorAssetLibrary()

#get input from command whether to create folders in the assets' local location or the root folder
try:
    unreal_local_path_val = ((sys.argv[1]))
    if(string_lib.equal_equal_str_str(unreal_local_path_val,"true")): #if true it means user wants local location
        asset_loc_path = True
    else:
        asset_loc_path = False
except Exception as err: #incase the program is not called from Utility Blueprint default value is false
    asset_loc_path = False


assets = editor_util_lib.get_selected_assets() #this is to get the selected assets as well as the path
count = len(assets)

#get the path to sort folders
if(asset_loc_path):
    if(count is not 0): #incase nothing is selected
        assetName = assets[0].get_name()
        assetPath = assets[0].get_path_name()
        path_len = len(assetName)
        path_len = (path_len*2)+1
        path = string_lib.left_chop(assetPath,path_len) # removing asset name from the path
    else:
        unreal.log_error("No asset selected. Please select an asset")
else:
    path = "\Game" #path is the main root folder

unreal.log("Path is {}".format(path))
if(count is 0):
    unreal.log_error("No asset selected. Please select an asset")
    

with unreal.ScopedSlowTask(count, "Moving the assets") as ST:
    ST.make_dialog(True)
    
    #iterate through the assets
    for asset in assets:
        asset_class = asset.get_class()  # get the class
        asset_name = system_lib.get_object_name(asset) # get the asset name
        class_name = system_lib.get_class_display_name(asset_class) #get the class name to create folders

        #move the assets to the path
        try:
            new_path = os.path.join(path,class_name,asset_name) #create path name using the path and class
            editor_asset_lib.rename_loaded_asset(asset,new_path)
            unreal.log("Successfully moved {} to {}".format(asset_name,new_path))
        except Exception as exception:
            unreal.log("Encountered an error {}. Please try again".format(exception))
        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, asset_name)
