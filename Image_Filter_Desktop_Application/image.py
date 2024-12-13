# importing the required module  
import sys  
  
# importing the necessary classes for the project  
from PyQt5.QtCore import Qt, QSize  
from PyQt5.QtWidgets import QApplication, QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, qApp, QFileDialog, QToolBar  
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QIcon, QKeySequence  
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter  
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QHBoxLayout, QGroupBox, QRadioButton, QPushButton


class ResponsiveWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Responsive Widget')

        # Create a vertical layout for the main widget
        main_layout = QVBoxLayout()

        # Create a horizontal layout to hold the subwidgets
        sub_layout = QHBoxLayout()

        # Create a group box for the image display widget
        image_groupbox = QGroupBox('Image')
        image_layout = QVBoxLayout()


        # Create a label to display the image
        self.image_label = QLabel(self)
        self.image_label.setText("No Image Selected")
        # self.image_label.setMaximumSize(500, 800)  # Set maximum size for the image label
        self.image_label.setBackgroundRole(QPalette.Base)  
        # setting the size policy of the label using the setSizePolicy() method and QSizePolicy class  
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)  
        # setting the setScaledContents() method to True  
        # to manually adjust the aspect ratio of the image  
        # in the application  
        self.image_label.setScaledContents(True)  
        image_layout.addWidget(self.image_label)

        image_groupbox.setLayout(image_layout)
        sub_layout.addWidget(image_groupbox)

        # Create a group box for the filtering options
        filter_groupbox = QGroupBox('Filter Options')
        filter_layout = QVBoxLayout()

        # Add filtering options (example: radio buttons)
        self.radio1 = QRadioButton('Filter Option 1')
        self.radio2 = QRadioButton('Filter Option 2')
        filter_layout.addWidget(self.radio1)
        filter_layout.addWidget(self.radio2)

        filter_groupbox.setLayout(filter_layout)
        sub_layout.addWidget(filter_groupbox)

        # Add the sub layout to the main layout
        main_layout.addLayout(sub_layout)

        # Create a button to upload an image
        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.clicked.connect(self.uploadImage)
        main_layout.addWidget(self.upload_button)

        # Create a button to open image view
        self.image_view_button = QPushButton('Image View', self)
        self.image_view_button.clicked.connect(self.openImageView)  # Ensure this line is present
        image_layout.addWidget(self.image_view_button)

        self.setLayout(main_layout)

    

    def openImageView(self):
        # Check if image is uploaded
        if self.image_label.pixmap() is None:
            QMessageBox.warning(self, "Warning", "No image is uploaded yet!")
            return

        # Open a new window to display the image
        pixmap = self.image_label.pixmap()
        # image_view_window = ImageViewWindow(pixmap)
        # image_view_window.show()

    def resizeEvent(self, event):
        # Update image size on resize
        if not self.image_label.pixmap() is None:
            pixmap = self.image_label.pixmap()
            pixmap = pixmap.scaledToWidth(min(self.width() // 2, pixmap.width()))  # Scale pixmap to fit widget width but not larger than half of widget width
            self.image_label.setPixmap(pixmap)



# defining the child class of the QMainWindow class  
class QImageViewer(QMainWindow):  
    # defining the initializing function  
    def __init__(self):  
        super().__init__()  
                # creating an object of the QPrinter class  
        self.printerObj = QPrinter()  
        # setting the initial scaling factor  
        self.scale_factor = 0.0  


        # creating an object of the QScrollArea class to display the scroll bar  
        self.scroll_area = QScrollArea()  
        # setting the background color of the scroll bar to display the image using the setBackgroundRole() method and QPalette class  
        self.scroll_area.setBackgroundRole(QPalette.Dark)  
        # setting the scrolling area to the image label using the setWidget() method  
        self.scroll_area.setWidget(self.image_label)  
        # setting the visibility of the scrolling area with the help of the setVisible() method  
        self.scroll_area.setVisible(False)  
  
        # setting the central widget to the scroll area using the setCentral Widget() method  
        self.setCentralWidget(self.scroll_area)  
  
        # configuring the title of the window  
        self.setWindowTitle("Image Viewer - JAVATPOINT")  
        # configuring the width and height of the window  
        self.window_width, self.window_height = self.geometry().width(), self.geometry().height()  
        # setting the Icon of the window  
        self.setWindowIcon(QIcon('logo.jpg'))  
        # using the resize() to set the size of the application  
        self.resize(self.window_width * 2, self.window_height * 2)  
  
        #--------------------------------------  
        # Creating a File Menu  
        #--------------------------------------  
        self.filemenu = self.menuBar().addMenu('&File')  
          
        #--------------------------------------  
        # Creating a File Toolbar  
        #--------------------------------------  
        self.filetoolbar = QToolBar('File')  
        self.filetoolbar.setIconSize(QSize(30, 30))  
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.filetoolbar)  
  
        # creating the menu options like open, save, save as, and print  
  
        # calling the user-defined makeAction() method to create the action to open the file...  
        self.open_doc_opt = self.makeAction(self, 'icons/image_1146.ico', 'Open Image...', 'Open Image...', self.openImage)  
        # using the setShortcut() method to set a shortcut to execute the 'Open' command  
        self.open_doc_opt.setShortcut(QKeySequence.Open)  
  
        # calling the user-defined makeAction() method to create the action to print the file  
        self.print_opt = self.makeAction(self, './icons/printer.ico', 'Print', 'Print', self.printImage)  
        # using the setShortcut() method to set a shortcut to execute the 'Print' command  
        self.print_opt.setShortcut(QKeySequence.Print)  
        # initially disabling the action by setting the value of setEnabled() method to False  
        self.print_opt.setEnabled(False)  
  
        # using the addActions() method to add all the created actions to the 'File' menu and toolbar  
        self.filemenu.addActions([self.open_doc_opt, self.print_opt])  
        self.filetoolbar.addActions([self.open_doc_opt, self.print_opt])  
  
        # adding the separator  
        self.filemenu.addSeparator()  
  
        # calling the user-defined makeAction() method to create the action to close the application  
        self.exit_opt = self.makeAction(self, '', 'Exit', 'Exit', self.close)  
        # using the setShortcut() method to set a shortcut to execute the 'Close' command  
        self.print_opt.setShortcut(QKeySequence.Close)  
  
        # using the addActions() method to add all the created actions to the 'File' menu and toolbar  
        self.filemenu.addActions([self.exit_opt])  
  
        #--------------------------------------  
        # Creating a View Menu  
        #--------------------------------------  
        self.viewmenu = self.menuBar().addMenu('&View')  
          
        #--------------------------------------  
        # Creating an View Tool bar  
        #--------------------------------------  
        self.viewtoolbar = QToolBar('Edit')  
        self.viewtoolbar.setIconSize(QSize(30, 30))  
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.viewtoolbar)  
  
        # calling the user-defined makeAction() method to create the action to zoom in the image  
        self.zoomIN_opt = self.makeAction(self, 'icons/zoomin_zoom_search_find_1531.ico', 'Zoom In (25%)', 'Zoom In (25%)', self.zoom_in)  
        # using the setShortcut() method to set a shortcut to execute the 'Zoom In' command  
        self.zoomIN_opt.setShortcut(QKeySequence.ZoomIn)  
        # initially disabling the action by setting the value of setEnabled() method to False  
        self.zoomIN_opt.setEnabled(False)  
          
        # calling the user-defined makeAction() method to create the action to zoom out the image  
        self.zoomOUT_opt = self.makeAction(self, 'icons/zoomout_zoom_search_find_1530.ico', 'Zoom Out (25%)', 'Zoom Out (25%)', self.zoom_out)  
        # using the setShortcut() method to set a shortcut to execute the 'Zoom Out' command  
        self.zoomOUT_opt.setShortcut(QKeySequence.ZoomOut)  
        # initially disabling the action by setting the value of setEnabled() method to False  
        self.zoomOUT_opt.setEnabled(False)  
  
        # calling the user-defined makeAction() method to create the action to set the normal size of the image  
        self.normalSize_opt = self.makeAction(self, '', 'Normal Size', 'Normal Size', self.normal_size)  
        # using the setShortcut() method to set a shortcut to execute the 'Normal Size' command  
        self.normalSize_opt.setShortcut(QKeySequence("Ctrl+S"))  
        # initially disabling the action by setting the value of setEnabled() method to False  
        self.normalSize_opt.setEnabled(False)  
        # setting the initial value of the setCheckable() method to True  
        self.normalSize_opt.setCheckable(True)  
  
        # using the addActions() method to add all the created actions to the 'View' menu and toolbar  
        self.viewmenu.addActions([self.zoomIN_opt, self.zoomOUT_opt, self.normalSize_opt])  
        self.viewtoolbar.addActions([self.zoomIN_opt, self.zoomOUT_opt])  
  
        # adding the separator  
        self.viewmenu.addSeparator()  
        self.viewtoolbar.addSeparator()  
  
        # calling the user-defined makeAction() method to create the action to set the image to window size  
        self.fitToWindow_opt = self.makeAction(self, './icons/fitToWindow.ico', 'Fit To Window', 'Fit To Window', self.fit_to_window)  
        # using the setShortcut() method to set a shortcut to execute the 'Fit to Window' command  
        self.fitToWindow_opt.setShortcut(QKeySequence("Ctrl+F"))  
        # initially disabling the action by setting the value of setEnabled() method to False  
        self.fitToWindow_opt.setEnabled(False)  
  
        # using the addActions() method to add all the created actions to the 'View' menu and toolbar  
        self.viewmenu.addActions([self.fitToWindow_opt])  
        self.viewtoolbar.addActions([self.fitToWindow_opt])  

       
        self.setCentralWidget(ResponsiveWidget())

  
    # defining the required methods of the class  
  
    # defining the method to open the image file   

    

    def openImage(self):  
        # creating an object of the QFileDialog.Options class  
        selections = QFileDialog.Options()  
        # calling the getOpenFileName() method to browse the image from the directory  
        file_name, _ = QFileDialog.getOpenFileName(  
            self,  
            'QFileDialog.getOpenFileName()',  
            '',  
            'Images (*.png *.jpeg *.jpg *.bmp *.gif)',  
            options = selections  
            )  
        # if the file name is not an empty string  
        if file_name:  
            # creating an object of the QImage class by passing the file name as its parameter  
            image = QImage(file_name)  
            # if the image file is empty, returning the message box displaying information  
            if image.isNull():  
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % file_name)  
                return  
  
            # using the setPixmap() method to create the off-screen image representation that can be used as a paint device  
            self.image_label.setPixmap(QPixmap.fromImage(image))  
            # setting the scale factor to 1.0  
            self.scale_factor = 1.0  
  
            # enabling the visibility of the scroll area  
            self.scroll_area.setVisible(True)  
            # enabling the "Print" action  
            self.print_opt.setEnabled(True)  
            # calling the fit_to_window() method  
            self.fit_to_window()  
            # enabling the "Fit To Window" action  
            self.fitToWindow_opt.setEnabled(True)  
            # calling the update_actions() method  
            self.update_actions()  
  
            # if the "Fit To Window" action is not checked  
            if not self.fitToWindow_opt.isChecked():  
                # calling the adjustSize() method to adjust the size of the image  
                self.image_label.adjustSize()  
  
    # defining the method to print the image  
    def printImage(self):  
        # creating an object of the QPrintDialog class  
        print_dialog = QPrintDialog(self.printerObj, self)  
        # if the print action is executed  
        if print_dialog.exec_():  
            # creating an object of the QPainter class by passing the object of the QPrinter class  
            the_painter = QPainter(self.printerObj)  
            # creating a rectangle to place the image  
            rectangle = the_painter.viewport()  
            # defining the size of the image  
            the_size = self.image_label.pixmap().size()  
            # scaling the image to the Aspect Ratio  
            the_size.scale(rectangle.size(), Qt.KeepAspectRatio)  
            # setting the view port of the image by calling the setViewport() method  
            the_painter.setViewport(rectangle.x(), rectangle.y(), the_size.width(), the_size.height())  
            # calling the setWindow() method  
            the_painter.setWindow(self.image_label.pixmap().rect())  
            # calling the drawPixmap() method  
            the_painter.drawPixmap(0, 0, self.image_label.pixmap())  
  
    # defining the method to zoom in on the image  
    def zoom_in(self):  
        # calling the user-defined scale_image() method passing 1.25 as the scaling factor  
        self.scale_image(1.25)  
  
    # defining the method to zoom out of the image  
    def zoom_out(self):  
        # calling the user-defined scale_image() method passing 0.8 as the scaling factor  
        self.scale_image(0.8)  
  
    # defining the method to set the normal size of the image  
    def normal_size(self):  
        # calling the adjustSize() method to adjust the size of the image  
        self.image_label.adjustSize()  
        # calling the user-defined scale_image() method passing 1.0 as the scaling factor  
        self.scale_factor = 1.0  
  
    # defining the method to set the size of the image fitting to the window  
    def fit_to_window(self):  
        # retrieving the Boolean value from the "Fit To Window" action  
        fitToWindow = self.fitToWindow_opt.isChecked()  
        # configuring the scroll area to resizable  
        self.scroll_area.setWidgetResizable(fitToWindow)  
        # if the retrieved value is False, calling the user-defined normal_size() method   
        if not fitToWindow:  
            self.normal_size()  
        # calling the user-defined update_actions() method  
        self.update_actions()  
  
    # defining the method to update the actions  
    def update_actions(self):  
        # enabling the "Zoom In", "Zoom Out", and "Normal Size" actions,  
        # if the "Fit To Window" is unchecked  
        self.zoomIN_opt.setEnabled(not self.fitToWindow_opt.isChecked())  
        self.zoomOUT_opt.setEnabled(not self.fitToWindow_opt.isChecked())  
        self.normalSize_opt.setEnabled(not self.fitToWindow_opt.isChecked())  
  
    # defining the method to scale the image  
    def scale_image(self, sf):  
        # defining the scaling factor of the image  
        self.scale_factor *= sf  
        # using the resize() method to resize the image as per the scaling factor  
        self.image_label.resize(self.scale_factor * self.image_label.pixmap().size())  
  
        # calling the user-defined adjust_scroll_bar() method to adjust the scrollbar as per the scaling factor  
        self.adjust_scroll_bar(self.scroll_area.horizontalScrollBar(), sf)  
        self.adjust_scroll_bar(self.scroll_area.verticalScrollBar(), sf)  
  
        # toggling the "Zoom In" and "Zoom Out" actions as per the scaling factor   
        self.zoomIN_opt.setEnabled(self.scale_factor < 3.0)  
        self.zoomOUT_opt.setEnabled(self.scale_factor > 0.333)  
  
    # defining the method to adjust the scroll bar  
    def adjust_scroll_bar(self, scroll_bar, scaleFactor):  
        # using the setValue() method to adjust length of the scrollbar according to the scaling factor  
        scroll_bar.setValue(int(scaleFactor * scroll_bar.value() + ((scaleFactor - 1) * scroll_bar.pageStep() / 2)))  
  
    # defining the method to create the actions of the menu and toolbar  
    def makeAction(self, parent_obj, icon_destination, name_of_action, status_tip, triggered_method):  
        # creating an object of the QAction() class  
        act = QAction(QIcon(icon_destination), name_of_action, parent_obj)  
        # updating the message in the status bar  
        act.setStatusTip(status_tip)  
        # calling the different functions designated to different actions  
        act.triggered.connect(triggered_method)  
        # returning the action  
        return act  
  
# main function  
if __name__ == '__main__':  
  
    # creating an object of the QApplication class  
    the_app = QApplication(sys.argv)  
      
    # creating an object of the Application class  
    imageViewerApp = QImageViewer()  
  
    # using the show() method to display the window  
    imageViewerApp.show()  
  
    # using the exit() function of the sys module to close the application  
    sys.exit(the_app.exec_())  