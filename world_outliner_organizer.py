import unreal

# instances of unreal classes
editor_level_lib = unreal.EditorLevelLibrary()
editor_filter_lib = unreal.EditorFilterLibrary()

#get all assets
assets = editor_level_lib.get_all_level_actors()

meshes = editor_filter_lib.by_class(assets, unreal.StaticMeshActor)
fog = editor_filter_lib.by_class(assets,unreal.AtmosphericFog)
lights = editor_filter_lib.by_id_name(assets,"Light")
reflection_captures = editor_filter_lib.by_class(assets,unreal.ReflectionCapture)
bps = editor_filter_lib.by_id_name(assets,"BP_")

#folder mapping
folders = {
    "StaticMeshes":meshes,
    "ReflectionCaptures":reflection_captures,
    "Blueprints":bps,
    "Lights":lights,
    "Fog":fog
}

for folder in folders:
    for asset in folders[folder]:
        asset.set_folder_path(folder)
