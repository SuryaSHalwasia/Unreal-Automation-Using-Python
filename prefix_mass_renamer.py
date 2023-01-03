import sys

import unreal

#PREFIXES
prefixAnimationSequence     = "ANIM_"
prefixAnimation             = "ANIM_"
prefixBlueprint             = "BP_"
prefixLevel                 = "LVL_"
prefixMaterial              = "M_"
prefixMaterialFunction      = "MF_"
prefixMaterialInstance      = "MI_"
prefixParticleSystem        = "PS_"
prefixSkeletalMesh          = "SK_"
prefixSkeleton              = "SKL_"
prefixStaticMesh            = "SM_"
prefixSoundCue              = "SC_"
prefixSoundWave             = "S_"
prefixTexture2D             = "T_"
prefixWidgetBlueprint       = "WBP_"

string_lib = unreal.StringLibrary() #using string library

#This returns the prefix based on the class name of the asset
def GetPrefix(className):
    prefix = ""
    if className == "AnimSequence":
        prefix = prefixAnimationSequence
    elif className == "Animation":
        prefix = prefixAnimation
    elif className == "Blueprint":
        prefix = prefixBlueprint
    elif className == "World":
        prefix = prefixLevel
    elif className == "Material":
        prefix = prefixMaterial
    elif className == "MaterialFunction":
        prefix = prefixMaterialFunction
    elif className == "MaterialInstance":
        prefix = prefixMaterialInstance
    elif className == "ParticleSystem":
        prefix = prefixParticleSystem
    elif className == "SkeletalMesh":
        prefix = prefixSkeletalMesh
    elif className == "Skeleton":
        prefix = prefixSkeleton
    elif className == "SoundCue":
        prefix = prefixSoundCue
    elif className == "SoundWave":
        prefix = prefixSoundWave
    elif className == "StaticMesh":
        prefix = prefixStaticMesh
    elif className == "Texture2D":
        prefix = prefixTexture2D
    elif className == "EditorUtilityWidgetBlueprint":
        prefix = prefixWidgetBlueprint
    else:
        prefix = "null"
    return  prefix

#the checkbox and the name is the result of system arguments. Eg. truenewname/ falsenewname
try:
    unreal_mass_rename_val = str((sys.argv[1])) #get the checkbox val and name enter by the user for renaming
    mass_name = string_lib.right_chop(unreal_mass_rename_val, 4) #if true then chop will give new name. If batch rename is false then name wont matter
    count = len(mass_name)
    mass_rename = string_lib.left_chop(unreal_mass_rename_val,count) #chop the name to get true or fals since only 4 letters were chopped above
except Exception as err:
    mass_rename = "fals" #default value of fals
    unreal.log_error("No inputs recived")

# instances of unreal classes
editor_util = unreal.EditorUtilityLibrary()
system_lib = unreal.SystemLibrary()

# get the selected assets
assets = editor_util.get_selected_assets()
count = len(assets)

suffix = 1 #incase more than one asset then append suffix
morethanOne = False #Only one asset is assumed

if(count is 0):
    unreal.log_error("Nothing is selected. Please select something")
elif (count >1):
    morethanOne = True #more than one asset

with unreal.ScopedSlowTask(count,"Renaming the assets") as ST:
    ST.make_dialog(True)
    #iterate through the assets
    for asset in assets:
        asset_name = system_lib.get_object_name(asset) #get the name
        asset_class = asset.get_class() #get the class
        class_name = system_lib.get_class_display_name(asset_class)
        asset_prefix = GetPrefix(class_name) #get the prefix

        if(string_lib.equal_equal_str_str(mass_rename,"fals")): #no renaming required
            if asset_prefix is "null":
                unreal.log_warning("No mapping for asset {} of type {}".format(asset_name, class_name))
                continue
            if not asset_name.startswith(asset_prefix):
                # rename the asset and add prefix
                new_name = asset_prefix + asset_name
                editor_util.rename_asset(asset, new_name)
                unreal.log("Successfully add prefix to {}. The new name is {}".format(asset_name, new_name))
            else:
                unreal.log("The asset {} is already prefixed.".format(asset_name))

        if(string_lib.equal_equal_str_str(mass_rename,"true")): #renaming
            unreal.log(mass_rename)
            if asset_prefix is "null":
                unreal.log_warning("No mapping for asset {} of type {}".format(asset_name, class_name))
                asset_prefix = ""
            if(morethanOne is True): #more than one asset will have a suffix number
                new_name = asset_prefix + mass_name + "_" + str(suffix)
            else:
                new_name = asset_prefix + mass_name
            editor_util.rename_asset(asset, new_name)
            
            unreal.log("1Successfully add prefix to {}. The new name is {}".format(asset_name, new_name))
            suffix = suffix+1
        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, asset_name)