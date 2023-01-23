import lib 

def test_base() :
    a = lib.barre(origin=(0,0),angle=15,angle_offset=0,length=5,k=0.1,theta_0=0)
    b = lib.barre((5,5),3,3,1,0,0,parent=a)
    assert b.get_absolute_angle() == 21