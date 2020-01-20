from model.fe14.chapter_data import ChapterData
from services.service_locator import locator
from ui.fe14_chapter_editor import FE14ChapterEditor
from utils.chapter_utils import detect_chapter_file_sub_folder

_CONFIG_PATH = "/map/config/%s.bin"
_DISPOS_PATH = "/GameData/Dispos/%s.bin.lz"
_PERSON_PATH = "/GameData/Person/%s.bin.lz"
_TERRAIN_PATH = "/GameData/Terrain/%s.bin.lz"


class ChapterService:
    def __init__(self):
        self.editor = FE14ChapterEditor()
        self.open_chapters = {}

    def get_chapter_data_from_chapter(self, chapter):
        cid = chapter["CID"].value
        if cid in self.open_chapters:
            return self.open_chapters[cid]
        chapter_data = ChapterData(chapter)
        self.open_chapters[cid] = chapter_data
        return chapter_data

    def get_display_name(self):
        return "Chapters"

    def save(self):
        for chapter_data in self.open_chapters.values():
            chapter_data.save()

    @staticmethod
    def is_cid_in_use(cid):
        driver = locator.get_scoped("Driver")
        entries = driver.modules["Chapters"].entries
        for entry in entries:
            print(entry["CID"].value, cid)
            if entry["CID"].value == cid:
                return True
        return False

    @staticmethod
    def create_chapter(source, new_chapter_cid):
        # Create the new chapter entry.
        driver = locator.get_scoped("Driver")
        chapter_module = driver.modules["Chapters"]
        chapter_module.entries_model.insertRow(chapter_module.entries_model.rowCount())

        # Copy properties from the source chapter, give it the new CID.
        new_chapter = chapter_module.entries[-1]
        for prop in source.values():
            prop.copy_to(new_chapter)
        new_chapter["Key (CID)"].value = new_chapter_cid
        new_chapter["CID"].value = new_chapter_cid

        # Create chapter files using the ones from the source chapter.
        open_files_service = locator.get_scoped("OpenFilesService")
        chapter_file_sub_folder = detect_chapter_file_sub_folder(source)
        source_suffix = chapter_file_sub_folder + source["CID"].value[4:]
        dest_suffix = chapter_file_sub_folder + new_chapter_cid[4:]
        config_archive = open_files_service.open_archive_direct(_CONFIG_PATH % source_suffix)
        person_archive = open_files_service.open_archive_direct(_PERSON_PATH % source_suffix)
        dispos_archive = open_files_service.open_archive_direct(_DISPOS_PATH % source_suffix)
        terrain_archive = open_files_service.open_archive_direct(_TERRAIN_PATH % source_suffix)
        open_files_service.register_or_overwrite_archive(_CONFIG_PATH % dest_suffix, config_archive)
        open_files_service.register_or_overwrite_archive(_PERSON_PATH % dest_suffix, person_archive)
        open_files_service.register_or_overwrite_archive(_DISPOS_PATH % dest_suffix, dispos_archive)
        open_files_service.register_or_overwrite_archive(_TERRAIN_PATH % dest_suffix, terrain_archive)
