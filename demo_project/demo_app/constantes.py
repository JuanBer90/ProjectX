from django.db import connection


class EstadosFase:
    FASE_NI = 'NO-INICIADA'
    FASE_DE= 'DESARROLLO'
    FASE_FI = 'FINALIZADA'

    def estados_fase(self):
        estados=[]
        estados.append(self.FASE_NI)
        estados.append(self.FASE_DE)
        estados.append(self.FASE_FI)
        return estados



class EstadosItem:
    ITEM_NI='INICIADO'
    ITEM_AP='APROBADO'
    ITEM_BL='BLOQUEADO'
    ITEM_EL='ELIMINADO'

    def estados_item(self):
        estados=[]
        estados.append(self.ITEM_NI)
        estados.append(self.ITEM_AP)
        estados.append(self.ITEM_BL)
        estados.append(self.ITEM_EL)
        return estados

class EstadoProyecto:
    PRO_IN='INICIADO'
    PRO_NI='NO-INICIADO'
    PRO_FI='FINALIZADO'



class RelacionEstados:
    A_S='ANTECESOR/SUCESOR'
    P_H='PADRE/HIJO'

    def estados_relacion(self):
        estados=[]
        estados.append(self.A_S)
        estados.append(self.P_H)
        return estados

class EstadosLB:
    ABIERTO='ABIERTO'
    CERRADO = 'CERRADO'



def execute_query(query):
   cursor = connection.cursor()
   cursor.execute(query)
   rows = cursor.fetchall()
   return rows

def execute_one(query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchone()


