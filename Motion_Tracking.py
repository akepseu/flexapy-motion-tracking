import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# Serial connection
ser = serial.Serial('COM4', 115200)  # Replace COM4 with your correct port

# Data storage
window_size = 100
ax_vals = deque([0]*window_size, maxlen=window_size)
ay_vals = deque([0]*window_size, maxlen=window_size)
az_vals = deque([0]*window_size, maxlen=window_size)
gx_vals = deque([0]*window_size, maxlen=window_size)
gy_vals = deque([0]*window_size, maxlen=window_size)
gz_vals = deque([0]*window_size, maxlen=window_size)

# Plotting setup
fig, (accel_ax, gyro_ax) = plt.subplots(2, 1)
fig.suptitle("Real-Time Motion Chart")

accel_line_x, = accel_ax.plot([], [], label='Accel X')
accel_line_y, = accel_ax.plot([], [], label='Accel Y')
accel_line_z, = accel_ax.plot([], [], label='Accel Z')
accel_ax.set_ylim(-20, 20)
accel_ax.legend()
accel_ax.set_title("Acceleration")

gyro_line_x, = gyro_ax.plot([], [], label='Gyro X')
gyro_line_y, = gyro_ax.plot([], [], label='Gyro Y')
gyro_line_z, = gyro_ax.plot([], [], label='Gyro Z')
gyro_ax.set_ylim(-3, 3)
gyro_ax.legend()
gyro_ax.set_title("Gyroscope")

def update(frame):
    if ser.in_waiting:
        try:
            line = ser.readline().decode().strip()
            print("Raw data:", line)  # Debug: Print the raw data from serial
            parts = line.split(',')
            if len(parts) == 6:
                # Convert to float instead of int to avoid conversion issues
                ax, ay, az, gx, gy, gz = map(float, parts)
                
                # If you need integers, you can cast to int later
                ax_vals.append(int(ax))  # Optional: convert to int if necessary
                ay_vals.append(int(ay))
                az_vals.append(int(az))
                gx_vals.append(int(gx))
                gy_vals.append(int(gy))
                gz_vals.append(int(gz))

                accel_line_x.set_data(range(len(ax_vals)), ax_vals)
                accel_line_y.set_data(range(len(ay_vals)), ay_vals)
                accel_line_z.set_data(range(len(az_vals)), az_vals)

                gyro_line_x.set_data(range(len(gx_vals)), gx_vals)
                gyro_line_y.set_data(range(len(gy_vals)), gy_vals)
                gyro_line_z.set_data(range(len(gz_vals)), gz_vals)

                accel_ax.relim()
                accel_ax.autoscale_view()
                gyro_ax.relim()
                gyro_ax.autoscale_view()
        except Exception as e:
            print("Error:", e)

    return accel_line_x, accel_line_y, accel_line_z, gyro_line_x, gyro_line_y, gyro_line_z

# Set frames to a known value and disable frame caching
ani = animation.FuncAnimation(
    fig, update, interval=20, frames=200, cache_frame_data=False, blit=True
)

plt.tight_layout()
plt.show()
