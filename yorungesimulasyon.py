import numpy as np
import matplotlib.pyplot as plt

# Sabitler
GRAVITY_CONSTANT = 6.67430e-11  # Evrensel çekim sabiti, m^3 kg^-1 s^-2
EARTH_MASS = 5.972e24          # Dünya'nın kütlesi, kg
AIR_DENSITY = 1.225            # Havanın yoğunluğu, kg/m^3
DRAG_COEFFICIENT = 0.47        # Rüzgar direnci katsayısı (küresel obje için)
OBJECT_AREA = 0.1              # Objenin alanı, m^2

# Başlangıç koşulları
initial_position = np.array([7e6, 0])    # Başlangıç konumu vektörü, m
initial_velocity = np.array([0, 7.12e3]) # Başlangıç hızı vektörü, m/s

def compute_orbit_with_drag(position, velocity, gravity, mass, air_density, drag_coefficient, object_area, wind_speed, time_step=10, steps=1000):
    positions = [position]
    velocities = [velocity]
    
    for _ in range(steps):
        distance = np.linalg.norm(positions[-1])
        drag_force = 0.5 * air_density * np.linalg.norm(velocities[-1] - wind_speed)**2 * drag_coefficient * object_area
        drag_acceleration = drag_force / mass
        gravitational_acceleration = -gravity * mass * positions[-1] / distance**3
        total_acceleration = gravitational_acceleration - drag_acceleration * (velocities[-1] - wind_speed) / np.linalg.norm(velocities[-1] - wind_speed)
        new_velocity = velocities[-1] + total_acceleration * time_step
        new_position = positions[-1] + new_velocity * time_step
        velocities.append(new_velocity)
        positions.append(new_position)
    
    return np.array(positions), np.array(velocities)

# Yörüngeyi hesapla
wind_speed = np.array([10, 0])  # Rüzgar hız vektörü, m/s
positions, velocities = compute_orbit_with_drag(initial_position, initial_velocity, GRAVITY_CONSTANT, EARTH_MASS, AIR_DENSITY, DRAG_COEFFICIENT, OBJECT_AREA, wind_speed)

# Sonuçları görselleştir
plt.plot(positions[:, 0], positions[:, 1])
plt.xlabel('X Konumu (m)')
plt.ylabel('Y Konumu (m)')
plt.title('Nesne Yörüngesi')
plt.show()

