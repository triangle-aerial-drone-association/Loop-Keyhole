# This code currently only do the following
# 1. Take off
# 2. Fly through 1st arch
# 3. Through 1st keyhole
# 4. Loop through 1st keyhole
# 5. Through 2nd keyhole(not very reliable at this, still need more experiment data)
# 6. move to a position preparing for loop 2nd keyhole(still experiementing)

from codrone_edu.drone import *
import time
import matplotlib.pyplot as plt

def fly_2_x(max_time:10, x_pos,y_pos,z_pos,velocity,direction):
    print("------------Flying toward coordinate",x_pos,y_pos,z_pos,direction)
    time_sec = max_time
    time_start = time.perf_counter()

    while (time.perf_counter() - time_start) < time_sec:
        pos_data = drone.get_position_data()
        save_flight_coordinance(pos_data)
        print(pos_data)
        if direction == "forward":
            if pos_data[1] >= x_pos:
                break
        else:
            if pos_data[1] <= x_pos:
                break

        drone.send_absolute_position(x_pos, y_pos, z_pos,velocity, 0, 0)
        time.sleep(0.01)

    dur = time.perf_counter() - time_start
    print("*********Time spent:", dur)
#
def fly_2_y(max_time:10, x_pos,y_pos,z_pos,velocity,direction):
    print("------------Flying toward coordinate", x_pos, y_pos, z_pos,direction)
    time_sec = max_time
    time_start = time.perf_counter()

    while (time.perf_counter() - time_start) < time_sec:
        pos_data = drone.get_position_data()
        save_flight_coordinance(pos_data)
        print(pos_data)
        if direction == "left":
            if pos_data[2] >= y_pos:
                break
        else:
            if pos_data[2] <= y_pos:
                break

        drone.send_absolute_position(x_pos, y_pos, z_pos,velocity, 0, 0)
        time.sleep(0.01)

    dur = time.perf_counter() - time_start
    print("*********Time spent:", dur)

def measure_dis(seconds):
    print("----------------Measuring the drone coordinate for",seconds)
    time_sec = seconds
    time_start = time.perf_counter()

    while (time.perf_counter() - time_start) < time_sec:
        pos_data = drone.get_position_data()
        save_flight_coordinance(pos_data)
        print(pos_data)

def save_flight_coordinance(pos_data):
    global t_list, x_list, y_list, z_list
    x_list.append(pos_data[1])
    y_list.append(pos_data[2])
    z_list.append(pos_data[3])
    t_list.append(pos_data[0])

d_move = 0

keyhole_center_z = 130

# list generated for the graphing of the data
t_list = []
x_list = []
z_list = []
y_list = []

roll_trim = 10
pitch_trim =0

prog_start_time = time.perf_counter()

drone = Drone()
drone.pair()
drone.set_initial_pressure()
drone.reset_sensor()
drone.set_trim(roll_trim, pitch_trim)


# take off
drone.takeoff()

# Note: with velocity 0.8, target x 1.8m, 2sec stop, the final x is around 2.45-2.5
# Note: 2.45 is near the center of the 2nd keyhole
# fly through arch #1 & keyhole #1
fly_2_x(10,1.83,0,1.3,0.8,"forward")
measure_dis(0.5)
# loop 1st keyhole by doing up+backward and then dive through
fly_2_x(10,1.83,0,1.8,0.8,"backward")
measure_dis(0.5)
fly_2_x(10,1.83,0,1.3,0.8,"forward")
measure_dis(0.5)

Total_Prog_Time = time.perf_counter() - prog_start_time
print("=====!!!!!!!===Total Runing Time",Total_Prog_Time)

drone.land()
drone.close()

plt.xlim(0, 60)
plt.ylim(0, 2)
plt.plot(t_list,z_list,'go')
plt.ylabel('Height (m)')
plt.xlabel('Time (seconds)')
plt.show()

plt.xlim(-3, 3)
plt.ylim(-2, 2)
plt.plot(x_list,y_list,'go')
plt.ylabel('Y (m)')
plt.xlabel('X (m)')
plt.show()