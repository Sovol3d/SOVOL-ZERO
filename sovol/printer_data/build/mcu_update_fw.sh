#!/bin/bash

echo "Start mcu_update_fw.sh now!!!"

   # Check if python3-serial is installed
if dpkg -l | grep -q "python3-serial"; then
   echo "python3-serial installed."
else
   sudo apt-get install python3-serial -y
fi

   # Check if klipper.bin exists
if [ -f /home/sovol/printer_data/build/mcu_klipper.bin ]; then

     # Check if  flash_can.py exist
   if [ -f /home/sovol/printer_data/build/flash_can.py ]; then
      echo "Found flash_can.py"
   else
      echo "No flash_can.py found in /home/sovol/printer_data/build.Exiting..."
      exit 1
   fi

   # get into mcu bootloader
   echo "Get into bootloader ..."
   python3 ~/printer_data/build/flash_can.py -f ~/printer_data/build/mcu_klipper.bin -u 0d1445047cdd &
   check_pid=$!
   sleep 5
   kill $check_pid

   #get bootloader id
   bootloder_id=$(ls /dev/serial/by-id/* | grep "usb-katapult_stm32h750xx")

   # Check if bootloader id is detected
   if [ -z "$bootloder_id" ]; then
      echo "Failed to detect bootloader id! Exiting..."
      exit 1
   fi

   # Flash MCU firmware
   python3 ~/printer_data/build/flash_can.py -f ~/printer_data/build/mcu_klipper.bin -d "$bootloder_id"

else
    echo "No mcu_klipper.bin found in /home/sovol/build. Exiting..."
fi