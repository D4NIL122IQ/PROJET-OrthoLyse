from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QLineEdit, \
    QPushButton, QGroupBox, QGridLayout, QSizePolicy, QMessageBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIntValidator, QIcon

from app.controllers.Menu_controllers import NavigationController
from app.controllers.Settings_controller import SettingsController


class Parametres(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = NavigationController()
        self.settings_controller = SettingsController()
        self.font_bold, self.font_family_bold = self.controller.set_font('./assets/Fonts/Poppins/Poppins-SemiBold.ttf')
        self.font_regular, self.font_family_regular = self.controller.set_font(
            './assets/Fonts/Poppins/Poppins-Regular.ttf')
        self.font_medium, self.font_family_medium = self.controller.set_font(
            './assets/Fonts/Poppins/Poppins-Medium.ttf')

        # creer les deux sections
        self.icone=self.creerIcone()
        self.sections = self.creerSections()
        self.bouton = self.creerBoutonValider()

        # ce layout va aligner verticalement les deux sections de paramètres et le boutoun valider
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.icone)
        main_layout.addStretch(1)
        main_layout.addLayout(self.sections)
        main_layout.addStretch(1)
        main_layout.addLayout(self.bouton)


        self.setLayout(main_layout)

        self.chargerValeurs()
        self.adjustFonts()

    def creerBoutonValider(self):

        self.btnValider = QPushButton("Valider")
        self.btnValider.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnValider.setFont(self.font_medium)
        self.btnValider.setMinimumSize(85, 30)
        self.btnValider.setMaximumSize(120, 36)
        self.btnValider.setCursor(Qt.PointingHandCursor)
        self.btnValider.setStyleSheet("""
            QPushButton {
                color:#fff;
                background-color: qlineargradient(spread:pad, 
                                                x1:0, y1:0, x2:0, y2:1, 
                                                stop:0 #56E0E0, 
                                                stop:0.5 #007299);
                border:1px solid #007299;                                
                border-radius:15px;

            }
            QPushButton:hover {
                background-color: #fff;

                color: #007299;
            }
        """)
        self.btnValider.clicked.connect(self.updateValeurs)

        # aligner le bouton horizontalement
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.btnValider)
        btn_layout.addSpacing(50)

        return btn_layout

    def creerSections(self):

        # creer la section modèles
        self.modeles = self.creerSectionModeles()

        # creer la section métriques
        self.metriques = self.creerSectionMetriques()

        # aligner les sections horizontalement
        sections_layout = QHBoxLayout()
        sections_layout.addStretch(3)
        sections_layout.addWidget(self.modeles)
        sections_layout.addStretch(1)
        sections_layout.addWidget(self.metriques)
        sections_layout.addStretch(3)

        return sections_layout

    def creerSectionModeles(self):

        # creer le titre
        titre = QLabel("<b>Modèle de transcription</b>")
        titre.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        titre.setFont(self.font_bold)
        titre.setStyleSheet("color:black;")
        # aligner ce texte horizontalement
        texte_layout = QHBoxLayout()
        texte_layout.addWidget(titre)
        texte_layout.addStretch(1)

        # creer les boutons radio
        base_radio = QRadioButton("Base \nRapide, basique.")
        small_radio = QRadioButton("Small\nÉquilibré, léger.")
        medium_radio = QRadioButton("Medium\nPrécis, fiable.")
        turbo_radio = QRadioButton("Turbo\nUltra-rapide, précis.")

        # aligner le texte et les boutons verticalement
        self.modeles_layout = QVBoxLayout()
        self.modeles_layout.addSpacing(8)
        self.modeles_layout.addLayout(texte_layout)
        self.modeles_layout.addStretch(2)
        self.btns = [base_radio, small_radio, medium_radio, turbo_radio]

        for btn in self.btns:
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setMinimumSize(180, 45)
            btn.setStyleSheet("""
                QRadioButton {
                    color: black;
                }
                QRadioButton:hover {
                    background:#efefef;
                }
            """)
            btn.setFont(self.font_regular)
            self.modeles_layout.addWidget(btn)
            self.modeles_layout.addStretch(1)

        modeles_section = QGroupBox()
        modeles_section.setLayout(self.modeles_layout)
        modeles_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # personnaliser les QGroupBox
        self.styleSection(modeles_section)

        return modeles_section

    def creerSectionMetriques(self):
        # creer le titre
        titre = QLabel("<b>Normes des métriques</b>")
        titre.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        titre.setFont(self.font_bold)
        titre.setStyleSheet("color:black;")
        # aligner ce texte horizontalement
        texte_layout = QHBoxLayout()
        texte_layout.addWidget(titre)
        texte_layout.addStretch(1)

        # creer le texte explicatif
        notice = QLabel(
            "Choisissez les valeurs normales  pour chacune des métriques suivantes selon la durée de votre enregistrement :")
        notice.setFont(self.font_regular)
        notice.setStyleSheet("color:grey;")
        notice.setWordWrap(True)

        # creer les metriques
        # layout sous forme de tableau
        metriques_layout = QGridLayout()

        # les étiquettes des métriques à configurer
        labels = [
            "Durée  : ", "Mots  : ", "Mots différents  : ",
            "Énoncés  : ", "Morphèmes  : ", "Morphèmes par énoncé  : ", "Lemmes  : "
        ]

        # pour pouvoir récupérer les valeurs saisies
        self.inputs = []

        # positionner les éléments
        for i, text in enumerate(labels):

            label = QLabel(text)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            label.setFont(self.font_regular)
            label.setStyleSheet("color:black;")
            label.setAlignment(Qt.AlignmentFlag.AlignRight)
            input = QLineEdit()
            input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            input.setMinimumSize(30, 25)
            input.setStyleSheet("""
                QLineEdit {
                    color: black;
                    background: #fff;
                    
                }
                QLineEdit:hover {
                    background: #efefef;
    
                }
            """)
            validator = QIntValidator()
            validator.setBottom(1)  # Accepte uniquement les entiers ≥ 1
            input.setValidator(validator)
            if i == 0:
                metriques_layout.addWidget(label, i, 0)
                metriques_layout.addWidget(input, i, 1)
            else:
                metriques_layout.addWidget(label, i, 1)
                metriques_layout.addWidget(input, i, 2)

            self.inputs.append(input)
        # ALIGNER LA GRILLE HORIZONTALEMENT
        metriques_contrainer = QHBoxLayout()
        metriques_contrainer.addLayout(metriques_layout)

        # aligner tous les layout verticalement
        self.normes_metrique_layout = QVBoxLayout()
        self.normes_metrique_layout.addSpacing(8)
        #normes_metrique_layout.setContentsMargins(30, 0, 30, 0)
        self.normes_metrique_layout.addLayout(texte_layout)
        self.normes_metrique_layout.addStretch(1)
        self.normes_metrique_layout.addWidget(notice)
        self.normes_metrique_layout.addStretch(1)
        self.normes_metrique_layout.addLayout(metriques_contrainer)
        self.normes_metrique_layout.addStretch(1)

        metriques_section = QGroupBox()
        metriques_section.setLayout(self.normes_metrique_layout)
        metriques_section.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred)

        # personnaliser les QGroupBox
        self.styleSection(metriques_section)

        return metriques_section

    def styleSection(self, section):
        section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        section.setStyleSheet(f"""QGroupBox{{
                                    background:#fff;
                                    border-radius:15px;
                            }}
                            QRadioButton{{
                                    border:1px solid #cecece ;
                                    border-radius:10px;
                                    padding:10px;
                            }}
                            QLineEdit{{
                                    border:1px solid #cecece;
                                    border-radius:6px;
                            }}
        """)

    def resizeEvent(self, event):
        largeur = self.width()

        # Calcul dynamique avec des bornes
        largeur_btn = max(85, min(largeur // 8, 120))
        hauteur_btn = max(30, min(largeur // 30, 36))

        self.btnValider.setFixedSize(largeur_btn, hauteur_btn)
        if self.width() > 940 and self.height() > 750:
            self.modeles.setMinimumSize(466, 450)
            self.metriques.setMinimumSize(466, 450)
            self.modeles_layout.setContentsMargins(30,0,30,10)
            self.normes_metrique_layout.setContentsMargins(20,0,20,10)


        else:
            self.modeles.setMinimumSize(280, 310)
            self.metriques.setMinimumSize(317, 310)


        self.styleSection(self.modeles)
        self.styleSection(self.metriques)
        self.adjustFonts()

    def chargerValeurs(self):

        try:
            metriques = self.settings_controller.get_metriques()
            champs = [
                "duree", "nbrMot", "motDif", "nbrEnonce",
                "morpheme", "morphemeEnonce", "lemme"
            ]

            for i, champ in enumerate(champs):
                if champ in metriques and i < len(self.inputs):
                    self.inputs[i].setText(str(metriques[champ]))

            # modèle
            model_whisper = self.settings_controller.get_model_whisper()
            if model_whisper in range(len(self.btns)):
                self.btns[model_whisper].setChecked(True)

        except Exception as e:
            print("Erreur lors du chargement :", str(e))

    def updateValeurs(self):


        try:
            valide = True
            nouvelles_valeurs = {}
            labels = ["duree", "nbrMot", "motDif", "nbrEnonce",
                      "morpheme", "morphemeEnonce", "lemme"]

            for i, label in enumerate(labels):
                champ = self.inputs[i]

                if champ.hasAcceptableInput():
                    nouvelles_valeurs[label] = int(champ.text())
                    champ.setStyleSheet("")
                else:
                    valide = False
                    champ.setToolTip("Veuillez entrer un nombre supérieur à 0")
                    champ.setStyleSheet("""QLineEdit{
                                            border: 1px solid red;
                                        }
                                        QToolTip{
                                            background:#fff;
                                            color:black;
                                        }""")

            if not valide:
                return

            # modèle choisi
            model_whisper = next((i for i, btn in enumerate(self.btns) if btn.isChecked()), 0)

            # mise à jour
            self.settings_controller.set_metriques(nouvelles_valeurs)
            self.settings_controller.set_model_whisper(model_whisper)

            msg = QMessageBox()
            msg.setText("Les paramètres ont été sauvegardés avec succès.")
            msg.setWindowTitle("Succès")
            close_button=msg.addButton("Fermer",QMessageBox.AcceptRole)
            msg.buttonClicked.connect(lambda: NavigationController()._instance.go_to_previous_page())
            msg.exec()


        except Exception as e:
            print("Erreur lors de la mise à jour :", str(e))

    def adjustFonts(self):
        """Ajuste dynamiquement la taille des polices selon la largeur de la fenêtre"""
        if self.width() > 940 and self.height() > 750:
            new_size_regular = 11
            new_size_bold = 16
            new_size_medium = 12

        else:
            new_size_regular = 9
            new_size_bold = 11
            new_size_medium = 10


        self.font_medium.setPointSize(new_size_medium)
        self.font_bold.setPointSize(new_size_bold)
        self.font_regular.setPointSize(new_size_regular)

        # Appliquer aux composants
        for btn in self.btns:
            btn.setFont(self.font_regular)

        for input in self.inputs:
            input.setFont(self.font_regular)

        for widget in self.findChildren(QLabel):
            if "<b>" in widget.text():
                widget.setFont(self.font_bold)
            else:
                widget.setFont(self.font_regular)

        self.btnValider.setFont(self.font_medium)

    def creerIcone(self):
        icon=QIcon('./assets/SVG/previousIcon.svg')


        #creer le bouton qui va contenir l'icone
        btn=QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(32,32))
        btn.setStyleSheet("background:transparent;")
        btn.clicked.connect(lambda: NavigationController()._instance.go_to_previous_page())
        btn.setCursor(Qt.PointingHandCursor)
        btn.setToolTip("Retour à la page précédente")
        #mettre le bouton dans un layout pour l'aligner horizontalement
        layout=QHBoxLayout()
        layout.addSpacing(10)
        layout.addWidget(btn)
        layout.addStretch(1)

        return layout