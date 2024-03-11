import sys, os, cv2, shutil
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import *


count = 0


#estrazione n video da cartella selezionata per la funzione automatica
def extract_videos(input_path_dir, output_path_dir,frame, interval):
    h = 1
    try:
        for file in os.listdir(input_path_dir):
            filename = os.fsdecode(file) 
            if filename.endswith(".mp4"):
                cap = cv2.VideoCapture(input_path_dir + '/' + filename) # create video capture object
                estrai_img(cap,h,output_path_dir,frame, interval)    
                h = h+1  
    except:
        print("Nessuna cartella di input selezionata")




#classe che richiama il file qt e assegna funzionamento agli elementi
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("C:/Users/Utente PC/Desktop/ProgettoIA/ai_course_template/src/scripts/form.ui",self)
        self.my_push_button2 = self.findChild(QPushButton, "pushButton_2")
        self.my_push_button3 = self.findChild(QPushButton, "pushButton_3")
        self.lineEdit.setValidator(QIntValidator(1,1000,self)) #frame
        self.lineEdit_2.setValidator(QIntValidator(1,100,self)) #intervallo
        self.my_push_button2.clicked.connect(self.input_choose_folder)
        self.my_push_button3.clicked.connect(self.output_choose_folder)        
        self.pushButton.clicked.connect(self.submit)
        

    #scelta cartella dove salvare frame video 
    def output_choose_folder(self):
        dialog = QFileDialog()
        self.path_dir_output = dialog.getExistingDirectory(None, "Select Folder")
        self.my_push_button3.setGeometry((QRect(150, 100, 420, 20)))
        self.my_push_button3.setText(self.path_dir_output)

    
    #scelta cartella dove sono presenti i video
    def input_choose_folder(self):
        dialog = QFileDialog()
        self.path_dir_input= dialog.getExistingDirectory(None, "Select Folder")
        self.my_push_button2.setGeometry((QRect(150, 50, 420, 20)))
        self.my_push_button2.setText(self.path_dir_input)
    
    #funzione per la scelta manuale dopo la scelta manuale dei frame
    def single_video_manual(self):
        global count
        self.numvideo = count
        if(self.radioButton_2.isChecked() == True):
            self.cap = cv2.VideoCapture(self.path_dir_input + '/' + self.filename[count]) # create video capture object
            self.estrai_img_2() 

    #funzione per la scelta automatica dopo la scelta manuale dei frame
    def single_video_automatic(self):
        global count
        if(self.radioButton.isChecked() == True):
            cap = cv2.VideoCapture(self.path_dir_input + '/' + self.filename[count]) # create video capture object
            estrai_img(cap,count+1,self.path_dir_output,self.lineEdit.text(),self.lineEdit_2.text())  
            count = count + 1  
            #iterazione sul prossimo i-esimo video
            if(count != len(self.filename)):
                self.interface_2()
                self.radioButton.toggled.connect(self.single_video_automatic)
                self.radioButton_2.toggled.connect(self.single_video_manual)
            else:
                widget.close()

    #funzione che permette di salvare i frame selezionati nell'apposita classe di percentuale
    def display_class(self):

        global count
        pulisci_cartella('C:/Users/Utente PC/Desktop/ProgettoIA/ai_course_template/data/provvisoria/')
        self.counter = 0
        
        #ciclo che permette di contare quanti frame sono stati selezionati
        self.prv = int(self.num_total_frame2 - self.num_total_frame)
        while(self.prv < self.num_total_frame2):
                self.my_checkbox = self.findChild(QCheckBox, "Frame"+str(self.prv))
                if(self.my_checkbox.isChecked() == True):
                    self.counter = self.counter + 1
                self.prv = self.prv + 1

        #controllo se i frame selezionati sono nel numero giusto
        if(self.counter == self.num_frame_classe):
            self.prv = int(self.num_total_frame2 - self.num_total_frame)
            #salvataggio dell'i-esimo frame selezionato all'interno dello step, nella classe di percentuale apposita
            while(self.prv < self.num_total_frame2):
                self.my_checkbox = self.findChild(QCheckBox, "Frame"+str(self.prv))
                if(self.my_checkbox.isChecked() == True):
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.prv)
                    ret, frame = self.cap.read()
            
                    if (os.path.exists(self.path_dir_output + '/' + str(self.class_manual-self.interval+self.perc_class)+ '-' +str(self.class_manual) + "%") == False):
                        os.makedirs(self.path_dir_output + '/' + str(self.class_manual-self.interval+self.perc_class)+ '-' +str(self.class_manual) + "%")
                                
                    self.frame_name = self.path_dir_output + '/' + str(self.class_manual-self.interval+self.perc_class)+ '-' +str(self.class_manual) + '%/' + str(self.prv)+ '.' + str(self.numvideo+1) +'.png'
                    cv2.imwrite(self.frame_name, frame)
                    
                self.prv = self.prv + 1
           
            self.num_total_frame2 = self.num_total_frame2 + self.num_total_frame # incremento dello step successivo
            self.perc_class = 1
            #esecuzione fin tanto che non è stata creata la classe 100%
            self.class_manual = self.class_manual + self.interval
            if(self.class_manual != 100):
                self.display_image()
            else: 
                count = count + 1  
                if(count != len(self.filename)):
                    self.interface_2()
                    self.radioButton.toggled.connect(self.single_video_automatic)
                    self.radioButton_2.toggled.connect(self.single_video_manual)
                else:
                    widget.close()
                


    #funzione per creazione e visualizzazione frame immagini   
    def display_image(self):

        pulisci_cartella('C:/Users/Utente PC/Desktop/ProgettoIA/ai_course_template/data/provvisoria/')        

        if (os.path.exists('C:/Users/Utente PC/Desktop/ProgettoIA/ai_course_template/data/provvisoria/') == False):
                os.makedirs('C:/Users/Utente PC/Desktop/ProgettoIA/ai_course_template/data/provvisoria/')

        #creazione di una cartella temporanea con il salvataggio delle immagini da visualizzare successivamente
        self.prv = int(self.num_total_frame2 - self.num_total_frame)
        while(self.prv < self.num_total_frame2):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES,  self.prv)
                ret, frame = self.cap.read()
                cv2.imwrite('C:/Users/Utente PC/Desktop/ProgettoIA/ai_course_template/data/provvisoria/' + str(self.prv) +'.png', frame)
                self.prv = self.prv +1
        
        #set dell'interfaccia che visualizza le immagini
        self.scrollArea = QtWidgets.QScrollArea(widgetResizable=True)
        widget.setFixedWidth(1320)
        widget.setFixedHeight(750) 
        self.setCentralWidget(self.scrollArea)
        content_widget = QtWidgets.QWidget()
        self.scrollArea.setWidget(content_widget)
        self._lay = QtWidgets.QGridLayout(content_widget)
        self.label2 = QLabel()
        self.label2.setText("Class: " + str(self.class_manual) + "%")
        self.label2.setFont(QFont("Arial", 20, weight=QtGui.QFont.Bold))
        self.label2.setAlignment(Qt.AlignCenter)
        self._lay.addWidget(self.label2)
        self.label3 = QLabel()
        self.label3.setText("You have to choose: " + str(int(self.num_frame_classe)) + " Frame")
        self.label3.setFont(QFont("Arial", 15))
        self.label3.setAlignment(Qt.AlignCenter)
        self._lay.addWidget(self.label3)

        #ciclo per visualizzare i frame(immagini) da selezionare
        self.prv = int(self.num_total_frame2 - self.num_total_frame)
        while(self.prv < self.num_total_frame2):
            pixmap = QPixmap('C:/Users/Utente PC/Desktop/ProgettoIA/ai_course_template/data/provvisoria/' + str(self.prv) +'.png')
            label = QtWidgets.QLabel(pixmap=pixmap)
            self._lay.addWidget(label)
            self.checkbox = QCheckBox()
            self.checkbox.setObjectName("Frame"+str(self.prv))
            self.checkbox.setText("Frame " +str(self.prv))
            self.checkbox.setFont(QFont("Arial", 15, weight=QtGui.QFont.Bold))
            #self.checkbox.setAlignment(Qt.AlignCenter)
            self._lay.addWidget(self.checkbox)
            self.prv = self.prv + 1 
        
        self.buttonext = QPushButton()
        self.buttonext.setText("Next Class")
        self.buttonext.setGeometry(QtCore.QRect(0,0,70, 10))
        self._lay.addWidget(self.buttonext)
        self.buttonext.clicked.connect(self.display_class)
        
    #funzione utilizzata per selezionare i singoli frame nella chiamata manuale dei video
    def estrai_img_2(self):
       
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame = int(self.lineEdit.text()) #frame da interfaccia grafica
        self.interval = int(self.lineEdit_2.text()) #intervallo da interfaccia grafica

        # conto il numero di frame nel video
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # numero di frame per uno step
        self.step_dim = int(self.frame_count/self.frame)
    
        self.step = 0
        self.cls = 0
        self.prv = 0
        self.perc_class = 0
       
        self.num_classi = 100/self.interval  #num di immagini spartite nelle classi
        self.num_total_frame = int(self.frame_count/self.num_classi) #n-esimo frame equivalente allo step da prendere
        self.interval_class = self.interval
        self.num_frame_classe = self.frame/self.num_classi #numero di foto in ogni classe
        self.step_iter = self.step_dim #numero frame per ogni classe
        self.class_manual = self.interval
        self.num_total_frame2 = self.num_total_frame
       
        self.display_image()

    #funzione che permette di ottenere i nomi dei video presenti nella cartella di input selezionata da interfaccia
    def extract_videos_2(self,input_path_dir, output_path_dir,frame, interval):
        filename = []
        try:
            for file in os.listdir(input_path_dir):
                filenam = os.fsdecode(file)      
                if filenam.endswith(".mp4"):
                    filename.append(filenam)
            return filename
        except:
            print("Nessuna cartella di input selezionata")

    #funzione per richiamare l'interfacia di selezione di ogni singolo video manuale
    def interface_2(self):
        self.scrollArea = QtWidgets.QScrollArea(widgetResizable=True)
        widget.setFixedWidth(250)
        widget.setFixedHeight(99) 
        self.setCentralWidget(self.scrollArea)
        content_widget = QtWidgets.QWidget()
        self.scrollArea.setWidget(content_widget)
        self._lay = QtWidgets.QVBoxLayout(content_widget)
        self.label = QLabel()
        self.label.setObjectName("label")
        self.label.setGeometry(0,0,20, 20)
        self.label.setText(self.filename[count])
        self._lay.addWidget(self.label)
        self.radioButton = QRadioButton()
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setGeometry(QRect(340, 60, 110, 24))
        self.radioButton.setChecked(False)
        self.radioButton.setText("Automatic")
        self._lay.addWidget(self.radioButton)
        self.radioButton_2 = QRadioButton()
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.setGeometry(QRect(390, 40, 110, 24))
        self.radioButton_2.setChecked(False)
        self.radioButton_2.setText("Manual")
        self._lay.addWidget(self.radioButton_2)
     
    #funzione richiamata dopo il click del submit
    def submit(self):
        
        #funzione per lo svolgimento automatico
        if ((self.radioButton.isChecked()) == True):
            widget.close()
            pulisci_cartella(self.path_dir_output)
            extract_videos(self.path_dir_input,self.path_dir_output, self.lineEdit.text(),self.lineEdit_2.text())
        #funzione per lo svolgimento manuale
        if ((self.radioButton_2.isChecked()) == True):
            self.filename = self.extract_videos_2(self.path_dir_input,self.path_dir_output, self.lineEdit.text(),self.lineEdit_2.text())
            pulisci_cartella(self.path_dir_output)
            self.interface_2()
            self.radioButton.toggled.connect(self.single_video_automatic)
            self.radioButton_2.toggled.connect(self.single_video_manual)


#cancella la cartella contenente i dati
def pulisci_cartella(output_path_dir):
    if((os.path.isdir(output_path_dir)) != False):      
        shutil.rmtree(output_path_dir)
   
    
    
def estrai_img(cap,h,output_path_dir,frame, interval):  #cap: oggetto video, h: numero del video, output_path_dir: percorso di output per il salvataggio, frame: num frame input, interval: intervallo classi input

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame = int(frame) #num frame da interfaccia
    interval = int(interval) #intervallo classi da interfaccia

    # conto il numero di frame nel video
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # numero di frame per uno step
    step_dim = int(frame_count/frame)

    #num di immagini spartite nelle classi
    num_classi = 100/interval

    step = 0
    cls = 0
    interval_class = interval #num intervalli
    num_frame_classe = frame/num_classi #num frame da visualizzare per ogni istanza dei frame
    
    percentage_class = 0
    
    while cls < int(num_classi): 
       
        #creazione cartella delle classi
        if (os.path.exists(output_path_dir + '/' + str(interval_class-interval+percentage_class)+ '-' +str(interval_class) + "%") == False):
                os.makedirs(output_path_dir + '/' + str(interval_class-interval+percentage_class)+ '-' +str(interval_class) + "%")

        #all'interno del ciclo è possibile salvare nella directory della percentuale selezionata num_classi di frame
        num_frame= 0
        while(num_frame < num_frame_classe): 
            cap.set(cv2.CAP_PROP_POS_FRAMES, step)
            ret, frame = cap.read()      
            frame_name = output_path_dir + '/' + str(interval_class-interval+percentage_class)+ '-' +str(interval_class)  + '%/' + str(num_frame) + '.' + str(h) +'.png'
            cv2.imwrite(frame_name, frame)
            step = step + step_dim
            num_frame = num_frame + 1
        
        percentage_class = 1
        interval_class = interval_class + interval
        cls = cls +1
        
        
#comandi per avviare l'interfaccia di qt
app=QApplication(sys.argv)
mainwindow=MainWindow()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setMinimumHeight(519)
widget.setMinimumWidth(580)
widget.setMaximumHeight(519)
widget.setMaximumWidth(550)
widget.show()
sys.exit(app.exec_())