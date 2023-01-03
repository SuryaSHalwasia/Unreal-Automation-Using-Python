#This program can clean unreferenced assets and empty folders. Select the options correctly.
import unreal
import sys

# instances of unreal classes
editor_asset_lib = unreal.EditorAssetLibrary()
string_lib = unreal.StringLibrary()

path = "/Game/"

#get input from command whether to remove unreferenced assets
try:
    unreal_unreferenced_assets_delete_val = ((sys.argv[1]))
    if(string_lib.equal_equal_str_str(unreal_unreferenced_assets_delete_val,"true")):
        unreferenced_assets_delete = True
    else:
        unreferenced_assets_delete = False
except Exception as err:
    unreferenced_assets_delete = False #incase Utility Blueprint is not used the default value is false


# get all assets
assets = editor_asset_lib.list_assets(path, recursive=True, include_folder=True) #get all assets
folders = [asset for asset in assets if editor_asset_lib.does_directory_exist(asset)] #get all folders
count = len(folders)
with unreal.ScopedSlowTask(count, "Deleting empty folders....") as ST:
    ST.make_dialog(True)
    #iterate through folders
    for folder in folders:
        dont_delete = editor_asset_lib.does_directory_have_assets(folder) #incase the folder has assets

        if not dont_delete:
            editor_asset_lib.delete_directory(folder)
            unreal.log("The folder {} was empty. It was successfully deleted".format(folder))
        if ST.should_cancel():
            break
        ST.enter_progress_frame(1)
    unreal.log("All empty folders are now deleted")

#delete unreferenced assets
if (unreferenced_assets_delete is True):
    # get all assets
    assets = editor_asset_lib.list_assets(path, recursive=True, include_folder=False)
    count = len(assets)
    currentDeleted = ""
    with unreal.ScopedSlowTask(count, "Deleting %s" %currentDeleted) as ST:
        ST.make_dialog(True)
        for asset in assets: #iterate through assets
            currentDeleted = asset
            refs = editor_asset_lib.find_package_referencers_for_asset(asset,False) #get number of references
            if(len(refs)<=0): #if assets has no referenced assets
                unreal.log("The asset deleted was %s." %asset)
                editor_asset_lib.delete_asset(asset) #deleting asset
            if ST.should_cancel():
                break
                unreal.log("All unreferenced assets are not deleted. The task was halted!")
            ST.enter_progress_frame(1,"Deleting %s" %currentDeleted)
    unreal.log("All unreferenced assets are now deleted")

