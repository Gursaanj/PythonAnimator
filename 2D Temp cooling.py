import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

# constants with manually tested divergence interval
L = 0.01
D = 4.25e-6
N = 100
dx = L/N
dtcon = 1e-4
dtdiv = 6e-4
d_list = [dtcon, dtdiv]
Tlo, Tmid, Thi = 200, 250, 400


# choosen times to make plots, with given temperature and change
t1, t2, t3, t4, t5 = 0.01, 0.1, 0.4, 1.0, 10.
epsilon = [d_list[0]/1000, d_list[1]/1000]
time_end = [t5 + epsilon[0], t5 + epsilon[1]]

# Creating the 2 arrays needed to be examined
Temp_p = np.empty((N+1, N+1), float)
Temp_p[0, :] = Thi
Temp_p[N, :] = Thi
Temp_p[:, 0] = Tlo
Temp_p[:, N] = Tlo

Temp = np.full((N+1, N+1), Tmid)
Temp[0, :] = Thi
Temp[N, :] = Thi
Temp[:, 0] = Tlo
Temp[:, N] = Tlo

# For the Function Itself
# Empty arrays for the worked convergence and divergence temperatures
it_con = 0
it_div = 0
c_list = [d_list[0]*D/(dx**2), d_list[1]*D/(dx**2)]
con_im = []
div_im = []
counter_con = 0
counter_div = 0

# Define the update functions for the figures and animations


def update_con(num, frm):
    ani_con.set_data(frm[num])


def update_div(num, frm):
    ani_div.set_data(frm[num])


# Calculate temperatures at different times t
# Take 1/10th of every datapoint for animation
while it_con < time_end[0]:
    x = np.roll(Temp, 1, axis=0)[1:N, 1:N]+np.roll(Temp, -1, axis=0)[1:N, 1:N]
    y = np.roll(Temp, 1, axis=1)[1:N, 1:N]+np.roll(Temp, -1, axis=1)[1:N, 1:N]
    dt_x = x - 2*Temp[1:N, 1:N]
    dt_y = y - 2*Temp[1:N, 1:N]
    Temp_p[1:N, 1:N] = Temp[1:N, 1:N] + c_list[0]*(dt_x + dt_y)
    Temp, Temp_p = Temp_p, Temp
    it_con = it_con + d_list[0]
    counter_con = counter_con + 1
    if counter_con % 10 == 0:
        con_im.append(np.copy(Temp))
    #print(counter_con)

# Reseting the arrays for Divergence Animation

Temp_place = np.empty((N+1, N+1), float)
Temp_place[0, :] = Thi
Temp_place[N, :] = Thi
Temp_place[:, 0] = Tlo
Temp_place[:, N] = Tlo

Temp_new = np.full((N+1, N+1), Tmid)
Temp_new[0, :] = Thi
Temp_new[N, :] = Thi
Temp_new[:, 0] = Tlo
Temp_new[:, N] = Tlo

while it_div < time_end[1]:
    x = np.roll(Temp_new, 1, axis=0)[1:N, 1:N]+np.roll(Temp_new, -1, axis=0)[1:N, 1:N]
    y = np.roll(Temp_new, 1, axis=1)[1:N, 1:N]+np.roll(Temp_new, -1, axis=1)[1:N, 1:N]
    dt_x = x - 2*Temp_new[1:N, 1:N]
    dt_y = y - 2*Temp_new[1:N, 1:N]
    Temp_place[1:N, 1:N] = Temp_new[1:N, 1:N] + c_list[1]*(dt_x + dt_y)
    Temp_new, Temp_place = Temp_place, Temp_new
    it_div = it_div + d_list[1]
    counter_div = counter_div + 1
    if counter_div % 10 == 0:
        div_im.append(np.copy(Temp_new))
    #print(counter_div)

# Plot animations and save
con_fig = plt.figure(1)
div_fig = plt.figure(2)
ani_con = plt.imshow(con_im[0])
ani_div = plt.imshow(div_im[0])
con_anim = anim.FuncAnimation(con_fig, update_con, frames=1000, repeat=False,
                              fargs=(con_im, ), interval=50)
con_anim.save('heat2d_converged.mp4', fps=20)
div_anim = anim.FuncAnimation(div_fig, update_div, frames=1000, repeat=False,
                              fargs=(div_im, ), interval=10)
div_anim.save('heat2d_diverged.mp4', fps=20)
