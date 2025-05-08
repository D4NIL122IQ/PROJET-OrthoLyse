import os
import json

class SettingsController:
    def __init__(self):
        self.chemin_fichier = os.path.normpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "../assets/JSON", "settings.json")
        )

    def charger_parametres(self):
        if not os.path.exists(self.chemin_fichier):
            raise FileNotFoundError("Fichier JSON non trouvé !")

        with open(self.chemin_fichier, "r", encoding="utf-8") as f:
            return json.load(f)

    def sauvegarder_parametres(self, data):
        with open(self.chemin_fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_model_whisper(self):
        data = self.charger_parametres()
        return data.get("modelWhisper", 0)

    def set_model_whisper(self, model_index):
        data = self.charger_parametres()
        data["modelWhisper"] = model_index
        self.sauvegarder_parametres(data)

    def get_metriques(self):
        data = self.charger_parametres()
        return data.get("ratio_metrique", {})

    def set_metriques(self, nouvelles_valeurs: dict):
        data = self.charger_parametres()
        data["ratio_metrique"] = nouvelles_valeurs
        self.sauvegarder_parametres(data)

