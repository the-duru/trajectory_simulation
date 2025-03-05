import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

def compute_orbit_with_drag(initial_position, initial_velocity, GRAVITY_CONSTANT, EARTH_MASS, AIR_DENSITY, DRAG_COEFFICIENT, OBJECT_AREA, wind_speed):
    # Basit bir örnek olarak yörünge hesaplaması yapacağız
    positions = []
    velocities = []
    
    # Örnek bir hesaplama döngüsü (bu kısım ihtiyacınıza göre detaylandırılabilir)
    for t in range(100):  # 100 adımlık örnek döngü
        new_position = initial_position + initial_velocity * t  # Basit bir hareket hesabı
        new_velocity = initial_velocity - (DRAG_COEFFICIENT * AIR_DENSITY * OBJECT_AREA * initial_velocity) / (2 * EARTH_MASS)  # Hava direnci etkisi
        
        positions.append(new_position)
        velocities.append(new_velocity)
    
    return np.array(positions), np.array(velocities)

def start_simulation():
    initial_position = np.array([0, 0])  # Başlangıç konumu tanımlanıyor
    initial_velocity = np.array([10, 10])  # Başlangıç hızı tanımlanıyor
    GRAVITY_CONSTANT = 9.81
    EARTH_MASS = 5.97e24
    AIR_DENSITY = 1.225
    DRAG_COEFFICIENT = 0.47
    OBJECT_AREA = 1.0
    
    # Kullanıcıdan girdiler al
    wind_speed_x = float(wind_speed_x_entry.get())
    wind_speed_y = float(wind_speed_y_entry.get())
    
    wind_speed = np.array([wind_speed_x, wind_speed_y])
    
    # Simülasyonu çalıştır
    positions, velocities = compute_orbit_with_drag(initial_position, initial_velocity, GRAVITY_CONSTANT, EARTH_MASS, AIR_DENSITY, DRAG_COEFFICIENT, OBJECT_AREA, wind_speed)
    
    # Sonuçları görselleştir
    plt.plot(positions[:, 0], positions[:, 1])
    plt.xlabel('X Konumu (m)')
    plt.ylabel('Y Konumu (m)')
    plt.title('Nesne Yörüngesi')
    plt.show()

# Tkinter arayüzü oluştur
root = tk.Tk()
root.title("Yörünge Simülatörü")

# Rüzgar hızı girdileri
tk.Label(root, text="Rüzgar Hızı X (m/s)").grid(row=0)
tk.Label(root, text="Rüzgar Hızı Y (m/s)").grid(row=1)

wind_speed_x_entry = tk.Entry(root)
wind_speed_y_entry = tk.Entry(root)

wind_speed_x_entry.grid(row=0, column=1)
wind_speed_y_entry.grid(row=1, column=1)

# Simülasyonu başlat butonu
start_button = tk.Button(root, text="Simülasyonu Başlat", command=start_simulation)
start_button.grid(row=2, column=1)

# Tkinter arayüz döngüsü
root.mainloop()
