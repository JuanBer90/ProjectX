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

