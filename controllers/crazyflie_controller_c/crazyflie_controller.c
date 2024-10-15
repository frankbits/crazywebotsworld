/*
 * Copyright 2022 Bitcraze AB
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
 *  ...........       ____  _ __
 *  |  ,-^-,  |      / __ )(_) /_______________ _____  ___
 *  | (  O  ) |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
 *  | / ,..´  |    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
 *     +.......   /_____/_/\__/\___/_/   \__,_/ /___/\___/
 *
 *
 * @file crazyflie_controller.c
 * Description: Controls the crazyflie in webots
 * Author:      Kimberly McGuire (Bitcraze AB)
 */

#include <math.h>
#include <stdio.h>

#include <webots/camera.h>
#include <webots/distance_sensor.h>
#include <webots/gps.h>
#include <webots/gyro.h>
#include <webots/inertial_unit.h>
#include <webots/keyboard.h>
#include <webots/motor.h>
#include <webots/robot.h>
#include <webots/supervisor.h>
#include <webots/compass.h>


int main(int argc, char **argv) {
  wb_robot_init();

  const int timestep = (int)wb_robot_get_basic_time_step();

  // Initialize motors
  WbDeviceTag m1_motor = wb_robot_get_device("m1_motor");
  wb_motor_set_position(m1_motor, INFINITY);
  WbDeviceTag m2_motor = wb_robot_get_device("m2_motor");
  wb_motor_set_position(m2_motor, INFINITY);
  WbDeviceTag m3_motor = wb_robot_get_device("m3_motor");
  wb_motor_set_position(m3_motor, INFINITY);
  WbDeviceTag m4_motor = wb_robot_get_device("m4_motor");
  wb_motor_set_position(m4_motor, INFINITY);

  // Initialize sensors
  WbDeviceTag gps = wb_robot_get_device("gps");
  wb_gps_enable(gps, timestep);
  WbDeviceTag range = wb_robot_get_device("range");
  wb_distance_sensor_enable(range, timestep);
  
  WbNodeRef this_node = wb_supervisor_node_get_self();
  WbFieldRef target_field = wb_supervisor_node_get_field(this_node,"target");
  WbFieldRef zrange_field = wb_supervisor_node_get_field(this_node, "zrange");
  WbFieldRef rotation_field = wb_supervisor_node_get_field(this_node, "rotation");

  while (wb_robot_step(timestep) != -1) {
    // Get measurements
    double x_global = wb_gps_get_values(gps)[0];
    double y_global = wb_gps_get_values(gps)[1];
    double z_global = wb_gps_get_values(gps)[2];
   
    // Get target 
    const double * target = wb_supervisor_field_get_sf_vec3f(target_field); 
    double target_x = target[0];
    double target_y = target[1];
    double target_z = target[2];
    
    // Most basic P-Controller for velocity (p=1)
    double forward_desired = target_x - x_global;
    double sideways_desired = target_y - y_global;
    double up_desired = target_z - z_global;
    
    // Avoid going lower than the floor
    if (z_global < 0.04 && up_desired < 0) up_desired = 0;   
    
    const double vel[6] = {forward_desired, sideways_desired, up_desired, 0, 0,0};
    wb_supervisor_node_set_velocity(this_node, vel);
    const double rot[4] = {0.0, 0.0, 1.0, 0.0};
    wb_supervisor_field_set_sf_rotation(rotation_field, rot);
    
    // Setting motorspeed for nicer visuals
    int motor_speed = 48;
    if (z_global < 0.1) motor_speed = 0;
    wb_motor_set_velocity(m1_motor, -motor_speed);
    wb_motor_set_velocity(m2_motor, motor_speed);
    wb_motor_set_velocity(m3_motor, -motor_speed);
    wb_motor_set_velocity(m4_motor, motor_speed);
      
    // Publish zranger values
    double z_range_value = wb_distance_sensor_get_value(range);
    wb_supervisor_field_set_sf_float(zrange_field, z_range_value);
  };

  wb_robot_cleanup();

  return 0;
}