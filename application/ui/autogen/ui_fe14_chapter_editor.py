# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\fe14_chapter_editor.ui',
# licensing of '.\fe14_chapter_editor.ui' applies.
#
# Created: Wed Jan 15 13:16:36 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_fe14_chapter_editor(object):
    def setupUi(self, simple_editor):
        simple_editor.setObjectName("simple_editor")
        simple_editor.resize(980, 606)
        self.verticalLayout = QtWidgets.QVBoxLayout(simple_editor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(simple_editor)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget_2 = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(self.widget_2)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.search_field = QtWidgets.QLineEdit(self.widget)
        self.search_field.setObjectName("search_field")
        self.horizontalLayout_2.addWidget(self.search_field)
        self.add_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_button.sizePolicy().hasHeightForWidth())
        self.add_button.setSizePolicy(sizePolicy)
        self.add_button.setMinimumSize(QtCore.QSize(5, 0))
        self.add_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.add_button.setObjectName("add_button")
        self.horizontalLayout_2.addWidget(self.add_button)
        self.remove_button = QtWidgets.QPushButton(self.widget)
        self.remove_button.setMinimumSize(QtCore.QSize(5, 0))
        self.remove_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.remove_button.setObjectName("remove_button")
        self.horizontalLayout_2.addWidget(self.remove_button)
        self.copy_to_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copy_to_button.sizePolicy().hasHeightForWidth())
        self.copy_to_button.setSizePolicy(sizePolicy)
        self.copy_to_button.setMinimumSize(QtCore.QSize(5, 0))
        self.copy_to_button.setMaximumSize(QtCore.QSize(80, 16777215))
        self.copy_to_button.setObjectName("copy_to_button")
        self.horizontalLayout_2.addWidget(self.copy_to_button)
        self.verticalLayout_2.addWidget(self.widget)
        self.list_view = QtWidgets.QListView(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_view.sizePolicy().hasHeightForWidth())
        self.list_view.setSizePolicy(sizePolicy)
        self.list_view.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.list_view.setObjectName("list_view")
        self.verticalLayout_2.addWidget(self.list_view)
        self.tab_widget = QtWidgets.QTabWidget(self.splitter)
        self.tab_widget.setMinimumSize(QtCore.QSize(600, 0))
        self.tab_widget.setObjectName("tab_widget")
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(simple_editor)
        self.tab_widget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(simple_editor)

    def retranslateUi(self, simple_editor):
        simple_editor.setWindowTitle(QtWidgets.QApplication.translate("simple_editor", "Form", None, -1))
        self.search_field.setPlaceholderText(QtWidgets.QApplication.translate("simple_editor", "Search...", None, -1))
        self.add_button.setText(QtWidgets.QApplication.translate("simple_editor", "+", None, -1))
        self.remove_button.setText(QtWidgets.QApplication.translate("simple_editor", "-", None, -1))
        self.copy_to_button.setText(QtWidgets.QApplication.translate("simple_editor", "Copy To", None, -1))

