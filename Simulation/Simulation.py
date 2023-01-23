from abc import ABC




class Scene :
    def __init__(self,name="Scène") :
        self.name = name
        self.moving = [] 
        self.refs = []
        self.result = []
    def __repr__(self) -> str:
        out = f"{self.name} :"
        out += "\n-------Pièces Mobiles---------\n"
        for i in self.moving :
            out += str(i)
        out += "\n-------Pièces fixes---------\n"
        for i in self.refs :
            out += str(i)
        out += "\n-------Résultat---------\n"
        for i in self.result :
            out += i
        return out
    
class object(ABC) : 
    def __init__(self):
        pass
    def __repr__(self) -> str:
        pass
    def draw(self) :
        pass
class liaison(object) :
    def __init__(self,M0:list,start=None,end=None):
        super().__init__()
        self.start = start 
        self.end = end
        self.M0 =M0
    def __repr__(self) -> str:
        pass
class pivotRetour(liaison) :
    id_object = 0
    def __init__(self,k_retour,f_frottement,M0:list,start=None,end=None):
        super().__init__(M0,start,end)
        self.id = pivotRetour.id_object 
        pivotRetour += 1
class LiaisonFlottante(liaison) :
    id_object = 0 
    def __init__(self, M0: list, start=None, end=None):
        super().__init__(M0, start, end) 
        self.id = LiaisonFlottante.id_object
        LiaisonFlottante.id_object += 1     
class baton(object) :
    id_object = 0
    def __init__(self,mass,J1,J2,start=None,end=None,fixed=False) :
        self.mass = mass
        self.J1 = J1
        self.J2 = J2 
        self.start = start
        self.end = end
        self.fixed = fixed 
        self.id = baton.id_object
        baton.id_object+= 1
    def __repr__(self) -> str:
        return f"Baton N°{self.id=} : début = {self.start}, fin = {self.end}  "


