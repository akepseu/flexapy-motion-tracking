import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import math

# Serial setup
ser = serial.Serial('COM4', 115200, timeout=1)

# Plot setup
fig, ax = plt.subplots()
ax.set_xlim(-2000, 2000)
ax.set_ylim(-2000, 2000)
ax.set_aspect('equal')
ax.grid(True)
ax.set_title("Motion Trail (Scaled from Real Units)")
ax.set_xlabel("X")
ax.set_ylabel("Y")

# Variables
trail_length = 100
trail = deque(maxlen=trail_length)
position = [0.0, 0.0]
velocity = [0.0, 0.0]
orientation = 0.0
dt = 0.03  # 30ms

# Plot elements
trail_line, = ax.plot([], [], lw=2, color='blue')
point, = ax.plot([], [], 'ro')
heading_line, = ax.plot([], [], color='green', lw=2)

def update(frame):
    global position, velocity, orientation

    if ser.in_waiting:
        try:
            line = ser.readline().decode('utf-8').strip()
            parts = line.split(',')

            if len(parts) != 6:
                print("Skipping line:", line)
                return trail_line, point, heading_line

            ax_raw = float(parts[0])    # in m/s²
            ay_raw = float(parts[1])    # in m/s²
            gz_raw = float(parts[5])    # in degrees/s

            # Convert gz to radians per second
            gz_rad = math.radians(gz_raw)

            # Update orientation
            orientation += gz_rad * dt

            # Rotate acceleration into world frame
            ax_world = ax_raw * math.cos(orientation) - ay_raw * math.sin(orientation)
            ay_world = ax_raw * math.sin(orientation) + ay_raw * math.cos(orientation)

            # Integrate acceleration to get velocity
            velocity[0] += ax_world * dt
            velocity[1] += ay_world * dt

            # Dampening
            velocity[0] *= 0.98
            velocity[1] *= 0.98

            # Integrate velocity to get position
            position[0] += velocity[0] * dt * 50  # Multiplied for visualization
            position[1] += velocity[1] * dt * 50

            # Store trail
            trail.append((position[0], position[1]))

            if trail:
                x_vals, y_vals = zip(*trail)
                trail_line.set_data(x_vals, y_vals)
                point.set_data(position[0], position[1])

                # Heading indicator
                length = 10
                hx = position[0] + length * math.cos(orientation)
                hy = position[1] + length * math.sin(orientation)
                heading_line.set_data([position[0], hx], [position[1], hy])

        except Exception as e:
            print("Error:", e)

    return trail_line, point, heading_line

ani = animation.FuncAnimation(fig, update, interval=30, blit=True)
plt.tight_layout()
plt.show()
