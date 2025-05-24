import matplotlib.pyplot as plt
from .trajectory_calc import TrajectoryCalculator
from .wind_model import WindModel

class TrajectorySimulator:
    """
    Simulates and visualizes projectile trajectories with wind effects.
    """
    
    def __init__(self, config=None):
        """
        Initialize the simulator with optional configuration.
        
        Args:
            config (dict): Configuration dictionary
        """
        self.config = config or {
            'gravity': 9.81,
            'air_density': 1.225,
            'drag_coefficient': 0.47
        }
        
    def run_simulation(self, initial_conditions, wind_conditions=None):
        """
        Run a trajectory simulation with given conditions.
        
        Args:
            initial_conditions (dict): Initial conditions for the projectile
            wind_conditions (dict): Wind model parameters
            
        Returns:
            dict: Simulation results
        """
        wind_model = WindModel(**(wind_conditions or {}))
        calculator = TrajectoryCalculator(
            wind_model=wind_model,
            gravity=self.config['gravity'],
            air_density=self.config['air_density'],
            drag_coefficient=self.config['drag_coefficient']
        )
        
        results = calculator.calculate_trajectory(
            initial_position=(initial_conditions['x0'], initial_conditions['y0']),
            initial_velocity=(initial_conditions['vx0'], initial_conditions['vy0']),
            mass=initial_conditions['mass'],
            cross_sectional_area=initial_conditions['cross_sectional_area'],
            time_step=initial_conditions.get('time_step', 0.1),
            max_time=initial_conditions.get('max_time', 10)
        )
        
        return results
    
    def plot_trajectory(self, results, title="Projectile Trajectory"):
        """
        Plot the trajectory from simulation results.
        
        Args:
            results (dict): Simulation results from run_simulation
            title (str): Plot title
        """
        plt.figure(figsize=(10, 6))
        plt.plot(results['x'], results['y'])
        plt.title(title)
        plt.xlabel("Horizontal Distance (m)")
        plt.ylabel("Altitude (m)")
        plt.grid(True)
        plt.axhline(0, color='k', linestyle='--')  # Ground level
        plt.show()