import unreal
import sys
# instances of unreal classes
editor_asset_lib = unreal.EditorAssetLibrary()
string_lib = unreal.StringLibrary()

path = "/Game/"

#get input from command
try:
    unreferenced_assets_delete1 = ((sys.argv[1]))
    if(string_lib.equal_equal_str_str(unreferenced_assets_delete1,"true")):
        unreferenced_assets_delete = True
    else:
        unreferenced_assets_delete = False
except Exception as err:
    unreferenced_assets_delete = False


#unreal.EditorLoadingAndSavingUtils().save_packages_with_dialog(assets,False)


# get all assets
assets = editor_asset_lib.list_assets(path, recursive=True, include_folder=True)
folders = [asset for asset in assets if editor_asset_lib.does_directory_exist(asset)]
count = len(folders)
with unreal.ScopedSlowTask(count, "Deleting empty folders....") as ST:
    ST.make_dialog(True)
    #iterate through folders
    for folder in folders:
        dont_delete = editor_asset_lib.does_directory_have_assets(folder)

        if not dont_delete:
            editor_asset_lib.delete_directory(folder)
            unreal.log("The folder {} was empty. It was successfully deleted".format(folder))
        if ST.should_cancel():
            break
        ST.enter_progress_frame(1)
    unreal.log("All empty folders are now deleted")

if (unreferenced_assets_delete is True):
    # get all assets
    assets = editor_asset_lib.list_assets(path, recursive=True, include_folder=False)
    count = len(assets)
    currentDeleted = ""
    with unreal.ScopedSlowTask(count, "Deleting %s" %currentDeleted) as ST:
        ST.make_dialog(True)
        for asset in assets:
            currentDeleted = asset
            refs = editor_asset_lib.find_package_referencers_for_asset(asset,False)
            if(len(refs)<=0):
                unreal.log("The asset deleted was %s." %asset)
                editor_asset_lib.delete_asset(asset)
            if ST.should_cancel():
                break
                unreal.log("All unreferenced assets are not deleted. The task was halted!")
            ST.enter_progress_frame(1,"Deleting %s" %currentDeleted)
    unreal.log("All unreferenced assets are now deleted")

