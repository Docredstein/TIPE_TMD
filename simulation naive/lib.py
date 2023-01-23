import typing



class simulation :
    object_dic = {}
    def __init__(self) -> None:
        pass
    def get_Object(self,id) :
        return simulation.object_dic[id]


class Object(simulation) :
    current_id=0
    
    def __init__(self) -> None:
        super().__init__()
        self.id = Object.current_id
        Object.current_id += 1
        simulation.object_dic[self.id] = self








class barre(Object) :
    def __init__(self,origin,angle,angle_offset,length,k,theta_0,fixe=False,parent:"barre"=None) -> None:
        super().__init__()
        self.origin = origin
        self.angle = angle
        self.relative_angle = angle
        self.angle_offset = theta_0
        self.length = length
        self.angle_offset = angle_offset
        self.k = k        
        
        self.parent = parent
        self.fixe = fixe
        self.absolute_angle = 0
    def __repr__(self) -> str:
        return f"Barre id={self.id}, origin = {self.origin}, relative_angle = {self.angle}, lenght = {self.length} parent :\n{self.parent}"
    def get_absolute_angle(self) -> float:
        if self.parent == None : 
            return self.angle 
        return self.angle + self.angle_offset + self.parent.get_absolute_angle()
    
        
