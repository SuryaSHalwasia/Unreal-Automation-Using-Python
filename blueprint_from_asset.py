#PLEASE NOTE: This script will only work for UE5+ as SubobjectDataHandle was introduced then
import unreal

# instances of unreal classes
editor_util_lib = unreal.EditorUtilityLibrary()
Factory = unreal.BlueprintFactory()
Factory.set_editor_property("ParentClass", unreal.Actor) #To set blueprint of type actor

assetTools = unreal.AssetToolsHelpers.get_asset_tools()
system_lib = unreal.SystemLibrary()
string_lib = unreal.StringLibrary()

@unreal.uclass()
class EditorAssetLIbrary(unreal.EditorAssetLibrary):
    pass

# get the selected assets
assets = editor_util_lib.get_selected_assets()
count = len(assets)

save = True #to ensure asset is saved
if(count is 0):
    unreal.log_error("No asset selected. Please select an asset")
    save = False

#iterate through the assets
with unreal.ScopedSlowTask(count, "Making blueprints from the assets") as ST:
    ST.make_dialog(True)
    for asset in assets:
        asset_class = asset.get_class()  # get the class
        class_name = system_lib.get_class_display_name(asset_class)
        if not (string_lib.contains(class_name, "ParticleSystem") or string_lib.contains(class_name, "StaticMesh")):  # check if the asset is a particle system or mesh
            unreal.log_error("The selected asset {} is not a particle system or static mesh.".format(system_lib.get_object_name(asset)))
            break

        assetName = asset.get_name()
        asset_original_name = asset.get_name() #to display in Scooped task
        assetPath = asset.get_path_name()
        
        asset_original_path = asset.get_path_name()
        unreal.log(asset_original_name)
        path_len = len(assetName)
        path_len = (path_len*2)+1
        assetPath = string_lib.left_chop(assetPath,path_len) # removing asset name from the path
        unreal.log(assetPath)


        if (assetName.startswith("SM_") or assetName.startswith("NS_")): #removing prefix if any
            assetName = string_lib.right_chop(assetName,3)
        elif assetName.startswith("P_"):
            assetName = string_lib.right_chop(assetName, 2)


        BlueprintName = string_lib.concat_str_str("BP_",assetName) 
        unreal.log(BlueprintName)

        new_blueprint = assetTools.create_asset(BlueprintName,assetPath,None,Factory) #create blueprint

        subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem) #required for blueprint
        root_data_handle = subsystem.k2_gather_subobject_data_for_blueprint(new_blueprint)
        #function to create the asset as an actor in the blueprint based on class
        def add_subobject(subsystem: unreal.SubobjectDataSubsystem,
                  blueprint: unreal.Blueprint,
                  new_class,
                  name: str ) -> ( unreal.SubobjectDataHandle, unreal.Object ):

            root_data_handle: unreal.SubobjectDataHandle = subsystem.k2_gather_subobject_data_for_blueprint(context=blueprint)[0]
            
            #create asset of type class
            sub_handle, fail_reason = subsystem.add_new_subobject(
                params=unreal.AddNewSubobjectParams(
                parent_handle=root_data_handle,
                new_class=new_class,
                blueprint_context=blueprint))

            if not fail_reason.is_empty():
                raise Exception("ERROR from sub_object_subsystem.add_new_subobject: {fail_reason}")
            #rename the created asset
            subsystem.rename_subobject(handle=sub_handle, new_name=unreal.Text(name))
            #attach to blueprint
            subsystem.attach_subobject(owner_handle=root_data_handle, child_to_add_handle=sub_handle)

            BFL = unreal.SubobjectDataBlueprintFunctionLibrary
            obj: Object = BFL.get_object(BFL.get_data(sub_handle)) #the obj is the asset created
            return sub_handle, obj
        #if selected is static mesh
        if (string_lib.contains(class_name, "StaticMesh")):
            sub_handle, obj = add_subobject(subsystem=subsystem, 
                                    blueprint=new_blueprint, 
                                    new_class=unreal.StaticMeshComponent, 
                                    name=assetName)
            assert isinstance(obj, unreal.StaticMeshComponent)
            mesh: unreal.StaticMesh = unreal.load_asset(asset_original_path) #load asset
            obj.set_static_mesh(new_mesh=mesh) #set asset to obj
            obj.set_editor_property(name="relative_location", value=unreal.Vector(0, 0, 0)) #reset loc
            unreal.log("Successfully created blueprint named {} from static mesh {}.".format(BlueprintName,asset_original_name))
       #if it is a particle system
        elif (string_lib.contains(class_name, "ParticleSystem")):
            sub_handle, obj = add_subobject(subsystem=subsystem, 
                                    blueprint=new_blueprint, 
                                    new_class=unreal.ParticleSystemComponent, 
                                    name=assetName)
            assert isinstance(obj, unreal.ParticleSystemComponent)
            particle: unreal.ParticleSystem = unreal.load_asset(asset_original_path)
            obj.set_template(new_template=particle)
            obj.set_editor_property(name="relative_location", value=unreal.Vector(0, 0, 0))
            unreal.log("Successfully created blueprint named {} from particle system {}.".format(BlueprintName,asset_original_name))
        
        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, asset_original_name)
if(save is True):
    EditorAssetLIbrary().save_loaded_asset(new_blueprint) #save asset