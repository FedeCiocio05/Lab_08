from database.DB_connect import DBConnect
from model.prezzo_DTO import Prezzo

"""
    PREZZO DAO
    Gestisce le operazioni di accesso alla tabella prezzo.
"""

class PrezzoDAO:
    @staticmethod
    def get_prezzi(id_distributore) -> list[Prezzo] | None:
        """
        Restituisce tutti i prezzi di un distributore
        :return: lista di tutti i Prezzi di un certo distributore
        """
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT * FROM prezzo WHERE id_distributore = %s """
        try:
            cursor.execute(query, (id_distributore,))
            for row in cursor:
                prezzo = Prezzo(
                    data=row["data"],
                    prezzo_litro=float(row["prezzo_litro"]),
                    id_distributore=row["id_distributore"],
                )
                result.append(prezzo)
        except Exception as e:
            print(f"Errore durante la query get_prezzi: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result
