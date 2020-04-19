import logging

from PySide2 import QtCore
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QInputDialog
from module.table_module import TableModule
from ui.autogen.ui_simple_editor import Ui_simple_editor
from ui.property_form import PropertyForm


class SimpleEditor(QWidget, Ui_simple_editor):
    def __init__(self, module: TableModule):
        super().__init__()
        self.setupUi(self)
        self.module = module
        self.selection = None
        self.model = self.module.entries_model

        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.list_view.setModel(self.proxy_model)

        self.list_view.selectionModel().currentRowChanged.connect(self._update_selection)
        self.search_field.textChanged.connect(self._update_filter)
        self.add_button.clicked.connect(self._on_add_pressed)
        self.remove_button.clicked.connect(self._on_remove_pressed)
        self.copy_to_button.clicked.connect(self._on_copy_to_pressed)

        self.property_form = PropertyForm(module.element_template)
        self.form_layout.setLayout(self.property_form)
        self.setWindowTitle(self.module.name)
        self.setWindowIcon(QIcon("paragon.ico"))
        self.copy_to_button.setEnabled(False)
        self.remove_button.setEnabled(False)
        self.splitter.setSizes([300, 680])
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

        if self.module.disable_add_remove:
            self.add_button.setVisible(False)
            self.remove_button.setVisible(False)
        logging.info("Generated SimpleEditor for " + self.module.name)

    def _update_selection(self, index: QtCore.QModelIndex):
        logging.info("Updating " + self.module.name + " to selected index " + str(index.row()))
        self.selection = self.proxy_model.data(index, QtCore.Qt.UserRole)
        self.property_form.update_target(self.selection)
        self.remove_button.setEnabled(self.selection is not None)
        self.copy_to_button.setEnabled(self.selection is not None)

    def _update_filter(self):
        self.proxy_model.setFilterRegExp(self.search_field.text())

    def _on_add_pressed(self):
        # Add the new entry.
        self.model.insertRow(self.model.rowCount())

        # Copy the first entry's properties into the new entry.
        source = self.module.entries[0]
        dest = self.module.entries[len(self.module.entries) - 1]
        self._copy_properties(source, dest)

    def _on_remove_pressed(self):
        for i in range(0, len(self.module.entries)):
            if self.module.entries[i] == self.selection:
                self.model.removeRow(i)
                self.model.beginResetModel()
                self.model.endResetModel()
                return

    def _on_copy_to_pressed(self):
        logging.info("Beginning copy to for " + self.module.name)
        choices = []
        for i in range(0, len(self.module.entries)):
            choices.append(str(i + 1) + ". " + self.model.data(self.model.index(i, 0), QtCore.Qt.DisplayRole))

        choice = QInputDialog.getItem(self, "Select Destination", "Destination", choices)
        if choice[1]:
            for i in range(0, len(choices)):
                if choice[0] == choices[i]:
                    self._copy_properties(self.selection, self.module.entries[i])
        else:
            logging.info("No choice selected for " + self.module.name + " copy to. Aborting.")

    @staticmethod
    def _copy_properties(source, destination):
        logging.info("Copying properties")
        source.copy_to(destination)
