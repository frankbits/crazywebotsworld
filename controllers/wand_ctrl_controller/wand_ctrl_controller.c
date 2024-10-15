/*
 * File:          wand_ctrl_controller.c
 * Date:
 * Description:
 * Author:
 * Modifications:
 */

/*
 * You may need to add include files like <webots/distance_sensor.h> or
 * <webots/motor.h>, etc.
 */
#include <math.h>
#include <stdio.h>


#include <webots/robot.h>
#include <webots/supervisor.h>
#include <webots/keyboard.h>


/*
 * You may want to add macros here.
 */
#define TIME_STEP 64

/*
 * This is the main program.
 * The arguments of the main function can be specified by the
 * "controllerArgs" field of the Robot node
 */
int main(int argc, char **argv) {
  /* necessary to initialize webots stuff */
  wb_robot_init();
  WbNodeRef self_node = wb_supervisor_node_get_self();
  WbFieldRef translation_field = wb_supervisor_node_get_field(self_node, "translation");
  WbFieldRef rotation_field = wb_supervisor_node_get_field(self_node, "rotation");
  WbFieldRef id_field = wb_supervisor_node_get_field(self_node, "wand_id");
  /*
   * You should declare here WbDeviceTag variables for storing
   * robot devices like this:
   *  WbDeviceTag my_sensor = wb_robot_get_device("my_sensor");
   *  WbDeviceTag my_actuator = wb_robot_get_device("my_actuator");
   */
  wb_keyboard_enable(TIME_STEP);

 
  double rotation[4] = {0,0,1,0};
  
  double yaw_desired = 0.0;
  int flip_desired = 1;


  int id = wb_supervisor_field_get_sf_int32(id_field);
  
  
  bool selected = false;
  
    printf("\n");

    printf("====== Controls =======\n");
  
    printf(" The Wand can be controlled from your keyboard!\n");
    printf(" All controllable movement is in world coordinates\n");
    printf("- Use the up, back, right and left button to move in the horizontal plane\n");
    printf("- Use Q and E to rotate around yaw\n");
    printf("- Use W and S to go up and down\n");
    printf("- Use A and D to switch between toggle states\n");
    printf("- Use number keys to switch between wand\n");
    
  
  while (wb_robot_step(TIME_STEP) != -1) {
      
      double forward_speed = 0.0;
      double sideward_speed = 0.0;
      double upward_speed = 0.0;
      
      
      
      
      int key = wb_keyboard_get_key();
      while (key > 0) {
        switch (key) {
          case WB_KEYBOARD_UP:
            if (selected) forward_speed = 0.5;
            break;
          case WB_KEYBOARD_DOWN:
            if (selected) forward_speed = -0.5;
            break;
          case WB_KEYBOARD_RIGHT:
            if (selected) sideward_speed = -0.5;
            break;
          case WB_KEYBOARD_LEFT:
            if (selected) sideward_speed = +0.5;
            break;
          case 'A':
            //rotation[2] = 1;
            if (selected) flip_desired = 1;
            break;
          case 'D':
            if (selected) flip_desired = 0;
            break;
          case 'W':
            if (selected) upward_speed = 0.5;
            break;
          case 'S':
            if (selected) upward_speed = -0.5;
            break;
          case 'Q':
            if (selected) yaw_desired += 0.2;
            //rotation[3] += 0.2;
            break;
          case 'E':
            if (selected) yaw_desired -= 0.2;
            //rotation[3] -= 0.2;
            break;
          default:
            {
            int nbr_int = key - '0';
            if (nbr_int >= 0 && nbr_int <= 9) {
              if (nbr_int == id) selected = true;
              else selected = false;
             }
            }
        }
        key = wb_keyboard_get_key();
      }
      rotation[0] = cos(yaw_desired/2) + cos(flip_desired/2); // to be 0 if flip = 0 to be some thing if flip = 3.14
      rotation[2] = sin(yaw_desired/2) + sin(flip_desired/2); // to be 1 if flip = 0 to be something if flip = 3.14
      
      if (!flip_desired) {
          rotation[0] = 0;
          rotation[1] = 0;
          rotation[2] = 1;
          rotation[3] = yaw_desired;
      } else {
          rotation[0] = cos(yaw_desired/2);
          rotation[1] = sin(yaw_desired/2);
          rotation[2] = 0;
          rotation[3] = 3.14;
      }
      
      const double vel[6] = {forward_speed, sideward_speed, upward_speed, 0, 0,0};
      wb_supervisor_node_set_velocity(self_node, vel);
      wb_supervisor_field_set_sf_rotation(rotation_field, (const double *)rotation);
   
   
  };

  /* Enter your cleanup code here */

  /* This is necessary to cleanup webots resources */
  wb_robot_cleanup();

  return 0;
}
