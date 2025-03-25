#!/bin/bash

echo "Start extruder_mcu_update_fw.sh now!!!"

FIRMWARE_PATH="/home/sovol/printer_data/build/extruder_mcu_klipper.bin"
if [ ! -f "$FIRMWARE_PATH" ]; then
    echo "Error: Firmware file not found at $FIRMWARE_PATH. Exiting..."
    exit 1
fi

FLASH_TOOL_PATH="/home/sovol/printer_data/build/flash_can.py"
if [ ! -f "$FLASH_TOOL_PATH" ]; then
    echo "Error: Flash tool not found at $FLASH_TOOL_PATH. Exiting..."
    exit 1
fi

echo "Attempting to enter bootloader..."
python3 "$FLASH_TOOL_PATH" -i can0 -f "$FIRMWARE_PATH" -u 61755fe321ac &
CHECK_PID=$!
sleep 5
kill $CHECK_PID 2>/dev/null

echo "Querying bootloader UUID..."
UUIDS=$(python3 "$FLASH_TOOL_PATH" -i can0 -q | grep -oP 'Detected UUID: \K[a-f0-9]+')

if [ -z "$UUIDS" ]; then
    echo "Error: No devices detected on CAN bus. Exiting..."
    exit 1
fi

DEFAULT_UUID="61755fe321ac"
UNSUPPORTED_UUID="58a72bb93aa4"

BOOTLOADER_ID=$(echo "$UUIDS" | head -n 1)

if [ "$BOOTLOADER_ID" == "$UNSUPPORTED_UUID" ]; then
    echo "Error: Firmware mismatch detected. UUID $UNSUPPORTED_UUID is not supported. Exiting..."
    exit 1
fi

if [ "$BOOTLOADER_ID" == "$DEFAULT_UUID" ]; then
    echo "Default UUID $DEFAULT_UUID found. Using it for firmware update."
else
    echo "Detected UUID: $BOOTLOADER_ID. Proceeding with firmware update."
fi

echo "Flashing MCU firmware with UUID: $BOOTLOADER_ID"
python3 "$FLASH_TOOL_PATH" -i can0 -f "$FIRMWARE_PATH" -u "$BOOTLOADER_ID"

if [ $? -eq 0 ]; then
    echo "Firmware update completed successfully!"
else
    echo "Error: Firmware update failed."
    exit 1
fi
