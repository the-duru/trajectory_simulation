import numpy as np
from scipy.integrate import odeint
from .wind_model import WindModel

class TrajectoryCalculator:
    """
    Calculates projectile trajectory considering wind and environmental factors.
    """
    
    def __init__(self, wind_model=None, gravity=9.81, air_density=1.225, drag_coefficient=0.47):
        """
        Initialize trajectory calculator.
        
        Args:
            wind_model (WindModel): Wind model instance
            gravity (float): Gravitational acceleration (m/s^2)
            air_density (float): Air density (kg/m^3)
            drag_coefficient (float): Drag coefficient of the projectile
        """
        self.wind_model = wind_model or WindModel()
        self.gravity = gravity
        self.air_density = air_density
        self.drag_coefficient = drag_coefficient
        
    def equations_of_motion(self, state, time, mass, cross_sectional_area):
        """
        Define the differential equations for projectile motion with drag.
        
        Args:
            state (list): [x, y, vx, vy] current state
            time (float): Current time
            mass (float): Mass of projectile (kg)
            cross_sectional_area (float): Cross-sectional area (m^2)
            
        Returns:
            list: Derivatives [dx/dt, dy/dt, dvx/dt, dvy/dt]
        """
        x, y, vx, vy = state
        
        # Wind components
        wind_x, wind_y = self.wind_model.get_wind_vector(altitude=y)
        turb_x, turb_y = self.wind_model.turbulent_wind(time)
        wind_x += turb_x
        wind_y += turb_y
        
        # Relative velocity to wind
        vx_rel = vx - wind_x
        vy_rel = vy - wind_y
        v_rel = np.sqrt(vx_rel**2 + vy_rel**2)
        
        # Drag force
        drag_force = 0.5 * self.air_density * v_rel**2 * self.drag_coefficient * cross_sectional_area
        
        # Derivatives
        dxdt = vx
        dydt = vy
        
        if v_rel > 0:
            dvxdt = -drag_force * vx_rel / (mass * v_rel)
            dvydt = -self.gravity - drag_force * vy_rel / (mass * v_rel)
        else:
            dvxdt = 0
            dvydt = -self.gravity
            
        return [dxdt, dydt, dvxdt, dvydt]
    
    def calculate_trajectory(self, initial_position, initial_velocity, mass, cross_sectional_area, time_step=0.1, max_time=10):
        """
        Calculate the trajectory by solving the differential equations.
        
        Args:
            initial_position (tuple): (x0, y0) in meters
            initial_velocity (tuple): (vx0, vy0) in m/s
            mass (float): Mass in kg
            cross_sectional_area (float): Area in m^2
            time_step (float): Time step for integration
            max_time (float): Maximum simulation time
            
        Returns:
            dict: Trajectory data with time, position and velocity arrays
        """
        initial_state = [initial_position[0], initial_position[1], 
                         initial_velocity[0], initial_velocity[1]]
        
        time_points = np.arange(0, max_time, time_step)
        
        solution = odeint(self.equations_of_motion, initial_state, time_points,
                          args=(mass, cross_sectional_area))
        
        return {
            'time': time_points,
            'x': solution[:, 0],
            'y': solution[:, 1],
            'vx': solution[:, 2],
            'vy': solution[:, 3]
        }