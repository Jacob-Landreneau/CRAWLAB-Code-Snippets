#!/bin/bash

for basename in 2019_RoboBoat_ZED_Fri_autonav1 2019_RoboBoat_ZED_Fri_autonav2 2019_RoboBoat_ZED_Fri_autonav3_0 2019_RoboBoat_ZED_Fri_autonav3_1 2019_RoboBoat_ZED_Fri_autonav3_2 2019_RoboBoat_ZED_Fri_autonav4 2019_RoboBoat_ZED_Fri_testing1 2019_RoboBoat_ZED_Fri_testing2 2019_RoboBoat_ZED_Fri_testing3 2019_RoboBoat_ZED_Fri_testing4 2019_RoboBoat_ZED_Thur_afternoon_autonav1 2019_RoboBoat_ZED_Thur_afternoon_autonav2 2019_RoboBoat_ZED_Thur_afternoon_autonav3 2019_RoboBoat_ZED_Thur_afternoon_dock1 2019_RoboBoat_ZED_Thur_afternoon_findpath1 2019_RoboBoat_ZED_Thur_afternoon_findpath2 2019_RoboBoat_ZED_Thur_afternoon_flag 2019_RoboBoat_ZED_Thur_afternoon_speed1 2019_RoboBoat_ZED_Thur_afternoon_speed2 2019_RoboBoat_ZED_Thur_morn_autonav1_0 2019_RoboBoat_ZED_Thur_morn_autonav2_0 2019_RoboBoat_ZED_Thur_morn_autonav3_0 2019_RoboBoat_ZED_Thur_morn_autonav4_0 2019_RoboBoat_ZED_Thur_morn_autonav5_0 2019_RoboBoat_ZED_Thur_morn_dock1_0 2019_RoboBoat_ZED_Thur_morn_dock2_0 2019_RoboBoat_ZED_Thur_morn_findpath1_0 2019_RoboBoat_ZED_Thur_morn_findpath2_0 2019_RoboBoat_ZED_Thur_morn_raiseflag1_0 2019_RoboBoat_ZED_Thur_morn_speed1_0 2019_RoboBoat_ZED_Thur_morn_speed2_0 2019_RoboBoat_ZED_Wed_autonav_0 2019_RoboBoat_ZED_Wed_dock_0 2019_RoboBoat_ZED_Wed_findpath_0 2019_RoboBoat_ZED_Wed_findpath2_0 2019_RoboBoat_ZED_Wed_perim_0 2019_RoboBoat_ZED_Wed_slolam_0 2019_RoboBoat_ZED_Wed_slolam1_0 2019_RoboBoat_ZED_Wed_speed_0 2019_RoboBoat_ZED_Wed_speedholo_0 2019_RoboBoat_ZED_Thur_afternoon_dock2 
do
    echo ""
    echo "Making movie with from $filename"
    echo ""
        
    ffmpeg -framerate 7 -i ${basename}_%05d.jpg ${basename}.mp4
done