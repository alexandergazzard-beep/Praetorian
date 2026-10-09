import unreal
assert unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True,True),'Refusing shutdown with unsaved packages'
print('IMPACT_RESTART_PACKAGES_SAVED',flush=True)
unreal.SystemLibrary.quit_editor()
