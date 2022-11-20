import unreal

# instances of unreal classes
editor_util_lib = unreal.EditorUtilityLibrary()
system_lib = unreal.SystemLibrary()
string_lib = unreal.StringLibrary()
# get the selected assets
assets = editor_util_lib.get_selected_assets()
count = len(assets)

if(count is 0):
    unreal.log_error("No asset selected. Please select a normal map")

#iterate through the assets
for asset in assets:
    asset_class = asset.get_class() #get the class
    class_name = system_lib.get_class_display_name(asset_class)
    if not string_lib.contains(class_name,"Texture2D"): #check if the asset is a texture
        unreal.log_error("The selected asset {} is not a texture.".format(system_lib.get_object_name(asset)))
        break
    if not string_lib.contains(str(asset.compression_settings),"NORMALMAP"): #check if the texture is a normal map
        unreal.log_error("The selected map {} is not a normal map.".format(system_lib.get_object_name(asset)))
        break
    asset.flip_green_channel = not(asset.flip_green_channel) #flip green channel
    flipping = asset.flip_green_channel
    if(flipping is True):
        unreal.log("The selected map {} has now flipped green channel.".format(system_lib.get_object_name(asset)))
    else:
        unreal.log("The selected map {} now does not have flipped green channel.".format(system_lib.get_object_name(asset)))