import sys
import os
import json
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QLineEdit, \
    QPushButton, QGroupBox, QGridLayout, QSizePolicy, QMessageBox, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIntValidator, QColor, QIcon
from frontend.controllers.Menu_controllers import NavigationController


class Parametres(QWidget):
    def __init__(self):
        super().__init__()
        #self.setMinimumSize(642,450)
        self.controller = NavigationController()
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
        self.modeles_layout.setContentsMargins(10, 0, 10, 0)
        self.modeles_layout.addLayout(texte_layout)
        self.modeles_layout.addStretch(2)
        self.btns = [base_radio, small_radio, medium_radio, turbo_radio]

        for btn in self.btns:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumSize(180, 45)
            btn.setStyleSheet("color:black;")
            btn.setFont(self.font_regular)
            self.modeles_layout.addWidget(btn)
            self.modeles_layout.addStretch(1)

        modeles_section = QGroupBox()
        modeles_section.setLayout(self.modeles_layout)
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
            input.setStyleSheet("color:black; background:#fff;")
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
        normes_metrique_layout = QVBoxLayout()
        normes_metrique_layout.addSpacing(8)
        normes_metrique_layout.setContentsMargins(30, 0, 30, 0)
        normes_metrique_layout.addLayout(texte_layout)
        normes_metrique_layout.addStretch(1)
        normes_metrique_layout.addWidget(notice)
        normes_metrique_layout.addStretch(1)
        normes_metrique_layout.addLayout(metriques_contrainer)
        normes_metrique_layout.addStretch(1)

        metriques_section = QGroupBox()
        metriques_section.setLayout(normes_metrique_layout)
        # personnaliser les QGroupBox
        self.styleSection(metriques_section)

        return metriques_section

    def styleSection(self, section):
        section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        section.setMinimumSize(380, 450)
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
            self.modeles.setFixedSize(466, 450)
            self.metriques.setFixedSize(466, 450)
            self.modeles_layout.setContentsMargins(30, 0, 30, 0)
        else:
            self.modeles.setFixedSize(280, 310)
            self.metriques.setFixedSize(317, 310)
            self.modeles_layout.setContentsMargins(20, 0, 20, 0)


        self.adjustFonts()

    def chargerValeurs(self):

        chemin_fichier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "settings.json")
        print(chemin_fichier)

        # Normaliser le chemin (Windows/Linux/Mac)
        chemin_fichier = os.path.normpath(chemin_fichier)

        if not os.path.exists(chemin_fichier):
            print("Erreur : Fichier JSON non trouvé !")
            return

        # ouvrir le fichier en mode lecture
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
            # charger les valeurs des metriques
            metriques = data.get("ratio_metrique", {})

            champs = [
                "duree", "nbrMot", "motDif", "nbrEnonce",
                "morpheme", "morphemeEnonce", "lemme"
            ]

            for i, champ in enumerate(champs):
                if champ in metriques and i < len(self.inputs):
                    self.inputs[i].setText(str(metriques[champ]))

                # charger les valeurs du modele
                # Charger et sélectionner le modèle de transcription
                model_whisper = data.get("modelWhisper", 0)
                if model_whisper == 0:
                    self.btns[0].setChecked(True)
                elif model_whisper == 1:
                    self.btns[1].setChecked(True)
                elif model_whisper == 2:
                    self.btns[2].setChecked(True)
                elif model_whisper == 3:
                    self.btns[3].setChecked(True)

    def updateValeurs(self):

        chemin_fichier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "settings.json")
        print(chemin_fichier)

        # Normaliser le chemin (Windows/Linux/Mac)
        chemin_fichier = os.path.normpath(chemin_fichier)

        if not os.path.exists(chemin_fichier):
            print("Erreur : Fichier JSON non trouvé !")
            return

        try:
            with open(chemin_fichier, "r", encoding="utf-8") as fichier:
                data = json.load(fichier)

            # Récupérer les valeurs saisies dans les QLineEdit
            ratio_metrique = data.get("ratio_metrique", {})
            labels = ["duree", "nbrMot", "motDif", "nbrEnonce",
                      "morpheme", "morphemeEnonce", "lemme"]

            valide = True

            for i, label in enumerate(labels):
                champ = self.inputs[i]

                if champ.hasAcceptableInput():
                    ratio_metrique[label] = int(champ.text())
                    champ.setStyleSheet("")  # reset le style
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
                return  # 🔒 ne pas aller plus loin si des valeurs sont fausses
            # mettre a jour la valeur de modeleWhisper dans le json
            # Mettre à jour le modèle de transcription choisi
            model_whisper = 0
            if self.btns[0].isChecked():
                model_whisper = 0
            elif self.btns[1].isChecked():
                model_whisper = 1
            elif self.btns[2].isChecked():
                model_whisper = 2
            elif self.btns[3].isChecked():
                model_whisper = 3

            data["modelWhisper"] = model_whisper
            # Réécrire les données modifiées dans le fichier JSON
            with open(chemin_fichier, "w", encoding="utf-8") as fichier:
                json.dump(data, fichier, ensure_ascii=False, indent=4)

            # Afficher le message de succès ici
            msg = QMessageBox()
            msg.setText("Les paramètres ont été sauvegardés avec succès.")
            msg.setWindowTitle("Succès")
            msg.exec()

        except FileNotFoundError:
            print("Fichier JSON non trouvé !")
        except json.JSONDecodeError:
            print("Erreur lors du chargement du JSON !")
        except ValueError:
            print("Erreur : Les valeurs saisies doivent être des nombres entiers.")

    def adjustFonts(self):
        """Ajuste dynamiquement la taille des polices selon la largeur de la fenêtre"""

        # Calcul des tailles basées sur des proportions mesurées
        new_size_regular = int(self.width() * 0.0106)
        new_size_bold = int(self.width() * 0.0149)
        new_size_medium = int(self.width() * 0.0106)

        # Limites
        new_size_regular = max(8, min(new_size_regular, 12))
        new_size_bold = max(9, min(new_size_bold, 14))
        new_size_medium = max(10, min(new_size_medium, 12))

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

        #mettre le bouton dans un layout pour l'aligner horizontalement
        layout=QHBoxLayout()
        layout.addSpacing(10)
        layout.addWidget(btn)
        layout.addStretch(1)

        return layout
