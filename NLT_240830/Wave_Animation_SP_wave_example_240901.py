# 코드 수정할 것 (ollama 작성, 240901)


import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.animation as animation

# Constants
omega_p = 1  # frequency of p-wave (radians per unit time)
omega_s = 0.5  # frequency of s-wave (radians per unit time)
amplitude_p = 2  # amplitude of p-wave
amplitude_s = 1  # amplitude of s-wave
speed_p = 4  # speed of p-wave
speed_s = 3  # speed of s-wave

# Create a figure and axis object
fig, ax = plt.subplots()

# Initialize arrays to store wave values
t = np.arange(0, 10, 0.01)  # time array (s)

def animate(i):
    global t
    
    # Plot p-wave at current frame
    x_p = i * speed_p / 100  # position of p-wave at current frame
    y_p = amplitude_p * np.sin(omega_p * t - omega_p * x_p)  # wave function for p-wave
    ax.clear()
    ax.plot(t, y_p)

    # Plot s-wave at current frame
    x_s = i * speed_s / 100  # position of s-wave at current frame
    y_s = amplitude_s * np.sin(omega_s * t - omega_s * x_s)  # wave function for s-wave
    ax2 = ax.twinx()
    ax2.plot(t, y_s, color='red')

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=200, interval=50)

plt.show()

