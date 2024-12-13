#!interpreter [optional-arg]
# -*- coding: utf-8 -*-



# Futures
from __future__ import print_function


# Built-in/Generic Imports
import sys

# Libs
from PyQt5.QtCore import Qt, QSize, QPoint, QRect, QSize
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QSizePolicy,
    QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QGroupBox,
    QRadioButton, QFileDialog, QAction, QToolBar, QScrollArea, QSlider, QRubberBand, QLineEdit
)
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QKeySequence, QPalette,  QColor, QTransform
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter


"""
{Description} {License_info}
"""

__author__     = 'Vikash'
__copyright__  = 'Copyright 2024, Image Processing Using PyQt5'
__credits__    = ['vikash baraiya']
__license__    = 'MPL 2.0'
__version__    = '1.0.0'
__maintainer__ = 'vikash'
__email__      = '{example@gmail.com}'
__status__     = '{Dev}'




class ResponsiveWidget(QWidget):
    """ResponsiveWidget class create a Widget and Main Layout"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize Application GUI"""
        self.setWindowTitle('Responsive Widget')
        main_layout = QVBoxLayout()

        # Creating the QScrollArea to display the image
        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setWidgetResizable(True)  # Make scroll area resizable
        self.scroll_area.setVisible(True)

        self.originPoint = QPoint()
        self.currentPoint = QPoint()
        self.rubberBand = None  # Initialize rubber band object

        # Image label inside the scroll area
        self.image_label = QLabel("No Image Selected")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label.setScaledContents(True)

        # Set image label as the widget for the scroll area
        self.scroll_area.setWidget(self.image_label)

        # Filter options section
        self.filter_groupbox = QGroupBox('Filter Options')
        self.filter_layout = QVBoxLayout()
        self.filter_groupbox.setLayout(self.filter_layout)

        # Add widgets to main layout
        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.scroll_area, 7)  # Add scroll area instead of image_label
        sub_layout.addWidget(self.filter_groupbox, 3)
        main_layout.addLayout(sub_layout)

        # Upload button
        self.upload_button = QPushButton('Upload Image')
        self.upload_button.clicked.connect(self.uploadImage)
        main_layout.addWidget(self.upload_button)

        self.setLayout(main_layout)

    def uploadImage(self):
        """Upload image from system to editor widget layout"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Open Image', '', 'Images (*.png *.jpg *.jpeg *.bmp *.gif)'
        )
        if file_name:
            image = QImage(file_name)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % file_name)
                return
            pixmap = QPixmap.fromImage(image)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))

    def updateContent(self, filter_name):
        # Clear existing sliders
        for i in reversed(range(self.filter_layout.count())):
            widget = self.filter_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Example of updating content based on filter action triggered
        if filter_name == 'Gray':
            self.grayscale()
        elif filter_name == 'Brightness':
            self.brightness()
        # Add more conditions as needed for additional filters

    def grayscale(self):
        self.grayscale_slider = QSlider(Qt.Horizontal)
        self.grayscale_slider.setMinimum(0)
        self.grayscale_slider.setMaximum(255)
        self.grayscale_slider.setValue(0)
        self.grayscale_slider.setTickInterval(10)
        self.grayscale_slider.setTickPosition(QSlider.TicksBelow)
        self.grayscale_slider.valueChanged.connect(self.applyGrayscale)
        self.filter_layout.addWidget(QLabel('Grayscale Intensity:'))
        self.filter_layout.addWidget(self.grayscale_slider)

    def applyGrayscale(self):
        intensity = self.grayscale_slider.value()
        pixmap = self.image_label.pixmap()
        if pixmap:
            grayscale_image = pixmap.toImage().convertToFormat(QImage.Format_Grayscale8)
            for x in range(grayscale_image.width()):
                for y in range(grayscale_image.height()):
                    pixel_value = grayscale_image.pixelColor(x, y).value()
                    new_value = max(0, min(255, pixel_value + intensity))
                    grayscale_image.setPixel(x, y, QColor(new_value, new_value, new_value).rgb())
            self.image_label.setPixmap(QPixmap.fromImage(grayscale_image))

    def brightness(self):
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(-100)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.setTickInterval(10)
        self.brightness_slider.setTickPosition(QSlider.TicksBelow)
        self.brightness_slider.valueChanged.connect(self.increaseBrightness)
        self.filter_layout.addWidget(QLabel('Brightness Adjustment:'))
        self.filter_layout.addWidget(self.brightness_slider)

    def increaseBrightness(self):
        adjustment = self.brightness_slider.value()
        pixmap = self.image_label.pixmap()
        if pixmap:
            brightness_image = pixmap.toImage()
            for x in range(brightness_image.width()):
                for y in range(brightness_image.height()):
                    pixel = QColor(brightness_image.pixel(x, y))
                    new_brightness = max(0, min(255, pixel.lightness() + adjustment))
                    pixel.setHsl(pixel.hue(), pixel.saturation(), new_brightness)
                    brightness_image.setPixel(x, y, pixel.rgb())
            self.image_label.setPixmap(QPixmap.fromImage(brightness_image))

    def rotateRight(self):
        transform = QTransform().rotate(90)
        pixmap = self.image_label.pixmap()
        if pixmap:
            rotated_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
            self.image_label.setPixmap(rotated_pixmap)

    def rotateLeft(self):
        transform = QTransform().rotate(-90)
        pixmap = self.image_label.pixmap()
        if pixmap:
            rotated_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
            self.image_label.setPixmap(rotated_pixmap)


    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.originPoint = event.pos()
            self.currentPoint = event.pos()
            if not self.rubberBand:
                self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
            self.rubberBand.setGeometry(QRect(self.originPoint, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if self.rubberBand and self.rubberBand.isVisible() and event.buttons() == Qt.LeftButton:
            self.currentPoint = event.pos()
            self.rubberBand.setGeometry(QRect(self.originPoint, self.currentPoint).normalized())

    def cropImageSave(self):
        if self.rubberBand and self.rubberBand.isVisible():
            self.rubberBand.hide()
            rect = self.rubberBand.geometry()
            croppedPixmap = self.image_label.pixmap().copy(rect)
            croppedPixmap.save('output.png')

class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.printerObj = QPrinter()
        self.scale_factor = 0.0

        self.responsiveWidget = ResponsiveWidget()
        self.setCentralWidget(self.responsiveWidget)
        
        # setting the central widget to the scroll area using the setCentral Widget() method  
        self.setCentralWidget(self.responsiveWidget)  

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/save_21411.ico"), QIcon.Selected, QIcon.On)
        self.setWindowIcon(icon)
        # self.setWindowIcon(QIcon('icons/save_21411.ico'))
        self.setWindowTitle("Image Viewer")
        self.resize(800, 600)

        self.createActions()
        self.createMenus()
        self.createToolbars()
        self.createLeftToolBar()

    def createActions(self):
        self.openAct = QAction(QIcon('icons/image_1146.ico'), "&Open...", self,
                               shortcut=QKeySequence.Open,
                               statusTip="Open an existing image",
                               triggered=self.openImage)

        self.exitAct = QAction(QIcon('icons/ic_exit_to_app_128_28418.ico'), "E&xit", self, shortcut="Ctrl+Q",
                               statusTip="Exit the application",
                               triggered=self.close)
        self.printAct = QAction(QIcon('icons/Print_22326.ico'),"Print", self,
                                shortcut=QKeySequence.Print, 
                                statusTip='Print as existing image',
                                 triggered=self.printImage)
        
        self.saveAct = QAction(QIcon('icons/save_21411.ico'),"Save", self,
                                shortcut=QKeySequence.Save, 
                                statusTip='Save as existing image',
                                 triggered=self.saveImage)

        
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewmenu = self.menuBar().addMenu('&View')

        self.fitToWindow_opt = self.makeAction(self, 'icons/fit_to_center_icon_215663.ico', 'Fit To Window', 'Fit To Window', self.fit_to_window)
        self.fitToWindow_opt.setShortcut(QKeySequence("Ctrl+F"))
        self.fitToWindow_opt.setEnabled(False)

        self.viewtoolbar = QToolBar('Edit')
        self.viewtoolbar.setIconSize(QSize(30, 30))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.viewtoolbar)

        self.viewmenu.addSeparator()
        self.viewmenu.addAction(self.fitToWindow_opt)

    def createToolbars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.openAct)

        self.zoomIN_opt = self.makeAction(self, 'icons/zoomin_zoom_search_find_1531.ico', 'Zoom In (25%)', 'Zoom In (25%)', self.zoom_in)
        self.zoomIN_opt.setShortcut(QKeySequence.ZoomIn)
        self.zoomIN_opt.setEnabled(False)

        self.zoomOUT_opt = self.makeAction(self, 'icons/zoomout_zoom_search_find_1530.ico', 'Zoom Out (25%)', 'Zoom Out (25%)', self.zoom_out)
        self.zoomOUT_opt.setShortcut(QKeySequence.ZoomOut)
        self.zoomOUT_opt.setEnabled(False)

        # New actions for rotate
        self.rotateRightAct = self.makeAction(self, 'icons/rotate_right_filled_icon_201938.ico', 'Rotate Right', 'Rotate Right', self.rotateRight)
        self.rotateRightAct.setEnabled(False)

        self.rotateLeftAct = self.makeAction(self, 'icons/rotate_left_filled_icon_201238.ico', 'Rotate Left', 'Rotate Left', self.rotateLeft)
        self.rotateLeftAct.setEnabled(False)

        # New actions for Crop
        self.CropAct = self.makeAction(self, 'icons/Crop.ico', 'Crop', 'Crop', self.imageCrop)
        self.CropAct.setEnabled(False)

        # New actions for Crop
        self.ResizeAct = self.makeAction(self, 'icons/resize.ico', 'Resize', 'Resize', self.imageResize)
        self.ResizeAct.setEnabled(False)

        self.normalSize_opt = self.makeAction(self, '', 'Normal Size', 'Normal Size', self.normal_size)
        self.normalSize_opt.setShortcut(QKeySequence("Ctrl+S"))
        self.normalSize_opt.setEnabled(False)
        self.normalSize_opt.setCheckable(True)


        self.viewmenu.addActions([self.zoomIN_opt, self.zoomOUT_opt, self.normalSize_opt])
        self.viewtoolbar.addActions([self.zoomIN_opt, self.zoomOUT_opt, self.rotateLeftAct, self.rotateRightAct, self.CropAct, self.ResizeAct])
        self.viewtoolbar.addSeparator()
        self.viewtoolbar.addAction(self.fitToWindow_opt)
        # Create a toolbar
       
    def createLeftToolBar(self):
        self.toolbar = QToolBar("Tools")
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        addmenubar = self.menuBar()

        help_menu = addmenubar.addMenu('Help')

        # # File -> open
        open_action = QAction(QIcon('icons/image_icon-icons.com_50366.ico'), 'Gray', self, statusTip='Gray as existing image')
        # open_action.triggered.connect(self.GrayImage)
        open_action.triggered.connect(lambda: self.onFilterActionTriggered('Gray'))
        # file_menu.addAction(open_action)

        brightness_action = QAction(QIcon('icons/contrast_sun.ico'),'Brightness', self, statusTip='Brighten the existing image')
        # self.brightness_action.triggered.connect(self.show_brightness_controls)
        brightness_action.triggered.connect(lambda: self.onFilterActionTriggered('Brightness'))

     

        # File menu
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        # file_menu.addAction(exit_action)
        #Add actions to the toolbar
        self.toolbar.addAction(open_action)
        self.toolbar.addAction(brightness_action)
        self.toolbar.addAction(exit_action)

    def onFilterActionTriggered(self, filter_name):
        self.responsiveWidget.updateContent(filter_name)

    
    def rotateRight(self):
        self.responsiveWidget.rotateRight()

    def rotateLeft(self):
        self.responsiveWidget.rotateLeft()

    def imageCrop(self):
        self.responsiveWidget.cropImageSave()

    def imageResize(self):
        # Create input fields for width and height
        self.widthEdit = QLineEdit()
        self.widthEdit.setPlaceholderText("Enter Width")
        self.widthEdit.setMinimumWidth(150)  # Set minimum width
        self.widthEdit.setMaximumWidth(200)  # Set maximum width
        self.responsiveWidget.filter_layout.addWidget(QLabel('Width:'))
        self.responsiveWidget.filter_layout.addWidget(self.widthEdit)

        self.responsiveWidget.filter_layout.addWidget(QLabel('✖'))

        self.heightEdit = QLineEdit()
        self.heightEdit.setPlaceholderText("Enter Height")
        self.heightEdit.setMinimumWidth(150)  # Set minimum width
        self.heightEdit.setMaximumWidth(200)  # Set maximum width
        self.responsiveWidget.filter_layout.addWidget(QLabel('Height:'))
        self.responsiveWidget.filter_layout.addWidget(self.heightEdit)

        # Create a resize button
        self.resizeBtn = QPushButton("Resize")
        self.resizeBtn.clicked.connect(self.resizeImage)
        self.responsiveWidget.filter_layout.addWidget(self.resizeBtn)

    def resizeImage(self, width, height):
        if width <= 0 or height <= 0:
            QMessageBox.warning(self, "Invalid Size", "Width and Height must be positive numbers.")
            return

        scaledPixmap = self.pixmap().scaled(QSize(width, height), Qt.KeepAspectRatio)
        self.setPixmap(scaledPixmap)
        
    def saveImage(self):
        pixmap = self.centralWidget().getImagePixmap()
        if pixmap:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save Image', '.', 'Images (*.png *.jpg *.jpeg *.bmp)')
            if filename:
                pixmap.save(filename)

    def openImage(self):
        selections = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            'Open Image',
            '',
            'Images (*.png *.jpeg *.jpg *.bmp *.gif)',
            options=selections
        )
        if file_name:
            image = QImage(file_name)
            pixmap = QPixmap(file_name)
            self.original_image = pixmap.toImage()
            self.display_image(self.original_image)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % file_name)
                return

            self.responsiveWidget.image_label.setPixmap(QPixmap.fromImage(image))
            self.scale_factor = 1.0
            self.responsiveWidget.scroll_area.setVisible(True)
            self.fit_to_window()
            self.fitToWindow_opt.setEnabled(True)
            self.update_actions()

            if not self.fitToWindow_opt.isChecked():
                self.responsiveWidget.image_label.adjustSize()


    def printImage(self):
        print_dialog = QPrintDialog(self.printerObj, self)
        if print_dialog.exec_():
            the_painter = QPainter(self.printerObj)
            rectangle = the_painter.viewport()
            the_size = self.responsiveWidget.image_label.pixmap().size()
            the_size.scale(rectangle.size(), Qt.KeepAspectRatio)
            the_painter.setViewport(rectangle.x(), rectangle.y(), the_size.width(), the_size.height())
            the_painter.setWindow(self.responsiveWidget.image_label.pixmap().rect())
            the_painter.drawPixmap(0, 0, self.responsiveWidget.image_label.pixmap())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def zoom_in(self):
        self.scale_image(1.25)

    def zoom_out(self):
        self.scale_image(0.8)

    def normal_size(self):
        self.responsiveWidget.image_label.adjustSize()
        self.scale_factor = 1.0

    def makeAction(self, parent_obj, icon_destination, name_of_action, status_tip, triggered_method):
        act = QAction(QIcon(icon_destination), name_of_action, parent_obj)
        act.setStatusTip(status_tip)
        act.triggered.connect(triggered_method)
        return act

    def fit_to_window(self):
        fitToWindow = self.fitToWindow_opt.isChecked()
        self.responsiveWidget.scroll_area.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normal_size()
        self.update_actions()

    def update_actions(self):
        self.zoomIN_opt.setEnabled(not self.fitToWindow_opt.isChecked())
        self.zoomOUT_opt.setEnabled(not self.fitToWindow_opt.isChecked())
        self.normalSize_opt.setEnabled(not self.fitToWindow_opt.isChecked())
        self.rotateRightAct.setEnabled(not self.fitToWindow_opt.isChecked())
        self.rotateLeftAct.setEnabled(not self.fitToWindow_opt.isChecked())
        self.CropAct.setEnabled(not self.fitToWindow_opt.isChecked())
        self.ResizeAct.setEnabled(not self.fitToWindow_opt.isChecked())

    def scale_image(self, sf):
        self.scale_factor *= sf
        self.responsiveWidget.image_label.resize(self.scale_factor * self.responsiveWidget.image_label.pixmap().size())

        self.adjust_scroll_bar(self.responsiveWidget.scroll_area.horizontalScrollBar(), sf)
        self.adjust_scroll_bar(self.responsiveWidget.scroll_area.verticalScrollBar(), sf)

        self.zoomIN_opt.setEnabled(self.scale_factor < 3.0)
        self.zoomOUT_opt.setEnabled(self.scale_factor > 0.333)

    def adjust_scroll_bar(self, scroll_bar, scaleFactor):
        scroll_bar.setValue(int(scaleFactor * scroll_bar.value() + ((scaleFactor - 1) * scroll_bar.pageStep() / 2)))

    # Apply Filters on Image

    def display_image(self, image):
        # Display image in QLabel
        pixmap = QPixmap.fromImage(image)
        self.responsiveWidget.image_label.setPixmap(pixmap)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_viewer = QImageViewer()
    image_viewer.show()
    sys.exit(app.exec_())