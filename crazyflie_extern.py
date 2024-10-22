from controller import Supervisor
from threading import Thread

from typing import List

class CrazyflieExternController(Supervisor):
    def __init__(self, run):
        super().__init__()
        print("Crazyflie extern-controller started.")

        self.wb_node = self._getNode(self)
  
        self.target_field = self.wb_node.getField('target')
        self.position_field = self.wb_node.getField('translation')
        self.range_finder = self.wb_node.getField('zrange')

        thread = Thread(target=run)
        thread.start()      
        timestep = int(self.getBasicTimeStep())
        while self.step(timestep) != -1:
            pass
    
    def setTarget(self, target: List[float]) -> None:
        """
        Set the target position of the Crazyflie. 

        Args: 
            target (List[float]): A list of 3 float describing the x, y and z coordinates.
        Returns: 
            None        
        """
        self.target_field.setSFVec3f(target)

    def getPosition(self) -> List[float]:
        """
        Get the position of the Crazyflie.
        
        Returns:
            float[]: The position of the Crazyflie as x, y, z coordinates in meter
        """
        return self.position_field.getSFVec3f()
    
    def getRange(self) -> float:
        """
        Get the current range value from the range finder. 
        (Sensor is pointing straight down.)

        Returns: 
            float: The current range in mm as a float
        """
        return self.range_finder.getSFFloat()

    def _getNode(self, super):
        robot = super.getSelf()
        return robot.getParentNode()
    

if __name__ == "__main__":
    wb = CrazyflieExternController()