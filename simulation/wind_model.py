import numpy as np

class WindModel:
    """
    Simulates wind effects on trajectory with different wind profiles.
    """
    
    def __init__(self, wind_speed=0.0, wind_direction=0.0, altitude_variation=False):
        """
        Initialize wind model.
        
        Args:
            wind_speed (float): Base wind speed in m/s
            wind_direction (float): Wind direction in degrees (0 = North, 90 = East)
            altitude_variation (bool): Whether wind speed varies with altitude
        """
        self.wind_speed = wind_speed
        self.wind_direction = np.radians(wind_direction)
        self.altitude_variation = altitude_variation
        
    def get_wind_vector(self, altitude=0.0):
        """
        Get wind vector components at given altitude.
        
        Args:
            altitude (float): Current altitude in meters
            
        Returns:
            tuple: (wind_x, wind_y) components in m/s
        """
        speed = self.wind_speed
        
        if self.altitude_variation:
            # Wind speed increases with altitude (simple model)
            speed = self.wind_speed * (1 + 0.1 * altitude / 1000)
            
        wind_x = speed * np.sin(self.wind_direction)
        wind_y = speed * np.cos(self.wind_direction)
        
        return wind_x, wind_y
    
    def turbulent_wind(self, time):
        """
        Add turbulence component to wind (simple sinusoidal model).
        
        Args:
            time (float): Current time in seconds
            
        Returns:
            tuple: (turbulence_x, turbulence_y) components in m/s
        """
        turbulence = 0.5 * np.sin(2 * np.pi * 0.2 * time)  # Simple turbulence model
        return turbulence, turbulence