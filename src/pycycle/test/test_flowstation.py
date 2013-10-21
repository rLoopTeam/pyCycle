
import unittest

from openmdao.util.testutil import assert_rel_error

from pycycle.flowstation import AirFlowStation

fs = AirFlowStation()
fs.add_reactant( ['N2', 'O2', 'AR', 'CO2', '', ''],[.7547, .232, .0128, 0.00046, 0., 0. ] )
fs.add_reactant( ['H2O', '', '', '', '', ''], [1., 0., 0., 0., 0., 0. ] )    
fs.add_reactant( ['CH2', 'CH', '', '', '', ''], [.922189, 0.07781, 0., 0., 0., 0. ] )           
fs.add_reactant( ['CH2', 'CH', '', '', '', ''], [.922189, 0.07781, 0., 0., 0., 0. ] )           
fs.add_reactant( ['C', 'H', '', '', '', ''], [.862,.138, 0., 0., 0., 0. ] )   
fs.add_reactant( ['Jet-A(g)', '', '', '', '', ''], [1., 0., 0., 0., 0., 0. ] )   


class FlowStationTestCase(unittest.TestCase):

    def setUp(self): 
        """Initialization function called before every test function""" 
        self.fs = AirFlowStation()

        self.fs.W = 100
        self.fs.setDryAir()
        self.fs.setTotalTP(518, 15)

    def tearDown(self): 
        """Clean up function called after every test function"""
        pass #nothing to do for this test

    def test_copyFS(self): 

        #print "TESTING"

        self.new_fs = AirFlowStation()

        self.new_fs.copy_from(self.fs)

        assert_rel_error(self,self.new_fs.Tt, 518, .001)
        assert_rel_error(self,self.new_fs.Pt, 15, .001)

     #all test function have to start with "test_" as the function name
    def test_setTotalTP(self):
        assert_rel_error(self,self.fs.Pt, 15.0, .001)
        assert_rel_error(self,self.fs.Tt, 518, .001)
        assert_rel_error(self,self.fs.ht, -6.2274, .001) #Tom says the ht values will be different
        assert_rel_error(self,self.fs.W, 100, .001)
        assert_rel_error(self,self.fs.rhot, .07815, .001)
        assert_rel_error(self,self.fs.gamt, 1.401, .001)

    def test_setTotal_hP(self):
        ht = self.fs.ht
        self.fs.setTotalTP(1000, 40) #just to move things around a bit
        self.fs.setTotal_hP(ht, 15)
        self.test_setTotalTP() #just call this since it has all the checks we need  

    def test_setTotal_SP(self):
        s = self.fs.s
        self.fs.setTotalTP(1000, 40) #just to move things around a bit
        self.fs.setTotalSP(s, 15)      
        self.test_setTotalTP() #just call this since it has all the checks we need  
     
    def test_delh(self):
        ht = self.fs.ht
        self.fs.setTotalTP(1000, 40)
        diffh = self.fs.ht - ht
        assert_rel_error(self,diffh, 117.4544, .001)        
        
    def test_dels(self):
        s = self.fs.s
        self.fs.setTotalTP(1000, 40)
        diffs = self.fs.s - s
        assert_rel_error(self,diffs, .092609, .001)        
        
    def test_set_WAR(self):
        self.fs.setWAR( 0.02 )
        self.fs.setTotalTP(1000, 15); 
        assert_rel_error(self,self.fs.Pt, 15., .001)
        assert_rel_error(self,self.fs.Tt, 1000, .001)
        assert_rel_error(self,self.fs.WAR, 0.02, .001)
        assert_rel_error(self,self.fs.FAR, 0, .001)
        assert_rel_error(self,self.fs.ht, -2.2500, .001)
        .001
    def test_setDryAir(self):
        self.fs.setDryAir()
        self.fs.setTotalTP(1000, 15); 
        assert_rel_error(self,self.fs.Pt, 15.,.001)
        assert_rel_error(self,self.fs.Tt, 1000, .001)
        assert_rel_error(self,self.fs.WAR, 0.0, .001)
        assert_rel_error(self,self.fs.FAR, 0, .001)
        assert_rel_error(self,self.fs.ht, 111.225, .001)
        assert_rel_error(self,self.fs.WAR, 0, .001)
        assert_rel_error(self,self.fs.FAR, 0, .001)



class TestBurn(unittest.TestCase): 
    def setUp(self):
        self.fs = AirFlowStation()

        self.fs.setDryAir()
        self.fs.setTotalTP(1100, 400)
        self.fs.W = 100
 
        self.fs.burn(4,2.5, -642)  
   
        
    #all test cases use the same checks here, so just re-use
    def _assert(self): 
        #print (self.fs._flow)  assert_rel_error(self,self.fs.W, 102.5, places=2)
        assert_rel_error(self,self.fs.FAR, .025, .001)   
        assert_rel_error(self,self.fs.Pt, 400, .001)
        assert_rel_error(self,self.fs.Tt, 2669.72, .001)
        assert_rel_error(self,self.fs.ht, 117.26, .001) 
        assert_rel_error(self,self.fs.rhot, .401845715, .001)
        assert_rel_error(self,self.fs.W, 102.5, .001)
        assert_rel_error(self,self.fs.gamt, 1.2935, .001)

    def test_burn(self):         
        self._assert()
        
    def test_add( self ):
        self.fs1 = AirFlowStation()

        self.fs1.setDryAir()
        self.fs1.setTotalTP(1000, 15)
        self.fs1.W = 10.
        self.fs1.setWAR( .02 )
        self.fs.add( self.fs1 )
        assert_rel_error(self,self.fs.W, 112.5, .001)
        assert_rel_error(self,self.fs.FAR, .02272, .001)   
        assert_rel_error(self,self.fs.Pt, 400, .001)
        assert_rel_error(self,self.fs.Tt, 2539.80, .001)
        assert_rel_error(self,self.fs.ht, 107.920, .001)
        assert_rel_error(self,self.fs.gamt, 1.2973, .001)
        
class TestStatics(unittest.TestCase): 
    def setUp(self):
        self.fs = AirFlowStation()
        self.fs.W = 100.
        self.fs.setDryAir()
        self.fs.setTotalTP(1100, 400)      
        #print (self.fs._flow)  

    #all test cases use the same checks here, so just re-use
    def _assert(self): 
 
        assert_rel_error(self,self.fs.area, 32.0066, .001)  
        assert_rel_error(self,self.fs.Mach, .3, .001)   
        assert_rel_error(self,self.fs.Ps, 376.219, .001)
        assert_rel_error(self,self.fs.Ts, 1081.732, .001)   
        assert_rel_error(self,self.fs.Vflow, 479.298, .001)
        assert_rel_error(self,self.fs.rhos, .9347, .001)       
        assert_rel_error(self,self.fs.Mach, .3, .001)   
        
    def test_set_Mach(self):
        self.fs.Mach = .3
        self._assert()

    def test_set_area(self):
        self.fs.area = 32.0066
        self.assertLess(self.fs.Mach, 1)
        self._assert()

    def test_set_Ps(self):
        self.fs.Ps = 376.219
        self._assert()
        
    def test_setStaticTsPsMN(self):
        self.fs.setStaticTsPsMN(1081.802, 376.219, .3)
        self._assert()
        
    def test_set_sub(self): 

        self.fs.sub_or_super = "sub"
        self.fs.area = 32
        self.assertLess(self.fs.Mach, 1)

    def test_set_super(self): 

        self.fs.sub_or_super = "super"
        self.fs.area = 32
        self.assertGreater(self.fs.Mach, 1)

        
if __name__ == "__main__":
    unittest.main()
    