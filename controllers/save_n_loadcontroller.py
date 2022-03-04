from models.save_n_loadmodel import Save_and_load


class Save_and_load_Ctrlr:
    def __init__(self):
         pass

    def dis_bonjour_save_n_load_ctrl(self):  #TEST INITIAL - A SUPPRIMER
        print ('Bonjour de la classe Save_and_load_Ctrlr - fichier save_n_loadcontroller')

    def save_program(self):
        # save all data of the whole program
        Save_and_load.save_in_db_backup(self)

    def load_progam(self):
        # load a backup of the program
        Save_and_load.load_db_backup(self)
