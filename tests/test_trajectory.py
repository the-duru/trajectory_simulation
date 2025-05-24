import pytest
import numpy as np
from trajectory_simulation.simulation.trajectory_calc import TrajectoryCalculator
from trajectory_simulation.simulation.wind_model import WindModel

class TestTrajectory:
    """Test cases for trajectory calculations."""
    
    def test_no_wind_trajectory(self):
        """Test trajectory with no wind."""
        calculator = TrajectoryCalculator()
        results = calculator.calculate_trajectory(
            initial_position=(0, 0),
            initial_velocity=(10, 10),
            mass=1,
            cross_sectional_area=0.1,
            max_time=2
        )
        
        # Check that projectile reaches maximum height and comes down
        assert np.max(results['y']) > 0
        assert results['y'][-1] < np.max(results['y'])
        
    def test_wind_effect(self):
        """Test that wind affects the trajectory."""
        no_wind_calc = TrajectoryCalculator()
        wind_calc = TrajectoryCalculator(wind_model=WindModel(wind_speed=5, wind_direction=90))
        
        no_wind_results = no_wind_calc.calculate_trajectory(
            initial_position=(0, 0),
            initial_velocity=(10, 10),
            mass=1,
            cross_sectional_area=0.1,
            max_time=2
        )
        
        wind_results = wind_calc.calculate_trajectory(
            initial_position=(0, 0),
            initial_velocity=(10, 10),
            mass=1,
            cross_sectional_area=0.1,
            max_time=2
        )
        
        # With eastward wind, x position should be greater
        assert wind_results['x'][-1] > no_wind_results['x'][-1]
        
    def test_altitude_variation(self):
        """Test that wind varies with altitude."""
        wind_model = WindModel(wind_speed=5, wind_direction=0, altitude_variation=True)
        calculator = TrajectoryCalculator(wind_model=wind_model)
        
        results = calculator.calculate_trajectory(
            initial_position=(0, 0),
            initial_velocity=(10, 50),  # High trajectory
            mass=1,
            cross_sectional_area=0.1,
            max_time=5
        )
        
        # Check that wind at peak altitude is stronger than at ground level
        peak_idx = np.argmax(results['y'])
        initial_wind = wind_model.get_wind_vector(altitude=0)
        peak_wind = wind_model.get_wind_vector(altitude=results['y'][peak_idx])
        
        assert np.linalg.norm(peak_wind) > np.linalg.norm(initial_wind)