class Save_and_load_Views:
    def __init__(self):
         pass

    def dis_bonjour_save_n_load_views(self):  # TEST INITIAL - A SUPPRIMER
        print ('Bonjour de la classe Save_and_load_Views - fichier save_n_loadviews')

    @classmethod
    def ask_programm_saving(cls):
        print("Voulez-vous faire une sauvegarde ? (O/N)")

    @classmethod
    def ask_backup_loading(cls):
        print("Voulez-vous charger une sauvegarde du programme ? (O/N)")
