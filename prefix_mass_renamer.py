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

string_lib = unreal.StringLibrary()


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
try:
    mass_rename1 = str((sys.argv[1]))
    mass_name = string_lib.right_chop(mass_rename1, 4)
    count = len(mass_name)
    mass_rename = string_lib.left_chop(mass_rename1,count)
    unreal.log_error(mass_rename)
except Exception as err:
    mass_rename = "fals"
    unreal.log_error("No inputs recived")
# instances of unreal classes
editor_util = unreal.EditorUtilityLibrary()
system_lib = unreal.SystemLibrary()

# get the selected assets
assets = editor_util.get_selected_assets()
count = len(assets)
suffix = 1
morethanOne = False
if(count is 0):
    unreal.log_error("Nothing is selected. Please select something")
elif (count >1):
    morethanOne = True
with unreal.ScopedSlowTask(count,"Renaming the assets") as ST:
    ST.make_dialog(True)
    for asset in assets:
        asset_name = system_lib.get_object_name(asset)
        asset_class = asset.get_class()
        class_name = system_lib.get_class_display_name(asset_class)
        asset_prefix = GetPrefix(class_name)
        if(string_lib.equal_equal_str_str(mass_rename,"fals")):
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
        if(string_lib.equal_equal_str_str(mass_rename,"true")):
            unreal.log(mass_rename)
            if asset_prefix is "null":
                unreal.log_warning("No mapping for asset {} of type {}".format(asset_name, class_name))
                asset_prefix = ""
            if(morethanOne is True):
                new_name = asset_prefix + mass_name + "_" + str(suffix)
            else:
                new_name = asset_prefix + mass_name
            editor_util.rename_asset(asset, new_name)
            unreal.log("1Successfully add prefix to {}. The new name is {}".format(asset_name, new_name))
            suffix = suffix+1
        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, asset_name)