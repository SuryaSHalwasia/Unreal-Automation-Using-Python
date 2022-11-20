import unreal

# instances of unreal classes
assetTools = unreal.AssetToolsHelpers.get_asset_tools()
material_editing_lib = unreal.MaterialEditingLibrary()
editor_asset_lib = unreal.EditorAssetLibrary()

system_lib = unreal.SystemLibrary()
string_lib = unreal.StringLibrary()
editor_util_lib = unreal.EditorUtilityLibrary()


Factory = unreal.MaterialFactoryNew()

unreal.log("*******PLEASE MAKE SURE THE TEXTURES ARE NAMED IN THE CONVENTION _D, _N, _M for diffuse, normal and masks map respectively************")
# get the selected assets
assets = editor_util_lib.get_selected_assets()
count = len(assets)

#get the name of the texture for the material
if(count is 0):
    unreal.log_error("No texture selected. Please select a texture")
else:
    assetName = assets[0].get_name()
    assetPath = assets[0].get_path_name()
    path_len = len(assetName)
    path_len = (path_len * 2) + 1
    path = string_lib.left_chop(assetPath, path_len)  # removing asset name from the path
    if (assetName.startswith("T_")) :  # removing prefix if any
        assetName = string_lib.right_chop(assetName, 2)
    assetName = string_lib.left_chop(assetName, 2)
    mat_name = string_lib.concat_str_str("M_",assetName)
    new_material = assetTools.create_asset(mat_name,path,None,Factory)
    unreal.log("Successfully created new material {}.".format(new_material))

#iterate through the assts
with unreal.ScopedSlowTask(count, "Making material from the texturess") as ST:
    ST.make_dialog(True)
    for asset in assets:
        assetName = asset.get_name()
        asset_class = asset.get_class()  # get the class
        class_name = system_lib.get_class_display_name(asset_class)
        if not string_lib.contains(class_name, "Texture2D"):  # check if the asset is a texture
            unreal.log_error("The selected asset {} is not a texture.".format(system_lib.get_object_name(asset)))
            break

        if string_lib.ends_with(assetName,"_D"):  # check if the texture is a BASE COLOR
            diffuse = material_editing_lib.create_material_expression(new_material,unreal.MaterialExpressionTextureSample,-384,-200)
            material_editing_lib.connect_material_property(diffuse,"RGB", unreal.MaterialProperty.MP_BASE_COLOR)
            diffuse.texture = asset
            unreal.log("Successfully added {} as diffuse map".format(assetName))
        elif string_lib.contains(str(asset.compression_settings), "NORMALMAP"):  # check if the texture is a NORMAL MAP
            normal = material_editing_lib.create_material_expression(new_material,unreal.MaterialExpressionTextureSample,-384,500)
            material_editing_lib.connect_material_property(normal,"RGB", unreal.MaterialProperty.MP_NORMAL)
            normal.texture = asset
            normal.sampler_type = unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL
            unreal.log("Successfully added {} as normal map".format(assetName))
        elif string_lib.ends_with(assetName,"_M"):  # check if the texture is a MASK MAP
            mask_map = material_editing_lib.create_material_expression(new_material, unreal.MaterialExpressionTextureSample,-384, 150)
            if (str(asset.compression_settings) is not  "TC_DEFAULT"):
                asset.compression_settings = unreal.TextureCompressionSettings.TC_DEFAULT
                editor_asset_lib.save_loaded_asset(asset)
            material_editing_lib.connect_material_property(mask_map, "R", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
            mask_map.texture = asset
            material_editing_lib.connect_material_property(mask_map, "G",unreal.MaterialProperty.MP_ROUGHNESS)
            mask_map.texture = asset
            material_editing_lib.connect_material_property(mask_map, "B", unreal.MaterialProperty.MP_METALLIC)
            mask_map.texture = asset
            unreal.log("Successfully added {} as mask map".format(assetName))
        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, assetName)

#save the asset
if (count is not 0):
    material_editing_lib.recompile_material(new_material)
    editor_asset_lib.save_loaded_asset(new_material)
    unreal.log("Successfully saved material {}.".format(new_material))