import logging
from copy import copy

from model.module import Module
from services.open_files_service import OpenFilesService
from services.service_locator import locator


class CommonModuleService:
    def __init__(self):
        self._open_modules = {}

    def open_common_module(self, module_template: Module, file_path: str) -> Module:
        # First, check the cache.
        key = (module_template, file_path)
        if key in self._open_modules:
            return self._open_modules[key]

        # Not in the cache. Need to open the selected file and create a module copy.
        # First, convert the file path to one that starts at the ROM root.
        open_files_service: OpenFilesService = locator.get_scoped("OpenFilesService")
        valid_path = open_files_service.to_valid_path_in_filesystem(file_path)
        if not valid_path:
            raise ValueError

        # Create the module copy and attach to the target file.
        module = copy(module_template)
        module.update_post_shallow_copy_fields()
        archive = None  # TODO: This should be a method of the Module class.
        try:
            archive = open_files_service.open(valid_path)
            module.attach_to(archive)
        except Exception as ex:
            logging.exception("Failed to attach to module.")
            open_files_service.close_archive(archive)
            raise ex

        # Cache the new module and return it.
        self._open_modules[key] = module
        return module

    def save(self):
        for module in self._open_modules.values():
            logging.info("Committing changes from " + module.name + ".")  # TODO: Move into commit_changes
            module.commit_changes()

    def close_modules_using_archive(self, archive):
        keys_to_delete = []
        for (key, module) in self._open_modules.items():
            if module.archive and module.archive == archive:
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del self._open_modules[key]