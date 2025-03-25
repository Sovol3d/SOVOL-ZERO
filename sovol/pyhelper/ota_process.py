import requests
import socket
import json
import sys

# Moonraker 的 API 地址
moonraker_api = "http://localhost:7125"

def update_progress(progress):
    # Example function to display or log the progress
    print(f"Download progress: {progress}")
    # 构造请求的数据
    data = {
    	"command": "printer.gcode.script",
    	"script": f"M117 {progress}"
    }
    # 发送请求
    response = requests.post(f"{moonraker_api}/printer/gcode/script", json=data)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        progress = sys.argv[1]
        update_progress(progress)
