class Grafo(object):
    def __init__(self):
        self.relaciones = {}
        
    def __str__(self):
        return str(self.relaciones)
 
    def agregar(self, elemento):
        self.relaciones.update({elemento:[]})
    
    def relacionar(self, elemento1, elemento2):
        self.relacionarUnilateral(elemento1, elemento2)
        self.relacionarUnilateral(elemento2, elemento1)
        
    def relacionarUnilateral(self, origen, destino):
        self.relaciones[origen].append(destino)
        
    def hay_ciclo(self):
        items=[]
        print self.relaciones
        for key,values in self.relaciones.iteritems():  
            aux=[key,values]
            items.append(aux)

        ciclo=False
        a=[]
        for item in items:
            
            item[1].sort()
            
            a.append(item[1])
        print a
            
        for item  in a:
             
             if a.count(item) > 1:
                    ciclo=True            
        return ciclo
    
    def imprimir(self):
        items=[]
        for key,values in self.relaciones.iteritems():    
            aux=[key,values]
            items.append(aux)

        ciclo=False
        for item  in items:
            lista_item=item[1]
            for element in lista_item:
                if lista_item.count(element) > 1:
                    ciclo=True
            print item
        return ciclo
        
    