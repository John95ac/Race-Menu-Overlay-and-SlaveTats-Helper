import os 
import sys 
import json 
import shutil 
import glob 
import random 
import configparser 
import re 
import time 
import zipfile 
import subprocess 
import webbrowser
from PyQt5.QtWidgets import (QApplication ,QMainWindow ,QVBoxLayout ,QWidget ,QPushButton ,
QFileDialog ,QLabel ,QTextEdit ,QMessageBox ,QHBoxLayout ,QFrame ,QMenu ,QTabWidget ,QGridLayout ,QSizeGrip ,QProgressBar ,QLineEdit ,QComboBox ,QScrollArea ,QSizePolicy ,QColorDialog ,QSpinBox ,QSlider ,QListWidget ,QListWidgetItem ,QDialog ,QDialogButtonBox ,QProgressDialog ,QCheckBox )
import subprocess

# --- START PATH FIX ---
if getattr(sys, 'frozen', False):
    # Running as a compiled executable
    BASE_PATH = os.path.dirname(sys.executable)
else:
    # Running as a .py script
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
# --- END PATH FIX ---

from PyQt5.QtWidgets import (QApplication ,QMainWindow ,QVBoxLayout ,QWidget ,QPushButton ,
QFileDialog ,QLabel ,QTextEdit ,QMessageBox ,QHBoxLayout ,QFrame ,QMenu ,QTabWidget ,QGridLayout ,QSizeGrip ,QProgressBar ,QLineEdit ,QComboBox ,QScrollArea ,QSizePolicy ,QColorDialog ,QSpinBox ,QSlider ,QListWidget ,QListWidgetItem ,QDialog ,QDialogButtonBox ,QProgressDialog ,QCheckBox )
from PyQt5.QtCore import Qt ,QMimeData ,QUrl ,QTimer ,QPoint ,QProcess ,QEvent ,QSize ,QFileSystemWatcher ,QThread ,QObject ,pyqtSignal ,pyqtSlot
from PyQt5.QtGui import QTextCursor ,QColor ,QDragEnterEvent ,QDropEvent ,QPainter ,QBrush ,QLinearGradient ,QPixmap ,QIcon ,QImage ,QMovie ,QDesktopServices
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QAction


def _resolve_app_icon ()->str :
    try :
        here =BASE_PATH
    except Exception :
        here =os .getcwd ()
    candidates =[]
    try :
        candidates .append (os.path .join (here ,'Data','log.ico'))
    except Exception :
        pass 
    try :
        candidates .append (os.path .join (os .getcwd (),'Data','log.ico'))
    except Exception :
        pass 
    try :
        candidates .append (os.path .join (here ,'log.ico'))
    except Exception :
        pass 
    candidates .append ('log.ico')
    for p in candidates :
        try :
            if os.path .exists (p ):
                return p 
        except Exception :
            continue 
    return None 


APP_TITLE ="Race Menu Overlay to SlaveTats Helper"


class GradientWidget (QWidget ):
    """Widget that paints a subtle horizontal dark gradient background."""
    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .start_color =QColor(35 ,35 ,45 )
        self .end_color =QColor(75 ,75 ,85 )

    def paintEvent (self ,event ):
        try :
            painter =QPainter (self )
            painter .setRenderHint (QPainter .Antialiasing )
            gradient =QLinearGradient (0 ,0 ,self .width (),0 )
            gradient .setColorAt (0 ,self .start_color )
            gradient .setColorAt (1 ,self .end_color )
            painter .fillRect (self .rect (),QBrush (gradient ))
        except Exception :
            pass 

    def _clear_new_highlight_styles (self ):
        """Restablece el estilo visual de filas y labels a modo 'normal'
        (quita el fondo ámbar y colores de 'nuevo').
        """
        try :
            for i in range (self .list_layout .count ()):
                item =self .list_layout .itemAt (i )
                w =item .widget ()if item else None 
                if not isinstance (w ,QWidget ):
                    continue 

                try :
                    w .setStyleSheet ("")
                except Exception :
                    pass 

                labels =w .findChildren (QLabel )
                for lbl in labels :
                    try :
                        t =lbl .text ().strip ().lower ()
                        if t .endswith ('.dds'):
                            lbl .setStyleSheet ("color: #E0E0E0;")
                        elif t =='name:':
                            lbl .setStyleSheet ("color:#C8C8C8;")
                    except Exception :
                        continue 
        except Exception :
            pass 


class CustomTitleBar (QWidget ):
    """Minimal custom title bar to emulate the example window style."""
    def __init__ (self ,parent ):
        super ().__init__ (parent )
        self .parent =parent 
        self .setFixedHeight (40 )

        self .setStyleSheet ("""
            QLabel { color: white; font-size: 15px; font-weight: bold; }
        """)

        self ._grad_start =QColor(30 ,30 ,34 ,235 )
        self ._grad_end =QColor(50 ,50 ,56 ,235 )
        self ._pressing =False 
        self ._offset =QPoint (0 ,0 )

        lay =QHBoxLayout (self )
        lay .setContentsMargins (8 ,0 ,8 ,0 )
        lay .setSpacing (8 )


        self .icon_label =QLabel ()
        try :
            _ico =_resolve_app_icon ()
        except Exception :
            _ico =None 
        if _ico :
            try :
                pm =QPixmap (_ico ).scaled (24 ,24 ,Qt .KeepAspectRatio ,Qt .SmoothTransformation )
                self .icon_label .setPixmap (pm )
            except Exception :
                pass 
        lay .addWidget (self .icon_label )


        self .file_btn =QPushButton ("File")
        self .file_btn .setFixedSize (70 ,28 )
        self .file_btn .setCursor (Qt .PointingHandCursor )
        self .file_btn .setStyleSheet (self ._menu_button_style ())
        try :
            self .file_btn .setToolTip ("Archivo: acciones principales")
        except Exception :
            pass 
        lay .addWidget (self .file_btn )
        self .file_menu =QMenu (self )
        try :
            self .file_menu .setTitle (APP_TITLE )
        except Exception :
            pass 
        self .file_menu .setStyleSheet (self ._menu_style ())

        try :
            header =QAction (APP_TITLE ,self )
            header .setEnabled (False )
            self .file_menu .addAction (header )
            self .file_menu .addSeparator ()
        except Exception :
            pass 
        act_select =QAction ("Select JSON",self )
        act_select .triggered .connect (self .parent .select_json )
        self .file_menu .addAction (act_select )

        act_generate =QAction ("Generate .psc file",self )
        act_generate .triggered .connect (self .parent .generate_psc )
        self .file_menu .addAction (act_generate )

        act_create =QAction ("Create Texture Folder && Copy DDS",self )
        act_create .triggered .connect (self .parent .create_texture_folder_structure )
        self .file_menu .addAction (act_create )

        self .file_menu .addSeparator ()


        act_restart =QAction ("Restart",self )
        act_restart .setShortcut ("Ctrl+R")
        try :
            act_restart .triggered .connect (self .parent .restart_app )
        except Exception :
            pass 
        self .file_menu .addAction (act_restart )

        self .file_menu .addSeparator ()


        self .file_menu .addSeparator ()

        act_exit =QAction ("Exit",self )
        act_exit .triggered .connect (self .parent .close )
        self .file_menu .addAction (act_exit )
        self .file_btn .clicked .connect (self ._show_file_menu )


        self .tools_btn =QPushButton ("Tabs")
        self .tools_btn .setFixedSize (100 ,28 )
        self .tools_btn .setCursor (Qt .PointingHandCursor )
        self .tools_btn .setStyleSheet (self ._menu_button_style ())
        self .tools_btn .setToolTip ("Tabs shortcuts")
        lay .addWidget (self .tools_btn )
        self .tools_menu =QMenu (self )
        self .tools_menu .setStyleSheet (self ._menu_style ())



        tab_actions =[
        ("SlaveTats → RaceMenu (.psc Generator)",0 ),
        ("RaceMenu → SlaveTats (.json Generator)",1 ),
        ("ST Creator (from DDS)",2 ),
        ("RM Creator (from DDS)",3 ),
        ("PCA Papyrus Compile Helper",4 ),
        ("Tips",5 )
        ]

        for name ,index in tab_actions :
            action =QAction (name ,self )
            action .triggered .connect (lambda checked ,i =index :self .parent .tabs .setCurrentIndex (i ))
            self .tools_menu .addAction (action )

        self .tools_btn .clicked .connect (self ._show_tools_menu )


        self .help_btn =QPushButton ("Help")
        self .help_btn .setFixedSize (70 ,28 )
        self .help_btn .setCursor (Qt .PointingHandCursor )
        self .help_btn .setStyleSheet (self ._menu_button_style ())
        try :
            self .help_btn .setToolTip ("Ayuda y acerca de")
        except Exception :
            pass 
        lay .addWidget (self .help_btn )
        self .help_menu =QMenu (self )
        self .help_menu .setStyleSheet (self ._menu_style ())
        act_about =QAction ("About",self )
        act_about .triggered .connect (self ._show_about )
        self .help_menu .addAction (act_about )
        self .help_btn .clicked .connect (self ._show_help_menu )

        lay .addStretch (1 )


        try :

            if hasattr (self .parent ,'setWindowTitle'):
                self .parent .setWindowTitle (APP_TITLE )
        except Exception :
            pass 
        self .title =QLabel (APP_TITLE )
        lay .addWidget (self .title )


        sep =QFrame ()
        sep .setFrameShape (QFrame .VLine )
        sep .setStyleSheet ("color: rgba(90, 90, 95, 0.8);")
        lay .addWidget (sep )


        self .min_btn =QPushButton ("-")
        self .min_btn .setFixedSize (35 ,28 )
        self .min_btn .setCursor (Qt .PointingHandCursor )
        self .min_btn .setStyleSheet (self ._window_btn_style ())
        self .min_btn .clicked .connect (self .parent .showMinimized )
        try :
            self .min_btn .setToolTip ("Minimizar ventana")
        except Exception :
            pass 
        lay .addWidget (self .min_btn )

        self .max_btn =QPushButton ("□")
        self .max_btn .setFixedSize (35 ,28 )
        self .max_btn .setCursor (Qt .PointingHandCursor )
        self .max_btn .setStyleSheet (self ._window_btn_style ())
        self .max_btn .clicked .connect (self ._toggle_max )
        try :
            self .max_btn .setToolTip ("Maximizar/Restaurar ventana")
        except Exception :
            pass 
        lay .addWidget (self .max_btn )

        self .close_btn =QPushButton ("×")
        self .close_btn .setFixedSize (35 ,28 )
        self .close_btn .setCursor (Qt .PointingHandCursor )
        self .close_btn .setStyleSheet (self ._window_btn_style (close =True ))
        self .close_btn .clicked .connect (self .parent .close )
        try :
            self .close_btn .setToolTip ("Cerrar aplicación")
        except Exception :
            pass 
        lay .addWidget (self .close_btn )

    def _menu_button_style (self ):
        return (
        "QPushButton { background: rgba(30,30,34,0.70); color:#fff; border:1px solid rgba(80,80,85,0.60); border-radius:4px; padding:4px 6px; }"
        "QPushButton:hover { background: rgba(48,48,54,0.75); }"
        )

    def _menu_style (self ):
        return (
        "QMenu { background: rgba(53,53,57,0.95); color:#fff; border:1px solid rgba(69,69,73,0.85); }"
        "QMenu::item { padding:6px 18px; }"
        "QMenu::item:selected { background: rgba(69,69,75,0.95); }"
        )

    def _show_file_menu (self ):
        pos =self .file_btn .mapToGlobal (QPoint (0 ,self .file_btn .height ()))
        self .file_menu .exec_ (pos )

    def _show_tools_menu (self ):
        pos =self .tools_btn .mapToGlobal (QPoint (0 ,self .tools_btn .height ()))
        self .tools_menu .exec_ (pos )

    def _show_help_menu (self ):
        pos =self .help_btn .mapToGlobal (QPoint (0 ,self .help_btn .height ()))
        self .help_menu .exec_ (pos )

    def _show_about (self ):
        try :
            dlg =AboutDialog (self .parent )
            dlg .setModal (True )
            dlg .exec_ ()
        except Exception :
            pass 

    def _window_btn_style (self ,close =False ):
        base =(
        "QPushButton { background: rgba(30,30,34,0.70); color:#fff; border:none; font-size:16px; font-weight:bold; }"
        "QPushButton:hover { background: rgba(70,70,76,0.80); }"
        )
        if close :
            base +="QPushButton:hover { background: rgba(255,85,85,0.85); }"
        return base 

    def _toggle_max (self ):
        if self .parent .isMaximized ():
            self .parent .showNormal ()
        else :
            self .parent .showMaximized ()


    def mousePressEvent (self ,event ):
        self ._offset =event .pos ()
        self ._pressing =True 

    def mouseMoveEvent (self ,event ):
        if self ._pressing and not self .parent .isMaximized ():
            self .parent .move (event .globalPos ()-self ._offset )

    def mouseReleaseEvent (self ,event ):
        self ._pressing =False 

    def paintEvent (self ,event ):

        painter =QPainter (self )
        painter .setRenderHint (QPainter .Antialiasing )
        grad =QLinearGradient (0 ,0 ,self .width (),0 )
        grad .setColorAt (0.0 ,self ._grad_start )
        grad .setColorAt (1.0 ,self ._grad_end )
        painter .fillRect (self .rect (),QBrush (grad ))


class AboutDialog (QDialog ):
    """Simple About dialog with links and dark style."""
    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        try :
            self .setWindowTitle ("About")
            self .setStyleSheet ("background-color: #1E1E1E; color: #E0E0E0;")
        except Exception :
            pass 
        self .init_ui ()

    def init_ui (self ):
        layout =QVBoxLayout (self )
        layout .setContentsMargins (20 ,20 ,20 ,20 )
        layout .setSpacing (15 )

        title_label =QLabel ("<b>Race Menu Overlay to SlaveTats Helper — Information</b>")
        title_label .setAlignment (Qt .AlignCenter )
        title_label .setStyleSheet ("font-size: 18px; color: #50FA7B;")
        layout .addWidget (title_label )

        description_text ="""
        <p>Hello! 👋 This window briefly explains how the tool works. It is designed to help you convert and organize RaceMenu/SlaveTats overlays with a modern dark-themed interface. 🐈‍⬛</p>

        <h3>What can you do? 😺</h3>
        <ul>
          <li><b>Import .psc → JSON</b>: Reads Papyrus scripts with <code>AddBodyPaint</code>/<code>AddFacePaint</code>/etc. calls and generates a JSON with normalized entries. 🧩</li>
          <li><b>Create from DDS</b>: Select a folder with <code>.dds</code> files, assign Area/Name to each file, and export a ready-to-use JSON. 🎨</li>
          <li><b>DDS Preview</b>: Open textures with a solid background or image, adjust contrast, zoom/pan to review details. 🖼️</li>
          <li><b>Copy/Structure and Package</b>: Creates the mod structure, copies textures, and packages it into a .7z/.zip file. 📦</li>
          <li><b>Backups</b>: Create and restore backups of your files to work safely. 💾</li>
        </ul>

        <h3>Main Tabs 😻</h3>
        <ul>
          <li><b>Tips</b>: Quick tips and motivational kittens. You can refresh to see another one. 🐾</li>
          <li><b>PSC Importer (JSON ← PSC)</b>: Drag and drop or select a <code>.psc</code> file, generate the JSON, and use the buttons to open the folder, copy DDS, and package.</li>
          <li><b>Create From Scratch (JSON → Mod)</b>: Start from a folder with <code>.dds</code> files, edit the Area/Name for each file, export the JSON, and finally create the mod.</li>
        </ul>

        <h3>Suggested Workflow 😽</h3>
        <ol>
          <li>Choose whether to start from a <b>.psc</b> (to convert to JSON) or from <b>.dds</b> (to create a new JSON).</li>
          <li>Review/edit the JSON if necessary.</li>
          <li>Use <b>Create structure & Copy DDS</b> to organize textures in the mod's folder.</li>
          <li><b>Package</b> into .7z/.zip when ready.</li>
        </ol>
        """
        description_label =QLabel (description_text )
        description_label .setWordWrap (True )
        description_label .setAlignment (Qt .AlignLeft )
        layout .addWidget (description_label )


        contact_label =QLabel ("<b>Contact and Support:</b>")
        contact_label .setStyleSheet ("font-size: 15px; color: #BD93F9;")
        layout .addWidget (contact_label )


        links_layout =QGridLayout ()
        links_layout .setSpacing (10 )


        nexus_button =QPushButton ("Nexus Mods 🎮")
        nexus_button .clicked .connect (lambda :QDesktopServices .openUrl (QUrl ("https://next.nexusmods.com/profile/John1995ac")))
        links_layout .addWidget (nexus_button ,0 ,0 )


        github_button =QPushButton ("GitHub 💻")
        github_button .clicked .connect (lambda :QDesktopServices .openUrl (QUrl ("https://github.com/John95ac")))
        links_layout .addWidget (github_button ,0 ,1 )


        kofi_button =QPushButton ("Ko-fi ☕")
        kofi_button .clicked .connect (lambda :QDesktopServices .openUrl (QUrl ("https://ko-fi.com/john95ac")))
        links_layout .addWidget (kofi_button ,1 ,0 )


        patreon_button =QPushButton ("Patreon ❤️")
        patreon_button .clicked .connect (lambda :QDesktopServices .openUrl (QUrl ("https://www.patreon.com/c/John95ac")))
        links_layout .addWidget (patreon_button ,1 ,1 )

        layout .addLayout (links_layout )


        button_box =QDialogButtonBox (QDialogButtonBox .Ok )
        button_box .accepted .connect (self .close )
        layout .addWidget (button_box )




class TipsTab (QWidget ):
    """Tab that shows a random cat image at the bottom-right corner."""
    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .parent =parent 
        self .setStyleSheet ("background-color: transparent; font-size: 14px;")


        self ._layout =QGridLayout (self )
        self ._layout .setContentsMargins (6 ,6 ,6 ,6 )
        self ._layout .setSpacing (6 )
        self ._layout .setRowStretch (0 ,0 )
        self ._layout .setRowStretch (1 ,1 )
        self ._layout .setColumnStretch (0 ,0 )
        self ._layout .setColumnStretch (1 ,1 )
        self ._layout .setRowMinimumHeight (1 ,360 )
        self ._layout .setColumnMinimumWidth (1 ,360 )


        try :
            self .btn_new =QPushButton ("New Tip")
            self .btn_new .setCursor (Qt .PointingHandCursor )
            self .btn_new .setFixedHeight (28 )
            self .btn_new .setStyleSheet (
            "QPushButton { background: #2b2b2b; color: #e0e0e0; border: 1px solid #3a3a3a; border-radius: 4px; padding: 4px 8px;}"
            "QPushButton:hover { background: #3a3a3a; }"
            )
            try :
                self .btn_new .setToolTip ("Mostrar otro tip")
            except Exception :
                pass 
            self .btn_new .clicked .connect (self .refresh )
            top_bar =QWidget ()
            top_bar .setStyleSheet ("background: transparent;")
            top_lay =QHBoxLayout (top_bar )
            top_lay .setContentsMargins (0 ,0 ,0 ,0 )
            top_lay .addStretch (1 )
            top_lay .addWidget (self .btn_new ,0 ,Qt .AlignRight )
            self ._layout .addWidget (top_bar ,0 ,1 ,alignment =Qt .AlignRight |Qt .AlignTop )
        except Exception :
            pass 


    def start_progress (self ,total :int =100 ,message :str ="Processing…"):
        try :
            self ._progress_total =max (1 ,int (total ))
            self ._progress_start =time .time ()
            self .progress_bar .setRange (0 ,self ._progress_total )
            self .progress_bar .setValue (0 )
            self .progress_bar .show ()
            self .status_label .setText (f"{message } 0%")
        except Exception :
            pass 

    def update_progress (self ,current :int ,message :str |None =None ):
        try :
            cur =int (current )
            total =max (1 ,getattr (self ,'_progress_total',100 ))
            cur =max (0 ,min (cur ,total ))
            self .progress_bar .setValue (cur )
            pct =int ((cur /total )*100 )
            if message is None :
                elapsed =int (time .time ()-getattr (self ,'_progress_start',time .time ()))
                self .status_label .setText (f"Processing… {pct }% (t: {elapsed }s)")
            else :
                self .status_label .setText (message )
        except Exception :
            pass 

    def finish_progress (self ,message :str ="Completed"):
        try :
            total =max (1 ,getattr (self ,'_progress_total',100 ))
            self .progress_bar .setRange (0 ,total )
            self .progress_bar .setValue (total )
            self .progress_bar .show ()
            self .status_label .setText (message )

            QTimer .singleShot (4000 ,self ._reset_progress )
        except Exception :
            pass 

    def _reset_progress (self ):
        try :
            self .progress_bar .hide ()
            self .status_label .setText ("Ready")
        except Exception :
            pass 


        self .bottom_box =QWidget ()
        self .bottom_box .setStyleSheet ("background: transparent;")
        h =QHBoxLayout (self .bottom_box )
        h .setContentsMargins (0 ,0 ,0 ,0 )
        h .setSpacing (10 )

        self .advice_label =QLabel ()
        self .advice_label .setWordWrap (True )
        self .advice_label .setAlignment (Qt .AlignCenter )
        self .advice_label .setStyleSheet ("background: transparent; font-size: 24px; font-weight: 600;")
        self .advice_label .setTextFormat (Qt .RichText )
        self .advice_label .setOpenExternalLinks (True )
        try :
            self .advice_label .setTextInteractionFlags (Qt .TextBrowserInteraction )
        except Exception :
            pass 
        self .advice_label .setFixedWidth (640 )
        self .advice_label .setMinimumHeight (150 )


        self .advice_box =QWidget (self )
        self .advice_box .setStyleSheet ("background: transparent;")
        try :
            self .advice_box .setAttribute (Qt .WA_TranslucentBackground ,True )
            self .advice_box .setAttribute (Qt .WA_TransparentForMouseEvents ,False )
        except Exception :
            pass 
        vbox =QVBoxLayout (self .advice_box )
        vbox .setContentsMargins (0 ,0 ,0 ,0 )
        vbox .setSpacing (0 )
        vbox .addWidget (self .advice_label ,alignment =Qt .AlignCenter )
        self ._advice_offset_left =56 
        self ._advice_offset_top =190 
        self .position_advice_box ()

        self .image_label =QLabel ()
        self .image_label .setStyleSheet ("background: transparent;")
        self .image_label .setMinimumSize (360 ,360 )
        self .image_label .setMaximumSize (360 ,360 )
        self .image_label .setScaledContents (False )
        try :
            self .image_label .setAttribute (Qt .WA_TransparentForMouseEvents ,True )
        except Exception :
            pass 

        self ._gif_movie =None 


        h .addWidget (self .image_label ,0 ,Qt .AlignVCenter )
        self ._layout .addWidget (self .bottom_box ,1 ,1 ,alignment =Qt .AlignRight |Qt .AlignBottom )


        self .ensure_image_on_top ()


        self .refresh ()

    def get_cat_dir (self ):
        """Return the directory where cat images are located. Prefer cwd Data/CAT, fallback to script Data/CAT."""
        cwd_path =os.path .join (os .getcwd (),'Data','CAT')
        if os.path .isdir (cwd_path ):
            return cwd_path 
        script_dir =BASE_PATH
        script_path =os.path .join (script_dir ,'Data','CAT')
        return script_path 

    def list_cat_images (self ):
        base =self .get_cat_dir ()

        files =[]
        try :

            files .extend (sorted (glob .glob (os.path .join (base ,'**','*.png'),recursive =True )))
            files .extend (sorted (glob .glob (os.path .join (base ,'**','*.PNG'),recursive =True )))
            files .extend (sorted (glob .glob (os.path .join (base ,'**','*.gif'),recursive =True )))
            files .extend (sorted (glob .glob (os.path .join (base ,'**','*.GIF'),recursive =True )))
        except Exception :
            pass 
        return files 

    def show_random_cat (self ):
        imgs =self .list_cat_images ()
        if not imgs :
            self .image_label .setText ("No cat images found in Data/CAT")
            self .image_label .setStyleSheet ("color: #CCCCCC; background: transparent;")
            return

        gifs =[p for p in imgs if p .lower ().endswith ('.gif')]
        available_gifs =[p for p in gifs if p not in self ._recent_cats]
        available_imgs =[p for p in imgs if p not in self ._recent_cats]

        if available_gifs and random .random ()<0.6 :
            path =random .choice (available_gifs )
        elif available_imgs :
            path =random .choice (available_imgs )
        else :
            # Permitir repetición si no hay suficientes únicas
            if gifs and random .random ()<0.6 :
                path =random .choice (gifs )
            else :
                path =random .choice (imgs )

        # Actualizar historial
        self ._recent_cats .append (path )
        if len (self ._recent_cats )>3 :
            self ._recent_cats .pop (0 )
        ext =os.path .splitext (path )[1 ].lower ()

        if getattr (self ,'_gif_movie',None )is not None :
            try :
                self ._gif_movie .stop ()
            except Exception :
                pass 
            self ._gif_movie =None 
            try :
                self .image_label .setMovie (None )
            except Exception :
                pass 
        if ext =='.gif'or ext =='.GIF':
            try :
                mv =QMovie (path )
                try :
                    mv .setCacheMode (QMovie .CacheAll )
                except Exception :
                    pass 
                try :
                    mv .setSpeed (100 )
                except Exception :
                    pass 
                try :
                    mv .setLoopCount (-1 )
                except Exception :
                    pass 

                max_w =self .image_label .maximumWidth ()
                max_h =self .image_label .maximumHeight ()
                try :
                    mv .setScaledSize (QSize (max_w ,max_h ))
                except Exception :
                    pass 
                self .image_label .setText ("")
                self .image_label .setStyleSheet ("background: transparent;")

                try :
                    self .image_label .setScaledContents (True )
                except Exception :
                    pass 
                self .image_label .setMovie (mv )
                self ._gif_movie =mv 
                try :
                    print (f"[TipsTab] Showing GIF: {os.path .basename (path )}")
                except Exception :
                    pass 
                mv .start ()
                return 
            except Exception :

                pass 

        pix =QPixmap (path )
        if pix .isNull ():
            self .image_label .setText ("Failed to load: "+os.path .basename (path ))
            self .image_label .setStyleSheet ("color: #FF8888; background: transparent;")
            return 
        max_w =self .image_label .maximumWidth ()
        max_h =self .image_label .maximumHeight ()
        scaled =pix .scaled (max_w ,max_h ,Qt .KeepAspectRatio ,Qt .SmoothTransformation )
        try :
            self .image_label .setScaledContents (False )
        except Exception :
            pass 
        self .image_label .setPixmap (scaled )
        try :
            print (f"[TipsTab] Showing PNG: {os.path .basename (path )}")
        except Exception :
            pass 

    def get_advice_ini_path (self ):
        """Preferred Advice.ini under Data/CAT (cwd), else under script dir."""
        cwd_path =os.path .join (os .getcwd (),'Data','CAT','Advice.ini')
        if os.path .isfile (cwd_path ):
            return cwd_path 
        script_dir =BASE_PATH
        return os.path .join (script_dir ,'Data','CAT','Advice.ini')

    def _candidate_advice_paths (self ):
        paths =[]

        paths .append (os.path .join (os .getcwd (),'Data','CAT','Advice.ini'))
        paths .append (os.path .join (os .getcwd (),'Data','CAT','Advice tips.ini'))
        script_dir =BASE_PATH

        paths .append (os.path .join (script_dir ,'Data','CAT','Advice.ini'))
        paths .append (os.path .join (script_dir ,'Data','CAT','Advice tips.ini'))
        return paths 

    def read_advices (self ):
        advices =[]
        for path in self ._candidate_advice_paths ():
            if not os.path .isfile (path ):
                continue 
            current =[]
            config =configparser .ConfigParser (strict =False )
            try :
                config .read (path ,encoding ='utf-8-sig')
                if config .has_section ('Advice'):
                    for _ ,val in config .items ('Advice'):
                        text =(val or '').strip ()
                        if text :
                            current .append (text )
                else :
                    for section in config .sections ():
                        for _ ,val in config .items (section ):
                            text =(val or '').strip ()
                            if text and not text .startswith ('['):
                                current .append (text )
                    for _ ,val in config .defaults ().items ():
                        text =(val or '').strip ()
                        if text :
                            current .append (text )
            except Exception :
                current =[]
            if not current :
                try :
                    with open (path ,'r',encoding ='utf-8-sig')as f :
                        for line in f :
                            s =line .strip ()
                            if not s :
                                continue 
                            if s .startswith (';')or s .startswith ('#')or s .startswith ('['):
                                continue 
                            if '='in s :
                                _ ,rhs =s .split ('=',1 )
                                rhs =rhs .strip ()
                                if rhs :
                                    current .append (rhs )
                            else :
                                current .append (s )
                except Exception :
                    pass 
            advices .extend (current )
        return advices 

    def show_random_advice (self ):
        advices =self .read_advices ()
        if advices :
            txt =random .choice (advices )

            try :
                link_color ='#4ea1ff'

                txt =re .sub (
                r"\[([^\]]+)\]\(([^)]+)\)",
                lambda m :f"<a href=\"{m .group (2 )}\"><span style=\"color:{link_color }; text-decoration: underline;\">{m .group (1 )}</span></a>",
                txt ,
                )

                txt =re .sub (r"\*\*([^*]+)\*\*",r"<b>\1</b>",txt )

                italic_color ='#7bd88f'
                txt =re .sub (
                r"(?<!\*)\*([^*]+)\*(?!\*)",
                lambda m :f"<i><span style=\"color:{italic_color }\">{m .group (1 )}</span></i>",
                txt ,
                )
            except Exception :
                pass 

            try :
                txt =txt .replace (r"\1","")
            except Exception :
                pass 

            txt =txt .replace ("\r\n","\n")
            txt =txt .replace ("\\r\\n","\n")
            txt =txt .replace ("\\\n","\n")
            txt =txt .replace ("\\n","\n")
            txt =txt .replace ("\n","<br>")
            self .advice_label .setText (txt )
            self .position_advice_box ()
            self .ensure_image_on_top ()
        else :
            paths =self ._candidate_advice_paths ()
            try :
                print ("[TipsTab] No advice found. Candidates:")
                for p in paths :
                    print (" -",p ,"exists=",os.path .isfile (p ))
            except Exception :
                pass 
            msg_lines =["No advice found. Tried:"]
            for p in paths :
                exists =os.path .isfile (p )
                msg_lines .append (f"- {p } (exists: {'yes'if exists else 'no'})")
            self .advice_label .setText ("<br>".join (msg_lines ))

    def refresh (self ):
        self .show_random_cat ()
        self .show_random_advice ()

    def ensure_image_on_top (self ):
        try :
            self .bottom_box .stackUnder (self .advice_box )
            self .advice_box .raise_ ()
        except Exception :
            pass 

    def position_advice_box (self ):
        try :
            left =getattr (self ,'_advice_offset_left',56 )
            top =getattr (self ,'_advice_offset_top',240 )
            w =self .advice_label .width ()or self .advice_label .sizeHint ().width ()or 640 
            try :
                fixed_w =self .advice_label .maximumWidth ()
                if fixed_w and fixed_w >0 :
                    w =fixed_w 
                else :
                    w =640 
            except Exception :
                w =640 
            content_h =self .advice_label .sizeHint ().height ()
            h =max (150 ,content_h )
            self .advice_box .setGeometry (left ,top ,w ,h )
        except Exception :
            pass 

    def showEvent (self ,event ):
        try :
            super ().showEvent (event )
        except Exception :
            pass 
        self .position_advice_box ()
        self .ensure_image_on_top ()

    def resizeEvent (self ,event ):
        try :
            super ().resizeEvent (event )
        except Exception :
            pass 
        self .position_advice_box ()
        self .ensure_image_on_top ()


class CopyWorker (QObject ):
    """Background worker to copy files with progress updates."""
    progress =pyqtSignal (int )
    total =pyqtSignal (int )
    finished =pyqtSignal ()
    error =pyqtSignal (str )
    log =pyqtSignal (str )
    psc_total =pyqtSignal (int )

    def __init__ (self ,src_dir :str ,dst_dir :str ):
        super ().__init__ ()
        self .src_dir =src_dir 
        self .dst_dir =dst_dir 
        self ._stop =False 

    @pyqtSlot ()
    def run (self ):
        try :
            if not os.path .isdir (self .src_dir ):
                raise FileNotFoundError (f"Source folder not found: {self .src_dir }")
            os .makedirs (self .dst_dir ,exist_ok =True )
            files =[f for f in os .listdir (self .src_dir )if os.path .isfile (os.path .join (self .src_dir ,f ))]
            total =len (files )
            self .total .emit (total )
            psc_count =0 
            for idx ,name in enumerate (files ,start =1 ):
                if self ._stop :
                    break 
                src =os.path .join (self .src_dir ,name )
                dst =os.path .join (self .dst_dir ,name )
                try :
                    shutil .copy2 (src ,dst )
                except Exception :

                    pass 
                try :
                    self .log .emit (f"COPY: {src } -> {dst }")
                except Exception :
                    pass 
                try :
                    if name .lower ().endswith ('.psc'):
                        psc_count +=1 
                except Exception :
                    pass 
                self .progress .emit (idx )
            try :
                self .psc_total .emit (int (psc_count ))
            except Exception :
                pass 
            self .finished .emit ()
        except Exception as e :
            self .error .emit (str (e ))

    def request_stop (self ):
        self ._stop =True 


class PSCDropArea (QLabel ):
    """Simple drop area to accept .psc files and call a callback with file paths."""
    def __init__ (self ,on_files_dropped ,parent =None ):
        super ().__init__ (parent )
        self ._on_files_dropped =on_files_dropped 
        self .setAcceptDrops (True )
        self .setText ("You can also drag .psc here")
        self .setAlignment (Qt .AlignCenter )
        try :
            self .setStyleSheet (
            "QLabel { border: 1px dashed #888; color: #cfcfcf; padding: 8px; background: rgba(255,255,255,0.03); }"
            "QLabel:disabled { border: 1px dashed #444; color: #666; background: rgba(255,255,255,0.02); }"
            )
        except Exception :
            pass 

    def _debug_log_ini_values (self ):
        """Imprime en el terminal PCA la ruta del INI y los valores leídos."""
        try :
            ini =self ._papyrus_ini_path ()
            q_copy =self ._load_papyrus_quiet_copy ()
            q_psc =self ._load_papyrus_quiet_psc ()
            q_end =self ._load_papyrus_quiet_end ()
            autorun =self ._load_papyrus_autorun ()
            q_master =self ._load_quiet_master ()
            msg =(
                f"INI: {ini }\n"
                f"QuietCopyStep={q_copy } | QuietPSCStep={q_psc } | QuietEndStep={q_end }\n"
                f"AutoRunOnAllPex={autorun } | QuietMode={q_master }"
            )
            try :
                self ._term_pca (f'<span style="color:#00BFFF">{self ._html_escape (msg ).replace("\n","<br>")}</span>',html =True )
            except Exception :
                self ._term_pca (msg ,html =False )
        except Exception :
            pass 

    def dragEnterEvent (self ,event ):
        try :
            if not self .isEnabled ():
                event .ignore ()
                return 
            md =event .mimeData ()
            if md .hasUrls ():
                for url in md .urls ():
                    p =url .toLocalFile ()
                    if p and p .lower ().endswith ('.psc'):
                        event .acceptProposedAction ()
                        return 
        except Exception :
            pass 
        event .ignore ()

    def dropEvent (self ,event ):
        try :
            if not self .isEnabled ():
                event .ignore ()
                return 
            md =event .mimeData ()
            files =[]
            if md .hasUrls ():
                for url in md .urls ():
                    p =url .toLocalFile ()
                    if p and p .lower ().endswith ('.psc'):
                        files .append (p )
            if files :
                if callable (self ._on_files_dropped ):
                    self ._on_files_dropped (files )
                event .acceptProposedAction ()
                return 
        except Exception :
            pass 
        event .ignore ()


class MoveCleanWorker (QObject ):
    """Moves .pex files from scripts to target folder and cleans source/scripts with progress."""
    progress =pyqtSignal (int )
    total =pyqtSignal (int )
    finished =pyqtSignal ()
    error =pyqtSignal (str )
    log =pyqtSignal (str )
    generated =pyqtSignal (str )

    def __init__ (self ,ruta_scripts :str ,ruta_destino_psc :str ,ruta_source_scripts :str ):
        super ().__init__ ()
        self .ruta_scripts =ruta_scripts 
        self .ruta_destino_psc =ruta_destino_psc 
        self .ruta_source_scripts =ruta_source_scripts 
        self ._stop =False 

    @pyqtSlot ()
    def run (self ):
        try :
            if not self .ruta_destino_psc or self .ruta_destino_psc =="RUTA DIRECTA":

                self .total .emit (1 )
                self .progress .emit (1 )
                self .finished .emit ()
                return 

            target_parent =os.path .dirname (self .ruta_destino_psc )
            os .makedirs (target_parent ,exist_ok =True )


            moves =[]
            if os.path .isdir (self .ruta_scripts ):
                for nombre in os .listdir (self .ruta_scripts ):
                    if nombre .endswith ('.pex'):
                        moves .append (os.path .join (self .ruta_scripts ,nombre ))


            deletes =[]
            if os.path .isdir (self .ruta_source_scripts ):
                for nombre in os .listdir (self .ruta_source_scripts ):
                    deletes .append (os.path .join (self .ruta_source_scripts ,nombre ))

            total_ops =len (moves )+len (deletes )
            self .total .emit (total_ops )

            idx =0 

            for src in moves :
                if self ._stop :
                    break 
                try :
                    dst =os.path .join (target_parent ,os.path .basename (src ))
                    shutil .move (src ,dst )
                    try :
                        self .log .emit (f"MOVE: {src } -> {dst }")
                    except Exception :
                        pass 
                    try :

                        self .generated .emit (os.path .basename (dst ))
                    except Exception :
                        pass 
                except Exception :
                    pass 
                idx +=1 
                self .progress .emit (idx )


            for path in deletes :
                if self ._stop :
                    break 
                try :
                    if os.path .isfile (path ):
                        os .remove (path )
                        try :
                            self .log .emit (f"CLEANED FILE: {path }")
                        except Exception :
                            pass 
                    elif os.path .isdir (path ):
                        shutil .rmtree (path )
                        try :
                            self .log .emit (f"CLEANED DIR: {path }")
                        except Exception :
                            pass 
                except Exception :
                    pass 
                idx +=1 
                self .progress .emit (idx )

            self .finished .emit ()
        except Exception as e :
            self .error .emit (str (e ))

    def request_stop (self ):
        self ._stop =True 

class PCAHelperTab (QWidget ):
    """Tab that replicates the PCA helper functions from the Tkinter app using PyQt."""
    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .parent =parent 

        self .ruta_origen =r"G:\\SteamLibrary\\steamapps\\common\\Skyrim Special Edition\\Mods\\SCREPTS PARA EL PCA SE MOVER SOLO CAUNDO SEA NESESARIO\\Source"
        self .ruta_scripts =r"G:\\MO2\\overwrite\\scripts"
        self .ruta_source_scripts =r"G:\\MO2\\overwrite\\source\\scripts"
        self .ruta_destino_psc ="RUTA DIRECTA"
        # Try to load routes from INI if present
        try :
            self ._load_routes ()
        except Exception :
            pass 

        lay =QVBoxLayout (self )
        lay .setContentsMargins (8 ,8 ,8 ,8 )
        lay .setSpacing (8 )


        try :
            # Enable full-tab drag-and-drop; we'll accept only during step 2 (after_copy)
            self .setAcceptDrops (True )
            # Track current PCA state to decide when to accept drops
            self ._pca_state ="init"

            title_row =QHBoxLayout ()
            title_row .setContentsMargins (0 ,0 ,0 ,0 )
            title_row .setSpacing (8 )
            title =QLabel ("PCA Papyrus Compile Helper")
            title .setAlignment (Qt .AlignCenter )
            title .setStyleSheet ("font-size: 16px; font-weight: bold; color: #66FF66;")
            title_row .addStretch (1 )
            title_row .addWidget (title )

            self .chk_quiet_master =QCheckBox ("Quiet MODE")
            try :
                self .chk_quiet_master .setToolTip (
                "Quiet MODE reduces console messages to lower CPU usage and improve UI responsiveness (at the cost of fewer logs).\n\n"
                "Toggle all silent modes:\n"
                "• Quiet copy: suppresses detailed logs in step 1 (shows start and summary).\n"
                "• Quiet .psc: shows only .psc filenames in purple, no code dump.\n"
                "• Quiet end: suppresses detailed end logs; shows cleanup notice and ALL DONE."
                )

                self .chk_quiet_master .setStyleSheet ("color: #FFD700; font-style: italic; font-weight: bold;")
            except Exception :
                pass 
            try :
                self .chk_quiet_master .setChecked (self ._load_quiet_master ())
            except Exception :
                self .chk_quiet_master .setChecked (False )
            try :
                self .chk_quiet_master .toggled .connect (self ._on_quiet_master_toggled )
            except Exception :
                pass 
            title_row .addWidget (self .chk_quiet_master )
            # Gear button to configure routes (floating top-right, not affecting layout)
            try :
                self .btn_routes_cfg =QPushButton ("⚙",self )
                self .btn_routes_cfg .setToolTip ("Configure source/overwrite routes")
                self .btn_routes_cfg .setCursor (Qt .PointingHandCursor )
                self .btn_routes_cfg .setFixedSize (40 ,40 )  # larger gear
                self .btn_routes_cfg .setStyleSheet (
                    "QPushButton { font-size: 22px; border: 1px solid #444; border-radius: 6px; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2b2b2b, stop:1 #1e1e1e); color: #ddd; }"
                    "QPushButton:hover { border-color: #777; color: #fff; }"
                )
                self .btn_routes_cfg .clicked .connect (self ._open_routes_dialog )
                try :
                    self .btn_routes_cfg .raise_ ()
                except Exception :
                    pass 
            except Exception :
                pass 
            title_row .addStretch (1 )
            lay .addLayout (title_row )

            subtitle =QLabel ("Copy required files, select or drag .psc, and move/clean the resulting .pex.")
            subtitle .setAlignment (Qt .AlignCenter )
            subtitle .setStyleSheet ("font-size: 12px; color: #CFCFCF;")
            lay .addWidget (subtitle )
        except Exception :
            pass 


        row1 =QHBoxLayout ()
        self .btn_copiar_archivos =QPushButton ("Copy Files to Scripts")
        self .btn_copiar_archivos .setStyleSheet ("QPushButton { background:#228B22; color:#fff; } QPushButton:disabled { background:#2b2b2b; color:#777; border-color:#444; }")
        self .btn_copiar_archivos .clicked .connect (self .copiar_archivos )
        self .btn_copiar_archivos .setToolTip ("Copy all files from the 'Source' folder to 'overwrite/source/scripts' to compile .psc files.")
        row1 .addWidget (self .btn_copiar_archivos )

        self .chk_quiet_copy =QCheckBox ("Quiet copy")
        try :
            self .chk_quiet_copy .setToolTip ("If enabled: step 1 will not print per-file detailed logs, only the start message and final summary.")
        except Exception :
            pass 
        try :

            self .chk_quiet_copy .setChecked (self ._load_papyrus_quiet_copy ())
        except Exception :
            self .chk_quiet_copy .setChecked (False )
        try :
            self .chk_quiet_copy .toggled .connect (lambda v :self ._save_papyrus_quiet_copy (bool (v )))
        except Exception :
            pass 
        row1 .addWidget (self .chk_quiet_copy )
        btn_open_origen =QPushButton ("Open Source Folder")
        try :
            btn_open_origen .setMinimumWidth (160 )
            btn_open_origen .setSizePolicy (QSizePolicy .Preferred ,QSizePolicy .Fixed )
        except Exception :
            btn_open_origen .setFixedWidth (160 )
        try :
            btn_open_origen .setStyleSheet (
                "QPushButton { background:#3a3a3f; color:#dddddd; border:1px solid #555555; border-radius:4px; padding:6px 10px; }"
                "QPushButton:hover { border-color:#888888; color:#ffffff; }"
            )
        except Exception :
            pass 
        btn_open_origen .clicked .connect (lambda :self .abrir_carpeta (self .ruta_origen ))
        btn_open_origen .setToolTip ("Open the source folder used to copy files.")
        row1 .addWidget (btn_open_origen )
        lay .addLayout (row1 )


        row2 =QHBoxLayout ()
        self .btn_copiar_psc =QPushButton ("Select and Copy .psc Files")
        self .btn_copiar_psc .setStyleSheet ("background:#8B0000; color:#fff;")
        self .btn_copiar_psc .clicked .connect (self .copiar_archivo_psc )
        self .btn_copiar_psc .setToolTip ("Select .psc files and copy them to 'overwrite/source/scripts' to compile.")
        row2 .addWidget (self .btn_copiar_psc )

        self .chk_quiet_psc =QCheckBox ("Quiet .psc")
        try :
            self .chk_quiet_psc .setToolTip ("If enabled: when selecting/dragging .psc only filenames will be shown in purple, no code dump.")
        except Exception :
            pass 
        try :
            self .chk_quiet_psc .setChecked (self ._load_papyrus_quiet_psc ())
        except Exception :
            self .chk_quiet_psc .setChecked (False )
        try :
            self .chk_quiet_psc .toggled .connect (lambda v :self ._save_papyrus_quiet_psc (bool (v )))
        except Exception :
            pass 
        row2 .addWidget (self .chk_quiet_psc )
        self .btn_open_psc =QPushButton ("Open PSC Folder")
        try :
            self .btn_open_psc .setMinimumWidth (160 )
            self .btn_open_psc .setSizePolicy (QSizePolicy .Preferred ,QSizePolicy .Fixed )
        except Exception :
            self .btn_open_psc .setFixedWidth (160 )
        try :
            self .btn_open_psc .setStyleSheet (
                "QPushButton { background:#3a3a3f; color:#dddddd; border:1px solid #555555; border-radius:4px; padding:6px 10px; }"
                "QPushButton:hover { border-color:#888888; color:#ffffff; }"
            )
        except Exception :
            pass 
        self .btn_open_psc .clicked .connect (lambda :self .abrir_carpeta (self .ruta_destino_psc if self .ruta_destino_psc and self .ruta_destino_psc !="RUTA DIRECTA"else os.path .dirname (self .ruta_origen )))
        self .btn_open_psc .setToolTip ("Open the folder where the selected .psc files are located.")
        row2 .addWidget (self .btn_open_psc )

        self .psc_drop =PSCDropArea (self .copiar_archivo_psc_desde_lista ,self )
        self .psc_drop .setMinimumWidth (240 )
        # Hide the dedicated drop zone visually, but keep tab-level drag&drop working
        try :
            self .psc_drop .setVisible (False )
            self .psc_drop .setMaximumHeight (0 )
            self .psc_drop .setSizePolicy (QSizePolicy .Ignored ,QSizePolicy .Fixed )
        except Exception :
            pass 
        row2 .addWidget (self .psc_drop ,1 )
        lay .addLayout (row2 )


        row3 =QHBoxLayout ()
        self .btn_ejecutar =QPushButton ("Run Move and Clean")
        self .btn_ejecutar .setStyleSheet ("background:#8B0000; color:#fff;")
        self .btn_ejecutar .clicked .connect (self .ejecutar_mover_y_eliminar )
        self .btn_ejecutar .setToolTip ("Move compiled .pex from 'overwrite/scripts' to the parent folder of the selected .psc and clean 'overwrite/source/scripts'.")
        row3 .addWidget (self .btn_ejecutar )

        self .chk_autorun =QCheckBox ("Auto-run when all .pex are ready")
        try :
            self .chk_autorun .setToolTip ("If enabled: when all expected .pex are detected, run 'Move and Clean' automatically.")
        except Exception :
            pass 
        try :
            self .chk_autorun .setChecked (self ._load_papyrus_autorun ())
        except Exception :
            self .chk_autorun .setChecked (False )
        try :
            self .chk_autorun .toggled .connect (lambda v :self ._save_papyrus_autorun (bool (v )))
        except Exception :
            pass 
        row3 .addWidget (self .chk_autorun )

        self .chk_quiet_end =QCheckBox ("Quiet end")
        try :
            self .chk_quiet_end .setToolTip ("If enabled: moved/cleaned files will not be listed; only a cleanup notice and the final ALL DONE message will be shown.")
        except Exception :
            pass 
        try :
            self .chk_quiet_end .setChecked (self ._load_papyrus_quiet_end ())
        except Exception :
            self .chk_quiet_end .setChecked (False )
        try :
            self .chk_quiet_end .toggled .connect (lambda v :self ._save_papyrus_quiet_end (bool (v )))
        except Exception :
            pass 
        row3 .addWidget (self .chk_quiet_end )
        btn_open_source_scripts =QPushButton ("📂 src")
        btn_open_source_scripts .setFixedWidth (48 )
        try :
            btn_open_source_scripts .setStyleSheet (
                "QPushButton { background:#3a3a3f; color:#dddddd; border:1px solid #555555; border-radius:4px; padding:4px 8px; }"
                "QPushButton:hover { border-color:#888888; color:#ffffff; }"
            )
        except Exception :
            pass 
        btn_open_source_scripts .clicked .connect (lambda :self .abrir_carpeta (self .ruta_source_scripts ))
        btn_open_source_scripts .setToolTip ("Open 'overwrite/source/scripts'.")
        row3 .addWidget (btn_open_source_scripts )
        btn_open_scripts =QPushButton ("📂 scripts")
        btn_open_scripts .setFixedWidth (72 )
        try :
            btn_open_scripts .setStyleSheet (
                "QPushButton { background:#3a3a3f; color:#dddddd; border:1px solid #555555; border-radius:4px; padding:4px 8px; }"
                "QPushButton:hover { border-color:#888888; color:#ffffff; }"
            )
        except Exception :
            pass 
        btn_open_scripts .clicked .connect (lambda :self .abrir_carpeta (self .ruta_scripts ))
        btn_open_scripts .setToolTip ("Open 'overwrite/scripts' (folder where compiled .pex appear).")
        row3 .addWidget (btn_open_scripts )
        lay .addLayout (row3 )

        try :
            if hasattr (self ,'chk_quiet_master'):
                if hasattr (self ,'chk_quiet_copy'):
                    self .chk_quiet_copy .toggled .connect (self ._on_quiet_child_toggled )
                if hasattr (self ,'chk_quiet_psc'):
                    self .chk_quiet_psc .toggled .connect (self ._on_quiet_child_toggled )
                if hasattr (self ,'chk_quiet_end'):
                    self .chk_quiet_end .toggled .connect (self ._on_quiet_child_toggled )

                self ._refresh_quiet_master_from_children ()
        except Exception :
            pass 


        row4 =QHBoxLayout ()
        self .btn_verificar =QPushButton ("Open Scripts")
        self .btn_verificar .setStyleSheet ("background:#8B0000; color:#fff;")
        self .btn_verificar .clicked .connect (lambda :self .abrir_carpeta (self .ruta_scripts ))
        self .btn_verificar .setToolTip (".pex indicator: Red = no .pex in 'overwrite/scripts'; Green = there are .pex.\nClick to open the folder.")
        row4 .addWidget (self .btn_verificar )
        lay .addLayout (row4 )



        try :
            if os.path .isdir (self .ruta_scripts ):
                self ._known_pex =set ([f for f in os .listdir (self .ruta_scripts )if f .endswith ('.pex')])
            else :
                self ._known_pex =set ()
        except Exception :
            self ._known_pex =set ()
        self ._pex_timer =QTimer (self )
        self ._pex_timer .timeout .connect (self .verificar_archivos_pex )
        self ._pex_timer .start (1000 )


        try :
            term_label =QLabel ("Output:")
            lay .addWidget (term_label )

            self .terminal_output_pca =QTextEdit ()
            self .terminal_output_pca .setReadOnly (True )
            self .terminal_output_pca .setStyleSheet (
            "QTextEdit {"
            " background-color: #1A1A1C;"
            " color: #4CAF50;"
            " border: 1px solid #333;"
            " border-radius: 4px;"
            " selection-background-color: #2E7D32;"
            " selection-color: #FFFFFF;"
            " font-family: Consolas, 'Courier New', monospace;"
            " font-size: 12px;"
            "}"
            )
            lay .addWidget (self .terminal_output_pca )
        except Exception :
            pass 


        self ._apply_base_styles ()
        self ._set_pca_state ("init")

        try :
            self ._psc_expected =0 
            self ._auto_move_in_progress =False 
        except Exception :
            pass 

        # Final: asegúrate de que las casillas reflejen el INI al iniciar
        try :
            if hasattr (self ,'chk_quiet_master'):
                self ._apply_flags_from_ini_on_startup ()
                self ._debug_log_ini_values ()
        except Exception :
            pass 

    def _term_pca (self ,text :str ,html :bool =False ):
        try :
            if not hasattr (self ,'terminal_output_pca')or self .terminal_output_pca is None :
                return 
            if html :
                try :
                    self .terminal_output_pca .append (text )
                except Exception :

                    self .terminal_output_pca .append (self ._strip_html (text ))
            else :
                self .terminal_output_pca .append (text )

            try :
                cursor =self .terminal_output_pca .textCursor ()
                cursor .movePosition (cursor .End )
                self .terminal_output_pca .setTextCursor (cursor )
                self .terminal_output_pca .ensureCursorVisible ()
                self .terminal_output_pca .viewport ().update ()

                self .terminal_output_pca .repaint ()
            except Exception :
                pass 
        except Exception :
            pass 

    def _strip_html (self ,s :str )->str :
        try :
            import re 
            return re .sub ('<[^<]+?>','',s )
        except Exception :
            return s 

    def _apply_flags_from_ini_on_startup (self ):
        """Carga explícitamente los flags del INI y los aplica a las casillas al iniciar.
        Evita que queden desmarcadas por cualquier estilo/estado aplicado antes.
        """
        try :
            # Lee valores del INI
            q_copy =self ._load_papyrus_quiet_copy ()
            q_psc =self ._load_papyrus_quiet_psc ()
            q_end =self ._load_papyrus_quiet_end ()
            autorun =self ._load_papyrus_autorun ()
            q_master =self ._load_quiet_master ()

            self ._quiet_syncing =True 
            try :
                if hasattr (self ,'chk_quiet_copy'):
                    self .chk_quiet_copy .setChecked (bool (q_copy ))
                if hasattr (self ,'chk_quiet_psc'):
                    self .chk_quiet_psc .setChecked (bool (q_psc ))
                if hasattr (self ,'chk_quiet_end'):
                    self .chk_quiet_end .setChecked (bool (q_end ))
                if hasattr (self ,'chk_autorun'):
                    self .chk_autorun .setChecked (bool (autorun ))

                # Master refleja el INI si está en True; si es False, calcula por hijos
                all_on =bool (q_copy and q_psc and q_end )
                master_val =bool (q_master ) if q_master is not None else all_on
                if hasattr (self ,'chk_quiet_master'):
                    self .chk_quiet_master .setChecked (master_val )
                # Guarda QuietMode para mantener coherencia si difiere de los hijos
                try :
                    self ._save_quiet_master (master_val )
                except Exception :
                    pass 
            finally :
                self ._quiet_syncing =False 
        except Exception :
            pass 


    def _papyrus_ini_path (self )->str :
        # Prefer the INI alongside this script under Data/; fall back to CWD/Data only if that INI exists.
        try :
            here =BASE_PATH
        except Exception :
            here =os .getcwd ()
        script_ini =os.path .join (here ,'Data','PapyrusCompiler.ini')
        try :
            if os.path .isfile (script_ini ):
                return script_ini 
        except Exception :
            pass 
        # Consider CWD/Data only if the INI file actually exists there
        try :
            cwd_ini =os.path .join (os .getcwd (),'Data','PapyrusCompiler.ini')
            if os.path .isfile (cwd_ini ):
                return cwd_ini 
        except Exception :
            pass 
        # Default to the script's Data path (will be created on save if missing)
        return script_ini 

    def _load_papyrus_autorun (self )->bool :
        try :
            ini =self ._papyrus_ini_path ()
            cfg =configparser .ConfigParser (strict =False )
            if os.path .isfile (ini ):
                cfg .read (ini ,encoding ='utf-8')
                return cfg .getboolean ('PCA','AutoRunOnAllPex',fallback =False )
        except Exception :
            pass 
        return False 

    def _save_papyrus_autorun (self ,value :bool ):
        try :
            ini =self ._papyrus_ini_path ()
            os .makedirs (os.path .dirname (ini ),exist_ok =True )
            cfg =configparser .ConfigParser (strict =False )
            if os.path .isfile (ini ):
                cfg .read (ini ,encoding ='utf-8')
            if not cfg .has_section ('PCA'):
                cfg .add_section ('PCA')
            cfg .set ('PCA','AutoRunOnAllPex','true'if value else 'false')
            with open (ini ,'w',encoding ='utf-8')as fh :
                cfg .write (fh )
        except Exception :
            pass 

    def _load_papyrus_quiet_copy (self )->bool :
        try :
            ini =self ._papyrus_ini_path ()
            cfg =configparser .ConfigParser (strict =False )
            if os.path .isfile (ini ):
                cfg .read (ini ,encoding ='utf-8')
                return cfg .getboolean ('PCA','QuietCopyStep',fallback =False )
        except Exception :
            pass 
        return False 

    def _save_papyrus_quiet_copy (self ,value :bool ):
        try :
            ini =self ._papyrus_ini_path ()
            os .makedirs (os.path .dirname (ini ),exist_ok =True )
            cfg =configparser .ConfigParser (strict =False )
            if os.path .isfile (ini ):
                cfg .read (ini ,encoding ='utf-8')
            if not cfg .has_section ('PCA'):
                cfg .add_section ('PCA')
            cfg .set ('PCA','QuietCopyStep','true'if value else 'false')
            with open (ini ,'w',encoding ='utf-8')as fh :
                cfg .write (fh )
        except Exception :
            pass 

    def _load_papyrus_quiet_end (self )->bool :
        try :
            ini =self ._papyrus_ini_path ()
            cfg =configparser .ConfigParser (strict =False )
            if os.path .isfile (ini ):
                cfg .read (ini ,encoding ='utf-8')
                return cfg .getboolean ('PCA','QuietEndStep',fallback =False )
        except Exception :
            pass 
        return False 

    def _save_papyrus_quiet_end (self ,value :bool ):
        try :
            ini =self ._papyrus_ini_path ()
            os .makedirs (os.path .dirname (ini ),exist_ok =True )
            cfg =configparser .ConfigParser (strict =False )
            if os.path .isfile (ini ):
                cfg .read (ini ,encoding ='utf-8')
            if not cfg .has_section ('PCA'):
                cfg .add_section ('PCA')
            cfg .set ('PCA','QuietEndStep','true'if value else 'false')
            with open (ini ,'w',encoding ='utf-8')as fh :
                cfg .write (fh )
        except Exception :
            pass 


    def _load_quiet_master (self )->bool :
        try :
            ini =self ._papyrus_ini_path ()
            cfg =configparser .ConfigParser (strict =False )
            if os.path .isfile (ini ):
                cfg .read (ini ,encoding ='utf-8')
                return cfg .getboolean ('PCA','QuietMode',fallback =False )
        except Exception :
            pass 
        return False 

    def _save_quiet_master (self ,value :bool ):
        try :
            ini =self ._papyrus_ini_path ()
            os .makedirs (os.path .dirname (ini ),exist_ok =True )
            cfg =configparser .ConfigParser (strict =False )
            if os.path .isfile (ini ):
                cfg .read (ini ,encoding ='utf-8')
            if not cfg .has_section ('PCA'):
                cfg .add_section ('PCA')
            cfg .set ('PCA','QuietMode','true'if value else 'false')
            with open (ini ,'w',encoding ='utf-8')as fh :
                cfg .write (fh )
        except Exception :
            pass 


    # ---- Routes (paths) config ----
    def _load_routes (self ):
        """Load route paths from [Route] section if present; keep current values as fallbacks."""
        try :
            ini =self ._papyrus_ini_path ()
            if not os.path .isfile (ini ):
                return 
            cfg =configparser .ConfigParser (strict =False )
            cfg .read (ini ,encoding ='utf-8')
            if cfg .has_section ('Route'):
                self .ruta_origen =cfg .get ('Route','ruta_origen',fallback =self .ruta_origen )
                self .ruta_scripts =cfg .get ('Route','ruta_scripts',fallback =self .ruta_scripts )
                self .ruta_source_scripts =cfg .get ('Route','ruta_source_scripts',fallback =self .ruta_source_scripts )
        except Exception :
            pass 

    def _save_routes (self ):
        """Persist current route paths to [Route] in the INI."""
        try :
            ini =self ._papyrus_ini_path ()
            os .makedirs (os.path .dirname (ini ),exist_ok =True )
            cfg =configparser .ConfigParser (strict =False )
            if os.path .isfile (ini ):
                cfg .read (ini ,encoding ='utf-8')
            if not cfg .has_section ('Route'):
                cfg .add_section ('Route')
            cfg .set ('Route','ruta_origen',str (self .ruta_origen ))
            cfg .set ('Route','ruta_scripts',str (self .ruta_scripts ))
            cfg .set ('Route','ruta_source_scripts',str (self .ruta_source_scripts ))
            with open (ini ,'w',encoding ='utf-8')as fh :
                cfg .write (fh )
        except Exception :
            pass 

    # ---- Emulator routes mode ----
    def _load_mo2_emulator (self )->bool :
        try :
            ini =self ._papyrus_ini_path ()
            cfg =configparser .ConfigParser (strict =False )
            if os.path .isfile (ini ):
                cfg .read (ini ,encoding ='utf-8')
                return cfg .getboolean ('StandAlone','mo2emulator',fallback =False )
        except Exception :
            pass 
        return False 

    def _save_mo2_emulator (self ,value :bool ):
        try :
            ini =self ._papyrus_ini_path ()
            os .makedirs (os.path .dirname (ini ),exist_ok =True )
            cfg =configparser .ConfigParser (strict =False )
            if os.path .isfile (ini ):
                cfg .read (ini ,encoding ='utf-8')
            if not cfg .has_section ('StandAlone'):
                cfg .add_section ('StandAlone')
            cfg .set ('StandAlone','mo2emulator','true'if value else 'false')
            with open (ini ,'w',encoding ='utf-8')as fh :
                cfg .write (fh )
        except Exception :
            pass 

    def _emulator_routes (self ):
        """Compute predefined emulator routes based on the program directory."""
        try :
            try :
                here =BASE_PATH
            except Exception :
                here =os .getcwd ()
            base =os.path .join (here ,'Data','Tutorial','MO2 environment emulator')
            return {
                'ruta_origen':os.path .join (base ,'Mods','Scripts clean'),
                'ruta_scripts':os.path .join (base ,'overwrite','scripts'),
                'ruta_source_scripts':os.path .join (base ,'overwrite','source','scripts'),
            }
        except Exception :
            return {
                'ruta_origen':self .ruta_origen ,
                'ruta_scripts':self .ruta_scripts ,
                'ruta_source_scripts':self .ruta_source_scripts ,
            }

    def _open_routes_dialog (self ):
        """Open a small dialog to edit route paths and save them to INI."""
        try :
            dlg =QDialog (self )
            dlg .setWindowTitle ("Configure Routes")
            dlg .resize (800 ,280 )  # larger window
            # Gradient background to match app style
            dlg .setStyleSheet (
                "QDialog { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1E1E20, stop:1 #131316); }"
                "QLabel { color: #ddd; }"
                "QLineEdit { background:#1a1a1c; color:#ddd; border:1px solid #333; border-radius:4px; padding:4px; }"
                "QPushButton { background:#2b2b2b; color:#ddd; border:1px solid #444; border-radius:4px; padding:6px 10px; }"
                "QPushButton:hover { border-color:#777; color:#fff; }"
            )
            v =QVBoxLayout (dlg )

            # Mode toggle: INI vs Stand-alone (emulator)
            mode_row =QHBoxLayout ()
            lbl_mode =QLabel ("Mode:")
            chk_emul =QCheckBox ("Activate Stand-alone mode (emulates MO2 environment; MO2 not required)")
            try :
                chk_emul .setStyleSheet ("QCheckBox { color:#00BFFF; font-weight:600; }")
            except Exception :
                pass 
            try :
                chk_emul .setToolTip (
                    "This feature lets you perform the process in stand-alone mode, without requiring MO2 or having your own reference list.\n"
                    "Just follow the instruction to paste the path in PCA 2022.1, and only RaceMenu will be compiled."
                )
            except Exception :
                pass 
            try :
                chk_emul .setChecked (self ._load_mo2_emulator ())
            except Exception :
                chk_emul .setChecked (False )
            mode_row .addWidget (lbl_mode )
            mode_row .addWidget (chk_emul )
            mode_row .addStretch (1 )
            v .addLayout (mode_row )

            # Info panel shown when Stand-alone mode is active
            info_box =QWidget ()
            info_layout =QVBoxLayout (info_box )
            info_layout .setContentsMargins (8 ,4 ,8 ,8 )
            info_layout .setSpacing (6 )
            info_label =QLabel (
                "Done. Now go to PCA 2022.1 → Settings, enable MO2 mode and paste this path into 'Data\Tutorial\MO2 environment emulator':"
            )
            try :
                info_label .setStyleSheet ("color:#C0E8FF;")
            except Exception :
                pass 
            # Compute emulator path
            try :
                here =BASE_PATH
            except Exception :
                here =os .getcwd ()
            emu_path =os.path .join (here ,'Data','Tutorial','MO2 environment emulator')
            path_row =QHBoxLayout ()
            path_edit =QLineEdit (emu_path )
            try :
                path_edit .setReadOnly (True )
            except Exception :
                pass 
            btn_copy_path =QPushButton ("Copy path")
            btn_copy_path .setToolTip ("Copy the emulator folder path to clipboard")
            path_row .addWidget (path_edit ,1 )
            path_row .addWidget (btn_copy_path )
            info_layout .addWidget (info_label )
            info_layout .addLayout (path_row )
            v .addWidget (info_box )

            def add_row (label ,text ):
                row =QHBoxLayout ()
                lbl =QLabel (label )
                edit =QLineEdit (text )
                btn_browse =QPushButton ("…")
                btn_browse .setFixedWidth (34 )
                btn_browse .setToolTip (f"Browse for {label}")
                row .addWidget (lbl )
                row .addWidget (edit ,1 )
                row .addWidget (btn_browse )
                v .addLayout (row )
                return edit ,btn_browse 

            e_origen ,b_origen =add_row ("Collected .psc folder" ,self .ruta_origen )
            e_scripts ,b_scripts =add_row ("Scripts folder" ,self .ruta_scripts )
            e_src_scripts ,b_src_scripts =add_row ("Source Scripts folder" ,self .ruta_source_scripts )

            def apply_mode_to_fields ():
                try :
                    if chk_emul .isChecked ():
                        emu =self ._emulator_routes ()
                        e_origen .setText (emu ['ruta_origen'])
                        e_scripts .setText (emu ['ruta_scripts'])
                        e_src_scripts .setText (emu ['ruta_source_scripts'])
                        # lock editing and browsing
                        for w in (e_origen ,e_scripts ,e_src_scripts ,b_origen ,b_scripts ,b_src_scripts ):
                            try :
                                w .setEnabled (False )
                            except Exception :
                                pass 
                        try :
                            info_box .setVisible (True )
                            # refresh shown path in case program folder moved
                            try :
                                here2 =BASE_PATH
                            except Exception :
                                here2 =os .getcwd ()
                            path_edit .setText (os.path .join (here2 ,'Data','Tutorial','MO2 environment emulator'))
                        except Exception :
                            pass 
                    else :
                        # restore current INI values to fields, enable editing
                        try :
                            # Reload from INI without altering self.* yet
                            ini =self ._papyrus_ini_path ()
                            if os.path .isfile (ini ):
                                cfg =configparser .ConfigParser (strict =False )
                                cfg .read (ini ,encoding ='utf-8')
                                r1 =cfg .get ('Route','ruta_origen',fallback =self .ruta_origen )
                                r2 =cfg .get ('Route','ruta_scripts',fallback =self .ruta_scripts )
                                r3 =cfg .get ('Route','ruta_source_scripts',fallback =self .ruta_source_scripts )
                            else :
                                r1 ,r2 ,r3 =self .ruta_origen ,self .ruta_scripts ,self .ruta_source_scripts 
                            e_origen .setText (r1 )
                            e_scripts .setText (r2 )
                            e_src_scripts .setText (r3 )
                        except Exception :
                            pass 
                        for w in (e_origen ,e_scripts ,e_src_scripts ,b_origen ,b_scripts ,b_src_scripts ):
                            try :
                                w .setEnabled (True )
                            except Exception :
                                pass 
                        try :
                            info_box .setVisible (False )
                        except Exception :
                            pass 
                except Exception :
                    pass 

            # initialize fields according to current mode
            apply_mode_to_fields ()
            try :
                chk_emul .toggled .connect (lambda _v :apply_mode_to_fields ())
            except Exception :
                pass 

            # Copy path handler: copy to clipboard and beep
            try :
                btn_copy_path .clicked .connect (lambda : (QApplication .clipboard () .setText (path_edit .text ()), QApplication .beep ()))
            except Exception :
                pass 

            def pick_dir (edit :QLineEdit ):
                try :
                    start =edit .text ().strip ()or os.path .expanduser ('~')
                except Exception :
                    start =os.path .expanduser ('~')
                d =QFileDialog .getExistingDirectory (dlg ,"Select folder" ,start )
                if d :
                    edit .setText (d )

            b_origen .clicked .connect (lambda :pick_dir (e_origen ))
            b_scripts .clicked .connect (lambda :pick_dir (e_scripts ))
            b_src_scripts .clicked .connect (lambda :pick_dir (e_src_scripts ))

            btns =QDialogButtonBox (QDialogButtonBox .Ok |QDialogButtonBox .Cancel ,parent =dlg )
            v .addWidget (btns )

            def on_accept ():
                try :
                    if chk_emul .isChecked ():
                        # Use emulator routes in runtime, persist only the mode flag
                        emu =self ._emulator_routes ()
                        self .ruta_origen =emu ['ruta_origen']
                        self .ruta_scripts =emu ['ruta_scripts']
                        self .ruta_source_scripts =emu ['ruta_source_scripts']
                        self ._save_mo2_emulator (True )
                    else :
                        # Save user-edited INI routes and disable emulator mode
                        self .ruta_origen =e_origen .text ().strip ()or self .ruta_origen 
                        self .ruta_scripts =e_scripts .text ().strip ()or self .ruta_scripts 
                        self .ruta_source_scripts =e_src_scripts .text ().strip ()or self .ruta_source_scripts 
                        self ._save_routes ()
                        self ._save_mo2_emulator (False )
                    # Refresh tooltips that show these paths
                    try :
                        self .btn_copiar_archivos .setToolTip (f"Copy all files from the 'Source' folder to 'overwrite/source/scripts' to compile .psc files.\nSource: {self .ruta_origen }")
                    except Exception :
                        pass 
                    try :
                        self .btn_open_psc .setToolTip ("Open the folder where the selected .psc files are located.")
                    except Exception :
                        pass 
                except Exception :
                    pass 
                dlg .accept ()

            btns .accepted .connect (on_accept )
            btns .rejected .connect (dlg .reject )

            dlg .exec_ ()
        except Exception :
            pass 

    def resizeEvent (self ,event ):
        """Keep the gear button pinned to the top-right corner without moving other widgets."""
        try :
            super ().resizeEvent (event )
        except Exception :
            try :
                QWidget .resizeEvent (self ,event )
            except Exception :
                pass 
        try :
            if hasattr (self ,'btn_routes_cfg')and self .btn_routes_cfg is not None :
                m =8  # margin
                x =self .width ()- self .btn_routes_cfg .width ()- m 
                y =m 
                self .btn_routes_cfg .move (x ,y )
        except Exception :
            pass 

    def _on_quiet_master_toggled (self ,value :bool ):
        try :
            if getattr (self ,'_quiet_syncing',False ):
                return 
            self ._apply_quiet_to_children (bool (value ))
        except Exception :
            pass 

    def _on_quiet_child_toggled (self ,value :bool ):
        try :
            if getattr (self ,'_quiet_syncing',False ):
                return 

            all_on =True 
            if hasattr (self ,'chk_quiet_copy'):
                all_on =all_on and self .chk_quiet_copy .isChecked ()
            if hasattr (self ,'chk_quiet_psc'):
                all_on =all_on and self .chk_quiet_psc .isChecked ()
            if hasattr (self ,'chk_quiet_end'):
                all_on =all_on and self .chk_quiet_end .isChecked ()
            self ._quiet_syncing =True 
            try :
                if hasattr (self ,'chk_quiet_master'):
                    self .chk_quiet_master .setChecked (all_on )

                self ._save_quiet_master (all_on )
            finally :
                self ._quiet_syncing =False 
        except Exception :
            pass 

    def _apply_quiet_to_children (self ,value :bool ):

        self ._quiet_syncing =True 
        try :
            if hasattr (self ,'chk_quiet_copy'):
                try :
                    self .chk_quiet_copy .setChecked (value )
                    self ._save_papyrus_quiet_copy (value )
                except Exception :
                    pass 
            if hasattr (self ,'chk_quiet_psc'):
                try :
                    self .chk_quiet_psc .setChecked (value )
                    self ._save_papyrus_quiet_psc (value )
                except Exception :
                    pass 
            if hasattr (self ,'chk_quiet_end'):
                try :
                    self .chk_quiet_end .setChecked (value )
                    self ._save_papyrus_quiet_end (value )
                except Exception :
                    pass 
            if hasattr (self ,'chk_quiet_master'):
                try :
                    self .chk_quiet_master .setChecked (value )
                    self ._save_quiet_master (value )
                except Exception :
                    pass 
        finally :
            self ._quiet_syncing =False 

    def _refresh_quiet_master_from_children (self ):
        try :
            all_on =True 
            if hasattr (self ,'chk_quiet_copy'):
                all_on =all_on and self .chk_quiet_copy .isChecked ()
            if hasattr (self ,'chk_quiet_psc'):
                all_on =all_on and self .chk_quiet_psc .isChecked ()
            if hasattr (self ,'chk_quiet_end'):
                all_on =all_on and self .chk_quiet_end .isChecked ()
            self ._quiet_syncing =True 
            try :
                if hasattr (self ,'chk_quiet_master'):
                    self .chk_quiet_master .setChecked (all_on )
            finally :
                self ._quiet_syncing =False 
        except Exception :
            pass 

    def _load_papyrus_quiet_psc (self )->bool :
        try :
            ini =self ._papyrus_ini_path ()
            cfg =configparser .ConfigParser (strict =False )
            if os.path .isfile (ini ):
                cfg .read (ini ,encoding ='utf-8')
                return cfg .getboolean ('PCA','QuietPSCStep',fallback =False )
        except Exception :
            pass 
        return False 

    def _save_papyrus_quiet_psc (self ,value :bool ):
        try :
            ini =self ._papyrus_ini_path ()
            os .makedirs (os.path .dirname (ini ),exist_ok =True )
            cfg =configparser .ConfigParser (strict =False )
            if os.path .isfile (ini ):
                cfg .read (ini ,encoding ='utf-8')
            if not cfg .has_section ('PCA'):
                cfg .add_section ('PCA')
            cfg .set ('PCA','QuietPSCStep','true'if value else 'false')
            with open (ini ,'w',encoding ='utf-8')as fh :
                cfg .write (fh )
        except Exception :
            pass 

    def _html_escape (self ,s :str )->str :
        try :
            return (
            s .replace ('&','&amp;')
            .replace ('<','&lt;')
            .replace ('>','&gt;')
            .replace ('"','&quot;')
            .replace ("'",'&#39;')
            )
        except Exception :
            return s 


    def _apply_base_styles (self ):
        try :
            base_btn =(
            "QPushButton { background:#8B0000; color:#fff; }"
            "QPushButton:disabled { background:#2b2b2b; color:#777; border-color:#444; }"
            )
            self .btn_copiar_archivos .setStyleSheet ("QPushButton { background:#228B22; color:#fff; } QPushButton:disabled { background:#2b2b2b; color:#777; border-color:#444; }")
            self .btn_copiar_psc .setStyleSheet (base_btn )
            self .btn_ejecutar .setStyleSheet (base_btn )
            self .btn_verificar .setStyleSheet (base_btn )
        except Exception :
            pass 

    def _set_pca_state (self ,state :str ):
        """States: init -> only 1 active; after_copy -> 2 active; after_psc -> 3 and 4 active;"""
        try :
            # Remember current state so the tab-level drag-and-drop can react accordingly
            self ._pca_state =state 
            if state =="init":

                self .btn_copiar_archivos .setEnabled (True )
                self .btn_copiar_psc .setEnabled (False )
                self .psc_drop .setEnabled (False )
                self .btn_ejecutar .setEnabled (False )
                self .btn_verificar .setEnabled (True )
                self ._apply_base_styles ()
            elif state =="after_copy":

                self .btn_copiar_archivos .setEnabled (False )
                self .btn_copiar_psc .setEnabled (True )
                self .psc_drop .setEnabled (True )
                self .btn_ejecutar .setEnabled (False )
                self .btn_verificar .setEnabled (True )

                self .btn_copiar_psc .setStyleSheet (
                "QPushButton { background:#DAA520; color:#000; }"
                "QPushButton:disabled { background:#2b2b2b; color:#777; border-color:#444; }"
                )
            elif state =="after_psc":

                self .btn_copiar_archivos .setEnabled (False )
                self .btn_copiar_psc .setEnabled (False )
                self .psc_drop .setEnabled (False )
                self .btn_ejecutar .setEnabled (True )
                self .btn_verificar .setEnabled (True )

                self .btn_ejecutar .setStyleSheet (
                "QPushButton { background:#DAA520; color:#000; }"
                "QPushButton:disabled { background:#2b2b2b; color:#777; border-color:#444; }"
                )
            else :

                self ._apply_base_styles ()
                self .btn_copiar_archivos .setEnabled (True )
                self .btn_copiar_psc .setEnabled (False )
                self .psc_drop .setEnabled (False )
                self .btn_ejecutar .setEnabled (False )
                self .btn_verificar .setEnabled (True )
        except Exception :
            pass 


    def dragEnterEvent (self ,event ):
        """Allow dropping .psc anywhere on the tab during step 2 (after_copy)."""
        try :
            if getattr (self ,'_pca_state',"init")=="after_copy":
                md =event .mimeData ()
                if md and md .hasUrls ():
                    for url in md .urls ():
                        p =url .toLocalFile ()
                        if p and p .lower ().endswith ('.psc'):
                            event .acceptProposedAction ()
                            return 
        except Exception :
            pass 
        event .ignore ()

    def dropEvent (self ,event ):
        """Handle .psc files dropped anywhere on the tab during step 2 (after_copy)."""
        try :
            if getattr (self ,'_pca_state',"init")!="after_copy":
                event .ignore ()
                return 
            files =[]
            md =event .mimeData ()
            if md and md .hasUrls ():
                for url in md .urls ():
                    p =url .toLocalFile ()
                    if p and p .lower ().endswith ('.psc'):
                        files .append (p )
            if files :
                try :
                    # Reuse the same handler used by the small drop area
                    self .copiar_archivo_psc_desde_lista (files )
                except Exception :
                    pass 
                event .acceptProposedAction ()
                return 
        except Exception :
            pass 
        event .ignore ()

    def copiar_archivos (self ):

        self .btn_copiar_archivos .setEnabled (False )


        try :
            if not (hasattr (self ,'chk_quiet_copy')and self .chk_quiet_copy .isChecked ()):
                self ._term_pca (f"START: Copying from '{self .ruta_origen }' to '{self .ruta_source_scripts }'")
            else :

                self ._term_pca (
                '<span style="color:#32CD32; font-weight:bold">COPYING SELECTED .PSC FILES IN PROGRESS!</span>',
                html =True 
                )
        except Exception :
            pass 


        self ._copy_thread =QThread (self )
        self ._copy_worker =CopyWorker (self .ruta_origen ,self .ruta_source_scripts )
        self ._copy_worker .moveToThread (self ._copy_thread )

        self ._psc_copied_count =0 

        def on_total (n ):

            win =self .window ()
            try :
                if hasattr (win ,'start_progress'):
                    win .start_progress (total =max (1 ,n ),message ="Copiando archivos…")
            except Exception :
                pass 

            if int (n )<=0 :
                try :
                    if hasattr (win ,'finish_progress'):
                        win .finish_progress (message ="No hay archivos para copiar")
                except Exception :
                    pass 
                self .btn_copiar_archivos .setEnabled (True )
                return 

        def on_progress (i ):

            win =self .window ()
            try :
                if hasattr (win ,'update_progress'):
                    win .update_progress (current =int (i ),message ="Copiando archivos…")
            except Exception :
                pass 

        def on_finished ():

            self .btn_copiar_archivos .setStyleSheet (
            "QPushButton { background:#228B22; color:#fff; }"
            "QPushButton:disabled { background:#2b2b2b; color:#777; border-color:#444; }"
            )

            win =self .window ()
            try :
                if hasattr (win ,'finish_progress'):
                    win .finish_progress (message ="Copia completada")
            except Exception :
                pass 

            try :
                self ._term_pca (f"PSC FILES PROCESSED: {int (getattr (self ,'_psc_copied_count',0 ))} UNITS")
            except Exception :
                pass 

            try :
                self ._term_pca (
                '<span style="color:#FFD700; font-weight:bold">NOW DRAG ALL .PSC INTO THE ENABLED DROP AREA. YOU CAN DROP ONE OR MULTIPLE FILES; JUST MAKE SURE THEY ARE IN THE SAME FOLDER.</span>',
                html =True 
                )
            except Exception :
                pass 

            try :
                self ._copy_thread .quit ()
            except Exception :
                pass 

            self ._set_pca_state ("after_copy")

        def on_error (msg ):
            self .btn_copiar_archivos .setEnabled (True )
            QMessageBox .critical (self ,"Error",f"An error occurred while copying files:\n{msg }")

            win =self .window ()
            try :
                if hasattr (win ,'finish_progress'):
                    win .finish_progress (message ="Copy finished with errors")
            except Exception :
                pass 
            try :
                self ._copy_thread .quit ()
            except Exception :
                pass 

        self ._copy_thread .started .connect (self ._copy_worker .run )
        self ._copy_worker .total .connect (on_total )
        try :
            self ._copy_worker .psc_total .connect (lambda c :setattr (self ,'_psc_copied_count',int (c )))
        except Exception :
            pass 
        self ._copy_worker .progress .connect (on_progress )
        self ._copy_worker .finished .connect (on_finished )
        self ._copy_worker .error .connect (on_error )
        try :
            def _copy_log_handler (s :str ):
                try :
                    if hasattr (self ,'chk_quiet_copy')and self .chk_quiet_copy .isChecked ():
                        return 
                    self ._term_pca (s )
                except Exception :
                    pass 
            self ._copy_worker .log .connect (_copy_log_handler )
        except Exception :
            pass 


        self ._copy_worker .finished .connect (self ._copy_worker .deleteLater )
        self ._copy_worker .finished .connect (self ._copy_thread .deleteLater )

        self ._copy_thread .start ()

        try :
            win =self .window ()
            if hasattr (win ,'progress_bar'):
                win .progress_bar .show ()
        except Exception :
            pass 

    def copiar_archivo_psc (self ):
        files ,_ =QFileDialog .getOpenFileNames (self ,"Seleccionar archivos .psc","","Archivos PSC (*.psc)")
        if not files :
            return 
        self .copiar_archivo_psc_desde_lista (files )

    def copiar_archivo_psc_desde_lista (self ,files ):

        try :
            self ._psc_expected =max (0 ,int (len (files )))
        except Exception :
            self ._psc_expected =0 
        if not files :
            return 
        files =[f for f in files if f and f .lower ().endswith ('.psc')]
        if not files :
            QMessageBox .warning (self ,"Warning","No valid .psc files were detected.")
            return 

        try :
            self ._term_pca (f"PSC SELECTED: {len (files )} file(s)")
            if hasattr (self ,'chk_quiet_psc')and self .chk_quiet_psc .isChecked ():
                for f in files :
                    name =os.path .basename (f )
                    self ._term_pca (f'<span style="color:#800080; font-weight:bold">{self ._html_escape (name )}</span>',html =True )
            else :
                for f in files :
                    self ._term_pca (f"FILE: {f }")
        except Exception :
            pass 
        self .ruta_destino_psc =os.path .dirname (files [0 ])
        os .makedirs (self .ruta_source_scripts ,exist_ok =True )
        for f in files :
            dst =os.path .join (self .ruta_source_scripts ,os.path .basename (f ))
            shutil .copy2 (f ,dst )
            try :
                if not (hasattr (self ,'chk_quiet_psc')and self .chk_quiet_psc .isChecked ()):
                    self ._term_pca (f"COPY PSC: {f } -> {dst }")
            except Exception :
                pass 

            if not (hasattr (self ,'chk_quiet_psc')and self .chk_quiet_psc .isChecked ()):
                try :
                    with open (f ,'r',encoding ='utf-8',errors ='ignore')as fh :
                        content =fh .read ()
                    name =os.path .basename (f )
                    self ._term_pca (f"===== BEGIN {name } =====")
                    for line in content .splitlines ():
                        esc =self ._html_escape (line )
                        self ._term_pca (f'<span style="color:#C08CFF">{esc }</span>',html =True )
                    self ._term_pca (f"===== END {name } =====")
                except Exception as e :
                    try :
                        self ._term_pca (f"ERROR READING PSC: {f } -> {e }")
                    except Exception :
                        pass 
        self .btn_copiar_psc .setStyleSheet (
        "QPushButton { background:#228B22; color:#fff; }"
        "QPushButton:disabled { background:#2b2b2b; color:#777; border-color:#444; }"
        )
        try :
            win =self .window ()
            if hasattr (win ,'show_toast'):
                win .show_toast (".psc copied",3000 )
        except Exception :
            pass 
        QMessageBox .information (self ,"Success",".psc files were copied successfully.")

        try :
            self ._term_pca ("<span style=\"color:#00BFFF; font-weight:bold; font-size:16px\">NOW EVERYTHING DEPENDS ON PCA TO CONTINUE</span>",html =True )
        except Exception :
            pass 

        self ._set_pca_state ("after_psc")

    def mover_archivos_pex (self ):
        if self .ruta_destino_psc =="RUTA DIRECTA"or not self .ruta_destino_psc :
            return 
        try :
            ruta_carpeta_padre =os.path .dirname (self .ruta_destino_psc )
            os .makedirs (ruta_carpeta_padre ,exist_ok =True )
            for archivo in os .listdir (self .ruta_scripts ):
                if archivo .endswith ('.pex'):
                    src =os.path .join (self .ruta_scripts ,archivo )
                    dst =os.path .join (ruta_carpeta_padre ,archivo )
                    shutil .move (src ,dst )
        except Exception :

            pass 

    def eliminar_contenido (self ):
        try :
            if not os.path .isdir (self .ruta_source_scripts ):
                return 
            for nombre in os .listdir (self .ruta_source_scripts ):
                p =os.path .join (self .ruta_source_scripts ,nombre )
                if os.path .isfile (p ):
                    os .remove (p )
                elif os.path .isdir (p ):
                    shutil .rmtree (p )
        except Exception :

            pass 

    def ejecutar_mover_y_eliminar (self ):

        self .btn_ejecutar .setEnabled (False )


        try :
            self ._term_pca ("START: Moving .pex and cleaning source/scripts")
        except Exception :
            pass 


        self ._move_thread =QThread (self )
        self ._move_worker =MoveCleanWorker (self .ruta_scripts ,self .ruta_destino_psc ,self .ruta_source_scripts )
        self ._move_worker .moveToThread (self ._move_thread )

        def on_total (n ):
            win =self .window ()
            try :
                if hasattr (win ,'start_progress'):
                    win .start_progress (total =max (1 ,int (n )),message ="Moviendo y limpiando…")
            except Exception :
                pass 

        def on_progress (i ):
            win =self .window ()
            try :
                if hasattr (win ,'update_progress'):
                    win .update_progress (current =int (i ),message ="Moviendo y limpiando…")
            except Exception :
                pass 

        def on_finished ():
            self .btn_ejecutar .setEnabled (True )
            self .btn_ejecutar .setStyleSheet (
            "QPushButton { background:#228B22; color:#fff; }"
            "QPushButton:disabled { background:#2b2b2b; color:#777; border-color:#444; }"
            )
            win =self .window ()
            try :
                if hasattr (win ,'finish_progress'):
                    win .finish_progress (message ="Movimiento y limpieza completos")
            except Exception :
                pass 

            try :
                if hasattr (self ,'chk_quiet_end')and self .chk_quiet_end .isChecked ():
                    self ._term_pca ('<span style="color:#00BFFF; font-weight:bold">CLEANUP ACTIVATED</span>',html =True )
            except Exception :
                pass 

            try :
                self ._term_pca (
                '<span style="color:#00BFFF; font-weight:bold">ALL DONE, EVERYTHING RETURNED TO NORMAL</span>',
                html =True 
                )
            except Exception :
                pass 

            # After showing ALL DONE, wait ~4 seconds, then clear output and show READY message in green
            try :
                def _clear_then_ready ():
                    try :
                        if hasattr (self ,'terminal_output_pca')and self .terminal_output_pca is not None :
                            self .terminal_output_pca .clear ()
                            self ._term_pca ('<span style="color:#00FF00; font-weight:bold">READY TO COMPILE ANOTHER PAPYRUS</span>',html =True )
                    except Exception :
                        pass 
                QTimer .singleShot (4000 ,_clear_then_ready )
            except Exception :
                pass 

            try :
                self ._auto_move_in_progress =False 
                self ._psc_expected =0 
            except Exception :
                pass 
            try :
                self ._move_thread .quit ()
            except Exception :
                pass 

            self ._apply_base_styles ()
            self ._set_pca_state ("init")

        def on_error (msg ):
            self .btn_ejecutar .setEnabled (True )
            QMessageBox .critical (self ,"Error",f"Error en mover/limpiar:\n{msg }")
            win =self .window ()
            try :
                if hasattr (win ,'finish_progress'):
                    win .finish_progress (message ="Movimiento/limpieza con errores")
            except Exception :
                pass 

            try :
                self ._auto_move_in_progress =False 
            except Exception :
                pass 
            try :
                self ._move_thread .quit ()
            except Exception :
                pass 

        self ._move_thread .started .connect (self ._move_worker .run )
        self ._move_worker .total .connect (on_total )
        self ._move_worker .progress .connect (on_progress )
        self ._move_worker .finished .connect (on_finished )
        self ._move_worker .error .connect (on_error )
        try :
            def _move_log_handler (s :str ):
                try :
                    if hasattr (self ,'chk_quiet_end')and self .chk_quiet_end .isChecked ():
                        return 
                    self ._term_pca (s )
                except Exception :
                    pass 
            self ._move_worker .log .connect (_move_log_handler )
        except Exception :
            pass 

        try :
            def _on_generated (name :str ):
                try :
                    if hasattr (self ,'chk_quiet_end')and self .chk_quiet_end .isChecked ():
                        return 
                    prefix ='<span style="color:#00FF00; font-weight:bold">READY, SUCCESSFULLY GENERATED \"</span>'
                    fname =f'<span style="color:#800080; font-weight:bold">{name }</span>'
                    suffix ='<span style="color:#00FF00; font-weight:bold">\"</span>'
                    self ._term_pca (prefix +fname +suffix ,html =True )
                except Exception :
                    try :
                        if hasattr (self ,'chk_quiet_end')and self .chk_quiet_end .isChecked ():
                            return 
                        self ._term_pca (f"READY, SUCCESSFULLY GENERATED \"{name }\"")
                    except Exception :
                        pass 
            self ._move_worker .generated .connect (_on_generated )
        except Exception :
            pass 
        self ._move_worker .finished .connect (self ._move_worker .deleteLater )
        self ._move_worker .finished .connect (self ._move_thread .deleteLater )
        self ._move_thread .start ()
        try :
            win =self .window ()
            if hasattr (win ,'progress_bar'):
                win .progress_bar .show ()
        except Exception :
            pass 

    def abrir_carpeta (self ,ruta :str ):
        try :
            if os.path .isdir (ruta ):
                os .startfile (ruta )
        except Exception :
            pass 

    def abrir_carpeta_psc (self ):
        if self .ruta_destino_psc !="RUTA DIRECTA":
            self .abrir_carpeta (self .ruta_destino_psc )
        else :
            QMessageBox .warning (self ,"Advertencia","Primero debe seleccionar archivos .psc para definir la ruta de destino.")

    def verificar_archivos_pex (self ):
        try :
            archivos_pex =[f for f in os .listdir (self .ruta_scripts )if f .endswith ('.pex')]

            if archivos_pex :
                self .btn_verificar .setStyleSheet ("background:#228B22; color:#fff;")
            else :
                self .btn_verificar .setStyleSheet ("background:#8B0000; color:#fff;")

            try :
                current =set (archivos_pex )
                new_ones =[f for f in current if f not in getattr (self ,'_known_pex',set ())]
                if new_ones :
                    for fname in sorted (new_ones ):
                        try :
                            msg =(
                            '<span style="color:#32CD32; font-weight:bold">READY, SUCCESSFULLY GENERATED "'
                            f'<span style="color:#DA70D6; font-weight:bold">{self ._html_escape (fname )}</span>'
                            '<span style="color:#32CD32; font-weight:bold">"</span>'
                            )
                            self ._term_pca (msg ,html =True )
                        except Exception :

                            try :
                                self ._term_pca (f'READY, SUCCESSFULLY GENERATED "{fname }"')
                            except Exception :
                                pass 
                self ._known_pex =current 

                try :
                    should_autorun =(
                    hasattr (self ,'chk_autorun')and self .chk_autorun .isChecked ()and 
                    int (getattr (self ,'_psc_expected',0 ))>0 and 
                    len (current )>=int (getattr (self ,'_psc_expected',0 ))and 
                    not bool (getattr (self ,'_auto_move_in_progress',False ))
                    )
                except Exception :
                    should_autorun =False 
                if should_autorun :
                    try :
                        self ._auto_move_in_progress =True 
                    except Exception :
                        pass 
                    try :
                        QTimer .singleShot (0 ,self .ejecutar_mover_y_eliminar )
                    except Exception :
                        pass 
            except Exception :
                pass 
        except Exception :
            pass 

class PSCImporterTab (QWidget ):
    """Second tab: import a Papyrus .psc (RaceMenu overlays) and export a JSON list.
    Rules:
    - Parse AddBodyPaint(...) -> area "Body"
    - Parse AddWarpaint(...) -> area "Face"
    - Texture path expected like "Actors\\Character\\Overlays\\<Section>\\file.dds". JSON texture stores the relative part starting at <Section>.
    - Section inferred as the first folder of the relative texture path. Fallback to script name.
    - Output JSON named <ScriptName>.json in the same folder as the .psc.
    """
    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .parent =parent 
        self .setAcceptDrops (True )
        self .setStyleSheet ("background: transparent;")
        self .last_output_path =None 

        lay =QVBoxLayout (self )
        lay .setContentsMargins (8 ,8 ,8 ,8 )
        lay .setSpacing (8 )

        title =QLabel ("RACE MENU TO SLAVETATS JSON GENERATOR")
        title .setAlignment (Qt .AlignCenter )
        title .setStyleSheet ("font-size: 16px; font-weight: bold; color: #66FF66;")
        lay .addWidget (title )

        info =QLabel ("Drag and drop .psc file here")
        info .setAlignment (Qt .AlignCenter )

        info .setStyleSheet ("font-size: 14px; color: #FFA500;")
        lay .addWidget (info )

        or_label2 =QLabel ("- OR -")
        or_label2 .setAlignment (Qt .AlignCenter )
        or_label2 .setStyleSheet ("font-size: 12px; color: #E0E0E0;")
        lay .addWidget (or_label2 )
        try :

            self .setToolTip ("Drag and drop a .psc file here to convert it to SlaveTats JSON")
        except Exception :
            pass 


        self .select_psc_btn =QPushButton ("Select PSC")
        try :
            self .select_psc_btn .setCursor (Qt .PointingHandCursor )
        except Exception :
            pass 
        self .select_psc_btn .setStyleSheet (
        "QPushButton { background: rgba(38,38,44,0.78); color:#E0E0E0; border:1px solid rgba(90,90,95,0.70); border-radius:4px; padding:6px 10px; } "
        "QPushButton:hover { background: rgba(62,62,68,0.85); }"
        )
        try :
            self .select_psc_btn .setToolTip ("Select .psc file")
        except Exception :
            pass 
        self .select_psc_btn .clicked .connect (self .select_psc )
        lay .addWidget (self .select_psc_btn )

        self .status =QLabel ("Ready")
        self .status .setStyleSheet ("font-size: 12px; color: #CFCFCF;")

        try :
            self .status .setTextInteractionFlags (Qt .TextSelectableByMouse )
            self .status .setContextMenuPolicy (Qt .DefaultContextMenu )
        except Exception :
            pass 
        lay .addWidget (self .status )

        self .preview =QTextEdit ()
        self .preview .setReadOnly (True )
        self .preview .setPlaceholderText ("The generated JSON or status messages will appear here.")
        try :
            self .preview .setToolTip ("Preview of the generated JSON and status messages")
        except Exception :
            pass 
        lay .addWidget (self .preview )


        btn_row =QHBoxLayout ()


        self .btn_style_gray =(
        "QPushButton {"
        " background: rgba(53,53,57,0.82);"
        " color: #E0E0E0;"
        " border: 1px solid rgba(90,90,95,0.70);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        "}"
        "QPushButton:hover { background: rgba(62,62,68,0.90); }"
        "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
        )
        self .btn_style_green =(
        "QPushButton {"
        " background: rgba(76,175,80,0.25);"
        " color: #FFFFFF;"
        " border: 1px solid rgba(76,175,80,0.80);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        "}"
        "QPushButton:hover { background: rgba(76,175,80,0.35); }"
        "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
        )

        self .btn_style_gray_light =(
        "QPushButton {"
        " background: rgba(53,53,57,0.62);"
        " color: #E0E0E0;"
        " border: 1px solid rgba(90,90,95,0.65);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        "}"
        "QPushButton:hover { background: rgba(62,62,68,0.78); }"
        "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
        )

        self .btn_style_blue =(
        "QPushButton {"
        " background: rgba(0, 188, 212, 0.35);"
        " color: #E0F7FA;"
        " border: 1px solid rgba(0, 188, 212, 0.70);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        "}"
        "QPushButton:hover { background: rgba(0, 188, 212, 0.55); }"
        "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
        )

        try :
            self .select_psc_btn .setStyleSheet (self .btn_style_green )
        except Exception :
            pass 

        try :
            self .select_psc_btn .setStyleSheet (self .select_psc_btn .styleSheet ()+"\nQPushButton { font-weight: bold; }")
        except Exception :
            pass 

        self .btn_refresh_psc =QPushButton ("Refresh")
        try :
            self .btn_refresh_psc .setCursor (Qt .PointingHandCursor )
        except Exception :
            pass 
        self .btn_refresh_psc .setStyleSheet (self .btn_style_blue )
        try :
            self .btn_refresh_psc .setToolTip ("Clear and reset this tab")
        except Exception :
            pass 
        self .btn_refresh_psc .clicked .connect (self .refresh_tab )
        btn_row .addWidget (self .btn_refresh_psc )

        self .open_folder_btn =QPushButton ("Open output folder")
        self .open_folder_btn .setEnabled (False )
        try :
            self .open_folder_btn .setToolTip ("Open output folder")
        except Exception :
            pass 
        self .open_folder_btn .clicked .connect (self .open_output_folder )
        self .copy_dds_btn =QPushButton ("Create mod folders")
        self .copy_dds_btn .setToolTip ("Select a FOLDER; ALL its contents (subfolders and files) will be copied to textures/actors/character/slavetats/<JSON_NAME>")
        self .copy_dds_btn .setEnabled (False )
        self .copy_dds_btn .clicked .connect (self .copy_dds_to_slavetats )
        self .pack_textures_btn =QPushButton ("Create Mod zip")
        self .pack_textures_btn .setToolTip ("Create SlaveTats <JSON_NAME>.7z with the textures folder and then delete the JSON and textures")
        self .pack_textures_btn .setEnabled (False )
        self .pack_textures_btn .clicked .connect (self .pack_textures_folder )


        self .open_folder_btn .setStyleSheet (self .btn_style_gray )

        self .copy_dds_btn .setStyleSheet (self .btn_style_gray_light )
        self .pack_textures_btn .setStyleSheet (self .btn_style_gray_light )

        btn_row .addStretch (1 )
        btn_row .addWidget (self .open_folder_btn )
        btn_row .addWidget (self .copy_dds_btn )
        btn_row .addWidget (self .pack_textures_btn )
        lay .addLayout (btn_row )


        term_label =QLabel ("Output Terminal:")
        lay .addWidget (term_label )

        self .terminal_output_importer =QTextEdit ()
        self .terminal_output_importer .setReadOnly (True )
        self .terminal_output_importer .setStyleSheet (
        "QTextEdit {"
        " background-color: #1A1A1C;"
        " color: #4CAF50;"
        " border: 1px solid #3A3A3F;"
        " border-radius: 4px;"
        " font-family: Consolas, 'Courier New', monospace;"
        " font-size: 12px;"
        "}"
        )
        lay .addWidget (self .terminal_output_importer )

    def refresh_tab (self ):
        """Resets the tab to its initial state."""
        try :
            self .status .setText ("Ready")
            self .preview .clear ()
            self .preview .setPlaceholderText ("The generated JSON or status messages will appear here.")
            self .terminal_output_importer .clear ()
            self .last_output_path =None 

            self .open_folder_btn .setEnabled (False )
            self .copy_dds_btn .setEnabled (False )
            self .pack_textures_btn .setEnabled (False )

            self .open_folder_btn .setStyleSheet (self .btn_style_gray )
            self .copy_dds_btn .setStyleSheet (self .btn_style_gray )
            self .pack_textures_btn .setStyleSheet (self .btn_style_gray )

            print ("[PSCImporterTab] Tab refreshed by user.")
        except Exception as e :
            print (f"[PSCImporterTab] Error refreshing tab: {e }")


    def dragEnterEvent (self ,event :QDragEnterEvent ):
        if event .mimeData ().hasUrls ():
            urls =event .mimeData ().urls ()
            if len (urls )==1 and urls [0 ].toLocalFile ().lower ().endswith ('.psc'):
                event .acceptProposedAction ()

    def dropEvent (self ,event :QDropEvent ):
        urls =event .mimeData ().urls ()
        if not urls :
            return 
        psc_path =urls [0 ].toLocalFile ()
        self .process_psc_file (psc_path )


    def parse_psc_to_json (self ,psc_path ):
        with open (psc_path ,'r',encoding ='utf-8',errors ='ignore')as f :
            text =f .read ()


        m =re .search (r"(?i)\bscriptname\s+([A-Za-z0-9_]+)",text )
        script_name =m .group (1 )if m else os.path .splitext (os.path .basename (psc_path ))[0 ]

        items =[]
        overlays_root_regex =re .compile (r"(?i)actors[\\/]+character[\\/]+overlays[\\/]+")



        pattern =re .compile (r"(?i)\bAdd(FacePaint|BodyPaint|Warpaint|HandPaint|FeetPaint)\s*\(\s*\"([^\"]+)\"\s*,\s*\"([^\"]+)\"\s*\)")
        for kind ,name ,full_path in pattern .findall (text ):
            k =kind .lower ()
            if k in ('warpaint','facepaint'):
                area ='Face'
            elif k =='bodypaint':
                area ='Body'
            elif k =='handpaint':
                area ='Hand'
            elif k =='feetpaint':
                area ='Feet'
            else :
                area ='Body'

            norm =full_path .replace ('/','\\')

            rel =overlays_root_regex .split (norm )
            if len (rel )>1 :
                rel_path =rel [1 ]
            else :

                rel_path =norm 

            while rel_path .startswith ('\\')or rel_path .startswith ('/'):
                rel_path =rel_path [1 :]

            if rel_path .lower ().startswith ('slavetats\\'):
                rel_path =rel_path .split ('\\',1 )[1 ]if '\\'in rel_path else rel_path 

            try :
                import re as _re 
                _parts =[p for p in _re .split (r"[\\/]+",rel_path .strip ('\\/'))if p ]
                rel_path ='\\'.join (_parts )
            except Exception :
                rel_path =rel_path .replace ('\\\\','\\').replace ('/','\\')

            parts =rel_path .split ('\\')
            if parts and parts [0 ]:
                section =parts [0 ]
            else :

                section =script_name 
            item ={
            'name':name ,
            'section':section ,
            'texture':rel_path ,
            'area':area ,
            }
            items .append (item )

        return {'_script_name':script_name ,'items':items }

    def select_psc (self ):
        options =QFileDialog .Options ()
        file_path ,_ =QFileDialog .getOpenFileName (
        self ,
        "Select .psc file",
        "",
        "Papyrus Scripts (*.psc);;All Files (*)",
        options =options ,
        )
        if file_path :
            self .process_psc_file (file_path )

    def process_psc_file (self ,psc_path ):
        try :

            win =self .window ()
            try :
                if hasattr (win ,'start_progress'):
                    win .start_progress (3 ,"Processing PSC…")
            except Exception :
                pass 
            data =self .parse_psc_to_json (psc_path )

            script_name =data .get ('_script_name')or os.path .splitext (os.path .basename (psc_path ))[0 ]

            target_dir =os.path .dirname (psc_path )
            try :
                os .makedirs (target_dir ,exist_ok =True )
            except Exception as e_mk :
                self .status .setText (f"Error creating destination folder: {target_dir }")
                self .preview .setPlainText (f"Could not create destination directory.\nDestination: {target_dir }\nDetails: {e_mk }")
                return 
            out_path =os.path .join (target_dir ,f"{script_name }.json")

            items =data .get ('items',[])
            if not items :
                raise ValueError ("No AddBodyPaint/AddWarpaint/AddFacePaint/AddHandPaint/AddFeetPaint entries found in the .psc")

            try :
                if hasattr (win ,'update_progress'):
                    win .update_progress (1 )
            except Exception :
                pass 
            with open (out_path ,'w',encoding ='utf-8')as f :
                json .dump (items ,f ,indent =4 ,ensure_ascii =False )

            self .status .setText ("JSON generated.")
            self .preview .setPlainText (json .dumps (items ,indent =4 ,ensure_ascii =False ))

            lines =[]
            for i ,it in enumerate (items ,start =1 ):
                name =it .get ('name','')
                area =it .get ('area','')
                section =it .get ('section','')
                tex =it .get ('texture','')
                lines .append (f"{i :03d}. [{area }] {name } | section={section } | texture={tex }")
            try :
                def _esc (s :str )->str :
                    return s .replace ('&','&amp;').replace ('<','&lt;').replace ('>','&gt;')

                body_html =(
                '<pre style="margin:0; color:#4CAF50; font-family:Consolas, \'Courier New\', monospace; font-size:12px;">'
                +_esc ("\n".join (lines ))+
                '</pre>'
                )
                header_html =(
                '<div style="margin-top:6px; color:#00BCD4; font-size:14px; font-weight:bold;">'
                'JSON GENERATED SUCCESSFULLY'
                '</div>'
                )
                instruction_html =(
                '<div style="margin-top:4px; color:#FFA500; font-size:12px; font-weight:bold;">'
                'NOW PRESS THE CREATE MOD FOLDERS BUTTON, THEN BROWSE TO MOD_NAME\\TEXTURES\\ACTORS\\CHARACTER\\OVERLAYS AND SELECT THE OVERLAYS FOLDER. INSIDE THERE WILL BE DDS OR SUBFOLDERS WITH DDS. THE IMPORTANT PART IS TO SELECT THE OVERLAYS FOLDER.'
                '</div>'
                )
                self .terminal_output_importer .setHtml (body_html +header_html +instruction_html )
                try :
                    self .terminal_output_importer .moveCursor (QTextCursor .End )
                except Exception :
                    pass 
            except Exception :

                self .terminal_output_importer .setPlainText ("\n".join (lines )+"\nJSON GENERATED SUCCESSFULLY")

            self .last_output_path =out_path 
            self .open_folder_btn .setEnabled (True )
            self .copy_dds_btn .setEnabled (True )

            try :
                self .open_folder_btn .setStyleSheet (self .btn_style_green )
                self .copy_dds_btn .setStyleSheet (self .btn_style_green )
            except Exception :
                pass 

            try :
                if hasattr (win ,'update_progress'):
                    win .update_progress (2 )
                if hasattr (win ,'finish_progress'):
                    win .finish_progress ("PSC processed")
            except Exception :
                pass 
        except Exception as e :

            try :
                import traceback 
                tb =traceback .format_exc ()
            except Exception :
                tb =""
            self .status .setText (f"Error: {e }")
            details =(
            f"PSC file: {psc_path }\n"
            f"Details: {str (e )}\n\n"
            f"Traceback:\n{tb }"
            )
            self .preview .setPlainText (details )
            try :
                self .terminal_output_importer .setPlainText ("ERROR\n"+details )
            except Exception :
                pass 

            try :
                if hasattr (win ,'_reset_progress'):
                    win ._reset_progress ()
            except Exception :
                pass 

    def open_output_folder (self ):
        try :
            if not self .last_output_path :
                self .status .setText ("No output yet")
                return 
            folder =os.path .dirname (self .last_output_path )
            if hasattr (os ,'startfile'):
                os .startfile (folder )
            else :
                QDesktopServices .openUrl (QUrl .fromLocalFile (folder ))
        except Exception as e :
            self .status .setText (f"Could not open folder: {e }")

    def copy_dds_to_slavetats (self ):
        try :
            if not self .last_output_path :
                self .status .setText ("Generate a JSON first")
                return 
            base_json_dir =os.path .dirname (self .last_output_path )

            try :
                cursor =self .terminal_output_importer .textCursor ()
                cursor .movePosition (QTextCursor .End )
                self .terminal_output_importer .setTextCursor (cursor )
                self .terminal_output_importer .insertHtml (
                '<br/>'
                '<div style="color:#FFA500; font-weight:bold; font-size:13px;">'
                'NOW BROWSE THE FOLDER THAT CONTAINS DDS FILES TO ORGANIZE'
                '</div>'
                '<div style="color:#FFA500; font-weight:bold; font-size:12px;">'
                'USUALLY LOCATED IN: MOD_NAME\\textures\\Actors\\Character\\Overlays\\&lt;CONTAINER_FOLDER&gt;\\ (FULL OF DDS)'
                '</div>'
                '<div style="color:#FFA500; font-weight:bold; font-size:12px;">'
                'SELECT THE FOLDER WITH THE DDS INSIDE'
                '</div><br/>'
                )
                try :
                    self .terminal_output_importer .moveCursor (QTextCursor .End )
                except Exception :
                    pass 
            except Exception :
                pass 

            src_dir =QFileDialog .getExistingDirectory (
            self ,
            "Select FOLDER (its CONTENT and subfolders will be copied)",
            base_json_dir ,
            QFileDialog .ShowDirsOnly |QFileDialog .DontResolveSymlinks ,
            )
            if not src_dir :
                self .status .setText ("Operation cancelled")
                return 

            try :
                selected_norm =os.path .normpath (src_dir )
                selected_basename =os.path .basename (selected_norm )

                parts =[p for p in selected_norm .replace ('/','\\').split ('\\')if p ]
                has_overlays_ancestor =any (p .lower ()=='overlays'for p in parts )
            except Exception :
                selected_norm =src_dir 
                selected_basename =os.path .basename (src_dir )
                parts =[p for p in src_dir .replace ('/','\\').split ('\\')if p ]
                has_overlays_ancestor =any (p .lower ()=='overlays'for p in parts )
            is_overlays =str (selected_basename ).lower ()=='overlays'
            if not (is_overlays or has_overlays_ancestor ):
                self .status .setText ("Please select the 'Overlays' folder or a folder INSIDE any 'Overlays'")
                try :
                    cursor =self .terminal_output_importer .textCursor ()
                    cursor .movePosition (QTextCursor .End )
                    self .terminal_output_importer .setTextCursor (cursor )
                    self .terminal_output_importer .insertHtml (
                    '<br/>'
                    '<div style="color:#FF5252; font-weight:bold; font-size:13px;">'
                    "INVALID SELECTION: SELECT '...\\Overlays' OR A FOLDER INSIDE ANY '...\\Overlays'"
                    '</div><br/>'
                    )
                    try :
                        self .terminal_output_importer .moveCursor (QTextCursor .End )
                    except Exception :
                        pass 
                except Exception :
                    pass 
                return 

            try :
                has_dds =False 
                for root ,dirs ,fnames in os .walk (src_dir ):
                    for fn in fnames :
                        if fn .lower ().endswith ('.dds'):
                            has_dds =True 
                            break 
                    if has_dds :
                        break 
                if not has_dds :

                    self .status .setText ("No .dds files found in the selected folder")
                    try :
                        cursor =self .terminal_output_importer .textCursor ()
                        cursor .movePosition (QTextCursor .End )
                        self .terminal_output_importer .setTextCursor (cursor )
                        self .terminal_output_importer .insertHtml (
                        '<br/>'
                        '<div style="color:#FF5252; font-weight:bold; font-size:13px;">'
                        'NO DDS FILES FOUND IN SELECTED FOLDER. PLEASE SELECT A FOLDER WITH AT LEAST ONE .DDS'
                        '</div><br/>'
                        )
                    except Exception :
                        pass 
                    return 
            except Exception :

                pass 

            original_json_name =os.path .splitext (os.path .basename (self .last_output_path ))[0 ]
            copy_root =src_dir 
            if is_overlays :

                try :
                    subdirs =[]
                    for entry in os .listdir (src_dir ):
                        p =os.path .join (src_dir ,entry )
                        if os.path .isdir (p ):
                            subdirs .append ((entry ,p ))
                    candidates =[]
                    for name ,p in subdirs :
                        has_dds_sub =False 
                        for r ,ds ,fs in os .walk (p ):
                            for fn in fs :
                                if fn .lower ().endswith ('.dds'):
                                    has_dds_sub =True 
                                    break 
                            if has_dds_sub :
                                break 
                        if has_dds_sub :
                            candidates .append ((name ,p ))
                    if len (candidates )==1 :
                        json_name =candidates [0 ][0 ]
                        copy_root =candidates [0 ][1 ]
                    else :

                        json_name =original_json_name 
                        copy_root =src_dir 
                except Exception :
                    json_name =original_json_name 
                    copy_root =src_dir 
            else :

                json_name =selected_basename 
                copy_root =src_dir 

            textures_root =os.path .join (base_json_dir ,"textures")
            slavetats_root =os.path .join (textures_root ,"actors","character","slavetats")
            target_dir =os.path .join (slavetats_root ,json_name )
            os .makedirs (target_dir ,exist_ok =True )
            import shutil 
            copied =0 
            errors =[]
            json_copied =False 

            total_files =0 
            try :
                for root ,dirs ,fnames in os .walk (copy_root ):
                    total_files +=len (fnames )
            except Exception :
                total_files =0 
            win =self .window ()
            try :
                if hasattr (win ,'start_progress'):

                    win .start_progress (max (1 ,total_files +2 ),"Copying files…")
            except Exception :
                pass 

            try :
                new_json_path =os.path .join (slavetats_root ,f"{json_name }.json")
                shutil .copy2 (self .last_output_path ,new_json_path )
                self .last_output_path =new_json_path 
                json_copied =True 
            except Exception as ce :
                errors .append (f"Copying JSON to slavetats -> {ce }")

            try :
                dds_list =[]
                for root ,dirs ,fnames in os .walk (copy_root ):
                    for fn in fnames :
                        if fn .lower ().endswith ('.dds'):
                            rel =os.path .relpath (os.path .join (root ,fn ),copy_root )
                            dds_list .append (rel )
                if dds_list :
                    max_show =60 
                    head ="\n".join (dds_list [:max_show ])
                    extra =len (dds_list )-max_show 
                    extra_msg =f"\n... (+{extra } more)"if extra >0 else ""
                    self .preview .setPlainText (f"DDS found: {len (dds_list )}\n\n{head }{extra_msg }")
                else :
                    self .preview .setPlainText ("No .dds files were found in the selected folder (other files will still be copied)")
            except Exception :
                pass 

            base_dst =target_dir 
            progressed =0 
            for root ,dirs ,fnames in os .walk (copy_root ):
                rel =os.path .relpath (root ,copy_root )
                dst_root =os.path .join (base_dst ,rel )if rel !='.'else base_dst 
                os .makedirs (dst_root ,exist_ok =True )
                for fn in fnames :
                    s =os.path .join (root ,fn )
                    d =os.path .join (dst_root ,fn )
                    try :
                        shutil .copy2 (s ,d )
                        copied +=1 
                    except Exception as ce :
                        errors .append (f"{s } -> {ce }")

                    progressed +=1 
                    try :
                        if hasattr (win ,'update_progress'):
                            win .update_progress (min (progressed +1 ,max (1 ,total_files +2 )))
                    except Exception :
                        pass 

            if copied >0 and os.path .isdir (textures_root ):
                self .pack_textures_btn .setEnabled (True )
                try :
                    self .pack_textures_btn .setStyleSheet (self .btn_style_green )
                except Exception :
                    pass 

            msg =f"Copied {copied } items."
            if errors :
                msg +=f" | Errors: {len (errors )} (see preview)"
                self .preview .setPlainText ("\n".join (errors ))

            try :

                original_json_path =os.path .join (base_json_dir ,f"{original_json_name }.json")
                if json_copied and os.path .isfile (original_json_path ):
                    os .remove (original_json_path )
                    msg +=" | Original JSON deleted"
            except Exception :
                pass 
            self .status .setText (msg )

            try :
                cursor =self .terminal_output_importer .textCursor ()
                cursor .movePosition (QTextCursor .End )
                self .terminal_output_importer .setTextCursor (cursor )
                self .terminal_output_importer .insertHtml (
                '<br/>'
                '<div style="color:#00BCD4; font-weight:bold; font-size:13px;">'
                'FILES COPIED AND JSON POSITIONED CORRECTLY. NEXT STEP: PACK AS ZIP TO SHARE OR INSTALL IN YOUR MOD LIST.'
                '</div><br/>'
                )
                try :
                    self .terminal_output_importer .moveCursor (QTextCursor .End )
                except Exception :
                    pass 
            except Exception :
                pass 

            try :
                if hasattr (win ,'finish_progress'):
                    win .finish_progress ("Copy finished")
            except Exception :
                pass 
        except Exception as e :
            try :
                import traceback 
                tb =traceback .format_exc ()
            except Exception :
                tb =""
            self .status .setText (f"Error copying DDS: {e }")
            self .preview .setPlainText (tb )
            try :
                win =self .window ()
                if hasattr (win ,'_reset_progress'):
                    win ._reset_progress ()
            except Exception :
                pass 

    def pack_textures_folder (self ):
        try :
            if not self .last_output_path :
                self .status .setText ("Generate a JSON first")
                return 
            base_json_dir =os.path .dirname (self .last_output_path )
            textures_root =os.path .join (base_json_dir ,"textures")
            if not os.path .isdir (textures_root ):
                self .status .setText ("Textures folder does not exist")
                return 
            json_name =os.path .splitext (os.path .basename (self .last_output_path ))[0 ]
            archive_basename =f"SLAVE TATS {json_name }"

            import shutil as _shutil 
            import subprocess 
            sevenz =_shutil .which ('7z')or _shutil .which ('7z.exe')

            win =self .window ()
            try :
                if hasattr (win ,'start_progress'):
                    win .start_progress (100 ,"Packing…")
            except Exception :
                pass 
            if sevenz :
                out_path =os.path .join (base_json_dir ,f"{archive_basename }.7z")

                try :
                    proc =subprocess .Popen (
                    [sevenz ,'a','-t7z','-mx=9','-bsp1',out_path ,'textures'],
                    cwd =base_json_dir ,
                    stdout =subprocess .PIPE ,
                    stderr =subprocess .STDOUT ,
                    text =True ,
                    encoding ='utf-8',
                    errors ='ignore'
                    )
                    if proc .stdout is not None :
                        for line in proc .stdout :
                            ln =line .strip ()

                            try :
                                import re as _re 
                                m =_re .search (r"(\d{1,3})%",ln )
                                if m :
                                    pct =int (max (0 ,min (100 ,int (m .group (1 )))))
                                    if hasattr (win ,'update_progress'):
                                        win .update_progress (pct )
                            except Exception :
                                pass 
                    ret =proc .wait ()
                    if ret !=0 :
                        raise subprocess .CalledProcessError (ret ,'7z')

                    try :
                        if os.path .isfile (self .last_output_path ):
                            os .remove (self .last_output_path )
                    except Exception :
                        pass 
                    try :
                        if os.path .isdir (textures_root ):
                            _shutil .rmtree (textures_root ,ignore_errors =True )
                    except Exception :
                        pass 
                    self .status .setText ("7z package created and JSON/textures cleaned.")
                    try :
                        if hasattr (win ,'finish_progress'):
                            win .finish_progress ("100% • Compressed mod ready")
                    except Exception :
                        pass 

                    try :
                        cursor =self .terminal_output_importer .textCursor ()
                        cursor .movePosition (QTextCursor .End )
                        self .terminal_output_importer .setTextCursor (cursor )
                        self .terminal_output_importer .insertHtml (
                        '<br/>'
                        '<div style="color:#FF69B4; font-weight:bold; font-size:13px;">'
                        'PACKAGE READY. YOU CAN NOW SHARE IT OR INSTALL IT. THIS IS A COMPLETE PORT TO SLAVETATS!'
                        '</div><br/>'
                        )
                        try :
                            self .terminal_output_importer .moveCursor (QTextCursor .End )
                        except Exception :
                            pass 
                    except Exception :
                        pass 
                except subprocess .CalledProcessError as ce :


                    zip_target =os.path .join (base_json_dir ,f"{archive_basename }.zip")

                    total_files =0 
                    for r ,d ,f in os .walk (textures_root ):
                        total_files +=len (f )
                    done =0 
                    with zipfile .ZipFile (zip_target ,'w',compression =zipfile .ZIP_DEFLATED )as zf :
                        for r ,d ,fns in os .walk (textures_root ):
                            for fn in fns :
                                abs_f =os.path .join (r ,fn )
                                arc_f =os.path .relpath (abs_f ,base_json_dir )
                                zf .write (abs_f ,arcname =arc_f )
                                done +=1 
                                try :
                                    if total_files >0 and hasattr (win ,'update_progress'):
                                        pct =int (done *100 /total_files )
                                        win .update_progress (pct )
                                except Exception :
                                    pass 
                    try :
                        if os.path .isfile (self .last_output_path ):
                            os .remove (self .last_output_path )
                    except Exception :
                        pass 
                    try :
                        if os.path .isdir (textures_root ):
                            _shutil .rmtree (textures_root ,ignore_errors =True )
                    except Exception :
                        pass 
                    self .status .setText ("7z failed; ZIP created and JSON/textures cleaned.")
                    try :
                        if hasattr (win ,'finish_progress'):
                            win .finish_progress ("100% • Compressed mod ready")
                    except Exception :
                        pass 

                    try :
                        cursor =self .terminal_output_importer .textCursor ()
                        cursor .movePosition (QTextCursor .End )
                        self .terminal_output_importer .setTextCursor (cursor )
                        self .terminal_output_importer .insertHtml (
                        '<br/>'
                        '<div style="color:#FF69B4; font-weight:bold; font-size:13px;">'
                        'PACKAGE READY. YOU CAN NOW SHARE IT OR INSTALL IT. THIS IS A COMPLETE PORT TO SLAVETATS!'
                        '</div><br/>'
                        )
                        try :
                            self .terminal_output_importer .moveCursor (QTextCursor .End )
                        except Exception :
                            pass 
                    except Exception :
                        pass 
            else :

                zip_target =os.path .join (base_json_dir ,f"{archive_basename }.zip")
                total_files =0 
                for r ,d ,f in os .walk (textures_root ):
                    total_files +=len (f )
                done =0 
                with zipfile .ZipFile (zip_target ,'w',compression =zipfile .ZIP_DEFLATED )as zf :
                    for r ,d ,fns in os .walk (textures_root ):
                        for fn in fns :
                            abs_f =os.path .join (r ,fn )
                            arc_f =os.path .relpath (abs_f ,base_json_dir )
                            zf .write (abs_f ,arcname =arc_f )
                            done +=1 
                            try :
                                if total_files >0 and hasattr (win ,'update_progress'):
                                    pct =int (done *100 /total_files )
                                    win .update_progress (pct )
                            except Exception :
                                pass 
                try :
                    if os.path .isfile (self .last_output_path ):
                        os .remove (self .last_output_path )
                except Exception :
                    pass 
                try :
                    if os.path .isdir (textures_root ):
                        _shutil .rmtree (textures_root ,ignore_errors =True )
                except Exception :
                    pass 
                self .status .setText ("ZIP created (7z not found) and JSON/textures cleaned.")
                try :
                    if hasattr (win ,'finish_progress'):
                        win .finish_progress ("100% • Compressed mod ready")
                except Exception :
                    pass 

                try :
                    cursor =self .terminal_output_importer .textCursor ()
                    cursor .movePosition (QTextCursor .End )
                    self .terminal_output_importer .setTextCursor (cursor )
                    self .terminal_output_importer .insertHtml (
                    '<br/>'
                    '<div style="color:#FF69B4; font-weight:bold; font-size:13px;">'
                    'PACKAGE READY. YOU CAN NOW SHARE IT OR INSTALL IT. THIS IS A COMPLETE PORT TO SLAVETATS!'
                    '</div><br/>'
                    )
                    try :
                        self .terminal_output_importer .moveCursor (QTextCursor .End )
                    except Exception :
                        pass 
                except Exception :
                    pass 
        except Exception as e :
            try :
                import traceback 
                tb =traceback .format_exc ()
            except Exception :
                tb =""
            self .status .setText (f"Error while packing: {e }")
            self .preview .setPlainText (tb )
            try :
                win =self .window ()
                if hasattr (win ,'_reset_progress'):
                    win ._reset_progress ()
            except Exception :
                pass 

class DdsPreviewWindow (QWidget ):
    """Ventana de vista previa para imágenes DDS con color de fondo configurable."""
    def __init__ (self ,path :str ,parent =None ,log_fn =None ):
        super ().__init__ (parent )
        self .setWindowTitle (os.path .basename (path ))

        self .resize (900 ,900 )
        try :
            self .setMinimumSize (300 ,300 )
        except Exception :
            pass 
        self ._bg =QColor(255 ,255 ,255 )
        self ._orig_pixmap =None 
        self ._orig_qimage =None 
        self ._orig_pil =None 
        self ._composited_pixmap =None 
        self ._path =path 
        self ._log_fn =log_fn 
        self ._scale =1.0 
        self ._did_fit =False 

        self ._fg_contrast =1.0 
        self ._bg_contrast =1.0 
        self ._bg_cache_path =None 
        self ._bg_cache_pil =None 

        try :
            self .setWindowFlags (self .windowFlags ()|Qt .Window )
        except Exception :
            pass 
        lay =QVBoxLayout (self )
        lay .setContentsMargins (8 ,8 ,8 ,8 )
        lay .setSpacing (8 )


        self .image_label =QLabel ("Loading…")
        self .image_label .setAlignment (Qt .AlignCenter )
        self .image_label .setStyleSheet ("background-color: #FFFFFF; color: #666;")
        self .image_label .setSizePolicy (QSizePolicy .Ignored ,QSizePolicy .Ignored )
        self .scroll =QScrollArea ()


        self .scroll .setWidgetResizable (False )
        try :
            self .scroll .setAlignment (Qt .AlignCenter )
        except Exception :
            pass 
        try :
            self .scroll .setMouseTracking (True )
        except Exception :
            pass 
        self .scroll .setWidget (self .image_label )

        self ._panning =False 
        self ._pan_start_pos =QPoint ()
        self ._pan_start_global =QPoint ()
        self ._h0 =0 
        self ._v0 =0 
        try :
            self .scroll .viewport ().setMouseTracking (True )
            self .scroll .viewport ().installEventFilter (self )
            self .image_label .setMouseTracking (True )
            self .image_label .installEventFilter (self )
        except Exception :
            pass 


        controls_widget =QWidget ()
        controls_widget .setStyleSheet ("background: transparent;")
        controls_grid =QGridLayout (controls_widget )
        controls_grid .setContentsMargins (0 ,0 ,0 ,0 )
        controls_grid .setHorizontalSpacing (10 )
        controls_grid .setVerticalSpacing (6 )
        try :

            controls_grid .setColumnStretch (2 ,2 )
            controls_grid .setColumnStretch (3 ,1 )
            controls_grid .setColumnStretch (6 ,2 )
            controls_grid .setColumnStretch (7 ,1 )
        except Exception :
            pass 
        self .btn_bg =QPushButton ("Change background…")
        try :
            self .btn_bg .setCursor (Qt .PointingHandCursor )
        except Exception :
            pass 

        _btn_style =(
        "QPushButton {"
        "  background-color: #3A3F4B;"
        "  color: #FFFFFF;"
        "  border: 1px solid #282C34;"
        "  border-radius: 6px;"
        "  padding: 6px 10px;"
        "}"
        "QPushButton:hover {"
        "  background-color: #4A5060;"
        "}"
        "QPushButton:pressed {"
        "  background-color: #2E3340;"
        "}"
        "QPushButton:disabled {"
        "  background-color: #2B2F3A; color: #777; border-color: #222;"
        "}"
        )
        self .btn_bg .setStyleSheet (_btn_style )

        self .btn_bg .clicked .connect (self ._choose_bg_color )
        try :
            self .btn_bg .setToolTip ("Elegir color de fondo o imagen de fondo (DDS)")
        except Exception :
            pass 
        controls_grid .addWidget (self .btn_bg ,0 ,9 )


        self .btn_fit =QPushButton ("Fit to window")
        try :
            self .btn_fit .setCursor (Qt .PointingHandCursor )
        except Exception :
            pass 
        self .btn_fit .setStyleSheet (_btn_style )

        self .btn_fit .clicked .connect (self ._fit_to_window )
        try :
            self .btn_fit .setToolTip ("Ajustar imagen al tamaño de la ventana")
        except Exception :
            pass 
        controls_grid .addWidget (self .btn_fit ,1 ,6 )

        self .btn_100 =QPushButton ("100%")
        try :
            self .btn_100 .setCursor (Qt .PointingHandCursor )
        except Exception :
            pass 
        self .btn_100 .setStyleSheet (_btn_style )
        self .btn_100 .clicked .connect (lambda :self ._set_zoom (1.0 ))
        try :
            self .btn_100 .setToolTip ("Ver al 100% (zoom 1:1)")
        except Exception :
            pass 
        controls_grid .addWidget (self .btn_100 ,1 ,7 )


        bg_lbl =QLabel ("Background:")
        try :
            bg_lbl .setStyleSheet ("color:#C8C8C8;")
        except Exception :
            pass 
        controls_grid .addWidget (bg_lbl ,0 ,0 )
        self .bg_combo =QComboBox ()
        try :
            self .bg_combo .setMinimumWidth (160 )

            self .bg_combo .setStyleSheet (
            "QComboBox { background-color: #2F3340; color: #FFFFFF; border: 1px solid #282C34; border-radius: 6px; padding: 4px 8px; }"
            "QComboBox QAbstractItemView { background-color: #2F3340; color: #FFFFFF; selection-background-color: #4A5060; }"
            )
        except Exception :
            pass 

        try :
            import types as _types 
        except Exception :
            _types =None 
        if not hasattr (self ,'_find_bg_dir'):
            def __fallback_find_bg_dir ():
                try :
                    base =BASE_PATH
                    cand1 =os.path .join (base ,'Data','DDS')
                    if os.path .isdir (cand1 ):
                        return cand1 
                except Exception :
                    pass 
                try :
                    cand2 =os.path .join (os .getcwd (),'Data','DDS')
                    if os.path .isdir (cand2 ):
                        return cand2 
                except Exception :
                    pass 
                return None 
            self ._find_bg_dir =__fallback_find_bg_dir 
        if not hasattr (self ,'_populate_bg_combo'):
            def __fallback_populate_bg_combo ():
                try :
                    self .bg_combo .clear ()
                    self .bg_combo .addItem ("White (no image)",userData =None )
                    bg_dir =self ._find_bg_dir ()
                    if not bg_dir or not os.path .isdir (bg_dir ):
                        return 
                    norm_paths =set ()
                    for ext in ("*.dds","*.DDS"):
                        for f in glob .glob (os.path .join (bg_dir ,ext )):
                            try :
                                norm_paths .add (os.path .normcase (os.path .abspath (f )))
                            except Exception :
                                norm_paths .add (f )
                    for f in sorted (norm_paths ,key =lambda p :os.path .basename (p ).lower ()):
                        self .bg_combo .addItem (os.path .basename (f ),userData =f )
                except Exception :
                    pass 
            self ._populate_bg_combo =__fallback_populate_bg_combo 
        if not hasattr (self ,'_on_bg_changed'):
            def __fallback_on_bg_changed (idx ):
                try :
                    self ._bg_cache_path =self .bg_combo .currentData ()
                    self ._bg_cache_pil =None 
                except Exception :
                    self ._bg_cache_path =None 
                    self ._bg_cache_pil =None 
                try :
                    if hasattr (self ,'_recompose'):
                        self ._recompose ()
                    if hasattr (self ,'_rescale'):
                        self ._rescale ()
                except Exception :
                    pass 
            self ._on_bg_changed =__fallback_on_bg_changed 
        self ._populate_bg_combo ()
        self .bg_combo .currentIndexChanged .connect (self ._on_bg_changed )
        try :
            self .bg_combo .setToolTip ("Seleccionar imagen de fondo DDS para previsualización")
        except Exception :
            pass 
        controls_grid .addWidget (self .bg_combo ,0 ,1 ,1 ,3 )


        def _choose_bg_color (self ):
            try :
                col =QColorDialog .getColor (self ._bg ,self ,"Choose background color")
            except Exception :
                col =None 
            if col and hasattr (col ,'isValid')and col .isValid ():
                self ._bg =col 
                try :
                    self .image_label .setStyleSheet (f"background-color: {col .name ()};")
                except Exception :
                    pass 
                try :

                    if hasattr (self ,'_recompose'):
                        self ._recompose ()
                    if hasattr (self ,'_rescale'):
                        self ._rescale ()
                except Exception :
                    pass 

        try :
            setattr (DdsPreviewWindow ,'_choose_bg_color',_choose_bg_color )
        except Exception :

            self ._choose_bg_color =_choose_bg_color .__get__ (self ,DdsPreviewWindow )


        def _fit_to_window_impl (self ):
            try :
                if not getattr (self ,'_orig_pixmap',None ):
                    return 
                vp =self .scroll .viewport ().size ()if hasattr (self ,'scroll')else None 
                if not vp or vp .width ()<=0 or vp .height ()<=0 :
                    return 
                img_w =max (1 ,self ._orig_pixmap .width ())
                img_h =max (1 ,self ._orig_pixmap .height ())
                scale_w =vp .width ()/img_w 
                scale_h =vp .height ()/img_h 
                new_scale =min (scale_w ,scale_h )
                if hasattr (self ,'_rescale'):
                    self ._scale =max (0.05 ,min (10.0 ,new_scale ))
                    self ._rescale ()
                if callable (getattr (self ,'_log_fn',None )):
                    try :
                        self ._log_fn (f"[DDS Preview] Fit to window, zoom {getattr (self ,'_scale',1.0 ):.2f}x")
                    except Exception :
                        pass 
            except Exception :
                pass 
        try :

            if not hasattr (DdsPreviewWindow ,'_fit_to_window'):
                setattr (DdsPreviewWindow ,'_fit_to_window',_fit_to_window_impl )
        except Exception :

            self ._fit_to_window =_fit_to_window_impl .__get__ (self ,DdsPreviewWindow )


        try :

            fg_lbl =QLabel ("FG Contrast:")
            fg_lbl .setStyleSheet ("color:#C8C8C8;")
            self .fg_slider =QSlider (Qt .Horizontal )
            self .fg_slider .setMinimum (20 )
            self .fg_slider .setMaximum (300 )
            self .fg_slider .setSingleStep (5 )
            self .fg_slider .setPageStep (10 )
            self .fg_slider .setTickInterval (20 )
            self .fg_slider .setTickPosition (QSlider .TicksBelow )
            self .fg_slider .setValue (100 )
            self .fg_slider .setFixedWidth (200 )
            self .fg_slider .valueChanged .connect (self ._on_fg_slider_changed )
            self .fg_val =QLabel ("1.00x")
            self .fg_val .setStyleSheet ("color:#B0FFC0;")
            controls_grid .addWidget (fg_lbl ,1 ,0 )
            controls_grid .addWidget (self .fg_slider ,1 ,1 ,1 ,3 )
            controls_grid .addWidget (self .fg_val ,1 ,4 )


            bgc_lbl =QLabel ("BG Contrast:")
            bgc_lbl .setStyleSheet ("color:#C8C8C8;")
            self .bg_slider =QSlider (Qt .Horizontal )
            self .bg_slider .setMinimum (20 )
            self .bg_slider .setMaximum (300 )
            self .bg_slider .setSingleStep (5 )
            self .bg_slider .setPageStep (10 )
            self .bg_slider .setTickInterval (20 )
            self .bg_slider .setTickPosition (QSlider .TicksBelow )
            self .bg_slider .setValue (100 )
            self .bg_slider .setFixedWidth (200 )
            self .bg_slider .valueChanged .connect (self ._on_bg_slider_changed )
            self .bg_val =QLabel ("1.00x")
            self .bg_val .setStyleSheet ("color:#B0FFC0;")
            controls_grid .addWidget (bgc_lbl ,0 ,4 )
            controls_grid .addWidget (self .bg_slider ,0 ,5 ,1 ,3 )
            controls_grid .addWidget (self .bg_val ,0 ,8 )
        except Exception :
            pass 



        try :
            self .size_grip =QSizeGrip (self )
            controls_grid .addWidget (self .size_grip ,1 ,9 ,1 ,1 ,alignment =Qt .AlignRight |Qt .AlignBottom )
        except Exception :
            pass 
        lay .addWidget (self .scroll ,1 )
        lay .addWidget (controls_widget )



        def __pv_pil_to_qimage (self ,im ):
            try :
                im =im .convert ('RGBA')
                w ,h =im .size 
                buf =im .tobytes ('raw','RGBA')
                qimg =QImage (buf ,w ,h ,QImage .Format_RGBA8888 )
                return qimg .copy ()
            except Exception :
                return None 

        def __pv_load_dds_qimage (self ,path :str ):
            try :
                from PIL import Image 
                try :
                    import PIL .DdsImagePlugin 
                except Exception :
                    pass 
                try :
                    import pillow_bc7 
                except Exception :
                    pass 
                im =Image .open (path )
                im .load ()
                im =im .convert ('RGBA')
                w ,h =im .size 
                buf =im .tobytes ('raw','RGBA')
                qimg =QImage (buf ,w ,h ,QImage .Format_RGBA8888 )
                return qimg .copy ()
            except Exception :
                return None 

        def __pv_recompose (self ):
            try :
                base_qimg =None 
                if getattr (self ,'_orig_pil',None )is not None :
                    try :
                        from PIL import ImageEnhance 
                        im =self ._orig_pil 
                        if abs (float (self ._fg_contrast )-1.0 )>1e-6 :
                            im =ImageEnhance .Contrast (im ).enhance (float (self ._fg_contrast ))
                        base_qimg =self ._pil_to_qimage (im )
                    except Exception :
                        base_qimg =getattr (self ,'_orig_qimage',None )
                else :
                    base_qimg =getattr (self ,'_orig_qimage',None )
                if base_qimg is None :
                    self ._composited_pixmap =getattr (self ,'_orig_pixmap',None )
                    return 
                canvas =QImage (base_qimg .size (),QImage .Format_RGBA8888 )

                try :
                    bg_path =self .bg_combo .currentData ()
                except Exception :
                    bg_path =None 
                if bg_path :
                    bg_qimg =None 
                    try :
                        from PIL import Image ,ImageEnhance 
                        if self ._bg_cache_path !=bg_path or getattr (self ,'_bg_cache_pil',None )is None :
                            bg_pil =Image .open (bg_path )
                            bg_pil .load ()
                            bg_pil =bg_pil .convert ('RGBA')
                            self ._bg_cache_path =bg_path 
                            self ._bg_cache_pil =bg_pil 
                        else :
                            bg_pil =self ._bg_cache_pil 
                        if abs (float (self ._bg_contrast )-1.0 )>1e-6 :
                            bg_pil_eff =ImageEnhance .Contrast (bg_pil ).enhance (float (self ._bg_contrast ))
                        else :
                            bg_pil_eff =bg_pil 
                        bg_qimg =self ._pil_to_qimage (bg_pil_eff )
                    except Exception :
                        bg_qimg =self ._load_dds_qimage (bg_path )
                    if bg_qimg is not None and not bg_qimg .isNull ():
                        bg_scaled =bg_qimg .scaled (base_qimg .width (),base_qimg .height (),Qt .IgnoreAspectRatio ,Qt .SmoothTransformation )
                        p =QPainter (canvas )
                        p .fillRect (canvas .rect (),self ._bg )
                        p .drawImage (0 ,0 ,bg_scaled )
                        p .setCompositionMode (QPainter .CompositionMode_SourceOver )
                        p .drawImage (0 ,0 ,base_qimg )
                        p .end ()
                    else :
                        p =QPainter (canvas )
                        p .fillRect (canvas .rect (),self ._bg )
                        p .drawImage (0 ,0 ,base_qimg )
                        p .end ()
                else :
                    p =QPainter (canvas )
                    p .fillRect (canvas .rect (),self ._bg )
                    p .drawImage (0 ,0 ,base_qimg )
                    p .end ()
                self ._composited_pixmap =QPixmap .fromImage (canvas )
            except Exception :
                self ._composited_pixmap =getattr (self ,'_orig_pixmap',None )

        def __pv_rescale (self ):
            base_pix =self ._composited_pixmap if getattr (self ,'_composited_pixmap',None )else getattr (self ,'_orig_pixmap',None )
            if not base_pix :
                return 
            base_w =base_pix .width ()
            base_h =base_pix .height ()
            target_w =max (1 ,int (base_w *self ._scale ))
            target_h =max (1 ,int (base_h *self ._scale ))
            scaled =base_pix .scaled (target_w ,target_h ,Qt .KeepAspectRatio ,Qt .SmoothTransformation )
            self .image_label .setPixmap (scaled )
            self .image_label .resize (scaled .size ())

        def __pv_fit_initial (self ):
            try :
                if not getattr (self ,'_orig_pixmap',None ):
                    return 
                vp =self .scroll .viewport ().size ()
                img_w =max (1 ,self ._orig_pixmap .width ())
                img_h =max (1 ,self ._orig_pixmap .height ())
                if vp .width ()>0 and vp .height ()>0 :
                    scale_w =vp .width ()/img_w 
                    scale_h =vp .height ()/img_h 
                    new_scale =min (scale_w ,scale_h )
                    new_scale =max (0.1 ,min (1.0 ,new_scale ))
                    self ._scale =new_scale 
                    self ._rescale ()
                    self ._did_fit =True 
            except Exception :
                pass 

        def __pv_load_image (self ,path :str ):
            pix =None 
            last_err =""
            try :
                from PIL import Image 
                try :
                    import PIL .DdsImagePlugin 
                except Exception :
                    pass 
                try :
                    import pillow_bc7 
                except Exception :
                    pass 
                im =Image .open (path )
                im .load ()
                im =im .convert ('RGBA')
                w ,h =im .size 
                self ._orig_pil =im .copy ()
                buf =im .tobytes ('raw','RGBA')
                qimage =QImage (buf ,w ,h ,QImage .Format_RGBA8888 )
                qimage =qimage .copy ()
                self ._orig_qimage =qimage 
                pix =QPixmap .fromImage (qimage )
            except Exception as e :
                last_err =str (e )
                pix =QPixmap (path )
            if pix is None or pix .isNull ():
                msg ="Could not load image"
                if last_err :
                    msg =f"Could not load image: {last_err }"
                self .image_label .setText (msg )
                try :
                    if callable (self ._log_fn ):
                        self ._log_fn (f"[DDS Preview] {os.path .basename (path )} -> {msg }",err =True )
                except Exception :
                    pass 
                self ._orig_pixmap =None 
                return 
            else :
                try :
                    if callable (self ._log_fn ):
                        self ._log_fn (f"[DDS Preview] Loaded {os.path .basename (path )} ({pix .width ()}x{pix .height ()})")
                except Exception :
                    pass 
            self ._orig_pixmap =pix 
            self ._recompose ()
            self ._rescale ()
            try :
                if not getattr (self ,'_did_fit',False ):
                    QTimer .singleShot (0 ,self ._fit_initial )
            except Exception :
                pass 


        for name ,fn in (
        ('_pil_to_qimage',__pv_pil_to_qimage ),
        ('_load_dds_qimage',__pv_load_dds_qimage ),
        ('_recompose',__pv_recompose ),
        ('_rescale',__pv_rescale ),
        ('_fit_initial',__pv_fit_initial ),
        ('_load_image',__pv_load_image ),
        ):
            try :
                if not hasattr (DdsPreviewWindow ,name ):
                    setattr (DdsPreviewWindow ,name ,fn )
            except Exception :
                try :
                    setattr (self ,name ,fn .__get__ (self ,DdsPreviewWindow ))
                except Exception :
                    pass 

        self ._load_image (path )

    def _choose_bg_color (self ):
        col =QColorDialog .getColor (self ._bg ,self ,"Choose background color")
        if hasattr (col ,'isValid')and col .isValid ():
            self ._bg =col 
            try :
                self .image_label .setStyleSheet (f"background-color: {col .name ()};")
            except Exception :
                pass 
            try :
                self ._recompose ()
                self ._rescale ()
            except Exception :
                pass 

    def _load_image (self ,path :str ):
        pix =None 
        last_err =""
        try :
            from PIL import Image 
            try :
                import PIL .DdsImagePlugin 
            except Exception :
                pass 
            try :
                import pillow_bc7 
            except Exception :
                pass 
            im =Image .open (path )
            im .load ()
            im =im .convert ('RGBA')
            w ,h =im .size 

            try :
                self ._orig_pil =im .copy ()
            except Exception :
                self ._orig_pil =None 
            buf =im .tobytes ('raw','RGBA')
            qimage =QImage (buf ,w ,h ,QImage .Format_RGBA8888 )
            qimage =qimage .copy ()
            self ._orig_qimage =qimage 
            pix =QPixmap .fromImage (qimage )
        except Exception as e :
            last_err =str (e )
            pix =QPixmap (path )
        if pix is None or pix .isNull ():
            msg ="Could not load image"
            if last_err :
                msg =f"Could not load image: {last_err }"
            self .image_label .setText (msg )
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] {os.path .basename (path )} -> {msg }",err =True )
            except Exception :
                pass 
            self ._orig_pixmap =None 
            return 
        else :
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] Loaded {os.path .basename (path )} ({pix .width ()}x{pix .height ()})")
            except Exception :
                pass 
        self ._orig_pixmap =pix 
        self ._recompose ()
        self ._rescale ()
        try :
            if not getattr (self ,'_did_fit',False ):
                QTimer .singleShot (0 ,self ._fit_initial )
        except Exception :
            pass 

    def _fit_initial (self ):
        try :
            if not self ._orig_pixmap :
                return 
            vp =self .scroll .viewport ().size ()
            img_w =max (1 ,self ._orig_pixmap .width ())
            img_h =max (1 ,self ._orig_pixmap .height ())
            if vp .width ()>0 and vp .height ()>0 :
                scale_w =vp .width ()/img_w 
                scale_h =vp .height ()/img_h 
                new_scale =min (scale_w ,scale_h )
                new_scale =max (0.1 ,min (1.0 ,new_scale ))
                self ._scale =new_scale 
                self ._rescale ()
                self ._did_fit =True 
        except Exception :
            pass 

    def resizeEvent (self ,event ):
        try :
            super ().resizeEvent (event )
        except Exception :
            pass 
        try :
            side =min (self .width (),self .height ())
            if self .width ()!=self .height ():
                self .resize (side ,side )
            if hasattr (self ,'size_spin'):
                self .size_spin .blockSignals (True )
                self .size_spin .setValue (side )
                self .size_spin .blockSignals (False )
        except Exception :
            pass 
        self ._rescale ()

    def wheelEvent (self ,event ):
        try :
            delta =0 
            if hasattr (event ,'angleDelta'):
                delta =event .angleDelta ().y ()
            elif hasattr (event ,'delta'):
                delta =event .delta ()
            if delta ==0 :
                return 
            factor =1.25 if delta >0 else 0.8 
            new_scale =max (0.1 ,min (10.0 ,self ._scale *factor ))
            if abs (new_scale -self ._scale )>1e-3 :
                self ._scale =new_scale 
                try :
                    if callable (self ._log_fn ):
                        self ._log_fn (f"[DDS Preview] Zoom: {self ._scale :.2f}x")
                except Exception :
                    pass 
                self ._rescale ()
        except Exception :
            pass 

    def keyPressEvent (self ,event ):
        try :
            if event .key ()==Qt .Key_Space :
                self ._space_down =True 
                try :
                    self .scroll .viewport ().setCursor (Qt .OpenHandCursor if not self ._panning else Qt .ClosedHandCursor )
                except Exception :
                    pass 
                event .accept ()
                return 
        except Exception :
            pass 
        try :
            super ().keyPressEvent (event )
        except Exception :
            pass 

    def keyReleaseEvent (self ,event ):
        try :
            if event .key ()==Qt .Key_Space :
                self ._space_down =False 
                try :
                    if not self ._panning :
                        self .scroll .viewport ().setCursor (Qt .ArrowCursor )
                except Exception :
                    pass 
                event .accept ()
                return 
        except Exception :
            pass 
        try :
            super ().keyReleaseEvent (event )
        except Exception :
            pass 

    def eventFilter (self ,obj ,event ):
        try :
            if obj in (self .scroll .viewport (),self .image_label ):
                if event .type ()==QEvent .Wheel :
                    try :
                        delta =event .angleDelta ().y ()
                    except Exception :
                        delta =0 
                    if delta !=0 :
                        step =0.1 if delta >0 else -0.1 
                        new_scale =max (0.05 ,min (10.0 ,self ._scale +step ))
                        if abs (new_scale -self ._scale )>1e-6 :
                            self ._scale =new_scale 
                            self ._rescale ()
                            try :
                                if callable (self ._log_fn ):
                                    self ._log_fn (f"[DDS Preview] Zoom {self ._scale :.2f}x")
                            except Exception :
                                pass 
                    event .accept ()
                    return True 
                if event .type ()==QEvent .MouseButtonPress and (event .button ()in (Qt .LeftButton ,Qt .MidButton )):
                    self ._panning =True 
                    self ._pan_start_pos =event .pos ()
                    self ._pan_start_global =event .globalPos ()
                    self ._h0 =self .scroll .horizontalScrollBar ().value ()
                    self ._v0 =self .scroll .verticalScrollBar ().value ()
                    try :
                        self .scroll .viewport ().setCursor (Qt .ClosedHandCursor )
                    except Exception :
                        pass 
                    return True 
                elif event .type ()==QEvent .MouseMove and self ._panning :
                    delta =event .globalPos ()-self ._pan_start_global 
                    self .scroll .horizontalScrollBar ().setValue (self ._h0 -delta .x ())
                    self .scroll .verticalScrollBar ().setValue (self ._v0 -delta .y ())
                    return True 
                elif event .type ()==QEvent .MouseButtonRelease and (event .button ()in (Qt .LeftButton ,Qt .MidButton )):
                    self ._panning =False 
                    try :
                        self .scroll .viewport ().setCursor (Qt .OpenHandCursor if getattr (self ,'_space_down',False )else Qt .ArrowCursor )
                    except Exception :
                        pass 
                    return True 
        except Exception :
            pass 
        return super ().eventFilter (obj ,event )

    def _rescale (self ):
        base_pix =self ._composited_pixmap if getattr (self ,'_composited_pixmap',None )else getattr (self ,'_orig_pixmap',None )
        if not base_pix :
            return 
        base_w =base_pix .width ()
        base_h =base_pix .height ()
        target_w =max (1 ,int (base_w *self ._scale ))
        target_h =max (1 ,int (base_h *self ._scale ))
        scaled =base_pix .scaled (target_w ,target_h ,Qt .KeepAspectRatio ,Qt .SmoothTransformation )
        self .image_label .setPixmap (scaled )
        self .image_label .resize (scaled .size ())

    def _populate_bg_combo (self ):
        try :
            self .bg_combo .clear ()
            self .bg_combo .addItem ("White (no image)",userData =None )
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] CWD: {os .getcwd ()}")
            except Exception :
                pass 
            bg_dir =self ._find_bg_dir ()
            if not bg_dir or not os.path .isdir (bg_dir ):
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] Background folder not found: Data/DDS",True )
                return 
            else :
                try :
                    if callable (self ._log_fn ):
                        self ._log_fn (f"[DDS Preview] Background dir: {bg_dir }")
                except Exception :
                    pass 
            norm_paths =set ()
            for ext in ("*.dds","*.DDS","*.png","*.jpg","*.jpeg","*.PNG","*.JPG","*.JPEG"):
                for f in glob .glob (os.path .join (bg_dir ,ext )):
                    try :
                        norm_paths .add (os.path .normcase (os.path .abspath (f )))
                    except Exception :
                        norm_paths .add (f )
            files =sorted (norm_paths ,key =lambda p :os.path .basename (p ).lower ())
            for f in files :
                self .bg_combo .addItem (os.path .basename (f ),userData =f )
            if callable (self ._log_fn ):
                self ._log_fn (f"[DDS Preview] Backgrounds found: {len (files )} in {bg_dir }")

            try :
                sel =self ._read_bg_selection_from_ini ()
                if sel is not None :
                    if sel .lower ()in ("non","none"):
                        self .bg_combo .setCurrentIndex (0 )
                    else :

                        base =os.path .basename (sel )
                        for i in range (self .bg_combo .count ()):
                            if self .bg_combo .itemText (i ).lower ()==base .lower ():
                                self .bg_combo .setCurrentIndex (i )
                                break 
            except Exception :
                pass 
        except Exception :
            pass 

    def _find_bg_dir (self ):
        try :
            candidates =[]

            try :
                candidates .append (os.path .join (os .getcwd (),'Data','DDS'))
            except Exception :
                pass 

            try :
                base =BASE_PATH
                cur =base 
                for _ in range (5 ):
                    candidates .append (os.path .join (cur ,'Data','DDS'))
                    nxt =os.path .dirname (cur )
                    if not nxt or nxt ==cur :
                        break 
                    cur =nxt 
            except Exception :
                pass 

            try :
                import sys 
                exe_dir =os.path .dirname (sys .executable )
                cur =exe_dir 
                for _ in range (5 ):
                    candidates .append (os.path .join (cur ,'Data','DDS'))
                    nxt =os.path .dirname (cur )
                    if not nxt or nxt ==cur :
                        break 
                    cur =nxt 
            except Exception :
                pass 

            try :
                import sys 
                argv0_dir =os.path .dirname (os.path .abspath (sys .argv [0 ]))
                cur =argv0_dir 
                for _ in range (5 ):
                    candidates .append (os.path .join (cur ,'Data','DDS'))
                    nxt =os.path .dirname (cur )
                    if not nxt or nxt ==cur :
                        break 
                    cur =nxt 
            except Exception :
                pass 

            for c in candidates :
                if c and os.path .isdir (c ):
                    return c 

            try :
                if callable (self ._log_fn ):
                    self ._log_fn ("[DDS Preview] Background folder not found. Checked: "+" | ".join (candidates ),True )
            except Exception :
                pass 
        except Exception :
            pass 
        return None 


    def _select_ini_path (self )->str :
        try :
            d =self ._find_bg_dir ()
            if d :
                return os.path .join (d ,'Select.ini')
        except Exception :
            pass 
        return None 

    def _read_bg_selection_from_ini (self ):
        """Devuelve nombre de archivo DDS (o 'non') si existe en Select.ini.
        Soporta formato simple ([DDS]\n<valor>) o clave 'selected' en la sección.
        """
        p =self ._select_ini_path ()
        if not p or not os.path .isfile (p ):
            return None 
        try :
            if callable (self ._log_fn ):
                self ._log_fn (f"[DDS Preview] Reading Select.ini: {p }")
        except Exception :
            pass 

        try :

            cp =configparser .ConfigParser ()
            cp .optionxform =str 
            cp .read (p ,encoding ='utf-8')
            if cp .has_section ('DDS'):

                if cp .has_option ('DDS','selected'):
                    return cp .get ('DDS','selected').strip ()
        except Exception :
            pass 

        try :
            with open (p ,'r',encoding ='utf-8',errors ='ignore')as f :
                lines =f .readlines ()
            in_sec =False 
            for ln in lines :
                s =ln .strip ()
                if not s or s .startswith (';')or s .startswith ('#'):
                    continue 
                if s .startswith ('[')and s .endswith (']'):
                    in_sec =(s [1 :-1 ].strip ().lower ()=='dds')
                    continue 
                if in_sec :

                    if '='in s :
                        s =s .split ('=',1 )[1 ].strip ()
                    return s 
        except Exception :
            pass 
        return None 

    def _write_bg_selection_to_ini (self ):
        """Escribe la selección actual a Select.ini (selected=<archivo>|non)."""
        p =self ._select_ini_path ()
        if not p :
            return 
        try :
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] Writing Select.ini: {p }")
            except Exception :
                pass 
            sel =None 
            try :
                data =self .bg_combo .currentData ()
                sel ='non'if not data else os.path .basename (str (data ))
            except Exception :
                sel ='non'

            try :
                os .makedirs (os.path .dirname (p ),exist_ok =True )
            except Exception :
                pass 
            cp =configparser .ConfigParser ()
            cp .optionxform =str 
            cp ['DDS']={'selected':sel }
            with open (p ,'w',encoding ='utf-8')as f :
                cp .write (f )
        except Exception :
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] Could not write Select.ini",True )
            except Exception :
                pass 

    def _on_bg_changed (self ,idx ):
        try :
            self ._recompose ()
            self ._rescale ()

            try :
                self ._write_bg_selection_to_ini ()
            except Exception :
                pass 
        except Exception :
            pass 

    def _load_dds_qimage (self ,path :str ):
        try :
            from PIL import Image 
            try :
                import PIL .DdsImagePlugin 
            except Exception :
                pass 
            try :
                import pillow_bc7 
            except Exception :
                pass 
            im =Image .open (path )
            im .load ()
            im =im .convert ('RGBA')
            w ,h =im .size 
            buf =im .tobytes ('raw','RGBA')
            qimg =QImage (buf ,w ,h ,QImage .Format_RGBA8888 )
            return qimg .copy ()
        except Exception as e :
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] Background '{os.path .basename (path )}' failed to load: {e }",True )
            except Exception :
                pass 
            return None 

    def _recompose (self ):
        try :

            fg_qimg =None 
            try :
                if getattr (self ,'_orig_pil',None )is not None :
                    from PIL import ImageEnhance 
                    im =self ._orig_pil 
                    c =float (getattr (self ,'_fg_contrast',1.0 )or 1.0 )
                    if abs (c -1.0 )>1e-6 :
                        im =ImageEnhance .Contrast (im ).enhance (c )
                    fg_qimg =self ._pil_to_qimage (im )
            except Exception :
                fg_qimg =None 
            if fg_qimg is None :
                fg_qimg =getattr (self ,'_orig_qimage',None )
            if fg_qimg is None :
                self ._composited_pixmap =getattr (self ,'_orig_pixmap',None )
                return 

            canvas =QImage (fg_qimg .size (),QImage .Format_RGBA8888 )


            bg_path =None 
            try :
                bg_path =self .bg_combo .currentData ()
            except Exception :
                bg_path =None 
            bg_img_q =None 
            if bg_path :
                try :
                    from PIL import Image ,ImageEnhance 
                    bg_pil =Image .open (bg_path )
                    bg_pil .load ()
                    bg_pil =bg_pil .convert ('RGBA')
                    c_bg =float (getattr (self ,'_bg_contrast',1.0 )or 1.0 )
                    if abs (c_bg -1.0 )>1e-6 :
                        bg_pil =ImageEnhance .Contrast (bg_pil ).enhance (c_bg )
                    bg_img_q =self ._pil_to_qimage (bg_pil )
                except Exception :
                    bg_img_q =self ._load_dds_qimage (bg_path )

            painter =QPainter (canvas )
            painter .fillRect (canvas .rect (),self ._bg )
            if bg_img_q is not None and not bg_img_q .isNull ():
                bg_scaled =bg_img_q .scaled (fg_qimg .width (),fg_qimg .height (),Qt .IgnoreAspectRatio ,Qt .SmoothTransformation )
                painter .drawImage (0 ,0 ,bg_scaled )
            painter .setCompositionMode (QPainter .CompositionMode_SourceOver )
            painter .drawImage (0 ,0 ,fg_qimg )
            painter .end ()

            self ._composited_pixmap =QPixmap .fromImage (canvas )
        except Exception :
            self ._composited_pixmap =getattr (self ,'_orig_pixmap',None )

    def _fit_to_window (self ):
        try :
            if not getattr (self ,'_orig_pixmap',None ):
                return 
            vp =self .scroll .viewport ().size ()
            if vp .width ()<=0 or vp .height ()<=0 :
                return 
            img_w =max (1 ,self ._orig_pixmap .width ())
            img_h =max (1 ,self ._orig_pixmap .height ())
            scale_w =vp .width ()/img_w 
            scale_h =vp .height ()/img_h 
            new_scale =min (scale_w ,scale_h )
            self ._scale =max (0.05 ,min (10.0 ,new_scale ))
            self ._rescale ()
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] Fit to window, zoom {self ._scale :.2f}x")
            except Exception :
                pass 
        except Exception :
            pass 

    def _set_zoom (self ,z :float ):
        try :
            self ._scale =max (0.05 ,min (10.0 ,float (z )))
            self ._rescale ()
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] Zoom {self ._scale :.2f}x")
            except Exception :
                pass 
        except Exception :
            pass 

    def _on_fg_slider_changed (self ,value :int ):
        try :
            self ._fg_contrast =max (0.2 ,min (3.0 ,float (value )/100.0 ))
            if hasattr (self ,'fg_val'):
                try :
                    self .fg_val .setText (f"{self ._fg_contrast :.2f}x")
                except Exception :
                    pass 
            self ._recompose ()
            self ._rescale ()
        except Exception :
            pass 

    def _on_bg_slider_changed (self ,value :int ):
        try :
            self ._bg_contrast =max (0.2 ,min (3.0 ,float (value )/100.0 ))
            if hasattr (self ,'bg_val'):
                try :
                    self .bg_val .setText (f"{self ._bg_contrast :.2f}x")
                except Exception :
                    pass 
            self ._recompose ()
            self ._rescale ()
        except Exception :
            pass 


class BackupManagerWindow (QDialog ):
    def __init__ (self ,psc_path :str ,parent =None ,log_fn =None ):
        super ().__init__ (parent )
        self ._psc_path =psc_path 
        self ._log_fn =log_fn 

        try :
            self ._base_name =os.path .splitext (os.path .basename (psc_path ))[0 ]
            self ._ext =os.path .splitext (psc_path )[1 ].lower ()or '.psc'
        except Exception :
            self ._base_name ="Script"
            self ._ext ='.psc'
        try :
            self .setWindowTitle (f"Backups — {self ._base_name }")
        except Exception :
            self .setWindowTitle ("Backups")
        try :
            self .resize (700 ,500 )
        except Exception :
            pass 


        try :
            self .setStyleSheet (
            """
                QDialog {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                  stop:0 rgba(35,35,45,255), stop:1 rgba(75,75,85,255));
                }
                QListWidget { background:#1A1A1C; color:#E0FFE0; border:1px solid #3A3A3F; }
                """
            )
        except Exception :
            pass 
        try :
            self .setModal (False )
            self .setWindowModality (Qt .NonModal )
        except Exception :
            pass 

        try :
            lay =QVBoxLayout (self )
            lay .setContentsMargins (8 ,8 ,8 ,8 )
            lay .setSpacing (8 )
            title =QLabel (f"Backups for {self ._base_name }")
            title .setAlignment (Qt .AlignCenter )
            title .setStyleSheet ("font-size: 15px; font-weight: bold; color: #66FF66;")
            lay .addWidget (title )

            self .listw =QListWidget ()
            self .listw .setStyleSheet ("QListWidget { background:#1A1A1C; color:#FFFFFF; border:1px solid #3A3A3F; }")
            lay .addWidget (self .listw ,1 )

            btns =QHBoxLayout ()
            self .btn_create =QPushButton ("Create backup now")
            self .btn_restore =QPushButton ("Restore selected")
            self .btn_open =QPushButton ("Open folder")
            self .btn_close =QPushButton ("Close")
            for b in (self .btn_create ,self .btn_restore ,self .btn_open ,self .btn_close ):
                try :
                    b .setStyleSheet ("QPushButton { background: rgba(38,38,44,0.78); color:#E0E0E0; border:1px solid rgba(90,90,95,0.70); border-radius:4px; padding:6px 10px; } QPushButton:hover { background: rgba(62,62,68,0.85); }")
                except Exception :
                    pass 
            btns .addWidget (self .btn_create )
            btns .addWidget (self .btn_restore )
            btns .addStretch (1 )
            btns .addWidget (self .btn_open )
            btns .addWidget (self .btn_close )
            lay .addLayout (btns )

            self .btn_close .clicked .connect (self .close )
            self .btn_open .clicked .connect (self ._open_folder )
            self .btn_create .clicked .connect (self ._create_backup )
            self .btn_restore .clicked .connect (self ._restore_selected )

            self ._refresh_list ()
        except Exception as e :
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[Backups] Init error: {e }",True )
            except Exception :
                pass 

    def _backup_dir (self )->str :
        src_dir =os.path .dirname (self ._psc_path )

        return os.path .join (src_dir ,'Backups')

    def _refresh_list (self ):
        try :
            self .listw .clear ()
            bdir =self ._backup_dir ()
            files =[]
            if os.path .isdir (bdir ):
                for f in os .listdir (bdir ):
                    if f .lower ().endswith (self ._ext ):
                        files .append (os.path .join (bdir ,f ))
            def _safe_mtime (p ):
                try :
                    return os.path .getmtime (p )
                except Exception :
                    return 0 

            import re 
            pat =None 
            try :
                pat =re .compile (r'_(\d{8})_(\d{6})'+re .escape (self ._ext )+r'$',re .IGNORECASE )
            except Exception :
                pat =None 
            def _sort_key (p ):
                try :
                    name =os.path .basename (p )
                    m =(pat .search (name )if pat else None )
                    if m :
                        ymd =m .group (1 )
                        hms =m .group (2 )
                        ts =int (ymd +hms )
                        return (0 ,-ts )
                except Exception :
                    pass 

                return (1 ,-int (_safe_mtime (p )))
            files .sort (key =_sort_key )
            for i ,f in enumerate (files ):
                item =QListWidgetItem (os.path .basename (f ))
                try :
                    if i ==0 :

                        item .setForeground (QBrush (QColor('#66FF66')))
                    else :

                        item .setForeground (QBrush (QColor('#FFFFFF')))
                except Exception :
                    pass 
                self .listw .addItem (item )
            if files :

                self .listw .setCurrentRow (0 )
        except Exception as e :
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[Backups] Error listing: {e }",True )
            except Exception :
                pass 

    def _ensure_dir (self ,path :str ):
        try :
            os .makedirs (path ,exist_ok =True )
        except Exception :
            pass 

    def _timestamp (self )->str :
        try :
            import datetime as _dt 
            return _dt .datetime .now ().strftime ('%Y%m%d_%H%M%S')
        except Exception :
            return str (int (time .time ()))

    def _create_backup (self ):
        try :
            if not os.path .isfile (self ._psc_path ):
                return 
            bdir =self ._backup_dir ()
            self ._ensure_dir (bdir )
            base_name =os.path .splitext (os.path .basename (self ._psc_path ))[0 ]
            out =os.path .join (bdir ,f"{base_name }_{self ._timestamp ()}{self ._ext }")
            shutil .copy2 (self ._psc_path ,out )
            self ._refresh_list ()
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[Backups] Created: {out }")
            except Exception :
                pass 
            # Blue message in parent tab terminal confirming backup creation
            try :
                parent =self .parent ()
                if parent is not None and hasattr (parent ,'output_terminal')and parent .output_terminal is not None :
                    cur =parent .output_terminal .textColor ()
                    parent .output_terminal .setTextColor (QColor('#00BFFF'))
                    parent .output_terminal .append ("A BACKUP HAS BEEN CREATED OF THE PSC")
                    parent .output_terminal .setTextColor (cur )
            except Exception :
                pass 
        except Exception as e :
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[Backups] Error creating: {e }",True )
            except Exception :
                pass 

    def _selected_backup_path (self )->str :
        try :
            row =self .listw .currentRow ()
            if row is None or row <0 :
                return None 
            it =self .listw .item (row )
            if it is None :
                return None 
            name =it .text ()
            return os.path .join (self ._backup_dir (),name )
        except Exception :
            return None 

    def _restore_selected (self ):
        try :
            src =self ._selected_backup_path ()
            if not src or not os.path .isfile (src ):
                return 
            shutil .copy2 (src ,self ._psc_path )
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[Backups] Restored to: {self ._psc_path }")
            except Exception :
                pass 

            try :
                parent =self .parent ()
                if parent is not None and hasattr (parent ,'_load_json_file'):
                    parent ._load_json_file (self ._psc_path )
            except Exception :
                pass 
        except Exception as e :
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[Backups] Error restoring: {e }",True )
            except Exception :
                pass 

    def _open_folder (self ):
        try :
            bdir =self ._backup_dir ()
            self ._ensure_dir (bdir )
            try :
                os .startfile (bdir )
            except Exception :
                subprocess .Popen (['explorer',bdir ])
        except Exception :
            pass 

    def _choose_bg_color (self ):
        col =QColorDialog .getColor (self ._bg ,self ,"Choose background color")
        if col .isValid ():
            self ._bg =col 
            self .image_label .setStyleSheet (f"background-color: {col .name ()};")
            self ._recompose ()
            self ._rescale ()

    def _load_image (self ,path :str ):
        pix =None 
        last_err =""
        try :
            from PIL import Image 

            try :
                import PIL .DdsImagePlugin 
            except Exception :
                pass 

            try :
                import pillow_bc7 
            except Exception :
                pass 
            im =Image .open (path )

            im .load ()

            im =im .convert ('RGBA')
            w ,h =im .size 

            self ._orig_pil =im .copy ()

            buf =im .tobytes ('raw','RGBA')
            qimage =QImage (buf ,w ,h ,QImage .Format_RGBA8888 )

            qimage =qimage .copy ()
            self ._orig_qimage =qimage 
            pix =QPixmap .fromImage (qimage )
        except Exception as e :
            last_err =str (e )

            pix =QPixmap (path )

        if pix is None or pix .isNull ():
            msg ="Could not load image"
            if last_err :
                msg =f"Could not load image: {last_err }"
            self .image_label .setText (msg )

            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] {os.path .basename (path )} -> {msg }",err =True )
            except Exception :
                pass 
            self ._orig_pixmap =None 
            return 
        else :
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] Loaded {os.path .basename (path )} ({pix .width ()}x{pix .height ()})")
            except Exception :
                pass 
        self ._orig_pixmap =pix 

        self ._recompose ()
        self ._rescale ()

        try :
            if not self ._did_fit :
                QTimer .singleShot (0 ,self ._fit_initial )
        except Exception :
            pass 

    def _fit_initial (self ):
        try :
            if not self ._orig_pixmap :
                return 
            vp =self .scroll .viewport ().size ()
            img_w =max (1 ,self ._orig_pixmap .width ())
            img_h =max (1 ,self ._orig_pixmap .height ())
            if vp .width ()>0 and vp .height ()>0 :
                scale_w =vp .width ()/img_w 
                scale_h =vp .height ()/img_h 
                new_scale =min (scale_w ,scale_h )

                new_scale =max (0.1 ,min (1.0 ,new_scale ))
                self ._scale =new_scale 
                self ._rescale ()
                self ._did_fit =True 
        except Exception :
            pass 

    def resizeEvent (self ,event ):
        try :
            super ().resizeEvent (event )
        except Exception :
            pass 

        try :
            side =min (self .width (),self .height ())
            if self .width ()!=self .height ():
                self .resize (side ,side )

            if hasattr (self ,'size_spin'):
                self .size_spin .blockSignals (True )
                self .size_spin .setValue (side )
                self .size_spin .blockSignals (False )
        except Exception :
            pass 

        try :

            if hasattr (self ,'_rescale'):
                self ._rescale ()
        except Exception :

            pass 

    def wheelEvent (self ,event ):
        try :
            delta =0 
            if hasattr (event ,'angleDelta'):
                delta =event .angleDelta ().y ()
            elif hasattr (event ,'delta'):
                delta =event .delta ()
            if delta ==0 :
                return 
            factor =1.25 if delta >0 else 0.8 
            new_scale =max (0.1 ,min (10.0 ,self ._scale *factor ))
            if abs (new_scale -self ._scale )>1e-3 :
                self ._scale =new_scale 

                try :
                    if callable (self ._log_fn ):
                        self ._log_fn (f"[DDS Preview] Zoom: {self ._scale :.2f}x")
                except Exception :
                    pass 
                self ._rescale ()
        except Exception :
            pass 

    def keyPressEvent (self ,event ):
        try :
            if event .key ()==Qt .Key_Space :
                self ._space_down =True 
                try :
                    self .scroll .viewport ().setCursor (Qt .OpenHandCursor if not self ._panning else Qt .ClosedHandCursor )
                except Exception :
                    pass 
                event .accept ()
                return 
        except Exception :
            pass 
        try :
            super ().keyPressEvent (event )
        except Exception :
            pass 

    def keyReleaseEvent (self ,event ):
        try :
            if event .key ()==Qt .Key_Space :
                self ._space_down =False 
                try :
                    if not self ._panning :
                        self .scroll .viewport ().setCursor (Qt .ArrowCursor )
                except Exception :
                    pass 
                event .accept ()
                return 
        except Exception :
            pass 
        try :
            super ().keyReleaseEvent (event )
        except Exception :
            pass 

    def eventFilter (self ,obj ,event ):
        try :
            if obj in (self .scroll .viewport (),self .image_label ):

                if event .type ()==QEvent .Wheel :
                    try :
                        delta =event .angleDelta ().y ()
                    except Exception :
                        delta =0 
                    if delta !=0 :
                        step =0.1 if delta >0 else -0.1 
                        new_scale =max (0.05 ,min (10.0 ,self ._scale +step ))
                        if abs (new_scale -self ._scale )>1e-6 :
                            self ._scale =new_scale 
                            self ._rescale ()
                            try :
                                if callable (self ._log_fn ):
                                    self ._log_fn (f"[DDS Preview] Zoom {self ._scale :.2f}x")
                            except Exception :
                                pass 
                    event .accept ()
                    return True 
                if event .type ()==QEvent .MouseButtonPress and (event .button ()in (Qt .LeftButton ,Qt .MidButton )):
                    self ._panning =True 
                    self ._pan_start_pos =event .pos ()
                    self ._pan_start_global =event .globalPos ()
                    self ._h0 =self .scroll .horizontalScrollBar ().value ()
                    self ._v0 =self .scroll .verticalScrollBar ().value ()
                    try :
                        self .scroll .viewport ().setCursor (Qt .ClosedHandCursor )
                    except Exception :
                        pass 
                    return True 
                elif event .type ()==QEvent .MouseMove and self ._panning :

                    delta =event .globalPos ()-self ._pan_start_global 
                    self .scroll .horizontalScrollBar ().setValue (self ._h0 -delta .x ())
                    self .scroll .verticalScrollBar ().setValue (self ._v0 -delta .y ())
                    return True 
                elif event .type ()==QEvent .MouseButtonRelease and (event .button ()in (Qt .LeftButton ,Qt .MidButton )):
                    self ._panning =False 
                    try :
                        self .scroll .viewport ().setCursor (Qt .OpenHandCursor if getattr (self ,'_space_down',False )else Qt .ArrowCursor )
                    except Exception :
                        pass 
                    return True 
        except Exception :
            pass 
        return super ().eventFilter (obj ,event )

    def _rescale (self ):

        base_pix =self ._composited_pixmap if self ._composited_pixmap else self ._orig_pixmap 
        if not base_pix :
            return 

        base_w =base_pix .width ()
        base_h =base_pix .height ()
        target_w =max (1 ,int (base_w *self ._scale ))
        target_h =max (1 ,int (base_h *self ._scale ))
        scaled =base_pix .scaled (target_w ,target_h ,Qt .KeepAspectRatio ,Qt .SmoothTransformation )
        self .image_label .setPixmap (scaled )
        self .image_label .resize (scaled .size ())

    def _populate_bg_combo (self ):
        try :
            self .bg_combo .clear ()
            self .bg_combo .addItem ("White (no image)",userData =None )
            bg_dir =self ._find_bg_dir ()
            if not bg_dir or not os.path .isdir (bg_dir ):
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] Background folder not found: Data/DDS",True )
                return 

            norm_paths =set ()
            for ext in ("*.dds","*.DDS"):
                for f in glob .glob (os.path .join (bg_dir ,ext )):
                    try :
                        norm_paths .add (os.path .normcase (os.path .abspath (f )))
                    except Exception :
                        norm_paths .add (f )
            files =sorted (norm_paths ,key =lambda p :os.path .basename (p ).lower ())
            for f in files :
                self .bg_combo .addItem (os.path .basename (f ),userData =f )
            if callable (self ._log_fn ):
                self ._log_fn (f"[DDS Preview] Backgrounds found: {len (files )} in {bg_dir }")
        except Exception :
            pass 

    def _find_bg_dir (self ):

        try :
            candidates =[]
            try :
                base =BASE_PATH
                candidates .append (os.path .join (base ,'Data','DDS'))
            except Exception :
                pass 
            try :
                candidates .append (os.path .join (os .getcwd (),'Data','DDS'))
            except Exception :
                pass 
            for c in candidates :
                if c and os.path .isdir (c ):
                    return c 
        except Exception :
            pass 
        return None 

    def _on_bg_changed (self ,idx ):
        try :

            try :
                self ._bg_cache_path =self .bg_combo .currentData ()
                self ._bg_cache_pil =None 
            except Exception :
                self ._bg_cache_path =None 
                self ._bg_cache_pil =None 
            self ._recompose ()
            self ._rescale ()
        except Exception :
            pass 

    def _load_dds_qimage (self ,path :str ):

        try :
            from PIL import Image 
            try :
                import PIL .DdsImagePlugin 
            except Exception :
                pass 
            try :
                import pillow_bc7 
            except Exception :
                pass 
            im =Image .open (path )
            im .load ()
            im =im .convert ('RGBA')
            w ,h =im .size 
            buf =im .tobytes ('raw','RGBA')
            qimg =QImage (buf ,w ,h ,QImage .Format_RGBA8888 )
            return qimg .copy ()
        except Exception as e :
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] Background '{os.path .basename (path )}' failed to load: {e }",True )
            except Exception :
                pass 
            return None 

    def _recompose (self ):

        try :
            if self ._orig_qimage is None and self ._orig_pil is None :
                self ._composited_pixmap =self ._orig_pixmap 
                return 

            fg_qimg =None 
            if self ._orig_pil is not None :
                try :
                    from PIL import ImageEnhance 
                    im =self ._orig_pil 
                    if abs (float (self ._fg_contrast )-1.0 )>1e-6 :
                        im =ImageEnhance .Contrast (im ).enhance (float (self ._fg_contrast ))
                    fg_qimg =self ._pil_to_qimage (im )
                except Exception :
                    fg_qimg =self ._orig_qimage 
            else :
                fg_qimg =self ._orig_qimage 

            if fg_qimg is None :
                self ._composited_pixmap =self ._orig_pixmap 
                return 

            canvas =QImage (fg_qimg .size (),QImage .Format_RGBA8888 )

            bg_path =None 
            try :
                bg_path =self .bg_combo .currentData ()
            except Exception :
                bg_path =None 
            if bg_path :

                try :
                    from PIL import Image ,ImageEnhance 
                    if self ._bg_cache_path !=bg_path or self ._bg_cache_pil is None :
                        bg_pil =Image .open (bg_path )
                        bg_pil .load ()
                        bg_pil =bg_pil .convert ('RGBA')
                        self ._bg_cache_path =bg_path 
                        self ._bg_cache_pil =bg_pil 
                    else :
                        bg_pil =self ._bg_cache_pil 
                    if abs (float (self ._bg_contrast )-1.0 )>1e-6 :
                        bg_pil_eff =ImageEnhance .Contrast (bg_pil ).enhance (float (self ._bg_contrast ))
                    else :
                        bg_pil_eff =bg_pil 
                    bg_qimg =self ._pil_to_qimage (bg_pil_eff )
                except Exception :
                    bg_qimg =self ._load_dds_qimage (bg_path )
                if bg_qimg is not None and not bg_qimg .isNull ():
                    bg_scaled =bg_qimg .scaled (fg_qimg .width (),fg_qimg .height (),Qt .IgnoreAspectRatio ,Qt .SmoothTransformation )
                    painter =QPainter (canvas )
                    painter .fillRect (canvas .rect (),self ._bg )
                    painter .drawImage (0 ,0 ,bg_scaled )
                    painter .setCompositionMode (QPainter .CompositionMode_SourceOver )
                    painter .drawImage (0 ,0 ,fg_qimg )
                    painter .end ()
                else :

                    painter =QPainter (canvas )
                    painter .fillRect (canvas .rect (),self ._bg )
                    painter .drawImage (0 ,0 ,fg_qimg )
                    painter .end ()
            else :

                painter =QPainter (canvas )
                painter .fillRect (canvas .rect (),self ._bg )
                painter .drawImage (0 ,0 ,fg_qimg )
                painter .end ()
            self ._composited_pixmap =QPixmap .fromImage (canvas )
        except Exception :

            self ._composited_pixmap =self ._orig_pixmap 

    def _pil_to_qimage (self ,im ):
        try :
            im =im .convert ('RGBA')
            w ,h =im .size 
            buf =im .tobytes ('raw','RGBA')
            qimg =QImage (buf ,w ,h ,QImage .Format_RGBA8888 )
            return qimg .copy ()
        except Exception :
            return None 

    def _on_fg_contrast_changed (self ,value ):
        try :
            self ._fg_contrast =float (value )
            self ._recompose ()
            self ._rescale ()
        except Exception :
            pass 

    def _on_bg_contrast_changed (self ,value ):
        try :
            self ._bg_contrast =float (value )
            self ._recompose ()
            self ._rescale ()
        except Exception :
            pass 

    def _on_fg_slider_changed (self ,v :int ):
        try :
            self ._fg_contrast =max (0.2 ,min (3.0 ,v /100.0 ))
            try :
                self .fg_val .setText (f"{self ._fg_contrast :.2f}x")
            except Exception :
                pass 
            self ._recompose ()
            self ._rescale ()
        except Exception :
            pass 

    def _on_bg_slider_changed (self ,v :int ):
        try :
            self ._bg_contrast =max (0.2 ,min (3.0 ,v /100.0 ))
            try :
                self .bg_val .setText (f"{self ._bg_contrast :.2f}x")
            except Exception :
                pass 
            self ._recompose ()
            self ._rescale ()
        except Exception :
            pass 

    def _fit_to_window (self ):
        try :
            if not self ._orig_pixmap :
                return 
            vp =self .scroll .viewport ().size ()
            if vp .width ()<=0 or vp .height ()<=0 :
                return 
            img_w =max (1 ,self ._orig_pixmap .width ())
            img_h =max (1 ,self ._orig_pixmap .height ())
            scale_w =vp .width ()/img_w 
            scale_h =vp .height ()/img_h 
            new_scale =min (scale_w ,scale_h )

            self ._scale =max (0.05 ,min (10.0 ,new_scale ))
            self ._rescale ()
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] Fit to window, zoom {self ._scale :.2f}x")
            except Exception :
                pass 
        except Exception :
            pass 

    def _set_zoom (self ,z :float ):
        try :
            self ._scale =max (0.05 ,min (10.0 ,float (z )))
            self ._rescale ()
            try :
                if callable (self ._log_fn ):
                    self ._log_fn (f"[DDS Preview] Zoom {self ._scale :.2f}x")
            except Exception :
                pass 
        except Exception :
            pass 

class STCreatorTab (QWidget ):
    """Create from scratch ST: UI skeleton to create a SlaveTats mod from zero."""
    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        try :
            self .setStyleSheet ("background: transparent;")
        except Exception :
            pass 

        self ._section_override =None 

        self ._json_path =None 

        self ._json_exported =False 

        self ._dds_watcher =None 
        self ._build_ui ()

    def _build_ui (self ):
        lay =QVBoxLayout (self )
        lay .setContentsMargins (8 ,8 ,8 ,8 )
        lay .setSpacing (8 )

        title =QLabel ("CREATE FROM SCRATCH AND MODIFY — SLAVETATS")
        title .setAlignment (Qt .AlignCenter )
        title .setStyleSheet ("font-size: 16px; font-weight: bold; color: #66FF66;")
        lay .addWidget (title )

        subtitle =QLabel ("Configure the base data and create the initial ST mod structure")
        subtitle .setAlignment (Qt .AlignCenter )
        subtitle .setStyleSheet ("font-size: 12px; color: #CFCFCF;")
        lay .addWidget (subtitle )





        self .btn_select_out =QPushButton ("Open environment folder")
        try :
            self .btn_select_out .setCursor (Qt .PointingHandCursor )
        except Exception :
            pass 

        try :
            self .btn_select_out .setEnabled (False )
        except Exception :
            pass 
        try :
            self .btn_select_out .setToolTip ("Open the loaded JSON folder or the parent folder of the DDS folder")
        except Exception :
            pass 
        self .btn_select_out .clicked .connect (self ._open_env_folder )


        self .btn_select_dds =QPushButton ("DRAG AND DROP JSON OR DDS FOLDER")
        try :
            self .btn_select_dds .setCursor (Qt .PointingHandCursor )
        except Exception :
            pass 
        self .btn_select_dds .setMinimumHeight (40 )
        try :
            self .btn_select_dds .setSizePolicy (QSizePolicy .Expanding ,QSizePolicy .Fixed )
        except Exception :
            pass 
        self .btn_select_dds .clicked .connect (self ._choose_dds_folder )

        try :
            self .btn_select_dds .setStyleSheet (self .btn_style_green )
        except Exception :
            pass 
        try :
            self .btn_select_dds .setToolTip ("Drag and drop the folder that contains your DDS files to start creating your mod, or drag an existing JSON to continue and add more DDS overlays")
        except Exception :
            pass 
        lay .addWidget (self .btn_select_dds )




        self .scroll =QScrollArea ()
        self .scroll .setWidgetResizable (True )
        self .scroll .setStyleSheet ("QScrollArea { background: transparent; }")
        self .list_container =QWidget ()

        self .list_container .setStyleSheet ("background-color: rgba(40,40,48,180); border: 1px solid #444; border-radius: 6px;")
        self .list_layout =QVBoxLayout (self .list_container )
        self .list_layout .setContentsMargins (2 ,2 ,2 ,2 )
        self .list_layout .setSpacing (6 )

        try :
            self ._reset_table ()
        except Exception :
            pass 
        self .scroll .setWidget (self .list_container )
        lay .addWidget (self .scroll )


        try :
            self .setAcceptDrops (True )
        except Exception :
            pass 


        action_row =QHBoxLayout ()

        self .btn_style_gray =(
        "QPushButton {"
        " background: rgba(53,53,57,0.82);"
        " color: #E0E0E0;"
        " border: 1px solid rgba(90,90,95,0.70);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        "}"
        "QPushButton:hover { background: rgba(62,62,68,0.90); }"
        "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
        )

        # Ensure green style exists locally and apply it to the main selector now
        try :
            self .btn_style_green =(
            "QPushButton {"
            " background: rgba(76,175,80,0.25);"
            " color: #FFFFFF;"
            " border: 1px solid rgba(76,175,80,0.80);"
            " border-radius: 4px;"
            " padding: 6px 10px;"
            "}"
            "QPushButton:hover { background: rgba(76,175,80,0.35); }"
            "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
            )
            self .btn_select_dds .setStyleSheet (self .btn_style_green )
        except Exception :
            pass 

        # Define RM tab green and blue styles locally
        self .btn_style_green =(
        "QPushButton {"
        " background: rgba(76,175,80,0.25);"
        " color: #FFFFFF;"
        " border: 1px solid rgba(76,175,80,0.80);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        "}"
        "QPushButton:hover { background: rgba(76,175,80,0.35); }"
        "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
        )

        self .btn_style_blue =(
        "QPushButton {"
        " background: rgba(0, 188, 212, 0.35);"
        " color: #E0F7FA;"
        " border: 1px solid rgba(0, 188, 212, 0.70);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        "}"
        "QPushButton:hover { background: rgba(0, 188, 212, 0.55); }"
        "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
        )

        # Apply green to the main DDS selector now that styles exist
        try :
            self .btn_select_dds .setStyleSheet (self .btn_style_green )
        except Exception :
            pass 
        self .btn_style_green =(
        "QPushButton {"
        " background: rgba(76,175,80,0.25);"
        " color: #FFFFFF;"
        " border: 1px solid rgba(76,175,80,0.80);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        "}"
        "QPushButton:hover { background: rgba(76,175,80,0.35); }"
        "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
        )


        self .btn_style_blue =(
        "QPushButton {"
        " background: rgba(0, 188, 212, 0.35);"
        " color: #E0F7FA;"
        " border: 1px solid rgba(0, 188, 212, 0.70);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        "}"
        "QPushButton:hover { background: rgba(0, 188, 212, 0.55); }"
        "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
        )

        # Ensure 'Select DDS folder' is green from startup (styles are now defined)
        try :
            self .btn_select_dds .setStyleSheet (self .btn_style_green )
        except Exception :
            pass 

        # Ensure the main selector button is green now that RM styles are defined
        try :
            if hasattr (self ,'btn_select_dds') and self .btn_select_dds is not None :
                self .btn_select_dds .setStyleSheet (self .btn_style_green )
        except Exception :
            pass 

        # Reaplicar estilo verde ahora que los estilos ya están definidos
        try :
            if hasattr (self ,'btn_select_dds') and self .btn_select_dds is not None :
                self .btn_select_dds .setStyleSheet (self .btn_style_green )
        except Exception :
            pass 

        self .btn_refresh_st =QPushButton ("Clean All")
        try :
            self .btn_refresh_st .setCursor (Qt .PointingHandCursor )
            self .btn_refresh_st .setToolTip ("Clear and reset this tab")
        except Exception :
            pass 

        try :
            self .btn_refresh_st .setStyleSheet (self .btn_style_blue )
        except Exception :
            pass 
        self .btn_refresh_st .clicked .connect (self .refresh_tab )
        action_row .addWidget (self .btn_refresh_st )


        self .btn_backups =QPushButton ("Backups")
        try :
            self .btn_backups .setEnabled (False )
            self .btn_backups .setToolTip ("Manage JSON backups (create/restore)")
        except Exception :
            pass 
        self .btn_export_json =QPushButton ("Export JSON")

        self .btn_export_json .setEnabled (False )
        try :
            self .btn_export_json .setToolTip ("Export JSON with entries from the DDS files (it will be saved in the parent folder of the DDS directory)")
        except Exception :
            pass 
        self .btn_export_json .clicked .connect (self ._export_json )
        self .btn_example_json =QPushButton ("JSON example")

        self .btn_example_json .setEnabled (False )
        try :
            self .btn_example_json .setToolTip ("Show a JSON example in the terminal")
        except Exception :
            pass 
        self .btn_example_json .clicked .connect (self ._print_json_example )

        self .btn_create_mod =QPushButton ("Create Mod zip")
        self .btn_create_mod .setEnabled (False )
        try :
            self .btn_create_mod .setToolTip ("Create mod structure and package (requires a DDS folder and an exported JSON in this session)")
        except Exception :
            pass 
        self .btn_create_mod .clicked .connect (self ._create_mod_package )
        self .btn_clear_term =QPushButton ("Clear terminal")
        try :
            self .btn_clear_term .setToolTip ("Clear terminal output")
        except Exception :
            pass 
        self .btn_clear_term .clicked .connect (self ._clear_terminal )

        try :
            self .btn_clear_term .setStyleSheet (self .btn_style_blue )
        except Exception :
            pass 


        for b in (self .btn_backups ,self .btn_select_out ,self .btn_export_json ,self .btn_example_json ,self .btn_create_mod ):
            try :
                b .setStyleSheet (self .btn_style_gray )
            except Exception :
                pass 

        try :
            self .btn_select_dds .setStyleSheet (self .btn_style_green )
        except Exception :
            pass 

        try :
            self .btn_backups .clicked .connect (self ._on_backups_clicked )
        except Exception :
            pass 

        action_row .addWidget (self .btn_backups )
        action_row .addWidget (self .btn_select_out )
        action_row .addStretch (1 )
        action_row .addWidget (self .btn_example_json )
        action_row .addWidget (self .btn_export_json )
        action_row .addWidget (self .btn_create_mod )
        action_row .addWidget (self .btn_clear_term )
        lay .addLayout (action_row )


        lay .addWidget (QLabel ("Output:"))
        self .output_terminal =QTextEdit ()
        self .output_terminal .setReadOnly (True )
        self .output_terminal .setStyleSheet (
        "QTextEdit { background-color: #1A1A1C; color: #4CAF50; border: 1px solid #3A3A3F; border-radius: 4px; font-family: Consolas, 'Courier New', monospace; font-size: 12px; }"
        )
        lay .addWidget (self .output_terminal )

        self ._dest_dir =None 
        self ._dds_dir =None 
        self ._rows =[]

        self ._preview_windows =[]

        self ._backup_windows =[]


        try :
            self ._set_action_buttons_enabled (False )
        except Exception :
            pass 

    def refresh_tab (self ):
        """Resets the tab to its initial state."""
        try :
            self ._section_override =None 
            self ._json_path =None 
            self ._json_exported =False 
            self ._dds_dir =None 
            try :
                if hasattr (self ,'section_edit'):
                    self .section_edit .setText ("")
            except Exception :
                pass 
            self ._rows .clear ()

            try :
                if self ._dds_watcher is not None :

                    self ._dds_watcher .deleteLater ()
            except Exception :
                pass 
            self ._dds_watcher =None 


            for i in reversed (range (self .list_layout .count ())):
                item =self .list_layout .itemAt (i )
                if item is None :continue 
                w =item .widget ()
                if w is not None :
                    w .setParent (None )


            self ._reset_table ()

            self .output_terminal .clear ()
            self ._set_action_buttons_enabled (False )


            if hasattr (self ,'btn_backups'):
                self .btn_backups .setEnabled (False )
                self .btn_backups .setStyleSheet (self .btn_style_gray )

            for win in self ._preview_windows :
                win .close ()
            self ._preview_windows .clear ()

            self ._log ("ST Creator tab has been refreshed.")
        except Exception as e :
            self ._log (f"Error refreshing ST Creator tab: {e }",err =True )

    def _reset_table (self ):
        """Crea/reemplaza la tabla de datos con un QGridLayout y agrega el encabezado.
        Columnas: 0=File, 1=Ruta, 2=Section, 3=Area, 4=Name
        Stretches: 2,1,1,1,2
        """
        try :

            if hasattr (self ,'table_widget')and self .table_widget is not None :
                try :
                    self .table_widget .setParent (None )
                except Exception :
                    pass 

            self .table_widget =QWidget ()
            self .grid =QGridLayout (self .table_widget )
            self .grid .setContentsMargins (6 ,2 ,6 ,2 )
            self .grid .setHorizontalSpacing (8 )
            self .grid .setVerticalSpacing (4 )

            lblA =QLabel ("File");lblRuta =QLabel ("Path");lblD =QLabel ("Section");lblB =QLabel ("Area");lblC =QLabel ("Name")
            # Tooltips for column headers
            try :
                lblA .setToolTip ("DDS filename. Click a row to preview.")
                lblRuta .setToolTip ("Folder relative to Section. Double-click to open the folder.")
                lblD .setToolTip ("Overlay section. This will be the SlaveTats group name. You can split into groups by using different names, but I suggest using a single name.")
                lblB .setToolTip ("Body area where this overlay applies. Select it and it will be automatically organized in the JSON.")
                lblC .setToolTip ("Individual tattoo name. You can add the name and a short description.")
            except Exception :
                pass 
            for L in (lblA ,lblRuta ,lblD ,lblB ,lblC ):
                try :
                    L .setStyleSheet ("color:#D8D8D8;font-weight:600;")
                except Exception :
                    pass 
            try :
                lblA .setMinimumWidth (160 )
            except Exception :
                pass 

            self .grid .addWidget (lblA ,0 ,0 )
            self .grid .addWidget (lblRuta ,0 ,1 )
            self .grid .addWidget (lblD ,0 ,2 )
            self .grid .addWidget (lblB ,0 ,3 )
            self .grid .addWidget (lblC ,0 ,4 )

            try :
                self .grid .setColumnStretch (0 ,2 )
                self .grid .setColumnStretch (1 ,1 )
                self .grid .setColumnStretch (2 ,1 )
                self .grid .setColumnStretch (3 ,1 )
                self .grid .setColumnStretch (4 ,2 )
            except Exception :
                pass 

            self .list_layout .addWidget (self .table_widget )
            self ._grid_row =1 
        except Exception :
            pass 

    def _set_action_buttons_enabled (self ,on :bool ):
        """Habilita/Deshabilita botones dependientes de haber cargado una carpeta DDS
        y aplica el estilo verde cuando están habilitados, gris cuando no.
        No afecta al botón "Clear terminal".
        """
        try :
            targets =[]

            if hasattr (self ,'btn_select_out'):
                targets .append (self .btn_select_out )
            if hasattr (self ,'btn_export_json'):
                targets .append (self .btn_export_json )
            if hasattr (self ,'btn_example_json'):
                targets .append (self .btn_example_json )

            for btn in targets :
                try :
                    btn .setEnabled (on )
                    btn .setStyleSheet (self .btn_style_green if on else self .btn_style_gray )
                except Exception :
                    pass 
        except Exception :
            pass 


        try :
            if hasattr (self ,'btn_create_mod'):


                if getattr (self ,'_json_exported',False ):
                    self .btn_create_mod .setEnabled (True )
                    self .btn_create_mod .setStyleSheet (self .btn_style_green )
                else :
                    self .btn_create_mod .setEnabled (False )
                    self .btn_create_mod .setStyleSheet (self .btn_style_gray )
        except Exception :
            pass 

    def _on_backups_clicked (self ):
        try :
            QTimer .singleShot (0 ,self ._open_backup_manager )
        except Exception :
            self ._open_backup_manager ()

    def _open_backup_manager (self ):
        try :
            p =getattr (self ,'_json_path',None )
            if not p or not os.path .isfile (p ):
                self ._log ("No JSON available for backups (export one first).",err =True )
                return 
            win =BackupManagerWindow (p ,parent =self ,log_fn =self ._log )
            try :
                self ._backup_windows .append (win )
            except Exception :
                pass 
            win .show ()
            try :
                win .raise_ ();win .activateWindow ()
            except Exception :
                pass 
        except Exception as e :
            try :
                self ._log (f"Backup UI error: {e }",err =True )
            except Exception :
                pass 

    def _resolve_dds_path (self ,fname :str ,section :str ,ruta :str ):
        """Resuelve ruta absoluta del DDS desde el entorno actual.
        Construye candidatos bajo textures/actors/character/slavetats.
        Retorna el primer path existente o None.
        """
        try :
            env_dir =None 
            if self ._dds_dir and os.path .isdir (self ._dds_dir ):

                env_dir =os.path .dirname (os.path .normpath (self ._dds_dir ))
            elif getattr (self ,'_json_path',None )and os.path .isfile (self ._json_path ):

                jp =os.path .normpath (self ._json_path )
                slv_dir =os.path .dirname (jp )
                parts =slv_dir .replace ('/','\\').split ('\\')

                idx_tex =None 
                for i ,p in enumerate (parts ):
                    if p .lower ()=='textures':
                        idx_tex =i ;break 
                if idx_tex is not None and idx_tex >0 :
                    env_dir ='\\'.join (parts [:idx_tex ])
                else :

                    env_dir =slv_dir 
                    for _ in range (4 ):
                        env_dir =os.path .dirname (env_dir )
            if not env_dir :
                return None 
            base_tex =os.path .join (env_dir ,'textures','actors','character','slavetats')
            section =(section or '').strip ().strip ('\\/')
            ruta =(ruta or '').strip ().strip ('\\/')
            adds =''
            try :
                if getattr (self ,'_json_path',None )and os.path .isfile (self ._json_path ):
                    adds =os.path .splitext (os.path .basename (self ._json_path ))[0 ].strip ()
            except Exception :
                adds =''
            candidates =[]
            if section and ruta :
                candidates .append (os.path .join (base_tex ,section ,ruta ,fname ))
            if section :
                candidates .append (os.path .join (base_tex ,section ,fname ))
            if ruta :
                candidates .append (os.path .join (base_tex ,ruta ,fname ))
            candidates .append (os.path .join (base_tex ,fname ))

            if adds :
                if section and ruta :
                    candidates .append (os.path .join (base_tex ,adds ,section ,ruta ,fname ))
                if section :
                    candidates .append (os.path .join (base_tex ,adds ,section ,fname ))
                if ruta :
                    candidates .append (os.path .join (base_tex ,adds ,ruta ,fname ))
                candidates .append (os.path .join (base_tex ,adds ,fname ))

            try :
                slavetats_dir =os.path .dirname (os.path .normpath (self ._json_path ))if getattr (self ,'_json_path',None )else None 
                if slavetats_dir and os.path .isdir (slavetats_dir ):
                    if section and ruta :
                        candidates .append (os.path .join (slavetats_dir ,section ,ruta ,fname ))
                    if section :
                        candidates .append (os.path .join (slavetats_dir ,section ,fname ))
                    if ruta :
                        candidates .append (os.path .join (slavetats_dir ,ruta ,fname ))
                    candidates .append (os.path .join (slavetats_dir ,fname ))
            except Exception :
                pass 
            for p in candidates :
                if os.path .isfile (p ):
                    return p 
            return None 
        except Exception :
            return None 

    def _create_mod_package (self ):
        """Crea estructura de mod y empaqueta en 7z/zip.
        Estructura: textures/actors/character/slavetats/<SECTION>/... + JSON en slavetats.
        """
        try :

            env_dir =None 
            if self ._dds_dir and os.path .isdir (self ._dds_dir ):
                env_dir =os.path .dirname (os.path .normpath (self ._dds_dir ))
            elif getattr (self ,'_json_path',None )and os.path .isfile (self ._json_path ):
                env_dir =os.path .dirname (os.path .normpath (self ._json_path ))
            if not env_dir or not os.path .isdir (env_dir ):
                self ._log ("Please select a JSON or a folder with DDS first.",err =True )
                return 

            section =self ._current_section ()


            data =self ._gather_json_data ()
            out_json =os.path .join (env_dir ,f"{section }.json")
            try :
                with open (out_json ,'w',encoding ='utf-8')as f :
                    json .dump (data ,f ,ensure_ascii =False ,indent =4 )
                self ._log (f"JSON updated → {out_json }")
            except Exception as e :
                self ._log (f"Could not write JSON: {e }",err =True )
                return 


            build_root =os.path .join (env_dir ,f"SLAVE TATS {section }")
            slv_section_dir =os.path .join (build_root ,'textures','actors','character','slavetats',section )
            try :
                os .makedirs (slv_section_dir ,exist_ok =True )
            except Exception as e :
                self ._log (f"Error creating structure: {e }",err =True )
                return 


            dds_base =self ._dds_dir if (self ._dds_dir and os.path .isdir (self ._dds_dir ))else None 

            try :
                if dds_base and os.path .basename (os.path .normpath (dds_base )).lower ()=='slavetats':
                    candidate =os.path .join (dds_base ,section )
                    if os.path .isdir (candidate ):
                        self ._log (f"Detected 'slavetats' as base; using section subfolder: {candidate }")
                        dds_base =candidate 
            except Exception :
                pass 
            if not dds_base :
                candidates =[
                os.path .join (env_dir ,section ),
                os.path .join (env_dir ,'textures','actors','character','slavetats',section ),
                ]
                dds_base =next ((c for c in candidates if os.path .isdir (c )),None )
                if dds_base :
                    self ._log (f"DDS folder inferred: {dds_base }")
            else :
                try :
                    self ._log (f"DDS folder selected: {dds_base }")
                except Exception :
                    pass 


            copied =0 
            if dds_base and os.path .isdir (dds_base ):
                for root ,_dirs ,files in os .walk (dds_base ):
                    rel_dir =os.path .relpath (root ,dds_base )
                    dst_dir =slv_section_dir if rel_dir in ('.','')else os.path .join (slv_section_dir ,rel_dir )
                    try :
                        os .makedirs (dst_dir ,exist_ok =True )
                    except Exception as e :
                        self ._log (f"Could not create destination folder: {dst_dir } ({e })",err =True )
                    for f in files :
                        src =os.path .join (root ,f )
                        try :
                            shutil .copy2 (src ,os.path .join (dst_dir ,f ))
                            copied +=1 
                        except Exception as e :
                            self ._log (f"Error copying {src }: {e }",err =True )
                self ._log (f"Copied {copied } files into {slv_section_dir }")
            else :
                self ._log ("Could not resolve the DDS folder; only the JSON will be packaged.",err =True )


            try :
                slavetats_root =os.path .join (build_root ,'textures','actors','character','slavetats')
                os .makedirs (slavetats_root ,exist_ok =True )
                shutil .copy2 (out_json ,os.path .join (slavetats_root ,f"{section }.json"))
            except Exception as e :
                self ._log (f"Could not copy JSON inside slavetats: {e }",err =True )


            archive_7z =os.path .join (env_dir ,f"SLAVE TATTO {section }.7z")
            archive_zip =os.path .join (env_dir ,f"SLAVE TATTO {section }.zip")

            def _find_7z_exe ():
                candidates =[
                '7z','7z.exe',
                r"C:\\Program Files\\7-Zip\\7z.exe",
                r"C:\\Program Files (x86)\\7-Zip\\7z.exe",
                ]
                for c in candidates :
                    try :
                        from shutil import which 
                        exe =which (c )if os.path .basename (c )==c else (c if os.path .isfile (c )else None )
                        if exe :
                            return exe 
                    except Exception :
                        continue 
                return None 

            seven =_find_7z_exe ()
            if seven :
                try :
                    creation =getattr (subprocess ,'CREATE_NO_WINDOW',0 )
                    startup =None 
                    try :
                        startup =subprocess .STARTUPINFO ()
                        startup .dwFlags |=subprocess .STARTF_USESHOWWINDOW 
                    except Exception :
                        startup =None 
                    cmd =[seven ,'a','-t7z',archive_7z ,os.path .join (build_root ,'*'),'-bsp0','-bso1','-bse1']
                    proc =subprocess .Popen (cmd ,stdout =subprocess .PIPE ,stderr =subprocess .STDOUT ,text =True ,creationflags =creation ,startupinfo =startup )
                    for line in proc .stdout or []:
                        self ._log (line .rstrip ())
                    ret =proc .wait ()
                    if ret ==0 and os.path .isfile (archive_7z ):
                        self ._log (f"Package created: {archive_7z }")
                        try :
                            self .output_terminal .append ("<span style='color:#BA68C8; font-weight:700'>THE MOD PACKAGE HAS BEEN SUCCESSFULLY CREATED, YOU CAN NOW SHARE IT</span>")
                        except Exception :
                            pass 
                    else :
                        raise RuntimeError (f"7z exit code {ret }")
                except Exception as e :
                    self ._log (f"7z failed ({e }); creating fallback ZIP…",err =True )
                    shutil .make_archive (os.path .splitext (archive_zip )[0 ],'zip',build_root )
                    self ._log (f"ZIP package created: {archive_zip }")
                    try :
                        self .output_terminal .append ("<span style='color:#BA68C8; font-weight:700'>THE MOD PACKAGE HAS BEEN SUCCESSFULLY CREATED, YOU CAN NOW SHARE IT</span>")
                    except Exception :
                        pass 
            else :
                try :
                    shutil .make_archive (os.path .splitext (archive_zip )[0 ],'zip',build_root )
                    self ._log (f"7-Zip not found. ZIP package created: {archive_zip }")
                    try :
                        self .output_terminal .append ("<span style='color:#BA68C8; font-weight:700'>THE MOD PACKAGE HAS BEEN SUCCESSFULLY CREATED, YOU CAN NOW SHARE IT</span>")
                    except Exception :
                        pass 
                except Exception as e :
                    self ._log (f"Could not create ZIP: {e }",err =True )
                    return 


            try :
                shutil .rmtree (build_root ,ignore_errors =True )
                self ._log (f"Cleanup done: deleted temporary folder '{build_root }'")
            except Exception as e :
                self ._log (f"Could not delete temporary folder: {e }",err =True )

            try :
                os .startfile (env_dir )
            except Exception :
                try :
                    subprocess .Popen (['explorer',env_dir ])
                except Exception :
                    pass 
        except Exception as e :
            self ._log (f"Error creating package: {e }",err =True )
        except Exception :
            pass 

    def _choose_output_dir (self ):
        try :
            base =QFileDialog .getExistingDirectory (self ,"Select destination folder")
            if base :
                self ._dest_dir =base 
                self ._log (f"Destination selected: {base }")
            else :
                self ._log ("Selection cancelled")
        except Exception as e :
            self ._log (f"Error selecting folder: {e }",err =True )

    def _open_env_folder (self ):
        try :
            env_dir =None 

            if getattr (self ,'_json_path',None )and os.path .isfile (self ._json_path ):
                env_dir =os.path .dirname (os.path .normpath (self ._json_path ))

            elif self ._dds_dir and os.path .isdir (self ._dds_dir ):
                env_dir =os.path .dirname (os.path .normpath (self ._dds_dir ))
            if not env_dir or not os.path .isdir (env_dir ):
                self ._log ("Please select a JSON or a folder with DDS first.",err =True )
                return 
            if not os.path .isdir (env_dir ):
                self ._log (f"Invalid environment folder: {env_dir }",err =True )
                return 

            try :
                os .startfile (env_dir )
                self ._log (f"Opening environment folder: {env_dir }")
            except Exception :

                subprocess .Popen (['explorer',env_dir ])
                self ._log (f"Opening environment folder (fallback): {env_dir }")
        except Exception as e :
            self ._log (f"Error opening environment folder: {e }",err =True )

    def _choose_dds_folder (self ):
        try :
            base =QFileDialog .getExistingDirectory (self ,"Select folder with DDS")
            if base :
                self ._load_dds_folder (base )
            else :
                self ._log ("DDS folder selection cancelled")
        except Exception as e :
            self ._log (f"Error selecting DDS folder: {e }",err =True )

    def _load_dds_folder (self ,base :str ):
        try :

            self ._json_path =None 
            self ._json_exported =False 
            self ._dds_dir =base 

            try :
                base_sec =os.path .basename (os.path .normpath (base ))or "MyPackTats"
                self ._section_override =base_sec 
                if hasattr (self ,'section_edit'):
                    self .section_edit .setText (base_sec )
            except Exception :
                self ._section_override =None 

            file_entries =[]
            try :
                for root ,_dirs ,fnames in os .walk (base ):
                    for f in fnames :
                        if f .lower ().endswith ('.dds'):
                            abs_p =os.path .join (root ,f )
                            rel_dir =os.path .relpath (root ,base )

                            if rel_dir =='.'or rel_dir ==''or rel_dir ==os .curdir :
                                rel_dir =''
                            file_entries .append ((abs_p ,rel_dir ,f ))
            except Exception :

                for f in os .listdir (base ):
                    if f .lower ().endswith ('.dds'):
                        file_entries .append ((os.path .join (base ,f ),'',f ))

            file_entries .sort (key =lambda t :(t [1 ].lower (),t [2 ].lower ()))
            files =file_entries 
            if not files :
                self ._log ("The folder does not contain .dds",err =True )

                try :
                    self ._set_action_buttons_enabled (False )
                except Exception :
                    pass 
                return 

            for i in reversed (range (self .list_layout .count ())):
                item =self .list_layout .itemAt (i )
                w =item .widget ()
                if w is not None :
                    w .setParent (None )
            self ._rows .clear ()

            self ._reset_table ()

            first_abs =None 
            for abs_path ,rel_dir ,fname in files :

                lbl =QLabel (fname );lbl .setStyleSheet ("color: #E0E0E0;")


                try :
                    base_name =os.path .basename (os.path .normpath (base ))or ''
                except Exception :
                    base_name =''
                ruta_text =rel_dir .replace ('/','\\').replace ('\\\\','\\')if rel_dir else base_name 
                ruta_label =QLabel (ruta_text );ruta_label .setStyleSheet ("color:#C0C0C0;")
                area =QComboBox ();area .addItems (["Body","Feet","Hand","Face"]);area .setMinimumWidth (140 )
                try :
                    area .setFocusPolicy (Qt .ClickFocus )
                    area .setToolTip ("Click to open. Mouse wheel disabled to avoid accidental changes.")
                    def _wheelEvent_area (e ,_c =area ):
                        try :
                            v =_c .view ()if hasattr (_c ,'view')else None 
                            if v and v .isVisible ():
                                return QComboBox .wheelEvent (_c ,e )
                        except Exception :
                            pass 
                        e .ignore ()
                    area .wheelEvent =_wheelEvent_area 
                except Exception :
                    pass 
                try :
                    area .setStyleSheet ("QComboBox { padding: 4px 8px; }")
                except Exception :
                    pass 
                name_edit =QLineEdit (os.path .splitext (fname )[0 ]);name_edit .setMinimumWidth (300 )
                sec_edit =QLineEdit (self ._current_section ());sec_edit .setMinimumWidth (180 )
                try :
                    sec_edit .setToolTip ("Section for this DDS entry. Defaults to folder or JSON section.")
                except Exception :
                    pass 

                r =getattr (self ,'_grid_row',1 )
                self .grid .addWidget (lbl ,r ,0 )
                self .grid .addWidget (ruta_label ,r ,1 )
                self .grid .addWidget (sec_edit ,r ,2 )
                self .grid .addWidget (area ,r ,3 )
                self .grid .addWidget (name_edit ,r ,4 )
                self ._grid_row =r +1 
                self ._rows .append ((abs_path ,name_edit ,area ,sec_edit ,ruta_label ))
                if first_abs is None :
                    first_abs =abs_path 

                try :
                    ruta_label .setToolTip ("Double-click to open this folder")
                    def _on_dbl_open_path (e ,_ruta =ruta_text ,_base =base ):
                        try :

                            target =_base 
                            if _ruta and _ruta .strip ():
                                base_name2 =os.path .basename (os.path .normpath (_base ))
                                if _ruta .strip ().lower ()!=(base_name2 or '').lower ():
                                    target =os.path .join (_base ,_ruta )
                            if os.path .isdir (target ):
                                try :
                                    os .startfile (target )
                                    self ._log (f"Opening folder: {target }")
                                except Exception :
                                    subprocess .Popen (['explorer',target ])
                                    self ._log (f"Opening folder (fallback): {target }")
                            else :
                                self ._log (f"Folder not found: {target }",err =True )
                        except Exception as ex :
                            self ._log (f"Open folder error: {ex }",err =True )
                    ruta_label .mouseDoubleClickEvent =_on_dbl_open_path 
                except Exception :
                    pass 

                try :
                    lbl .mousePressEvent =(lambda p =abs_path :(lambda e :self ._open_preview_window (p )))()
                    lbl .setToolTip ("Click to preview in a window")
                except Exception :
                    pass 

            try :
                self .list_layout .addStretch (1 )
            except Exception :
                pass 
            self ._log (f"Loaded {len (files )} DDS from {base }")

            try :
                self .output_terminal .append ("<span style='color:#00BCD4; font-weight:700'>A SET OF DDS HAS BEEN LOADED AND IS READY TO CONFIGURE THE JSON. REMEMBER IT IS BETTER TO KEEP ALL DDS IN THE SAME FOLDER</span>")
            except Exception :
                pass 

            try :

                self ._set_action_buttons_enabled (True )
            except Exception :
                pass 

            try :
                self ._setup_dds_watcher (base )
            except Exception as e :
                self ._log (f"Watcher no disponible: {e }",err =True )
        except Exception as e :
            self ._log (f"Error loading DDS: {e }",err =True )
            try :
                self ._set_action_buttons_enabled (False )
            except Exception :
                pass 

    def _open_preview_window (self ,path :str ):
        try :

            win =DdsPreviewWindow (path ,None ,log_fn =self ._log )
            self ._preview_windows .append (win )
            win .show ()
            win .raise_ ()
            win .activateWindow ()
        except Exception as e :
            self ._log (f"Error abriendo vista previa: {e }",err =True )


    def dragEnterEvent (self ,event ):
        try :
            if event .mimeData ().hasUrls ():
                for url in event .mimeData ().urls ():
                    p =url .toLocalFile ()
                    if not p :
                        continue 

                    if os.path .isdir (p )or p .lower ().endswith ('.json'):
                        event .acceptProposedAction ()
                        return 
            event .ignore ()
        except Exception :
            event .ignore ()

    def dropEvent (self ,event ):
        try :
            folders =[]
            json_files =[]
            for url in event .mimeData ().urls ():
                p =url .toLocalFile ()
                if not p :
                    continue 
                if os.path .isdir (p ):
                    folders .append (p )
                elif p .lower ().endswith ('.json'):
                    json_files .append (p )

            if json_files :
                self ._load_json_file (json_files [0 ])
                return 
            if not folders :
                return 
            for base in folders :
                try :

                    has_dds =False 
                    for _root ,_dirs ,fnames in os .walk (base ):
                        if any (fn .lower ().endswith ('.dds')for fn in fnames ):
                            has_dds =True 
                            break 
                except Exception :
                    has_dds =False 
                if has_dds :
                    self ._load_dds_folder (base )
                    return 

            self ._log ("The dropped folder does not contain .dds",err =True )
            try :
                self ._set_action_buttons_enabled (False )
            except Exception :
                pass 
        except Exception as e :
            self ._log (f"Drop error: {e }",err =True )
            try :
                self ._set_action_buttons_enabled (False )
            except Exception :
                pass 

    def _load_json_file (self ,path :str ):
        """Carga un archivo JSON existente (lista de entradas) y rellena la UI para editar.
        Permite modificar nombres, áreas y volver a exportar.
        """
        try :
            with open (path ,'r',encoding ='utf-8')as f :
                data =json .load (f )
            if not isinstance (data ,list )or not data :
                self ._log ("El JSON no contiene una lista válida de entradas.",err =True )
                return 
        except Exception as e :
            self ._log (f"Error leyendo JSON: {e }",err =True )
            return 


        self ._json_path =path 
        self ._json_exported =False 

        try :
            for i in reversed (range (self .list_layout .count ())):
                item =self .list_layout .itemAt (i )
                w =item .widget ()
                if w is not None :
                    w .setParent (None )
        except Exception :
            pass 
        self ._rows .clear ()


        try :
            first =data [0 ]
            sec =(first .get ('section')or '').strip ()
            self ._section_override =sec or None 
        except Exception :
            self ._section_override =None 

        try :
            show_sec =None 
            if self ._section_override :
                show_sec =self ._section_override 
            elif self ._dds_dir and os.path .isdir (self ._dds_dir ):
                show_sec =os.path .basename (os.path .normpath (self ._dds_dir ))or "MiPackTats"
            else :
                show_sec ="MiPackTats"
            if hasattr (self ,'section_edit'):
                self .section_edit .setText (show_sec )
        except Exception :
            pass 


        self ._reset_table ()


        count =0 
        for item in data :
            try :
                fname =None 
                tex =item .get ('texture')if isinstance (item ,dict )else None 
                if isinstance (tex ,str )and tex :

                    tex_norm =tex .replace ('/','\\')
                    fname =os.path .basename (tex_norm )
                if not fname :
                    fname =(item .get ('name')or 'texture').strip ()+'.dds'

                lbl =QLabel (fname )
                lbl .setStyleSheet ("color: #E0E0E0;")

                ruta_label =QLabel ("")
                ruta_label .setStyleSheet ("color:#C0C0C0;")

                try :
                    ruta_sel =""
                    if isinstance (tex ,str )and tex :
                        parts =tex_norm .split ('\\')



                        if len (parts )>=3 :
                            subdirs =parts [1 :-1 ]
                            if subdirs :
                                ruta_sel ='\\'.join (subdirs )
                        elif len (parts )>=2 :

                            ruta_sel =parts [0 ]
                    ruta_label .setText (ruta_sel )
                except Exception :
                    ruta_label .setText ("")
                area =QComboBox ();area .addItems (["Body","Feet","Hand","Face"])
                area .setMinimumWidth (140 )
                try :
                    area .setFocusPolicy (Qt .ClickFocus )
                    area .setToolTip ("Click to open. Mouse wheel disabled to avoid accidental changes.")
                    def _wheelEvent_area_json (e ,_c =area ):
                        try :
                            v =_c .view ()if hasattr (_c ,'view')else None 
                            if v and v .isVisible ():
                                return QComboBox .wheelEvent (_c ,e )
                        except Exception :
                            pass 
                        e .ignore ()
                    area .wheelEvent =_wheelEvent_area_json 
                except Exception :
                    pass 
                try :
                    area .setStyleSheet ("QComboBox { padding: 4px 8px; }")
                except Exception :
                    pass 
                name_edit =QLineEdit ((item .get ('name')or os.path .splitext (fname )[0 ]).strip ())
                name_edit .setMinimumWidth (300 )

                row_sec =(item .get ('section')or '').strip ()if isinstance (item ,dict )else ''
                if not row_sec :
                    row_sec =(self ._section_override or self ._current_section ())
                sec_edit =QLineEdit (row_sec )
                sec_edit .setMinimumWidth (180 )
                try :
                    sec_edit .setToolTip ("Section for this DDS entry. Defaults to folder or JSON section.")
                except Exception :
                    pass 

                r =getattr (self ,'_grid_row',1 )
                self .grid .addWidget (lbl ,r ,0 )
                self .grid .addWidget (ruta_label ,r ,1 )
                self .grid .addWidget (sec_edit ,r ,2 )
                self .grid .addWidget (area ,r ,3 )
                self .grid .addWidget (name_edit ,r ,4 )
                self ._grid_row =r +1 


                try :
                    j_area =(item .get ('area')or '').strip ()
                    if j_area :

                        jl =j_area .lower ()
                        idx ={"body":0 ,"feet":1 ,"hand":2 ,"face":3 }.get (jl ,None )
                        if idx is None and jl =='head':
                            idx =3 
                        if idx is not None :
                            area .setCurrentIndex (idx )
                except Exception :
                    pass 


                abs_path =fname 
                self ._rows .append ((abs_path ,name_edit ,area ,sec_edit ,ruta_label ))


                try :
                    ruta_label .setToolTip ("Double-click to open this folder")
                    def _on_dbl_open_path_json (e ,_fname =fname ,_sec_edit =sec_edit ,_ruta_label =ruta_label ,_tex_norm =tex_norm if isinstance (tex ,str )and tex else None ):
                        try :
                            section =(_sec_edit .text ().strip ()if hasattr (_sec_edit ,'text')else '')or self ._current_section ()
                            ruta_txt =(_ruta_label .text ().strip ()if hasattr (_ruta_label ,'text')else '')
                            section =section .strip ('\\/')
                            ruta_txt =ruta_txt .strip ('\\/')
                            if ruta_txt and section and ruta_txt .lower ()==section .lower ():
                                ruta_txt =''
                            p =None 

                            if self ._dds_dir and os.path .isdir (self ._dds_dir ):
                                local_base =self ._dds_dir 
                                local_candidates =[
                                os.path .join (local_base ,section ,ruta_txt ,_fname )if (section and ruta_txt )else None ,
                                os.path .join (local_base ,ruta_txt ,_fname )if ruta_txt else None ,
                                os.path .join (local_base ,section ,_fname )if section else None ,
                                os.path .join (local_base ,_fname ),
                                ]
                                if _tex_norm :
                                    local_candidates .insert (0 ,os.path .join (local_base ,_tex_norm ))
                                for cand in [c for c in local_candidates if c ]:
                                    if os.path .isfile (cand ):
                                        p =cand ;break 
                            if not p and _tex_norm :
                                env_p =self ._resolve_dds_path (os.path .basename (_tex_norm ),section ,ruta_txt )
                                if env_p :p =env_p 
                            if p and os.path .isfile (p ):
                                folder =os.path .dirname (p )
                                if os.path .isdir (folder ):
                                    try :
                                        os .startfile (folder )
                                        self ._log (f"Opening folder: {folder }")
                                    except Exception :
                                        subprocess .Popen (['explorer',folder ])
                                        self ._log (f"Opening folder (fallback): {folder }")
                                else :
                                    self ._log (f"Folder not found: {folder }",err =True )
                            else :

                                base_dir =None 
                                if self ._dds_dir and os.path .isdir (self ._dds_dir ):
                                    base_dir =self ._dds_dir 
                                elif getattr (self ,'_json_path',None )and os.path .isfile (self ._json_path ):
                                    base_dir =os.path .dirname (os.path .normpath (self ._json_path ))
                                target =None 
                                if base_dir :
                                    if ruta_txt :
                                        target =os.path .join (base_dir ,section ,ruta_txt )
                                        if not os.path .isdir (target ):
                                            target =os.path .join (base_dir ,ruta_txt )
                                    else :
                                        target =os.path .join (base_dir ,section )
                                if target and os.path .isdir (target ):
                                    try :
                                        os .startfile (target )
                                        self ._log (f"Opening folder: {target }")
                                    except Exception :
                                        subprocess .Popen (['explorer',target ])
                                        self ._log (f"Opening folder (fallback): {target }")
                                else :
                                    self ._log ("Folder for this entry could not be resolved.",err =True )
                        except Exception as ex :
                            self ._log (f"Open folder error: {ex }",err =True )
                    ruta_label .mouseDoubleClickEvent =_on_dbl_open_path_json 
                except Exception :
                    pass 


                try :
                    lbl .setToolTip ("Click to preview this DDS (resolverá la ruta real)")
                    def _on_click_preview (e ,_fname =fname ,_sec_edit =sec_edit ,_ruta_label =ruta_label ,_tex_norm =tex_norm if isinstance (tex ,str )and tex else None ):
                        try :
                            section =(_sec_edit .text ().strip ()if hasattr (_sec_edit ,'text')else '')or self ._current_section ()
                            ruta_txt =(_ruta_label .text ().strip ()if hasattr (_ruta_label ,'text')else '')
                            section =section .strip ('\\/')
                            ruta_txt =ruta_txt .strip ('\\/')

                            if ruta_txt and section and ruta_txt .lower ()==section .lower ():
                                ruta_txt =''

                            p =None 
                            if self ._dds_dir and os.path .isdir (self ._dds_dir ):
                                local_base =self ._dds_dir 
                                local_candidates =[

                                os.path .join (local_base ,section ,ruta_txt ,_fname )if (section and ruta_txt )else None ,
                                os.path .join (local_base ,ruta_txt ,_fname )if ruta_txt else None ,
                                os.path .join (local_base ,section ,_fname )if section else None ,
                                os.path .join (local_base ,_fname ),
                                ]

                                if _tex_norm :

                                    local_candidates .insert (0 ,os.path .join (local_base ,_tex_norm ))
                                for cand in [c for c in local_candidates if c ]:
                                    try :
                                        self ._log (f"[DDS Preview] try(local): {cand }")
                                    except Exception :
                                        pass 
                                    if os.path .isfile (cand ):
                                        p =cand 
                                        break 
                            if not p :

                                if _tex_norm :
                                    env_p =self ._resolve_dds_path (os.path .basename (_tex_norm ),section ,ruta_txt )

                                    try :
                                        if getattr (self ,'_json_path',None )and os.path .isfile (self ._json_path ):
                                            slv_dir =os.path .dirname (os.path .normpath (self ._json_path ))
                                            direct_env =os.path .join (slv_dir ,_tex_norm )
                                            try :
                                                self ._log (f"[DDS Preview] try(json-slv): {direct_env }")
                                            except Exception :
                                                pass 
                                            if os.path .isfile (direct_env ):
                                                p =direct_env 
                                            elif env_p :
                                                p =env_p 
                                        elif env_p :
                                            p =env_p 
                                    except Exception :
                                        if env_p :
                                            p =env_p 
                                if not p :
                                    try :
                                        self ._log ("[DDS Preview] try(resolver)")
                                    except Exception :
                                        pass 
                                    p =self ._resolve_dds_path (_fname ,section ,ruta_txt )

                            if not p and _tex_norm and getattr (self ,'_json_path',None )and os.path .isfile (self ._json_path ):
                                try :
                                    slv_dir =os.path .dirname (os.path .normpath (self ._json_path ))
                                    best =None 
                                    best_score =-1 
                                    for root ,dirs ,files in os .walk (slv_dir ):
                                        for fn in files :
                                            if fn .lower ()==_fname .lower ():
                                                full =os.path .join (root ,fn )
                                                rel =os.path .relpath (full ,slv_dir ).replace ('/','\\')

                                                score =2 if rel .lower ().endswith (_tex_norm .lower ())else 1 
                                                try :
                                                    self ._log (f"[DDS Preview] try(search): {full } (score={score })")
                                                except Exception :
                                                    pass 
                                                if score >best_score :
                                                    best =full ;best_score =score 
                                    if best and os.path .isfile (best ):
                                        p =best 
                                except Exception :
                                    pass 
                            if p and os.path .isfile (p ):
                                try :
                                    self ._log (f"[DDS Preview] Resolved: {p }")
                                except Exception :
                                    pass 
                                self ._open_preview_window (p )
                            else :
                                self ._log (f"DDS not found for preview: {_fname } (Section='{section }', Ruta='{ruta_txt }')",err =True )
                        except Exception as ex :
                            try :
                                self ._log (f"Preview error: {ex }",err =True )
                            except Exception :
                                pass 
                    lbl .mousePressEvent =_on_click_preview 
                except Exception :
                    pass 
                count +=1 
            except Exception :
                continue 


        try :
            self .list_layout .addStretch (1 )
        except Exception :
            pass 

        self ._log (f"Loaded {count } entries from JSON: {path }")

        try :
            self .output_terminal .append ("<span style='color:#00BCD4; font-weight:700'>A PRECONFIGURED JSON HAS BEEN LOADED</span>")
        except Exception :
            pass 

        try :
            self ._set_action_buttons_enabled (True )
            if hasattr (self ,'btn_select_out'):
                if not self ._dds_dir and self ._json_path :

                    self .btn_select_out .setEnabled (True )
                    self .btn_select_out .setStyleSheet (self .btn_style_green )
                elif not self ._dds_dir and not self ._json_path :
                    self .btn_select_out .setEnabled (False )
                    self .btn_select_out .setStyleSheet (self .btn_style_gray )

            if hasattr (self ,'btn_create_mod'):
                if getattr (self ,'_json_exported',False ):
                    self .btn_create_mod .setEnabled (True )
                    self .btn_create_mod .setStyleSheet (self .btn_style_green )
                else :
                    self .btn_create_mod .setEnabled (False )
                    self .btn_create_mod .setStyleSheet (self .btn_style_gray )

            if hasattr (self ,'btn_backups'):
                self .btn_backups .setEnabled (True )
                self .btn_backups .setStyleSheet (self .btn_style_green )
        except Exception :
            pass 


        try :

            if self ._dds_dir and os.path .isdir (self ._dds_dir ):
                self ._setup_dds_watcher (self ._dds_dir )

                self ._bind_preview_handlers_for_current_rows ()

                try :
                    self ._on_dds_directory_changed (self ._dds_dir )
                except Exception :
                    pass 
            else :

                env_dir =os.path .dirname (os.path .normpath (self ._json_path ))if self ._json_path else None 
                section =self ._current_section ()
                candidates =[]
                if env_dir :

                    candidates .append (os.path .join (env_dir ,section ))

                    candidates .append (os.path .join (env_dir ,'textures','actors','character','slavetats',section ))
                dds_dir =next ((c for c in candidates if c and os.path .isdir (c )),None )
                if dds_dir :
                    self ._dds_dir =dds_dir 
                    self ._log (f"DDS folder inferred from JSON: {dds_dir }")

                    self ._setup_dds_watcher (dds_dir )

                    self ._bind_preview_handlers_for_current_rows ()

                    try :
                        self ._on_dds_directory_changed (self ._dds_dir )
                    except Exception :
                        pass 
        except Exception as e :
            self ._log (f"No se pudo configurar vigilancia de DDS: {e }",err =True )

    def _create_structure_skeleton (self ):
        section =self ._current_section ()
        if not self ._dest_dir :
            self ._log ("Select a destination folder.",err =True )
            return 

        try :
            textures_root =os.path .join (self ._dest_dir ,'textures','actors','character','slavetats',section )
            os .makedirs (textures_root ,exist_ok =True )
            scripts_src =os.path .join (self ._dest_dir ,'scripts','Source')
            os .makedirs (scripts_src ,exist_ok =True )
            self ._log (f"Structure created: {textures_root }")
        except Exception as e :
            self ._log (f"Error creating structure: {e }",err =True )
            return 
        self ._log (f"Base structure for '{section }' ready.")

    def _export_json (self ):
        try :
            section =self ._current_section ()


            env_dir =None 
            if self ._dds_dir and os.path .isdir (self ._dds_dir ):
                env_dir =os.path .dirname (os.path .normpath (self ._dds_dir ))
            elif getattr (self ,'_json_path',None )and os.path .isfile (self ._json_path ):
                env_dir =os.path .dirname (os.path .normpath (self ._json_path ))
            if not env_dir or not os.path .isdir (env_dir ):
                self ._log ("Selecciona primero un JSON o una carpeta con DDS.",err =True )
                return 
            data =self ._gather_json_data ()

            out_json =os.path .join (env_dir ,f"{section }.json")

            try :
                backup_dir =os.path .join (env_dir ,'Backups')
                os .makedirs (backup_dir ,exist_ok =True )
                if os.path .isfile (out_json ):
                    ts =time .strftime ('%Y%m%d-%H%M%S')
                    backup_name =f"{section }_{ts }.json"
                    backup_path =os.path .join (backup_dir ,backup_name )
                    shutil .copy2 (out_json ,backup_path )
                    self ._log (f"Backup previo creado → {backup_path }")
                else :
                    self ._log (f"Carpeta de backups lista → {backup_dir }")
            except Exception as be :
                self ._log (f"No se pudo crear backup previo: {be }",err =True )
            with open (out_json ,'w',encoding ='utf-8')as f :
                json .dump (data ,f ,ensure_ascii =False ,indent =4 )
            self ._log (f"JSON generated with {len (data )} entries → {out_json }")

            try :
                self .output_terminal .append ("<span style='color:#00BCD4; font-weight:700'>THE JSON HAS BEEN CREATED WITH EVERYTHING</span>")
            except Exception :
                pass 

            self ._json_path =out_json 
            try :
                if hasattr (self ,'btn_backups'):
                    self .btn_backups .setEnabled (True )
                    self .btn_backups .setStyleSheet (self .btn_style_green )
            except Exception :
                pass 

            try :
                self ._clear_new_highlight_styles ()
            except Exception :
                pass 

            try :
                self ._load_json_file (out_json )
            except Exception as le :
                self ._log (f"No se pudo recargar el JSON recién creado: {le }",err =True )

            self ._json_exported =True 
            try :
                if hasattr (self ,'btn_create_mod'):
                    self .btn_create_mod .setEnabled (True )
                    self .btn_create_mod .setStyleSheet (self .btn_style_green )
            except Exception :
                pass 
        except Exception as e :
            self ._log (f"Error exporting JSON: {e }",err =True )

    def _log (self ,msg :str ,err :bool =False ):
        color ="#FF7043"if err else "#4CAF50"
        self .output_terminal .append (f"<span style='color:{color }'>"+msg .replace ("<","&lt;").replace (">","&gt;")+"</span>")

    def _clear_terminal (self ):
        try :
            self .output_terminal .clear ()
        except Exception :
            pass 

    def _gather_json_data (self ):
        data =[]
        for abs_path ,name_edit ,area_combo ,sec_edit ,ruta_label in self ._rows :
            fname =os.path .basename (abs_path )
            row_section =(sec_edit .text ().strip ()or self ._current_section ())

            try :
                ruta =(ruta_label .text ()or '').strip ().strip ('\\/')

                if ruta and row_section and ruta .lower ()==row_section .lower ():
                    ruta =''
            except Exception :
                ruta =''
            texture_path =f"{row_section }\\{fname }"if not ruta else f"{row_section }\\{ruta }\\{fname }"
            data .append ({
            "name":name_edit .text ().strip ()or os.path .splitext (fname )[0 ],
            "section":row_section ,
            "texture":texture_path ,
            "area":area_combo .currentText (),
            })
        return data 

    def _print_json_example (self ):
        try :
            section =self ._current_section ()
            if not self ._rows :
                self ._log ("No hay DDS cargados para ejemplo.",err =True )
                return 
            data =self ._gather_json_data ()
            self ._log (f"Ejemplo JSON para section '{section }' ({len (data )} entradas):")

            pretty =json .dumps (data ,ensure_ascii =False ,indent =4 )
            safe =pretty .replace ("<","&lt;").replace (">","&gt;")
            try :
                self .output_terminal .append ("<pre style='color:#FFD54F; margin:0'>"+safe +"</pre>")
            except Exception :
                for line in safe .splitlines ():
                    try :
                        self .output_terminal .append ("<span style='color:#FFD54F'>"+line +"</span>")
                    except Exception :
                        pass 

            try :
                self .output_terminal .append ("<span style='color:#00BCD4; font-weight:700'>A JSON PREVIEW HAS BEEN PERFORMED</span>")
            except Exception :
                pass 
        except Exception as e :
            self ._log (f"Error generando ejemplo JSON: {e }",err =True )

    def _current_section (self )->str :
        try :

            if getattr (self ,'_section_override',None ):
                return self ._section_override 
            if self ._dds_dir :
                base =os.path .basename (os.path .normpath (self ._dds_dir ))
                return base or "MiPackTats"
            return "MiPackTats"
        except Exception :
            return "MiPackTats"

    def _on_section_changed (self ,text :str ):
        try :
            t =(text or "").strip ()

            self ._section_override =t or None 
        except Exception :
            pass 


    def _setup_dds_watcher (self ,directory :str ):
        try :
            if not directory or not os.path .isdir (directory ):
                return 

            if self ._dds_watcher is not None :
                try :
                    self ._dds_watcher .deleteLater ()
                except Exception :
                    pass 
            self ._dds_watcher =QFileSystemWatcher ()
            try :
                self ._dds_watcher .addPath (directory )
            except Exception :

                self ._dds_watcher .addPaths ([directory ])
            self ._dds_watcher .directoryChanged .connect (self ._on_dds_directory_changed )
            self ._log (f"Watching DDS folder for new files: {directory }")
        except Exception as e :
            self ._log (f"Watcher error: {e }",err =True )

    def _listed_dds_basenames (self ):
        try :
            names =set ()
            for abs_path ,_name ,_area ,*_ in self ._rows :
                try :
                    names .add (os.path .basename (abs_path ).lower ())
                except Exception :
                    pass 
            return names 
        except Exception :
            return set ()

    def _existing_relkeys (self ):
        """Conjunto de claves (ruta_relativa + '|' + filename) actualmente listadas.
        Normaliza ruta vacía y trata 'ruta == section' como vacía para coherencia.
        """
        keys =set ()
        try :
            for abs_path ,name_edit ,area_combo ,sec_edit ,ruta_label in self ._rows :
                try :
                    fname =os.path .basename (abs_path )
                except Exception :

                    fname =str (abs_path )
                section =(sec_edit .text ().strip ()if hasattr (sec_edit ,'text')else '')
                ruta =(ruta_label .text ().strip ()if hasattr (ruta_label ,'text')else '')
                if ruta and section and ruta .lower ()==section .lower ():
                    ruta =''
                key =f"{ruta .lower ()}|{fname .lower ()}"
                keys .add (key )
        except Exception :
            pass 
        return keys 

    def _add_dds_row (self ,base :str ,rel_dir :str ,fname :str ,highlight :bool =False ):
        """Añade una fila al grid, igual que al cargar carpeta DDS. highlight=True pinta el filename en amarillo."""

        lbl =QLabel (fname )
        try :
            lbl .setStyleSheet ("color: #FFD54F; font-weight: 600;"if highlight else "color: #E0E0E0;")
        except Exception :
            pass 

        try :
            base_name =os.path .basename (os.path .normpath (base ))or ''
        except Exception :
            base_name =''
        ruta_text =rel_dir .replace ('/','\\').replace ('\\\\','\\')if rel_dir else (base_name )
        ruta_label =QLabel (ruta_text )
        try :
            ruta_label .setStyleSheet ("color:#C0C0C0;")
        except Exception :
            pass 
        area =QComboBox ();area .addItems (["Body","Feet","Hand","Face"]);area .setMinimumWidth (140 )
        try :
            area .setFocusPolicy (Qt .ClickFocus )
            area .setToolTip ("Click to open. Mouse wheel disabled to avoid accidental changes.")
            def _wheelEvent_area_added (e ,_c =area ):
                try :
                    v =_c .view ()if hasattr (_c ,'view')else None 
                    if v and v .isVisible ():
                        return QComboBox .wheelEvent (_c ,e )
                except Exception :
                    pass 
                e .ignore ()
            area .wheelEvent =_wheelEvent_area_added 
        except Exception :
            pass 
        try :
            area .setStyleSheet ("QComboBox { padding: 4px 8px; }")
        except Exception :
            pass 
        name_edit =QLineEdit (os.path .splitext (fname )[0 ]);name_edit .setMinimumWidth (300 )
        sec_edit =QLineEdit (self ._current_section ());sec_edit .setMinimumWidth (180 )
        try :
            sec_edit .setToolTip ("Section for this DDS entry. Defaults to folder or JSON section.")
        except Exception :
            pass 

        r =getattr (self ,'_grid_row',1 )
        self .grid .addWidget (lbl ,r ,0 )
        self .grid .addWidget (ruta_label ,r ,1 )
        self .grid .addWidget (sec_edit ,r ,2 )
        self .grid .addWidget (area ,r ,3 )
        self .grid .addWidget (name_edit ,r ,4 )
        self ._grid_row =r +1 
        abs_path =os.path .join (base ,rel_dir ,fname )if rel_dir else os.path .join (base ,fname )
        self ._rows .append ((abs_path ,name_edit ,area ,sec_edit ,ruta_label ))

        try :
            lbl .mousePressEvent =(lambda p =abs_path :(lambda e :self ._open_preview_window (p )))()
            if highlight :
                lbl .setToolTip ("Nuevo DDS detectado — Click to preview")
            else :
                lbl .setToolTip ("Click to preview in a window")
        except Exception :
            pass 

    def _on_dds_directory_changed (self ,changed_dir :str ):
        """Reconciliar: buscar recursivamente DDS bajo la carpeta base y añadir los que no están en UI.
        Los nuevos se muestran resaltados en amarillo.
        """
        try :
            base =self ._dds_dir if (self ._dds_dir and os.path .isdir (self ._dds_dir ))else changed_dir 
            if not base or not os.path .isdir (base ):
                return 
            existing =self ._existing_relkeys ()
            added =0 
            for root ,_dirs ,files in os .walk (base ):
                for fn in files :
                    if not fn .lower ().endswith ('.dds'):
                        continue 
                    rel_dir =os.path .relpath (root ,base )
                    if rel_dir =='.'or not rel_dir or rel_dir .strip ()=='':
                        rel_dir =''
                    key =f"{rel_dir .replace ('/','\\').lower ()}|{fn .lower ()}"
                    if key not in existing :
                        self ._add_dds_row (base ,rel_dir ,fn ,highlight =True )
                        existing .add (key )
                        added +=1 
            if added :
                self ._log (f"DDS nuevos agregados desde carpeta: {added }")
        except Exception as e :
            self ._log (f"Error manejando cambio en carpeta DDS: {e }",err =True )

    def _compute_ruta_options (self ):
        """Devuelve lista de rutas relativas ('' incluido) bajo 'textures/actors/character/slavetats'.
        Se utiliza para poblar el combo 'Ruta'.
        """
        try :

            env_dir =None 
            if self ._dds_dir and os.path .isdir (self ._dds_dir ):
                env_dir =os.path .dirname (os.path .normpath (self ._dds_dir ))
            elif getattr (self ,'_json_path',None )and os.path .isfile (self ._json_path ):
                env_dir =os.path .dirname (os.path .normpath (self ._json_path ))
            if not env_dir or not os.path .isdir (env_dir ):
                return [""]
            root =os.path .join (env_dir ,'textures','actors','character','slavetats')
            if not os.path .isdir (root ):
                return [""]
            options =set ([""])
            for r ,dirs ,_files in os .walk (root ):
                for d in dirs :
                    rel =os.path .relpath (os.path .join (r ,d ),root )
                    rel =rel .replace ('/','\\')

                    if rel and rel .strip ('. '):
                        options .add (rel )
            out =sorted (options ,key =lambda s :(0 if s ==""else 1 ,s .lower ()))
            return out or [""]
        except Exception :
            return [""]

    def _bind_preview_handlers_for_current_rows (self ):
        """Recorre las filas actuales y conecta el click del QLabel de filename
        para abrir la previsualización, si existe carpeta DDS.
        """
        try :
            if not (self ._dds_dir and os.path .isdir (self ._dds_dir )):
                return 

            for i in range (self .list_layout .count ()):
                item =self .list_layout .itemAt (i )
                w =item .widget ()if item else None 
                if not isinstance (w ,QWidget ):
                    continue 

                labels =w .findChildren (QLabel )
                for lbl in labels :
                    try :
                        text =lbl .text ().strip ()
                        if text .lower ().endswith ('.dds'):
                            abs_path =os.path .join (self ._dds_dir ,text )
                            lbl .setToolTip ("Click to preview in a window")
                            lbl .mousePressEvent =(lambda p =abs_path :(lambda e :self ._open_preview_window (p )))()
                            break 
                    except Exception :
                        continue 
        except Exception :
            pass 


class RMCreatorTab (QWidget ):
    """Create from scratch RM: build a RaceMenu script and overlays from DDS."""
    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        try :
            self .setStyleSheet ("background: transparent;")
        except Exception :
            pass 
        self ._dds_dir =None 
        self ._rows =[]
        self ._preview_windows =[]
        self ._build_ui ()

    def _build_ui (self ):
        lay =QVBoxLayout (self )
        lay .setContentsMargins (8 ,8 ,8 ,8 )
        lay .setSpacing (8 )

        title =QLabel ("CREATE FROM SCRATCH AND MODIFY — RACEMENU")
        title .setAlignment (Qt .AlignCenter )
        title .setStyleSheet ("font-size: 16px; font-weight: bold; color: #66FF66;")
        lay .addWidget (title )

        subtitle =QLabel ("Configure your PSC from a DDS container folder, or load an existing PSC to add more overlays")
        subtitle .setAlignment (Qt .AlignCenter )
        subtitle .setStyleSheet ("font-size: 12px; color: #CFCFCF;")
        lay .addWidget (subtitle )


        self .btn_select_dds =QPushButton ("DRAG AND DROP PSC OR DDS FOLDER")
        try :
            self .btn_select_dds .setCursor (Qt .PointingHandCursor )
        except Exception :
            pass 
        self .btn_select_dds .setMinimumHeight (40 )
        try :
            self .btn_select_dds .setSizePolicy (QSizePolicy .Expanding ,QSizePolicy .Fixed )
        except Exception :
            pass 
        try :
            self .btn_select_dds .setStyleSheet (self .btn_style_green )
        except Exception :
            pass 
        try :
            self .btn_select_dds .setToolTip ("Drag and drop the folder that contains your DDS files to start creating your mod, or drag an existing PSC to continue and add more DDS overlays")
        except Exception :
            pass 
        self .btn_select_dds .clicked .connect (self ._choose_dds_folder )
        lay .addWidget (self .btn_select_dds )


        self .scroll =QScrollArea ()
        self .scroll .setWidgetResizable (True )
        self .scroll .setStyleSheet ("QScrollArea { background: transparent; }")
        self .list_container =QWidget ()
        self .list_container .setStyleSheet ("background-color: rgba(40,40,48,180); border: 1px solid #444; border-radius: 6px;")
        self .list_layout =QVBoxLayout (self .list_container )
        self .list_layout .setContentsMargins (2 ,2 ,2 ,2 )
        self .list_layout .setSpacing (6 )

        # Ensure inner widgets participate in drag-and-drop by forwarding events
        try :
            self .scroll .setAcceptDrops (True )
            self .list_container .setAcceptDrops (True )
            # Forward events to the tab handlers so drops work anywhere in the tab
            self .scroll .dragEnterEvent =self .dragEnterEvent
            self .scroll .dropEvent =self .dropEvent
            self .list_container .dragEnterEvent =self .dragEnterEvent
            self .list_container .dropEvent =self .dropEvent
        except Exception :
            pass 


        try :
            self ._reset_table ()
        except Exception :
            pass 
        self .scroll .setWidget (self .list_container )
        lay .addWidget (self .scroll )


        try :
            self .setAcceptDrops (True )
        except Exception :
            pass 


        action_row =QHBoxLayout ()


        self .btn_style_gray =(
        "QPushButton {"
        " background: rgba(53,53,57,0.82);"
        " color: #E0E0E0;"
        " border: 1px solid rgba(90,90,95,0.70);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        "}"
        "QPushButton:hover { background: rgba(62,62,68,0.90); }"
        "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
        )

        # Define RM local styles and apply green to the main select button
        try :
            self .btn_style_green =(
            "QPushButton {"
            " background: rgba(76,175,80,0.25);"
            " color: #FFFFFF;"
            " border: 1px solid rgba(76,175,80,0.80);"
            " border-radius: 4px;"
            " padding: 6px 10px;"
            "}"
            "QPushButton:hover { background: rgba(76,175,80,0.35); }"
            "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
            )
            self .btn_style_blue =(
            "QPushButton {"
            " background: rgba(0, 188, 212, 0.35);"
            " color: #E0F7FA;"
            " border: 1px solid rgba(0, 188, 212, 0.70);"
            " border-radius: 4px;"
            " padding: 6px 10px;"
            "}"
            "QPushButton:hover { background: rgba(0, 188, 212, 0.55); }"
            "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
            )
            if hasattr (self ,'btn_select_dds') and self .btn_select_dds is not None :
                self .btn_select_dds .setStyleSheet (self .btn_style_green )
        except Exception :
            pass 

        self .btn_refresh_rm =QPushButton ("Clean All")
        try :
            self .btn_refresh_rm .setCursor (Qt .PointingHandCursor )
            self .btn_refresh_rm .setToolTip ("Clear and reset this tab")
        except Exception :
            pass 
        self .btn_refresh_rm .clicked .connect (self .refresh_tab )
        action_row .addWidget (self .btn_refresh_rm )


        self .btn_backups =QPushButton ("Backups")
        self .btn_backups .setEnabled (False )
        try :
            self .btn_backups .setToolTip ("Manage .psc backups (create/restore)")
        except Exception :
            pass 

        self .btn_backups .clicked .connect (self ._on_backups_clicked )
        self .btn_export_psc =QPushButton ("Export .psc")
        self .btn_export_psc .setEnabled (False )
        try :
            self .btn_export_psc .setToolTip ("Export RaceMenu script (.psc) into the DDS parent folder → scripts/Source")
        except Exception :
            pass 
        self .btn_export_psc .clicked .connect (self ._export_psc )

        self .btn_create_mod =QPushButton ("Create Mod zip")
        self .btn_create_mod .setEnabled (False )
        try :
            self .btn_create_mod .setToolTip ("Create Overlays structure and package (7z/zip)")
        except Exception :
            pass 
        self .btn_create_mod .clicked .connect (self ._create_mod_package )

        self .btn_clear_term =QPushButton ("Clear terminal")
        self .btn_clear_term .clicked .connect (self ._clear_terminal )


        self .btn_psc_example =QPushButton ("PSC example")
        self .btn_psc_example .setEnabled (False )
        try :
            self .btn_psc_example .setToolTip ("Generate a PSC preview in the terminal (does not save a file)")
        except Exception :
            pass 
        self .btn_psc_example .clicked .connect (self ._print_psc_example )

        for b in (self .btn_refresh_rm ,self .btn_backups ,self .btn_export_psc ,self .btn_create_mod ,self .btn_clear_term ,self .btn_psc_example ):
            try :
                b .setStyleSheet (self .btn_style_gray )
            except Exception :
                pass 

        try :
            self .btn_refresh_rm .setStyleSheet (self .btn_style_blue )
        except Exception :
            pass 
        try :
            self .btn_clear_term .setStyleSheet (self .btn_style_blue )
        except Exception :
            pass 

        action_row .addWidget (self .btn_backups )
        action_row .addStretch (1 )
        action_row .addWidget (self .btn_psc_example )
        action_row .addWidget (self .btn_export_psc )
        action_row .addWidget (self .btn_create_mod )
        action_row .addWidget (self .btn_clear_term )
        lay .addLayout (action_row )


        lay .addWidget (QLabel ("Output:"))
        self .output_terminal =QTextEdit ()
        self .output_terminal .setReadOnly (True )
        self .output_terminal .setStyleSheet (
        "QTextEdit { background-color: #1A1A1C; color: #66FF66; border: 1px solid #3A3A3F; border-radius: 4px; font-family: Consolas, 'Courier New', monospace; font-size: 12px; }"
        )
        lay .addWidget (self .output_terminal )

    def _reset_table (self ):
        """Crea o reinicia la tabla principal (encabezados y grid) para RM Creator.
        Columnas: 0=File, 1=Path, 2=Type, 3=Name
        """
        try :
            # Limpiar widgets previos del list_layout
            try :
                for i in reversed (range (self .list_layout .count ())) :
                    item =self .list_layout .itemAt (i )
                    w =item .widget ()
                    if w is not None :
                        w .setParent (None )
            except Exception :
                pass 

            # Contenedor de la tabla y grid
            table =QWidget ()
            grid =QGridLayout (table )
            grid .setContentsMargins (6 ,6 ,6 ,6 )
            grid .setHorizontalSpacing (10 )
            grid .setVerticalSpacing (6 )

            # Encabezados
            h_file =QLabel ("File")
            h_path =QLabel ("Path")
            h_type =QLabel ("Type")
            h_name =QLabel ("Name")
            try :
                h_style ="font-weight: 700; color: #A5D6A7;"
                h_file .setStyleSheet (h_style )
                h_path .setStyleSheet (h_style )
                h_type .setStyleSheet (h_style )
                h_name .setStyleSheet (h_style )
            except Exception :
                pass 

            grid .addWidget (h_file ,0 ,0 )
            grid .addWidget (h_path ,0 ,1 )
            grid .addWidget (h_type ,0 ,2 )
            grid .addWidget (h_name ,0 ,3 )

            try :
                grid .setColumnStretch (0 ,2 )
                grid .setColumnStretch (1 ,2 )
                grid .setColumnStretch (2 ,1 )
                grid .setColumnStretch (3 ,2 )
            except Exception :
                pass 

            self .grid =grid 
            self ._grid_row =1 

            self .list_layout .addWidget (table )
        except Exception as e :
            try :
                self ._log (f"Error creando tabla: {e }",err =True )
            except Exception :
                pass 

    def refresh_tab (self ):
        """Resets the tab to its initial state."""
        try :
            self ._dds_dir =None 
            self ._rows .clear ()
            self ._section_override =None 
            self ._loaded_psc_path =None 


            while self .list_layout .count ():
                itm =self .list_layout .takeAt (0 )
                w =itm .widget ()
                if w :
                    try :
                        w .setParent (None )
                    except Exception :
                        pass 


            self ._reset_table ()

            self .output_terminal .clear ()
            self ._set_buttons (False )
            # Also disable Backups button on full reset
            try :
                if hasattr (self ,'btn_backups')and self .btn_backups is not None :
                    self .btn_backups .setEnabled (False )
                    try :
                        self .btn_backups .setStyleSheet (self .btn_style_gray )
                    except Exception :
                        pass 
            except Exception :
                pass 

            for win in self ._preview_windows :
                win .close ()
            self ._preview_windows .clear ()

            self ._log ("RM Creator tab has been refreshed.")
        except Exception as e :
            self ._log (f"Error refreshing RM Creator tab: {e }",err =True )


    def dragEnterEvent (self ,event ):
        try :
            if event .mimeData ().hasUrls ():
                for url in event .mimeData ().urls ():
                    p =url .toLocalFile ()
                    if os.path .isdir (p ):
                        event .acceptProposedAction ();return 
                    ext =os.path .splitext (p )[1 ].lower ()
                    if ext in ('.psc','.dds'):
                        event .acceptProposedAction ();return 
            event .ignore ()
        except Exception :
            event .ignore ()

    def dropEvent (self ,event ):
        try :
            for url in event .mimeData ().urls ():
                p =url .toLocalFile ()
                if os.path .isdir (p ):
                    self ._load_dds_folder (p );return 
                ext =os.path .splitext (p )[1 ].lower ()
                if ext =='.psc':
                    self ._load_psc_file (p );return 
                if ext =='.dds':
                    self ._load_dds_folder (os.path .dirname (p ));return 
        except Exception as e :
            self ._log (f"Drop error: {e }",err =True )


    def _choose_dds_folder (self ):
        try :
            base =QFileDialog .getExistingDirectory (self ,"Select folder with DDS")
            if base :
                self ._load_dds_folder (base )
            else :
                self ._log ("DDS folder selection cancelled")
        except Exception as e :
            self ._log (f"Error selecting DDS folder: {e }",err =True )

    def _load_dds_folder (self ,base :str ):
        try :

            files =[]
            for root ,_dirs ,fnames in os .walk (base ):
                for f in fnames :
                    if f .lower ().endswith ('.dds'):
                        files .append (os.path .join (root ,f ))
            files .sort (key =lambda p :p .lower ())
            if not files :
                self ._log ("No DDS found in selected folder",err =True )
                return 

            while self .list_layout .count ():
                itm =self .list_layout .takeAt (0 )
                w =itm .widget ()
                if w :
                    try :
                        w .setParent (None )
                    except Exception :
                        pass 

            self ._reset_table ()
            self ._rows .clear ()
            self ._dds_dir =base 
            for fpath in files :
                # File label (file name only)
                rel_to_base =os.path .relpath (fpath ,start =base )
                try :
                    base_name_disp =os.path .basename (fpath )
                except Exception :
                    base_name_disp =rel_to_base 
                file_label =QLabel (base_name_disp )
                file_label .setStyleSheet ("color:#F0F0F0;")
                try :
                    file_label .mousePressEvent =lambda e ,p =fpath :self ._open_preview_window (p )
                    file_label .setToolTip (fpath )
                    file_label .setWordWrap (False )
                    file_label .setSizePolicy (QSizePolicy .Expanding ,QSizePolicy .Fixed )
                except Exception :
                    pass 

                # Path (show only the last directory name under the selected base)
                try :
                    rel_dir =os.path .relpath (os.path .dirname (fpath ),base )
                except Exception :
                    rel_dir ="."
                if rel_dir =='.'or not rel_dir or rel_dir .strip ()=='':
                    # If file is directly under base, show the base (matrix) folder name
                    try :
                        rel_dir_disp =os.path .basename (os.path .normpath (base ))
                    except Exception :
                        rel_dir_disp =os.path .basename (base )
                else :
                    try :
                        rel_dir_disp =os.path .basename (rel_dir )
                    except Exception :
                        rel_dir_disp =rel_dir 
                ruta_label =QLabel (rel_dir_disp )
                try :
                    ruta_label .setStyleSheet ("color:#C0C0C0;")
                    ruta_label .setToolTip ("Double-click to open this folder")
                    def _on_dbl_open_path (e ,_ruta =rel_dir ,_base =base ):
                        try :
                            target =_base if not _ruta else os.path .join (_base ,_ruta )
                            if os.path .isdir (target ):
                                try :
                                    os .startfile (target )
                                    self ._log (f"Opening folder: {target }")
                                except Exception :
                                    subprocess .Popen (['explorer',target ])
                                    self ._log (f"Opening folder (fallback): {target }")
                            else :
                                self ._log (f"Folder not found: {target }",err =True )
                        except Exception as ex :
                            self ._log (f"Open folder error: {ex }",err =True )
                    ruta_label .mouseDoubleClickEvent =_on_dbl_open_path 
                except Exception :
                    pass 

                type_combo =QComboBox ()
                type_combo .addItems (["BodyPaint","Warpaint","HandPaint","FeetPaint","FacePaint"])
                type_combo .setMinimumWidth (180 )
                # Disable mouse wheel from changing selection accidentally
                try :
                    type_combo .wheelEvent =lambda e :e .ignore ()
                    type_combo .setToolTip ("Scroll deshabilitado: haga clic para abrir y seleccione una opción")
                except Exception :
                    pass 
                name_edit =QLineEdit (os.path .splitext (os.path .basename (fpath ))[0 ])
                name_edit .setStyleSheet ("color:#E8FFE8;")
                try :
                    name_edit .setSizePolicy (QSizePolicy .Expanding ,QSizePolicy .Fixed )
                except Exception :
                    pass 

                r =getattr (self ,'_grid_row',1 )
                try :
                    self .grid .addWidget (file_label ,r ,0 )
                    self .grid .addWidget (ruta_label ,r ,1 )
                    self .grid .addWidget (type_combo ,r ,2 )
                    self .grid .addWidget (name_edit ,r ,3 )
                except Exception :
                    pass 
                self ._grid_row =r +1 
                # Keep first three for compatibility with _build_psc_content; Path label is extra
                self ._rows .append ((fpath ,name_edit ,type_combo ,ruta_label ))

            self .list_layout .addStretch (1 )

            self ._set_buttons (True )
            self ._log (f"Loaded DDS folder: {base }")
            try :
                cur =self .output_terminal .textColor ()
                self .output_terminal .setTextColor (QColor('#00BFFF'))
                self .output_terminal .append ("A SET OF DDS HAS BEEN LOADED AND IS READY TO CONFIGURE THE PSC. REMEMBER IT IS BETTER TO KEEP ALL DDS IN THE SAME FOLDER")
                self .output_terminal .setTextColor (cur )
            except Exception :
                pass 
            # In DDS mode, keep Create Mod disabled until PSC is exported
            try :
                if hasattr (self ,'btn_create_mod')and self .btn_create_mod is not None :
                    self .btn_create_mod .setEnabled (False )
                    try :
                        self .btn_create_mod .setStyleSheet (self .btn_style_gray )
                    except Exception :
                        pass 
            except Exception :
                pass 
        except Exception as e :
            self ._log (f"Error loading DDS folder: {e }",err =True )

    def _set_buttons (self ,on :bool ):
        try :
            for b in (getattr (self ,'btn_export_psc',None ),getattr (self ,'btn_create_mod',None ),getattr (self ,'btn_psc_example',None )):
                if b is None :
                    continue 
                b .setEnabled (on )
                try :
                    b .setStyleSheet (self .btn_style_green if on else self .btn_style_gray )
                except Exception :
                    pass 
        except Exception :
            pass 

    def _open_preview_window (self ,path :str ):
        try :
            win =DdsPreviewWindow (path ,None ,log_fn =self ._log )
            self ._preview_windows .append (win )
            win .show ();win .raise_ ();win .activateWindow ()
        except Exception as e :
            self ._log (f"Error abriendo vista previa: {e }",err =True )

    def _current_section (self )->str :
        try :

            if getattr (self ,'_section_override',None ):
                return self ._section_override 

            if self ._dds_dir :
                base =os.path .basename (os.path .normpath (self ._dds_dir ))
                return base or "MyRMOverlays"

            return "MyRMOverlays"
        except Exception :
            return "MyRMOverlays"

    def _export_psc (self ):
        try :
            # If a PSC is loaded, overwrite it in place (PSC mode). Otherwise use DDS mode behavior.
            loaded_psc =getattr (self ,'_loaded_psc_path',None )
            if loaded_psc and os.path .isfile (loaded_psc ):
                # Determine section name from override or filename
                try :
                    # Prefer the real Overlays container if available
                    section =getattr (self ,'_psc_overlays_folder_name',None ) or getattr (self ,'_section_override',None ) or os.path .splitext (os.path .basename (loaded_psc ))[0 ]
                except Exception :
                    section =self ._current_section ()

                psc_content =self ._build_psc_content (section )
                # Write to same PSC path
                with open (loaded_psc ,'w',encoding ='utf-8')as f :
                    f .write ("\n".join (psc_content ))
                self ._log (f"PSC actualizado → {loaded_psc }")

                # Backup next to it in Backups folder
                try :
                    scripts_dir =os.path .dirname (loaded_psc )
                    bdir =os.path .join (scripts_dir ,'Backups')
                    os .makedirs (bdir ,exist_ok =True )
                    base_name =os.path .splitext (os.path .basename (loaded_psc ))[0 ]
                    import time as _t 
                    ts =_t .strftime ('%Y%m%d_%H%M%S')
                    bpath =os.path .join (bdir ,f"{base_name }_{ts }.psc")
                    shutil .copy2 (loaded_psc ,bpath )
                    try :
                        if hasattr (self ,'output_terminal')and self .output_terminal is not None :
                            cur =self .output_terminal .textColor ()
                            self .output_terminal .setTextColor (QColor('#00BFFF'))
                            self .output_terminal .append ("A BACKUP HAS BEEN CREATED OF THE PSC")
                            self .output_terminal .setTextColor (cur )
                    except Exception :
                        pass 
                except Exception as e :
                    self ._log (f"[Backups] Error creating automatic backup: {e }",True )

                try :
                    if hasattr (self ,'btn_backups')and self .btn_backups is not None :
                        self .btn_backups .setEnabled (True )
                        try :
                            self .btn_backups .setStyleSheet (self .btn_style_green )
                        except Exception :
                            pass 
                except Exception :
                    pass 

                self ._log ("— — — Generated PSC — — —")
                for line in psc_content :
                    self ._log (line )
                try :
                    os .startfile (os.path .dirname (loaded_psc ))
                except Exception :
                    subprocess .Popen (['explorer',os.path .dirname (loaded_psc )])
                try :
                    if hasattr (self ,'output_terminal')and self .output_terminal is not None :
                        cur =self .output_terminal .textColor ()
                        self .output_terminal .setTextColor (QColor('#00BFFF'))
                        self .output_terminal .append ("THE PSC HAS BEEN CREATED WITH EVERYTHING")
                        self .output_terminal .setTextColor (cur )
                except Exception :
                    pass 
                return 

            # DDS mode (no PSC loaded): original flow, exporting to DDS parent/scripts/Source
            if not self ._dds_dir or not os.path .isdir (self ._dds_dir ):
                self ._log ("Selecciona primero una carpeta con DDS.",err =True )
                return 
            env_dir =os.path .dirname (os.path .normpath (self ._dds_dir ))
            section =self ._current_section ()
            scripts_dir =os.path .join (env_dir ,'scripts','Source')
            os .makedirs (scripts_dir ,exist_ok =True )

            psc_content =self ._build_psc_content (section )
            out_psc =os.path .join (scripts_dir ,f"{section }.psc")
            with open (out_psc ,'w',encoding ='utf-8')as f :
                f .write ("\n".join (psc_content ))
            self ._log (f"PSC creado → {out_psc }")

            # Automatic backup of the generated PSC (timestamped) + blue confirmation message
            try :
                bdir =os.path .join (scripts_dir ,'Backups')
                os .makedirs (bdir ,exist_ok =True )
                base_name =os.path .splitext (os.path .basename (out_psc ))[0 ]
                import time as _t 
                ts =_t .strftime ('%Y%m%d_%H%M%S')
                bpath =os.path .join (bdir ,f"{base_name }_{ts }.psc")
                shutil .copy2 (out_psc ,bpath )
                try :
                    if hasattr (self ,'output_terminal')and self .output_terminal is not None :
                        cur =self .output_terminal .textColor ()
                        self .output_terminal .setTextColor (QColor('#00BFFF'))
                        self .output_terminal .append ("A BACKUP HAS BEEN CREATED OF THE PSC")
                        self .output_terminal .setTextColor (cur )
                except Exception :
                    pass 
            except Exception as e :
                self ._log (f"[Backups] Error creating automatic backup: {e }",True )

            try :
                self ._loaded_psc_path =out_psc 
                if hasattr (self ,'btn_backups')and self .btn_backups is not None :
                    self .btn_backups .setEnabled (True )
                    try :
                        self .btn_backups .setStyleSheet (self .btn_style_green )
                    except Exception :
                        pass 
                # After exporting PSC in DDS mode, allow creating the Mod zip
                if hasattr (self ,'btn_create_mod')and self .btn_create_mod is not None :
                    self .btn_create_mod .setEnabled (True )
                    try :
                        self .btn_create_mod .setStyleSheet (self .btn_style_green )
                    except Exception :
                        pass 
            except Exception :
                pass 

            self ._log ("— — — Generated PSC — — —")
            for line in psc_content :
                self ._log (line )
            try :
                os .startfile (scripts_dir )
            except Exception :
                subprocess .Popen (['explorer',scripts_dir ])
            # Blue success message confirming PSC creation
            try :
                if hasattr (self ,'output_terminal')and self .output_terminal is not None :
                    cur =self .output_terminal .textColor ()
                    self .output_terminal .setTextColor (QColor('#00BFFF'))
                    self .output_terminal .append ("THE PSC HAS BEEN CREATED WITH EVERYTHING")
                    self .output_terminal .setTextColor (cur )
            except Exception :
                pass 
        except Exception as e :
            self ._log (f"No se pudo crear PSC: {e }",err =True )

    def _load_psc_file (self ,path :str ):
        try :
            if not os.path .isfile (path ):
                self ._log (f"PSC no encontrado: {path }",err =True );return 
            with open (path ,'r',encoding ='utf-8',errors ='ignore')as f :
                content =f .read ().splitlines ()
            self ._log (f"— — — Loaded PSC: {path } — — —")
            self ._loaded_psc_path =path 
            try :
                cur =self .output_terminal .textColor ()
                self .output_terminal .setTextColor (QColor('#00BFFF'))
                self .output_terminal .append ("A PRECONFIGURED PSC HAS BEEN LOADED")
                self .output_terminal .setTextColor (cur )
            except Exception :
                pass 
            for line in content :
                self ._log (line )

            import re 
            sec =None 
            for line in content :
                m =re .match (r"\s*scriptName\s+([A-Za-z0-9_]+)\s+extends",line )
                if m :
                    sec =m .group (1 )
                    break 
            if not sec :
                sec =os.path .splitext (os.path .basename (path ))[0 ]

            self ._section_override =sec 
            self ._log (f"Section override: {self ._section_override }")


            add_re =re .compile (r"Add(Warpaint|BodyPaint|FacePaint|HandPaint|FeetPaint)\(\s*\"([^\"]+)\"\s*,\s*\"([^\"]+)\"\s*\)")
            entries =[]
            for line in content :
                m =add_re .search (line )
                if not m :
                    continue 
                typ ,disp_name ,rel =m .group (1 ),m .group (2 ),m .group (3 )
                rel_norm =rel .replace ('/','\\')
                parts =[p for p in rel_norm .split ('\\')if p ]
                lower =[p .lower ()for p in parts ]
                section =None 
                if 'overlays'in lower :
                    idx =lower .index ('overlays')
                    if idx +1 <len (parts ):
                        section =parts [idx +1 ]
                basename =parts [-1 ]if parts else os.path .basename (rel_norm )
                # Last directory right before the filename (e.g., "Face" in Overlays\SFO\Face\<file>.dds)
                try :
                    lastdir =parts [-2 ]if len (parts )>=2 else ''
                except Exception :
                    lastdir =''
                entries .append ({'type':typ ,'name':disp_name ,'section':section ,'basename':basename ,'lastdir':lastdir })


            if entries :

                modroot =os.path .abspath (os.path .join (os.path .dirname (path ),os .pardir ,os .pardir ))

                section_name =next ((e ['section']for e in entries if e .get ('section')),None )
                if section_name :

                    overlays_base =os.path .join (modroot ,'textures','actors','character')
                    candidate =os.path .join (overlays_base ,'overlays',section_name )
                    if not os.path .isdir (candidate ):

                        try :
                            caps =[d for d in os .listdir (overlays_base )if os.path .isdir (os.path .join (overlays_base ,d ))]
                        except Exception :
                            caps =[]
                        overlays_dirname =next ((d for d in caps if d .lower ()=='overlays'),None )
                        if overlays_dirname :
                            candidate =os.path .join (overlays_base ,overlays_dirname ,section_name )
                    if not os.path .isdir (candidate ):

                        try :
                            wanted ={e ['basename'].lower ()for e in entries if e .get ('basename')}
                        except Exception :
                            wanted =set ()
                        found_parent =None 
                        try :
                            scan_root =os.path .join (modroot ,'textures')
                            for root ,dirs ,files in os .walk (scan_root ):
                                for f in files :
                                    if f .lower ()in wanted and f .lower ().endswith ('.dds'):
                                        found_parent =root 
                                        break 
                                if found_parent :
                                    break 
                        except Exception :
                            found_parent =None 
                        if found_parent :
                            candidate =found_parent 

                    if os.path .isdir (candidate ):
                        try :
                            self ._log (f"DDS folder resolved: {candidate }")
                        except Exception :
                            pass 
                        # Normalize to Overlays/<container> level and remember it
                        try :
                            cand_norm =os.path .normpath (candidate )
                            parts =cand_norm .split (os .sep )
                            # find 'overlays' (case-insensitive) and pick the immediate next segment as container
                            idx =next ((i for i ,p in enumerate (parts )if p .lower ()=='overlays'),-1 )
                            if idx >=0 and idx +1 <len (parts ):
                                container =parts [idx +1 ]
                                root =os.path .join (*parts [:idx +2 ])
                            else :
                                # fallback to the candidate itself
                                container =os.path .basename (cand_norm )
                                root =cand_norm 
                            self ._overlays_source_dir =root 
                            self ._psc_overlays_folder_name =container 
                        except Exception :
                            self ._overlays_source_dir =candidate 
                            try :
                                self ._psc_overlays_folder_name =os.path .basename (os.path .normpath (candidate ))
                            except Exception :
                                pass 
                        self ._load_dds_folder (candidate )
                    else :
                        self ._log ("The DDS folder could not be located from the PSC. Check the structure textures/actors/character/Overlays/<Section>.",err =True )
                else :
                    self ._log ("The 'Overlays' folder was not found in the PSC paths.",err =True )


                by_base ={e ['basename'].lower ():e for e in entries if e .get ('basename')}
                for abs_path ,name_edit ,type_combo ,*rest in getattr (self ,'_rows',[]):
                    base =os.path .basename (abs_path ).lower ()
                    in_psc =base in by_base 
                    e =by_base .get (base )
                    # Update Name and Type if found in PSC
                    if in_psc and e is not None :
                        try :
                            name_edit .setText (e ['name'])
                        except Exception :
                            pass 
                        try :
                            idx =type_combo .findText (e ['type'],Qt .MatchFixedString )
                            if idx >=0 :
                                type_combo .setCurrentIndex (idx )
                        except Exception :
                            pass 
                    # Path column should always show the last folder that contains the DDS
                    try :
                        ruta_label =rest [0 ]if rest else None 
                        if ruta_label is not None :
                            parent_dir =os.path .basename (os.path .dirname (abs_path ))
                            ruta_label .setText (parent_dir )
                    except Exception :
                        pass 

                    # Highlight items NOT present in PSC as new (yellowish)
                    if not in_psc :
                        try :
                            # Subtle amber/yellow styles to indicate "new"
                            name_edit .setStyleSheet ("color:#FFD54F;")
                        except Exception :
                            pass 
                        try :
                            type_combo .setStyleSheet ("QComboBox { color:#FFD54F; }")
                        except Exception :
                            pass 
                        try :
                            if ruta_label is not None :
                                ruta_label .setStyleSheet ("color:#FFD54F;")
                        except Exception :
                            pass 

            self ._set_buttons (True )
            try :
                self .btn_backups .setEnabled (True )
                self .btn_backups .setStyleSheet (self .btn_style_green )
            except Exception :
                pass 
            # When a PSC is loaded, enable Create Mod immediately
            try :
                if hasattr (self ,'btn_create_mod')and self .btn_create_mod is not None :
                    self .btn_create_mod .setEnabled (True )
                    try :
                        self .btn_create_mod .setStyleSheet (self .btn_style_green )
                    except Exception :
                        pass 
            except Exception :
                pass 
        except Exception as e :
            self ._log (f"Error leyendo PSC: {e }",err =True )

    def _on_backups_clicked (self ):
        try :
            self ._log ("[Backups] Click recibido, abriendo gestor...")
        except Exception :
            pass 
        try :
            QTimer .singleShot (0 ,self ._open_backup_manager )
        except Exception as e :
            try :
                self ._log (f"[Backups] Error scheduling open: {e }",err =True )
            except Exception :
                pass 

    def _open_backup_manager (self ):
        try :
            try :
                self ._log ("[Backups] _open_backup_manager()")
            except Exception :
                pass 
            path =getattr (self ,'_loaded_psc_path',None )
            if not path or not os.path .isfile (path ):
                self ._log ("Primero abre un .psc para gestionar respaldos.",err =True )
                return 

            win =BackupManagerWindow (path ,None ,log_fn =self ._log )
            try :
                self ._preview_windows .append (win )
            except Exception :

                try :
                    self ._child_windows .append (win )
                except Exception :
                    self ._child_windows =[win ]
            win .show ();win .raise_ ();win .activateWindow ()
        except Exception as e :
            try :
                self ._log (f"Error opening backup manager: {e }",err =True )
            except Exception :
                pass 
            try :
                QMessageBox .critical (self ,"Backups",f"The backup manager could not be opened..\n\n{e }")
            except Exception :
                pass 

    def _build_psc_content (self ,section :str ):

        warpaint_lines =[]
        body_lines =[]
        hand_lines =[]
        feet_lines =[]
        face_lines =[]
        for abs_path ,name_edit ,area_combo ,*_ in self ._rows :
            name =name_edit .text ().strip ()or os.path .splitext (os.path .basename (abs_path ))[0 ]
            area =(area_combo .currentText ()or 'BodyPaint').strip ()

            rel_tex =f"Actors\\\\Character\\\\Overlays\\\\{section }\\\\{os.path .basename (abs_path )}"
            sel =area .lower ()
            if sel =='warpaint':
                warpaint_lines .append (f'    self.AddWarpaint("{name }", "{rel_tex }")')
            elif sel =='bodypaint':
                body_lines .append (f'    self.AddBodyPaint("{name }", "{rel_tex }")')
            elif sel =='handpaint':
                hand_lines .append (f'    self.AddHandPaint("{name }", "{rel_tex }")')
            elif sel =='feetpaint':
                feet_lines .append (f'    self.AddFeetPaint("{name }", "{rel_tex }")')
            elif sel =='facepaint':
                face_lines .append (f'    self.AddFacePaint("{name }", "{rel_tex }")')

        lines =[f"scriptName {section } extends RaceMenuBase"]

        if warpaint_lines :
            lines +=[
            "",
            "Event OnWarpaintRequest()",
            *warpaint_lines ,
            "EndEvent",
            ]
        if body_lines :
            lines +=[
            "",
            "Event OnBodyPaintRequest()",
            *body_lines ,
            "EndEvent",
            ]
        if face_lines :
            lines +=[
            "",
            "Event OnFacePaintRequest()",
            *face_lines ,
            "EndEvent",
            ]
        if hand_lines :
            lines +=[
            "",
            "Event OnHandPaintRequest()",
            *hand_lines ,
            "EndEvent",
            ]
        if feet_lines :
            lines +=[
            "",
            "Event OnFeetPaintRequest()",
            *feet_lines ,
            "EndEvent",
            ]
        return lines 

    def _print_psc_example (self ):
        try :
            if not self ._dds_dir or not os.path .isdir (self ._dds_dir ):

                section ="MyRMOverlays"
                example =[
                f"scriptName {section } extends RaceMenuBase",
                "",
                "; Add your events here (OnBodyPaintRequest, etc.)",
                ]
            else :
                section =self ._current_section ()
                example =self ._build_psc_content (section )
            # Header and example in orange
            try :
                if hasattr (self ,'output_terminal')and self .output_terminal is not None :
                    cur =self .output_terminal .textColor ()
                    self .output_terminal .setTextColor (QColor('#FFD54F'))
                    self .output_terminal .append ("— — — PSC EXAMPLE — — —")
                    for line in example :
                        self .output_terminal .append (line )
                    # Append confirmation line in blue
                    self .output_terminal .setTextColor (QColor('#00BFFF'))
                    self .output_terminal .append ("A PSC PREVIEW HAS BEEN PERFORMED")
                    # Restore previous color
                    self .output_terminal .setTextColor (cur )
            except Exception :
                # Fallback to normal log if color handling fails
                self ._log ("— — — PSC EXAMPLE — — —")
                for line in example :
                    self ._log (line )
        except Exception as e :
            self ._log (f"Could not generate PSC example: {e }",err =True )

    def _gather_json_data (self ):
        """Collect rows into JSON entries for SlaveTats pack.
        Uses current section and optional last-folder shown in Path column.
        Structure per item: {name, section, texture, area}
        """
        try :
            data =[]
            for abs_path ,name_edit ,area_combo ,*rest in self ._rows :
                fname =os.path .basename (abs_path )
                row_section =self ._current_section ()

                # Optional last folder from Path column (ruta_label)
                ruta =''
                try :
                    ruta_label =rest [0 ]if rest else None 
                    ruta =(ruta_label .text ()if ruta_label is not None else '') .strip () .strip ('\\/')
                    if ruta and row_section and ruta .lower ()==row_section .lower ():
                        ruta =''
                except Exception :
                    ruta =''

                texture_path =f"{row_section }\\{fname }"if not ruta else f"{row_section }\\{ruta }\\{fname }"

                data .append ({
                "name":name_edit .text () .strip ()or os.path .splitext (fname )[0 ],
                "section":row_section ,
                "texture":texture_path ,
                "area":(area_combo .currentText ()or 'BodyPaint'),
                })
            return data 
        except Exception :
            return []

    def _create_mod_package (self ):
        try :
            # Determine mode and env_dir
            section =self ._current_section ()
            dds_mode =bool (self ._dds_dir and os.path .isdir (self ._dds_dir ))
            psc_mode =bool (getattr (self ,'_loaded_psc_path',None )and os.path .isfile (self ._loaded_psc_path ))
            if not dds_mode and not psc_mode :
                self ._log ("Select a folder with DDS first or load a .psc.",err =True )
                return 

            if dds_mode :
                env_dir =os.path .dirname (os.path .normpath (self ._dds_dir ))
                scripts_dir =os.path .join (env_dir ,'scripts','Source')
                os .makedirs (scripts_dir ,exist_ok =True )
                psc_name =f"{section }.psc"
                psc_path =os.path .join (scripts_dir ,psc_name )
                # Ensure PSC exists; generate if missing
                if not os.path .isfile (psc_path ):
                    try :
                        content =self ._build_psc_content (section )
                        with open (psc_path ,'w',encoding ='utf-8')as f :
                            f .write ("\n".join (content ))
                        self ._log (f"PSC creado → {psc_path }")
                    except Exception as e :
                        self ._log (f"No se pudo crear PSC: {e }",err =True )
                        return 
                overlays_source =self ._dds_dir 
            else :
                # PSC mode packs from existing mod folder
                psc_path =self ._loaded_psc_path 
                scripts_dir =os.path .dirname (psc_path )
                env_dir =os.path .dirname (os.path .dirname (scripts_dir ))
                # Try to use overlays folder actually found during PSC load; fallback to search
                overlays_source =getattr (self ,'_overlays_source_dir',None )
                if not overlays_source or not os.path .isdir (overlays_source ):
                    candidates =[
                    os.path .join (env_dir ,'textures','actors','character','Overlays',section ),
                    os.path .join (env_dir ,'Textures','actors','character','Overlays',section ),
                    ]
                    overlays_source =next ((c for c in candidates if os.path .isdir (c )),None )
                    # As a last resort, scan textures tree for any folder that contains the PSC-listed DDS
                    if not overlays_source :
                        try :
                            textures_root =os.path .join (env_dir ,'textures')
                            if os.path .isdir (textures_root ):
                                overlays_source =None 
                        except Exception :
                            overlays_source =None 
                    if overlays_source :
                        try :
                            # Normalize to Overlays/<container>
                            cand_norm =os.path .normpath (overlays_source )
                            parts =cand_norm .split (os .sep )
                            idx =next ((i for i ,p in enumerate (parts )if p .lower ()=='overlays'),-1 )
                            if idx >=0 and idx +1 <len (parts ):
                                container =parts [idx +1 ]
                                root =os.path .join (*parts [:idx +2 ])
                            else :
                                container =os.path .basename (cand_norm )
                                root =cand_norm 
                            self ._overlays_source_dir =root 
                            self ._psc_overlays_folder_name =container 
                        except Exception :
                            self ._overlays_source_dir =overlays_source 
                            try :
                                self ._psc_overlays_folder_name =os.path .basename (os.path .normpath (overlays_source ))
                            except Exception :
                                pass 
                if not overlays_source or not os.path .isdir (overlays_source ):
                    self ._log ("Overlays folder for the loaded PSC not found.",err =True )
                    return 

            # Build staging folder
            build_root =os.path .join (env_dir ,f"RACEMENU_BUILD_{section }")
            # In PSC mode, derive the Overlays container from the real DDS container, never the script name
            try :
                if dds_mode :
                    # DDS mode: use the base folder that the user selected
                    folder_name =os.path .basename (os.path .normpath (self ._dds_dir )) if getattr (self ,'_dds_dir',None ) else section 
                else :
                    folder_name =getattr (self ,'_psc_overlays_folder_name',None )
                    if not folder_name and overlays_source :
                        # Derive from overlays_source path: Overlays/<container>
                        cand_norm =os.path .normpath (overlays_source )
                        parts =cand_norm .split (os .sep )
                        idx =next ((i for i ,p in enumerate (parts )if p .lower ()=='overlays'),-1 )
                        if idx >=0 and idx +1 <len (parts ):
                            folder_name =parts [idx +1 ]
                        else :
                            folder_name =os.path .basename (cand_norm )
                if not folder_name :
                    folder_name ='MyRMOverlays'
            except Exception :
                folder_name ='MyRMOverlays' 
            overlays_dst =os.path .join (build_root ,'textures','actors','character','Overlays',folder_name )
            scripts_dst_dir =os.path .join (build_root ,'scripts','Source')
            try :
                os .makedirs (overlays_dst ,exist_ok =True )
                os .makedirs (scripts_dst_dir ,exist_ok =True )
            except Exception as e :
                self ._log (f"Error creando estructura temporal: {e }",err =True )
                return 

            # Copy Overlays (entire DDS folder into <SECTION>)
            try :
                copied =0 
                for root ,_dirs ,files in os .walk (overlays_source ):
                    rel =os.path .relpath (root ,overlays_source )
                    dst =overlays_dst if rel in ('.','')else os.path .join (overlays_dst ,rel )
                    os .makedirs (dst ,exist_ok =True )
                    for f in files :
                        srcf =os.path .join (root ,f )
                        shutil .copy2 (srcf ,os.path .join (dst ,f ))
                        copied +=1 
                self ._log (f"Copiados {copied } archivos a Overlays/{folder_name }")
            except Exception as e :
                self ._log (f"Error copiando DDS/Overlays: {e }",err =True )
                return 

            # Copy PSC
            try :
                shutil .copy2 (psc_path ,os.path .join (scripts_dst_dir ,os.path .basename (psc_path )))
            except Exception as e :
                self ._log (f"Error copiando PSC: {e }",err =True )
                return 

            # Make zip: RACEMENU <PSCNAME>.zip in env_dir
            psc_base =os.path .splitext (os.path .basename (psc_path ))[0 ]
            archive_zip =os.path .join (env_dir ,f"RACEMENU {psc_base }.zip")

            def _find_7z_exe ():
                candidates =[
                '7z','7z.exe',
                r"C:\\Program Files\\7-Zip\\7z.exe",
                r"C:\\Program Files (x86)\\7-Zip\\7z.exe",
                ]
                for c in candidates :
                    try :
                        from shutil import which 
                        exe =which (c )if os.path .basename (c )==c else (c if os.path .isfile (c )else None )
                        if exe :
                            return exe 
                    except Exception :
                        continue 
                return None 

            seven =_find_7z_exe ()
            try :
                if seven :
                    creation =getattr (subprocess ,'CREATE_NO_WINDOW',0 )
                    startup =None 
                    try :
                        startup =subprocess .STARTUPINFO ()
                        startup .dwFlags |=subprocess .STARTF_USESHOWWINDOW 
                    except Exception :
                        startup =None 
                    # 7z zip
                    cmd =[seven ,'a','-tzip',archive_zip ,os.path .join (build_root ,'*'),'-bsp0','-bso1','-bse1']
                    proc =subprocess .Popen (cmd ,stdout =subprocess .PIPE ,stderr =subprocess .STDOUT ,text =True ,creationflags =creation ,startupinfo =startup )
                    for line in proc .stdout or []:
                        self ._log (line .rstrip ())
                    ret =proc .wait ()
                    if ret !=0 :
                        raise RuntimeError (f"7z exit code {ret }")
                else :
                    # Python fallback zip
                    shutil .make_archive (os.path .splitext (archive_zip )[0 ],'zip',build_root )
                self ._log (f"Paquete ZIP creado: {archive_zip }")
                try :
                    self .output_terminal .append ("<span style='color:#BA68C8; font-weight:700'>THE MOD PACKAGE HAS BEEN SUCCESSFULLY CREATED, YOU CAN NOW SHARE IT</span>")
                except Exception :
                    pass 
            except Exception as e :
                self ._log (f"No se pudo crear ZIP: {e }",err =True )
                return 

            # Clean only the temporary build folder (do NOT touch originals)
            try :
                shutil .rmtree (build_root ,ignore_errors =True )
            except Exception :
                pass 

            # Open env_dir
            try :
                os .startfile (env_dir )
            except Exception :
                try :
                    subprocess .Popen (['explorer',env_dir ])
                except Exception :
                    pass 
        except Exception as e :
            self ._log (f"Error creando paquete: {e }",err =True )


    def _log (self ,msg :str ,err :bool =False ):
        try :
            if not hasattr (self ,'output_terminal')or self .output_terminal is None :
                return 
            cur =self .output_terminal .textColor ()
            if err :
                self .output_terminal .setTextColor (QColor('#FF6B6B'))
            else :
                self .output_terminal .setTextColor (QColor('#66FF66'))
            self .output_terminal .append (msg )
            self .output_terminal .setTextColor (cur )
        except Exception :
            pass 

    def _clear_terminal (self ):
        try :
            if hasattr (self ,'output_terminal'):
                self .output_terminal .clear ()
        except Exception :
            pass 


class TipsTab (QWidget ):
    """Tab that shows a random cat image at the bottom-right corner."""
    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .parent =parent
        self ._recent_cats =[]
        self .setStyleSheet ("background-color: transparent; font-size: 14px;")


        self ._layout =QGridLayout (self )
        self ._layout .setContentsMargins (6 ,6 ,6 ,6 )
        self ._layout .setSpacing (6 )


        self ._layout .setRowStretch (0 ,0 )
        self ._layout .setRowStretch (1 ,1 )
        self ._layout .setColumnStretch (0 ,0 )
        self ._layout .setColumnStretch (1 ,1 )

        self ._layout .setRowMinimumHeight (1 ,360 )
        self ._layout .setColumnMinimumWidth (1 ,360 )


        try :
            self .btn_new =QPushButton ("New Tip")
            self .btn_new .setCursor (Qt .PointingHandCursor )
            self .btn_new .setFixedHeight (28 )
            self .btn_new .setStyleSheet (
            "QPushButton { background: #2b2b2b; color: #e0e0e0; border: 1px solid #3a3a3a; border-radius: 4px; padding: 4px 8px;}"
            "QPushButton:hover { background: #3a3a3a; }"
            )
            self .btn_new .clicked .connect (self .refresh )
            top_bar =QWidget ()
            top_bar .setStyleSheet ("background: transparent;")
            top_lay =QHBoxLayout (top_bar )
            top_lay .setContentsMargins (0 ,0 ,0 ,0 )
            top_lay .addStretch (1 )
            top_lay .addWidget (self .btn_new ,0 ,Qt .AlignRight )
            self ._layout .addWidget (top_bar ,0 ,1 ,alignment =Qt .AlignRight |Qt .AlignTop )
        except Exception :
            pass 

        try:
            # Web Documents Button (red translucent style)
            self.btn_web = QPushButton("Web Documents John95AC")
            self.btn_web.setCursor(Qt.PointingHandCursor)
            self.btn_web.setFixedHeight(28)
            self.btn_web.setToolTip("Web page that gathers documents, advancements, and more about these programs and mods")
            self.btn_web.setStyleSheet(
                "QPushButton { background: rgba(139, 0, 0, 0.8); color: white; border: 1px solid rgba(170, 0, 0, 0.8); border-radius: 4px; padding: 4px 8px;}"
                "QPushButton:hover { background: rgba(170, 0, 0, 0.9); }"
            )
            self.btn_web.clicked.connect(self.parent.open_web_interface)

            # Container for bottom-left positioning
            bottom_left_container = QWidget()
            bottom_left_container.setStyleSheet("background: transparent;")
            bottom_left_layout = QVBoxLayout(bottom_left_container)
            bottom_left_layout.setContentsMargins(0, 0, 0, 0)
            bottom_left_layout.addWidget(self.btn_web, alignment=Qt.AlignBottom | Qt.AlignLeft)
            bottom_left_layout.addStretch(1)  # Push buttons to bottom

            self._layout.addWidget(bottom_left_container, 1, 0, alignment=Qt.AlignBottom | Qt.AlignLeft)
        except Exception:
            pass


        self .bottom_box =QWidget ()
        self .bottom_box .setStyleSheet ("background: transparent;")
        h =QHBoxLayout (self .bottom_box )
        h .setContentsMargins (0 ,0 ,0 ,0 )
        h .setSpacing (10 )

        self .advice_label =QLabel ()
        self .advice_label .setWordWrap (True )

        self .advice_label .setAlignment (Qt .AlignCenter )

        self .advice_label .setStyleSheet ("background: transparent; font-size: 24px; font-weight: 600;")

        self .advice_label .setTextFormat (Qt .RichText )
        self .advice_label .setOpenExternalLinks (True )
        try :

            self .advice_label .setTextInteractionFlags (Qt .TextBrowserInteraction )
        except Exception :
            pass 

        self .advice_label .setFixedWidth (640 )
        self .advice_label .setMinimumHeight (150 )


        self .advice_box =QWidget (self )
        self .advice_box .setStyleSheet ("background: transparent;")
        try :

            self .advice_box .setAttribute (Qt .WA_TranslucentBackground ,True )
            self .advice_box .setAttribute (Qt .WA_TransparentForMouseEvents ,False )
        except Exception :
            pass 
        vbox =QVBoxLayout (self .advice_box )

        vbox .setContentsMargins (0 ,0 ,0 ,0 )
        vbox .setSpacing (0 )
        vbox .addWidget (self .advice_label ,alignment =Qt .AlignCenter )

        self ._advice_offset_left =56 

        self ._advice_offset_top =190 
        self .position_advice_box ()

        self .image_label =QLabel ()
        self .image_label .setStyleSheet ("background: transparent;")

        self .image_label .setMinimumSize (360 ,360 )
        self .image_label .setMaximumSize (360 ,360 )
        self .image_label .setScaledContents (False )

        try :
            self .image_label .setAttribute (Qt .WA_TransparentForMouseEvents ,True )
        except Exception :
            pass 


        h .addWidget (self .image_label ,0 ,Qt .AlignVCenter )


        self ._layout .addWidget (self .bottom_box ,1 ,1 ,alignment =Qt .AlignRight |Qt .AlignBottom )


        self .ensure_image_on_top ()


        self .refresh ()

    def get_cat_dir (self ):
        """Return the directory where cat images are located.
        Preference: current working directory Data/CAT, fallback to script directory Data/CAT.
        """
        cwd_path =os.path .join (os .getcwd (),'Data','CAT')
        if os.path .isdir (cwd_path ):
            return cwd_path 
        script_dir =BASE_PATH
        script_path =os.path .join (script_dir ,'Data','CAT')
        return script_path 

    def list_cat_images (self ):
        base =self .get_cat_dir ()

        files =[]
        try :
            files .extend (sorted (glob .glob (os.path .join (base ,'**','*.png'),recursive =True )))
            files .extend (sorted (glob .glob (os.path .join (base ,'**','*.PNG'),recursive =True )))
            files .extend (sorted (glob .glob (os.path .join (base ,'**','*.gif'),recursive =True )))
            files .extend (sorted (glob .glob (os.path .join (base ,'**','*.GIF'),recursive =True )))
        except Exception :
            pass 
        return files 

    def show_random_cat (self ):
        print (f"[Debug-Tips-Init] Call to show_random_cat, current recent: {self ._recent_cats}")
        imgs =self .list_cat_images ()
        print (f"[Debug-Tips] imgs loaded: {[os.path .basename (img )for img in imgs ]} (total: {len (imgs )})")
        if not imgs :
            self .image_label .setText ("No cat images found in Data/CAT")
            self .image_label .setStyleSheet ("color: #CCCCCC; background: transparent;")
            return

        available =[img for img in imgs if os.path .normpath (img ).lower ()not in [os.path .normpath (r ).lower ()for r in self ._recent_cats]]
        print (f"[Debug-Tips] available after filter: {[os.path .basename (a )for a in available ]} (total: {len (available )})")
        if len (available )>0 :
            path =random .choice (available )
        else :
            path =random .choice (imgs )
        print (f"[Debug-Tips] Chosen from {'available' if len (available )>0 else 'full list'}: {os.path .basename (path )}")

        ext =os.path .splitext (path )[1 ].lower ()

        if getattr (self ,'_gif_movie',None )is not None :
            try :
                self ._gif_movie .stop ()
            except Exception :
                pass
            self ._gif_movie =None
            try :
                self .image_label .setMovie (None )
            except Exception :
                pass
        if ext =='.gif':
            try :
                mv =QMovie (path )
                try :
                    mv .setCacheMode (QMovie .CacheAll )
                except Exception :
                    pass
                try :
                    mv .setLoopCount (-1 )
                except Exception :
                    pass

                max_w =self .image_label .maximumWidth ()
                max_h =self .image_label .maximumHeight ()
                try :
                    mv .setScaledSize (QSize (max_w ,max_h ))
                except Exception :
                    pass
                self .image_label .setText ("")
                self .image_label .setStyleSheet ("background: transparent;")
                try :
                    self .image_label .setScaledContents (True )
                except Exception :
                    pass
                self .image_label .setMovie (mv )
                self ._gif_movie =mv
                mv .start ()
                self ._recent_cats .append (os.path .normpath (path ).lower ())
                while len (self ._recent_cats )>3 :
                    self ._recent_cats .pop (0 )
                print (f"[Debug-Tips] History after update: {[os.path .basename (os.path .normpath (r ))for r in self ._recent_cats]}")
                return
            except Exception :

                pass

        pix =QPixmap (path )
        if pix .isNull ():
            self .image_label .setText ("Failed to load: "+os.path .basename (path ))
            self .image_label .setStyleSheet ("color: #FF8888; background: transparent;")
            return
        max_w =self .image_label .maximumWidth ()
        max_h =self .image_label .maximumHeight ()
        scaled =pix .scaled (max_w ,max_h ,Qt .KeepAspectRatio ,Qt .SmoothTransformation )
        try :
            self .image_label .setScaledContents (False )
        except Exception :
            pass
        self .image_label .setPixmap (scaled )
        self ._recent_cats .append (os.path .normpath (path ).lower ())
        while len (self ._recent_cats )>3 :
            self ._recent_cats .pop (0 )
        print (f"[Debug-Tips] History after update: {[os.path .basename (os.path .normpath (r ))for r in self ._recent_cats]}")

    def get_advice_ini_path (self ):
        """Return preferred Advice.ini path if it exists; else fallback path (may or may not exist)."""
        cwd_path =os.path .join (os .getcwd (),'Data','CAT','Advice.ini')
        if os.path .isfile (cwd_path ):
            return cwd_path 
        script_dir =BASE_PATH
        return os.path .join (script_dir ,'Data','CAT','Advice.ini')

    def _candidate_advice_paths (self ):
        """Return candidate INI paths (both Advice.ini and Advice tips.ini) in CWD and script dir."""
        paths =[]

        paths .append (os.path .join (os .getcwd (),'Data','CAT','Advice.ini'))
        paths .append (os.path .join (os .getcwd (),'Data','CAT','Advice tips.ini'))

        script_dir =BASE_PATH
        paths .append (os.path .join (script_dir ,'Data','CAT','Advice.ini'))
        paths .append (os.path .join (script_dir ,'Data','CAT','Advice tips.ini'))
        return paths 

    def read_advices (self ):
        advices =[]

        for path in self ._candidate_advice_paths ():
            if not os.path .isfile (path ):
                continue 
            current =[]

            config =configparser .ConfigParser (strict =False )
            try :
                config .read (path ,encoding ='utf-8-sig')
                if config .has_section ('Advice'):
                    for _ ,val in config .items ('Advice'):
                        text =(val or '').strip ()
                        if text :
                            current .append (text )
                else :
                    for section in config .sections ():
                        for _ ,val in config .items (section ):
                            text =(val or '').strip ()
                            if text and not text .startswith ('['):
                                current .append (text )
                    for _ ,val in config .defaults ().items ():
                        text =(val or '').strip ()
                        if text :
                            current .append (text )
            except Exception :
                current =[]


            if not current :
                try :
                    with open (path ,'r',encoding ='utf-8-sig')as f :
                        for line in f :
                            s =line .strip ()
                            if not s :
                                continue 
                            if s .startswith (';')or s .startswith ('#')or s .startswith ('['):
                                continue 
                            if '='in s :
                                _ ,rhs =s .split ('=',1 )
                                rhs =rhs .strip ()
                                if rhs :
                                    current .append (rhs )
                            else :
                                current .append (s )
                except Exception :
                    pass 

            advices .extend (current )

        return advices 

    def show_random_advice (self ):
        advices =self .read_advices ()
        if advices :
            txt =random .choice (advices )

            try :

                txt =re .sub (r"\*\*([^*]+)\*\*",r"<b>\1</b>",txt )

                italic_color ='#7bd88f'
                txt =re .sub (
                r"(?<!\*)\*([^*]+)\*(?!\*)",
                lambda m :f"<i><span style=\"color:{italic_color }\">{m .group (1 )}</span></i>",
                txt ,
                )
            except Exception :
                pass 

            try :
                txt =re .sub (r"\[([^\]]+)\]\(([^)]+)\)",r'<a href="\2">\1</a>',txt )
            except Exception :
                pass 


            txt =txt .replace ("\r\n","\n")

            txt =txt .replace ("\\r\\n","\n")

            txt =txt .replace ("\\\\n","\n")

            txt =txt .replace ("\\n","\n")

            txt =txt .replace ("\n","<br>")
            self .advice_label .setText (txt )

            self .position_advice_box ()
            self .ensure_image_on_top ()
        else :
            paths =self ._candidate_advice_paths ()

            try :
                print ("[TipsTab] No advice found. Candidates:")
                for p in paths :
                    print (" -",p ,"exists=",os.path .isfile (p ))
            except Exception :
                pass 
            msg_lines =["No advice found. Tried:"]
            for p in paths :
                exists =os.path .isfile (p )
                msg_lines .append (f"- {p } (exists: {'yes'if exists else 'no'})")
            self .advice_label .setText ("<br>".join (msg_lines ))

    def refresh (self ):
        self .show_random_cat ()
        self .show_random_advice ()

    def ensure_image_on_top (self ):
        """Ensure the advice overlay is on top to allow hyperlink clicks; image stays behind.
        """
        try :

            self .bottom_box .stackUnder (self .advice_box )

            self .advice_box .raise_ ()
        except Exception :
            pass 

    def position_advice_box (self ):
        """Position the overlay advice box at the configured top-left offset with a size
        that fits the label's content width and height, without affecting layout.
        """
        try :
            left =getattr (self ,'_advice_offset_left',56 )
            top =getattr (self ,'_advice_offset_top',240 )

            w =self .advice_label .width ()or self .advice_label .sizeHint ().width ()or 640 

            try :
                fixed_w =self .advice_label .maximumWidth ()
                if fixed_w and fixed_w >0 :
                    w =fixed_w 
                else :
                    w =640 
            except Exception :
                w =640 
            content_h =self .advice_label .sizeHint ().height ()
            h =max (150 ,content_h )
            self .advice_box .setGeometry (left ,top ,w ,h )
        except Exception :
            pass 

    def showEvent (self ,event ):
        try :
            super ().showEvent (event )
        except Exception :
            pass 
        self .position_advice_box ()
        self .ensure_image_on_top ()

    def resizeEvent (self ,event ):
        try :
            super ().resizeEvent (event )
        except Exception :
            pass 
        self .position_advice_box ()
        self .ensure_image_on_top ()

class RaceMenuTattooGenerator (QMainWindow ):
    def __init__ (self ):
        super ().__init__ ()
        self .setWindowFlags (Qt .FramelessWindowHint )
        self .setWindowTitle ("RaceMenu SlaveTats Script Generator")

        self .setGeometry (100 ,100 ,1100 ,800 )


        self .setStyleSheet ("""
            QMainWindow { background-color: #2D2D2D; }
            QLabel { color: #E0E0E0; font-size: 12px; }
            QPushButton { background: rgba(28,28,32,0.70); color: #E0E0E0; border: 1px solid rgba(90,90,95,0.60); border-radius: 4px; padding: 6px 10px; min-width: 80px; }
            QPushButton:hover { background: rgba(52,52,58,0.78); }
            QTextEdit { background-color: #252525; color: #E0E0E0; border: 1px solid #555; font-family: Consolas, Courier New, monospace; }
            QMessageBox { background-color: #2D2D2D; }
            QMessageBox QLabel { color: #FFFFFF; }
            /* Tab styles: transparent pane to reveal gradient; semi-transparent tabs */
            QTabWidget::pane { border: 1px solid rgba(69,69,73,0.50); background: transparent; }
            QTabBar::tab { background: rgba(53,53,57,0.35); color: #e0e0e0; padding: 6px 10px; border: 1px solid rgba(69,69,73,0.60); border-bottom: none; border-top-left-radius: 4px; border-top-right-radius: 4px; }
            QTabBar::tab:selected { background: rgba(69,69,75,0.45); }
            QTabBar::tab:hover { background: rgba(62,62,68,0.40); }
        """)


        self .setAcceptDrops (True )


        self .blink_timer =QTimer ()
        self .blink_timer .timeout .connect (self .toggle_button_color )
        self .blink_state =False 


        self .success_sound =QSound (":/sounds/success.wav")


        try :
            _ico =_resolve_app_icon ()
            if _ico :
                self .setWindowIcon (QIcon (_ico ))
        except Exception :
            pass 


        self .gradient_widget =GradientWidget ()
        self .gradient_widget .setStyleSheet ("border: none;")
        self .setCentralWidget (self .gradient_widget )

        self .main_layout =QVBoxLayout (self .gradient_widget )
        self .main_layout .setContentsMargins (0 ,0 ,0 ,0 )
        self .main_layout .setSpacing (0 )

        self .title_bar =CustomTitleBar (self )
        self .main_layout .addWidget (self .title_bar )

        self .content_container =QWidget ()
        self .content_container .setStyleSheet ("background-color: transparent; border: none;")
        self .main_layout .addWidget (self .content_container )

        self .content_layout =QVBoxLayout (self .content_container )
        self .content_layout .setContentsMargins (8 ,8 ,8 ,8 )
        self .content_layout .setSpacing (8 )

        self .initUI ()


        try :
            self .status_bar_container =QWidget ()
            self .status_bar_container .setFixedHeight (24 )
            self .status_bar_container .setStyleSheet (
            "background-color: #1f1f21; border-top: 1px solid #3a3a3f;"
            )
            bar_layout =QHBoxLayout (self .status_bar_container )
            bar_layout .setContentsMargins (8 ,0 ,4 ,0 )
            bar_layout .setSpacing (8 )

            self .status_label =QLabel ("Ready")
            self .status_label .setStyleSheet ("color: #cfcfcf; font-size: 12px;")
            bar_layout .addWidget (self .status_label ,0 ,Qt .AlignVCenter |Qt .AlignLeft )


            bar_layout .addStretch (1 )


            self .progress_bar =QProgressBar ()
            self .progress_bar .setFixedHeight (16 )
            self .progress_bar .setMinimumWidth (360 )
            self .progress_bar .setRange (0 ,100 )
            self .progress_bar .setValue (0 )
            self .progress_bar .setTextVisible (True )
            self .progress_bar .setFormat ("%p%")
            self .progress_bar .setStyleSheet (
            "QProgressBar { background-color: #2b2b2b; color: #ffffff; border: 1px solid #3a3a3a; border-radius: 3px; text-align: center; }"
            "QProgressBar::chunk { background-color: #00bcd4; }"
            )
            self .progress_bar .hide ()
            bar_layout .addWidget (self .progress_bar ,0 ,Qt .AlignVCenter |Qt .AlignRight )

            self .size_grip =QSizeGrip (self .status_bar_container )

            self .size_grip .setStyleSheet ("background: transparent;")
            bar_layout .addWidget (self .size_grip ,0 ,Qt .AlignRight |Qt .AlignBottom )

            self .main_layout .addWidget (self .status_bar_container )
        except Exception :
            pass 






    def start_progress (self ,total :int =100 ,message :str ="Processing…"):
        try :
            self ._progress_total =max (1 ,int (total ))
            self ._progress_start =time .time ()
            self .progress_bar .setRange (0 ,self ._progress_total )
            self .progress_bar .setValue (0 )
            self .progress_bar .show ()
            self .status_label .setText (f"{message } 0%")
        except Exception :
            pass 

    def update_progress (self ,current :int ,message :str |None =None ):
        try :
            cur =int (current )
            total =max (1 ,getattr (self ,'_progress_total',100 ))
            cur =max (0 ,min (cur ,total ))
            self .progress_bar .setValue (cur )
            pct =int ((cur /total )*100 )
            if message is None :
                elapsed =int (time .time ()-getattr (self ,'_progress_start',time .time ()))
                self .status_label .setText (f"Processing… {pct }% (t: {elapsed }s)")
            else :
                self .status_label .setText (message )
        except Exception :
            pass 

    def finish_progress (self ,message :str ="Completed",hide_after_ms :int =4000 ):
        try :
            total =max (1 ,getattr (self ,'_progress_total',100 ))
            self .progress_bar .setRange (0 ,total )
            self .progress_bar .setValue (total )
            self .progress_bar .show ()
            self .status_label .setText (message )
            QTimer .singleShot (int (max (0 ,hide_after_ms )),self ._reset_progress )
        except Exception :
            pass 

    def _reset_progress (self ):
        try :
            self .progress_bar .hide ()
            self .status_label .setText ("Ready")
        except Exception :
            pass 

    def restart_app (self ):
        """Restart the current application: relaunch the same script and close this instance."""
        try :
            exe =sys .executable 
            script =os.path.join(BASE_PATH, os.path.basename(sys.argv[0]))
            args =[script ]+sys .argv [1 :]
            QProcess .startDetached (exe ,args ,os .getcwd ())
        except Exception :
            pass 

        try :
            self .close ()
        except Exception :
            pass 

    def initUI (self ):

        self .tabs =QTabWidget ()
        self .content_layout .addWidget (self .tabs )

        central_widget =QWidget ()

        try :
            central_widget .setStyleSheet ("background: transparent;")
        except Exception :
            pass 
        layout =QVBoxLayout ()
        central_widget .setLayout (layout )
        self .tabs .addTab (central_widget ,"SlaveTats → RaceMenu (.psc Generator)")


        title_label =QLabel ("SLAVETATS TO RACE MENU SCRIPT GENERATOR")
        title_label .setAlignment (Qt .AlignCenter )

        title_label .setStyleSheet ("font-size: 16px; font-weight: bold; color: #66FF66;")
        layout .addWidget (title_label )


        drag_label =QLabel ("Drag and drop a JSON file here")
        drag_label .setAlignment (Qt .AlignCenter )
        drag_label .setStyleSheet ("font-size: 14px; color: #FFA500;")
        layout .addWidget (drag_label )


        or_label =QLabel ("- OR -")
        or_label .setAlignment (Qt .AlignCenter )
        or_label .setStyleSheet ("font-size: 12px; color: #E0E0E0;")
        layout .addWidget (or_label )


        self .select_json_btn =QPushButton ("Select JSON")
        self .select_json_btn .clicked .connect (self .select_json )

        self .select_json_btn .setStyleSheet (
        "QPushButton {"
        " background: rgba(76,175,80,0.25);"
        " color: #FFFFFF;"
        " border: 1px solid rgba(76,175,80,0.80);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        " font-weight: bold;"
        "}"
        " QPushButton:hover { background: rgba(76,175,80,0.40); }"
        )
        try :
            self .select_json_btn .setToolTip ("Select RaceMenu JSON (overlays)")
        except Exception :
            pass 
        layout .addWidget (self .select_json_btn )


        self .file_path_label =QLabel ("No file selected")
        self .file_path_label .setWordWrap (True )
        layout .addWidget (self .file_path_label )


        self .json_preview_label =QLabel ("JSON Preview:")
        layout .addWidget (self .json_preview_label )

        self .json_preview =QTextEdit ()
        self .json_preview .setReadOnly (True )
        layout .addWidget (self .json_preview )


        self .generate_psc_btn =QPushButton ("Generate .psc file")
        self .generate_psc_btn .clicked .connect (self .generate_psc )
        self .generate_psc_btn .setEnabled (False )
        self .normal_button_style ="""
            QPushButton {
                background: rgba(28,28,32,0.70);
                color: #E0E0E0;
                border: 1px solid rgba(90,90,95,0.60);
                padding: 5px;
                min-width: 80px;
            }
        """

        self .active_button_style ="""
            QPushButton {
                background: rgba(76,175,80,0.25);
                color: #FFFFFF;
                border: 1px solid rgba(76,175,80,0.80);
                padding: 5px;
                min-width: 80px;
                font-weight: bold;
            }
        """

        self .active_button_style_blink ="""
            QPushButton {
                background: rgba(76,175,80,0.45);
                color: #FFFFFF;
                border: 1px solid rgba(76,175,80,0.90);
                padding: 5px;
                min-width: 80px;
                font-weight: bold;
            }
        """

        self .btn_style_gray =(
        "QPushButton {"
        " background: rgba(53,53,57,0.82);"
        " color: #E0E0E0;"
        " border: 1px solid rgba(90,90,95,0.70);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        "}"
        "QPushButton:hover { background: rgba(62,62,68,0.90); }"
        "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
        )
        self .btn_style_green =(
        "QPushButton {"
        " background: rgba(76,175,80,0.25);"
        " color: #FFFFFF;"
        " border: 1px solid rgba(76,175,80,0.80);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        "}"
        "QPushButton:hover { background: rgba(76,175,80,0.35); }"
        "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
        )

        self .generate_psc_btn .setStyleSheet (self .btn_style_gray )
        try :
            self .generate_psc_btn .setToolTip ("Generate Papyrus script (.psc) from selected JSON")
        except Exception :
            pass 



        self .create_folder_btn =QPushButton ("Create Organized Texture Folder and Copy DDS Files")
        self .create_folder_btn .clicked .connect (self .create_texture_folder_structure )
        self .create_folder_btn .setEnabled (False )
        self .create_folder_btn_normal_style ="""
            QPushButton {
                background: rgba(38,38,44,0.78);
                color: #E0E0E0;
                border: 1px solid rgba(90,90,95,0.70);
                border-radius: 4px;
                padding: 6px 10px;
                min-width: 80px;
            }
            QPushButton:hover { background: rgba(62,62,68,0.85); }
        """

        self .create_folder_btn .setStyleSheet (self .btn_style_gray )
        try :
            self .create_folder_btn .setToolTip ("Create organized texture folder and copy DDS files referenced by the JSON")
        except Exception :
            pass 


        btn_row =QHBoxLayout ()

        btn_style_blue =(
        "QPushButton {"
        " background: rgba(0, 188, 212, 0.35);"
        " color: #E0F7FA;"
        " border: 1px solid rgba(0, 188, 212, 0.70);"
        " border-radius: 4px;"
        " padding: 6px 10px;"
        "}"
        "QPushButton:hover { background: rgba(0, 188, 212, 0.55); }"
        "QPushButton:disabled { background: rgba(53,53,57,0.40); color: #BDBDBD; border-color: rgba(90,90,95,0.45); }"
        )
        self .refresh_psc_tab_btn =QPushButton ("Refresh")
        try :
            self .refresh_psc_tab_btn .setCursor (Qt .PointingHandCursor )
            self .refresh_psc_tab_btn .setToolTip ("Clear and reset this tab")
        except Exception :
            pass 
        self .refresh_psc_tab_btn .setStyleSheet (btn_style_blue )

        self .refresh_psc_tab_btn .clicked .connect (
        lambda :(
        self .file_path_label .setText ("No file selected"),
        self .json_preview .clear (),
        self .terminal_output .clear (),
        self .generate_psc_btn .setEnabled (False ),
        self .generate_psc_btn .setStyleSheet (self .btn_style_gray ),
        self .create_folder_btn .setEnabled (False ),
        self .create_folder_btn .setStyleSheet (self .btn_style_gray ),

        self .video_btn .setEnabled (False )
        )
        )
        btn_row .addWidget (self .refresh_psc_tab_btn )
        btn_row .addStretch (1 )
        btn_row .addWidget (self .generate_psc_btn )
        btn_row .addWidget (self .create_folder_btn )

        self .video_btn =QPushButton ("Next Steps Hint")
        try :
            self .video_btn .setCursor (Qt .PointingHandCursor )
            self .video_btn .setToolTip ("Next steps hint: https://john95ac.github.io/website-documents-John95AC/Race_Menu_Overlay_to_SlaveTats_Helper/index.html")
        except Exception :
            pass 

        self .video_btn .setStyleSheet (btn_style_blue )
        self .video_btn .clicked .connect (self .open_wiki_link )

        try :
            self .video_btn .setEnabled (False )
        except Exception :
            pass 
        btn_row .addWidget (self .video_btn )
        layout .addLayout (btn_row )


        self .terminal_label =QLabel ("Output Terminal:")
        layout .addWidget (self .terminal_label )

        self .terminal_output =QTextEdit ()
        self .terminal_output .setReadOnly (True )

        self .terminal_output .setStyleSheet (
        "QTextEdit {"
        " background-color: #1A1A1C;"
        " color: #4CAF50;"
        " border: 1px solid #3A3A3F;"
        " border-radius: 4px;"
        " font-family: Consolas, 'Courier New', monospace;"
        " font-size: 12px;"
        "}"
        )
        layout .addWidget (self .terminal_output )



        self .psc_importer_tab =PSCImporterTab (self )
        self .tabs .addTab (self .psc_importer_tab ,"RaceMenu → SlaveTats (.json Generator)")


        try :
            self .st_creator_tab =STCreatorTab (self )
            self .tabs .addTab (self .st_creator_tab ,"ST Creator (from DDS)")
        except Exception :
            pass 


        try :
            self .rm_creator_tab =RMCreatorTab (self )
            self .tabs .addTab (self .rm_creator_tab ,"RM Creator (from DDS)")
        except Exception :
            pass 


        try :
            self .pca_helper_tab =PCAHelperTab (self )
            self .tabs .addTab (self .pca_helper_tab ,"PCA Papyrus Compile Helper")
        except Exception :
            pass 


        try :
            self .tips_tab =TipsTab (self )
            self .tabs .addTab (self .tips_tab ,"Tips")
        except Exception :

            pass 


        try :
            self .tabs .currentChanged .connect (self .on_tab_changed )
        except Exception :
            pass 

    def toggle_button_color (self ):
        if self .blink_state :
            self .generate_psc_btn .setStyleSheet (self .active_button_style )
        else :
            self .generate_psc_btn .setStyleSheet (self .active_button_style_blink )
        self .blink_state =not self .blink_state 

    def on_tab_changed (self ,index :int ):
        try :
            w =self .tabs .widget (index )
            if isinstance (w ,TipsTab ):
                w .refresh ()
        except Exception :
            pass 


    def dragEnterEvent (self ,event :QDragEnterEvent ):
        if event .mimeData ().hasUrls ():
            urls =event .mimeData ().urls ()
            if len (urls )==1 and urls [0 ].toLocalFile ().lower ().endswith ('.json'):
                event .acceptProposedAction ()

                self .blink_timer .start (500 )

    def dragLeaveEvent (self ,event ):

        self .blink_timer .stop ()

        if self .generate_psc_btn .isEnabled ():
            self .generate_psc_btn .setStyleSheet (self .active_button_style )
        else :
            self .generate_psc_btn .setStyleSheet (self .normal_button_style )
        self .blink_state =False 

    def dropEvent (self ,event :QDropEvent ):

        self .blink_timer .stop ()

        if self .generate_psc_btn .isEnabled ():
            self .generate_psc_btn .setStyleSheet (self .active_button_style )
        else :
            self .generate_psc_btn .setStyleSheet (self .normal_button_style )
        self .blink_state =False 

        urls =event .mimeData ().urls ()
        if urls :
            file_path =urls [0 ].toLocalFile ()
            self .process_json_file (file_path )

    def select_json (self ):
        options =QFileDialog .Options ()
        file_path ,_ =QFileDialog .getOpenFileName (
        self ,"Select JSON file","",
        "JSON Files (*.json);;All Files (*)",options =options )

        if file_path :
            self .process_json_file (file_path )

    def process_json_file (self ,file_path ):
        self .file_path =file_path 
        self .file_path_label .setText (f"Selected file: {file_path }")
        self .log_terminal (f"JSON file selected: {file_path }")

        try :
            with open (file_path ,'r',encoding ='utf-8')as f :
                self .json_data =json .load (f )


            preview_text =json .dumps (self .json_data ,indent =4 )
            self .json_preview .setPlainText (preview_text )
            self .log_terminal ("JSON loaded successfully.")

            self .log_terminal ("JSON WAS READ SUCCESSFULLY, NOW CONTINUE WITH THE PSC GENERATION.",warning =True )


            self .generate_psc_btn .setEnabled (True )

            self .generate_psc_btn .setStyleSheet (self .btn_style_green )
            self .create_folder_btn .setEnabled (False )

            self .create_folder_btn .setStyleSheet (self .btn_style_gray )


        except Exception as e :
            self .log_terminal (f"Error loading JSON: {str (e )}",error =True )
            msg =QMessageBox ()
            msg .setIcon (QMessageBox .Critical )
            msg .setText ("Error loading JSON")
            msg .setInformativeText (str (e ))
            msg .setWindowTitle ("Error")
            msg .exec_ ()

    def generate_psc (self ):
        if not hasattr (self ,'json_data')or not self .json_data :
            self .log_terminal ("No JSON data to process.",error =True )
            return 

        try :

            json_filename =os.path .splitext (os.path .basename (self .file_path ))[0 ]

            script_name =json_filename .replace (' ','_')


            base_dir =os.path .dirname (self .file_path )
            scripts_dir =os.path .join (base_dir ,"scripts")
            source_dir =os.path .join (scripts_dir ,"Source")

            os .makedirs (source_dir ,exist_ok =True )
            self .log_terminal (f"Directories created: {source_dir }")


            psc_content =f"""scriptName {script_name } extends RaceMenuBase

function OnBodyPaintRequest()\n"""

            for item in self .json_data :
                name =item .get ('name','')
                texture_path =item .get ('texture','')

                if name and texture_path :

                    texture_path =texture_path .replace ('/','\\\\').replace ('\\','\\\\')
                    psc_content +=f'    self.AddBodyPaint("{name }", "Actors\\\\Character\\\\Overlays\\\\{texture_path }")\n'

            psc_content +="endFunction"


            psc_file_path =os.path .join (source_dir ,f"{script_name }.psc")

            with open (psc_file_path ,'w',encoding ='utf-8')as f :
                f .write (psc_content )

            self .log_terminal (f".psc file generated successfully: {psc_file_path }")


            self .success_sound .play ()


            self .json_preview .setPlainText (psc_content )


            os .startfile (source_dir )


            try :
                self .create_folder_btn .setEnabled (True )

                self .create_folder_btn .setStyleSheet (self .btn_style_green )
            except Exception :
                pass 


            self .log_terminal (
            "READY: THE FOLDER WITH THE PSC FILE WAS CREATED. NOW CONTINUE BY ORGANIZING THE CORRECT DDS FOLDER ORDER. JUST PRESS THE NEXT BUTTON.",
            color ="#00BCD4",
            )

        except Exception as e :
            self .log_terminal (f"Error generating .psc file: {str (e )}",error =True )
            msg =QMessageBox ()
            msg .setIcon (QMessageBox .Critical )
            msg .setText ("Error generating script")
            msg .setInformativeText (str (e ))
            msg .setWindowTitle ("Error")
            msg .exec_ ()

    def create_texture_folder_structure (self ):
        if not hasattr (self ,'file_path'):
            self .log_terminal ("No JSON file selected.",error =True )
            return 

        try :

            try :
                self .window ().start_progress (100 ,"Preparing copy…")
            except Exception :
                pass 

            json_filename =os.path .splitext (os.path .basename (self .file_path ))[0 ]
            base_dir =os.path .dirname (self .file_path )



            top_level_name =None 
            try :

                if isinstance (self .json_data ,list ):
                    for it in self .json_data :
                        tex =(it or {}).get ('texture','')if isinstance (it ,dict )else ''
                        if not tex :
                            continue 

                        tex_norm =str (tex ).replace ('\\','/').lstrip ('/').strip ()

                        for pre in ("actors/character/overlays/","Actors/Character/Overlays/"):
                            if tex_norm .startswith (pre ):
                                tex_norm =tex_norm [len (pre ):]
                                break 
                        segs =[s for s in tex_norm .split ('/')if s ]
                        if segs :
                            top_level_name =segs [0 ]
                            break 
            except Exception :
                top_level_name =None 

            if not top_level_name :

                top_level_name =json_filename 


            textures_folder =os.path .join (base_dir ,"textures")
            actors_folder =os.path .join (textures_folder ,"Actors")
            character_folder =os.path .join (actors_folder ,"Character")
            overlays_folder =os.path .join (character_folder ,"Overlays")
            final_folder =os.path .join (overlays_folder ,top_level_name )

            os .makedirs (final_folder ,exist_ok =True )
            self .log_terminal (f"Created texture folder structure: {final_folder }")


            json_folder =os.path .dirname (self .file_path )
            src_root =None 
            for root ,dirs ,files in os .walk (json_folder ):

                for d in dirs :
                    if d .lower ()==top_level_name .lower ():
                        src_root =os.path .join (root ,d )
                        break 
                if src_root :
                    break 
            if not src_root :

                candidate =os.path .join (json_folder ,top_level_name )
                if os.path .isdir (candidate ):
                    src_root =candidate 
            if not src_root :

                self .log_terminal (
                f"Top-level folder '{top_level_name }' not found under JSON folder; copying from JSON folder root instead.",
                warning =True ,
                )
                src_root =json_folder 


            files_to_copy =[]
            for root ,dirs ,files in os .walk (src_root ):
                for fname in files :
                    src_path =os.path .join (root ,fname )
                    rel_path =os.path .relpath (src_path ,src_root )
                    dst_path =os.path .join (final_folder ,rel_path )
                    files_to_copy .append ((src_path ,dst_path ))

            if not files_to_copy :
                self .log_terminal ("No files found to copy in the source folder",warning =True )
                try :
                    self .window ().finish_progress ("No files to copy",hide_after_ms =2000 )
                except Exception :
                    pass 
            else :
                copied_count =0 
                total =len (files_to_copy )
                try :
                    self .window ().start_progress (total ,"Copying files…")
                except Exception :
                    pass 
                for src_path ,dst_path in files_to_copy :
                    try :
                        os .makedirs (os.path .dirname (dst_path ),exist_ok =True )
                        shutil .copy2 (src_path ,dst_path )
                        self .log_terminal (
                        f"Copied: {os.path .basename (src_path )} (to: {os.path .relpath (dst_path ,final_folder )})"
                        )
                        copied_count +=1 
                        try :
                            self .window ().update_progress (copied_count )
                        except Exception :
                            pass 
                    except Exception as copy_error :
                        self .log_terminal (f"Failed to copy {src_path }: {str (copy_error )}",error =True )

                self .log_terminal (f"Successfully copied {copied_count }/{total } files (preserved folders)")
                try :
                    self .window ().finish_progress ("Copy completed",hide_after_ms =2000 )
                except Exception :
                    pass 

                self .log_terminal (
                "DONE: THE TEXTURES FOLDER WAS CREATED WITH ITS NEW HIERARCHY.",
                color ="#FFA500",
                )
                self .log_terminal (
                "MAKE SURE TO MOVE THE NEW <span style=\"color:#00BCD4\">TEXTURES</span> AND <span style=\"color:#00BCD4\">SCRIPTS FOLDERS</span> TO A NEW EMPTY MOD IN YOUR MOD LIST, THEN PROCEED.",
                color ="#FFA500",
                )
                self .log_terminal (
                "TWO STEPS REMAIN:",
                color ="#FFA500",
                )
                self .log_terminal (
                "1) COMPILE THE PEX USING A PAPYRUS COMPILER (SEVERAL METHODS ARE POSSIBLE).",
                color ="#FFA500",
                )
                self .log_terminal (
                "2) CREATE AN ESP, WHICH IS VERY EASY WITH SSEDIT AND THE PASCAL I CREATED.",
                color ="#FFA500",
                )
                self .log_terminal (
                "WATCH THE VIDEO BY PRESSING THE BUTTON OR ON THE NEXUS PAGE; IN ABOUT ONE MINUTE YOU WILL HAVE THE MOD READY. GOOD LUCK!",
                color ="#FFA500",
                )

                try :
                    self .video_btn .setEnabled (True )
                except Exception :
                    pass 


            self .success_sound .play ()


            os .startfile (final_folder )

        except Exception as e :
            self .log_terminal (f"Error creating texture folders: {str (e )}",error =True )
            msg =QMessageBox ()
            msg .setIcon (QMessageBox .Critical )
            msg .setText ("Error creating texture folders")
            msg .setInformativeText (str (e ))
            msg .setWindowTitle ("Error")
            msg .exec_ ()

    def open_tutorial_video (self ):
        """Open the tutorial video data/Tutorial/012.mp4 using the system's default player.
        The path is resolved relative to the selected JSON's folder if available; otherwise relative to CWD.
        """
        try :

            try :
                base_dir =os.path .dirname (self .file_path )if hasattr (self ,'file_path')else os .getcwd ()
            except Exception :
                base_dir =os .getcwd ()

            candidates =[
            os.path .join (base_dir ,'data','Tutorial','012.mp4'),
            os.path .join (base_dir ,'Data','Tutorial','012.mp4'),
            ]
            video_path =None 
            for p in candidates :
                if os.path .isfile (p ):
                    video_path =p 
                    break 
            if video_path is None :

                fallback =os.path .join ('data','Tutorial','012.mp4')
                if os.path .isfile (fallback ):
                    video_path =os.path .abspath (fallback )

            if video_path :
                self .log_terminal (f"Opening tutorial video: {video_path }",color ="#00BCD4")
                os .startfile (video_path )
            else :
                msg ="Tutorial video not found at data/Tutorial/012.mp4"
                self .log_terminal (msg ,error =True )
                mb =QMessageBox ()
                mb .setIcon (QMessageBox .Warning )
                mb .setWindowTitle ("Video not found")
                mb .setText ("Could not find the tutorial video.")
                mb .setInformativeText ("Expected at: data/Tutorial/012.mp4 relative to the JSON folder.")
                mb .exec_ ()
        except Exception as e :
            self .log_terminal (f"Error opening tutorial video: {str (e )}",error =True )
            try :
                mb =QMessageBox ()
                mb .setIcon (QMessageBox .Critical )
                mb .setWindowTitle ("Error opening video")
                mb .setText ("An error occurred while opening the tutorial video.")
                mb .setInformativeText (str (e ))
                mb .exec_ ()
            except Exception :
                pass 

    def open_web_interface(self):
        """Open the web interface URL in the default browser."""
        url = QUrl("https://john95ac.github.io/website-documents-John95AC/index.html")
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, "Error", "Could not open web browser to access the documentation.") 

    def log_terminal (self ,message ,error =False ,warning =False ,color =None ):

        if color is None :
            if error :
                color ="#FF5252"
            elif warning :
                color ="#FFA500"
            else :
                color ="#4CAF50"

        self .terminal_output .moveCursor (QTextCursor .End )
        self .terminal_output .insertHtml (f'<span style="color:{color }">>> {message }</span><br>')
        self .terminal_output .moveCursor (QTextCursor .End )
        self .terminal_output .ensureCursorVisible ()

    def open_wiki_link(self):
        """Open the wiki URL in the default browser."""
        url = QUrl("https://john95ac.github.io/website-documents-John95AC/Race_Menu_Overlay_to_SlaveTats_Helper/index.html")
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, "Error", "Could not open web browser to access the wiki.")

if __name__ =="__main__":
    app =QApplication ([])

    try :
        _ico =_resolve_app_icon ()
        if _ico :
            app .setWindowIcon (QIcon (_ico ))
    except Exception :
        pass 


    dark_palette =app .palette ()
    dark_palette .setColor (dark_palette .Window ,QColor(45 ,45 ,45 ))
    dark_palette .setColor (dark_palette .WindowText ,Qt .white )
    dark_palette .setColor (dark_palette .Base ,QColor(25 ,25 ,25 ))
    dark_palette .setColor (dark_palette .AlternateBase ,QColor(45 ,45 ,45 ))

    dark_palette .setColor (dark_palette .ToolTipBase ,QColor(60 ,60 ,60 ))
    dark_palette .setColor (dark_palette .ToolTipText ,Qt .white )
    dark_palette .setColor (dark_palette .Text ,Qt .white )
    dark_palette .setColor (dark_palette .Button ,QColor(45 ,45 ,45 ))
    dark_palette .setColor (dark_palette .ButtonText ,Qt .white )
    dark_palette .setColor (dark_palette .BrightText ,Qt .red )
    dark_palette .setColor (dark_palette .Link ,QColor(42 ,130 ,218 ))
    dark_palette .setColor (dark_palette .Highlight ,QColor(42 ,130 ,218 ))
    dark_palette .setColor (dark_palette .HighlightedText ,Qt .black )
    app .setPalette (dark_palette )


    app .setStyleSheet ("""
        /* Visible tooltips on dark theme */
        QToolTip {
            background-color: rgba(50,50,50,0.95);
            color: #FFFFFF;
            border: 1px solid #666;
            padding: 4px 6px;
            font-size: 12px;
        }
        QMessageBox {
            background-color: #2D2D2D;
        }
        QMessageBox QLabel {
            color: #FFFFFF;
        }
        QMessageBox QPushButton {
            color: #FFFFFF;
        }
    """)

    generator =RaceMenuTattooGenerator ()
    generator .show ()
    app .exec_ ()