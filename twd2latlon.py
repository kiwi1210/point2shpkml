# reference: http://blog.ez2learn.com/2009/08/15/lat-lon-to-twd97/

from math import tan, sin, cos, radians, degrees

class TMToLatLon(object):
    def __init__(self,
        a = 6378137.0,
        b = 6356752.314245,
        long0 = radians(121),
        k0 = 0.9999,
        dx = 250000,
        dy = 0,
    ):		
    
        self.a = a
        self.b = b
        self.long0 = long0
        self.k0 = k0
        self.dx = dx
        self.dy = dy
        
    
    def convert(self, x, y):

        a = self.a
        b = self.b
        long0 = self.long0
        k0 = self.k0
        dx = self.dx
        dy = self.dy
        e = (1-b**2/a**2)**0.5
        
        x -= dx
        y -= dy

        # Calculate the Meridional Arc
        M = y/k0

        # Calculate Footprint Latitude
        mu = M/(a*(1.0 - e ** 2/4.0 - 3 * e ** 4/64.0 - 5* e** 6/256.0))
        e1 = (1.0 - (1.0 - e ** 2) ** 0.5) / (1.0 + (1.0 - e**2)**0.5)

        J1 = 3*e1/2 - 27*e1** 3/32.0
        J2 = 21*e1** 2/16 - 55*e1**4/32.0
        J3 = 151*e1**3/96.0
        J4 = 1097*e1**4/512.0

        fp = mu + J1*sin(2*mu) + J2*sin(4*mu) + J3*sin(6*mu) + J4*sin(8*mu)

        # Calculate Latitude and Longitude

        e2 = (e*a/b)**2
        C1 = e2*cos(fp)**2
        T1 = tan(fp)**2
        R1 = a*(1-e**2)/((1-e**2*(sin(fp)**2))**(3.0/2.0))
        N1 = a/((1-e**2*(sin(fp)**2))**0.5)

        D = x/(N1*k0)

        # lat
        Q1 = N1*tan(fp)/R1
        Q2 = (D**2)/2.0
        Q3 = (5 + 3*T1 + 10*C1 - 4*C1**2 - 9*e2)*D**4/24.0;
        Q4 = (61 + 90*T1 + 298*C1 + 45*T1**2 - 3*C1**2 - 252*e2)*D**6/720.0
        lat = fp - Q1*(Q2 - Q3 + Q4)

        # long
        Q5 = D
        Q6 = (1 + 2*T1 + C1)*D**3/6
        Q7 = (5 - 2*C1 + 28*T1 - 3*C1**2 + 8*e2 + 24*T1**2)*D**5/120.0
        lon = long0 + (Q5 - Q6 + Q7)/cos(fp)

        return degrees(lat), degrees(lon)
        
if __name__ == '__main__':

    c = TMToLatLon()
    #x = radians(float(input('X: ')))
    #y = radians(float(input('y: ')))
    x = 250000.0
    y = 2765777.563632634
    print('input x,y: ', x, y)
    lat, lon = c.convert(x, y)
    print (lat, lon)