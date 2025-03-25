
echo "Start extruder_mcu_update_fw.sh now!!!"

if [ -f /home/sovol/printer_data/build/extruder_mcu_klipper.bin ]; then
    

    if [ -f /home/sovol/printer_data/build/flash_can.py ]; then
        echo "Found flash_can.py"
    else
        echo "No flash_can.py found in /home/sovol/printer_data/build. Exiting..."
        exit 1
    fi

    echo "Get into bootloader ..."
    python3 ~/printer_data/build/flash_can.py -i can0 -f ~/printer_data/build/extra_mcu_klipper.bin -u 58a72bb93aa4 &
    check_pid=$!
    sleep 5
    kill $check_pid

    bootloader_id="58a72bb93aa4"
    echo "Using default UUID $bootloader_id for firmware update."

    echo "Flashing MCU firmware with UUID: $bootloader_id"
    python3 ~/printer_data/build/flash_can.py -i can0 -f ~/printer_data/build/extra_mcu_klipper.bin -u "$bootloader_id"

    if [ $? -eq 0 ]; then
        echo "Firmware update completed successfully!"
    else
        echo "Error: Firmware update failed."
        exit 1
    fi

else
    echo "No extruder_mcu_klipper.bin found in /home/sovol/printer_data/build. Exiting..."
    exit 1
fi
