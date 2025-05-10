import os
from PIL import Image
from PyQt5.QtGui import QPixmap
from PIL.ImageFilter import SHARPEN

from PyQt5.QtWidgets import (
    QApplication , QWidget,
    QFileDialog,QLabel,QPushButton,
    QListWidget,QHBoxLayout,QVBoxLayout
    )

from PyQt5.QtCore import Qt

app = QApplication([])
win = QWidget()

win.resize(700,500)
win.setWindowTitle('Easy Editor')
lb_image = QLabel('картинка')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')
btn_save = QPushButton('Сохранить')
btn_reset = QPushButton('Сбросить фильтры')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image,95)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_save)
row_tools.addWidget(btn_bw)
row_tools.addWidget(btn_reset)
col2.addLayout(row_tools)

row.addLayout(col1,20)
row.addLayout(col2,80)
win.setLayout(row)
win.show()

workdir = ''
def filter(files,extensions):
    result = []
    for filename in  files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg','.jpeg', '.png','.gif','.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir),extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)


btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'
        self.original_image = None

    def loadImage(self,dir,filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir,filename)
        self.image = Image.open(image_path)
        self.original_image = self.image.copy()

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename) 
        self.showImage(image_path)
    
    def left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        Image_path = os.path.join(workdir, self.save_dir,self.filename)
        self.showImage(Image_path)

    def right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        Image_path = os.path.join(workdir, self.save_dir,self.filename)
        self.showImage(Image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        Image_path = os.path.join(workdir, self.save_dir,self.filename)
        self.showImage(Image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        Image_path = os.path.join(workdir, self.save_dir,self.filename)
        self.showImage(Image_path)


    def saveImage(self):
        path = os.path.join(self.dir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)

    def showImage(self,path):
        pixmapimage = QPixmap(path)
        label_width , label_height = lb_image.width() ,lb_image.height()
        scaled_mixmap = pixmapimage.scaled(label_width,label_height,Qt.KeepAspectRatio)
        lb_image.setPixmap(scaled_mixmap)
        lb_image.setVisible(True)
    
    def resetImage(self):
        if self.original_image is None:
            return
        self.image = self.original_image.copy()
        self.showImage(os.path.join(workdir,self.filename))

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir,filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)


lw_files.currentRowChanged.connect(showChosenImage)
workimage = ImageProcessor()
lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.left)
btn_right.clicked.connect(workimage.right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)
btn_reset.clicked.connect(workimage.resetImage)


app.exec()
