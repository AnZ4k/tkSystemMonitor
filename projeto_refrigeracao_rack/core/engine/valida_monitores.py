import psutil
import wmi
import platform
import subprocess
import json

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    memory_info = psutil.virtual_memory()

    pc_clock = {}
    if cpu_freq:
        pc_clock = {f"c{i}": freq.current for i, freq in enumerate(psutil.cpu_freq(percpu=True)) if freq is not None}

    pc_temp = get_cpu_temperature()
    pc_usage = {f"c{i}": psutil.cpu_percent(interval=1, percpu=True)[i] for i in range(psutil.cpu_count())}

    system_info = {
        "cpu": {
            "clock": round(cpu_freq.current, 2) if cpu_freq else 0,
            "temp": pc_temp.get("c0", 0),  # Altera para pegar a temperatura ou 0 se não disponível
            "usage": cpu_usage,
            "pc_clock": pc_clock,
            "pc_temp": pc_temp,
            "pc_usage": pc_usage
        },
        "memory": {
            "total_size": round(memory_info.total / (1024 * 1024), 2),  # Total em MB com 2 casas decimais
            "used": round(memory_info.used / (1024 * 1024), 2),          # Usado em MB com 2 casas decimais
            "free": round(memory_info.available / (1024 * 1024), 2),      # Livre em MB com 2 casas decimais
            "frequency": round(cpu_freq.max, 2) if cpu_freq else 0
        }
    }

    return system_info

def get_cpu_temperature():
    if platform.system() == "Windows":
        try:
            w = wmi.WMI(namespace="root\\wmi")
            temperature_info = w.MSAcpi_ThermalZone()
            temperatures = {f"c{i}": round(temp.CurrentTemperature / 10.0 - 273.15, 2) for i, temp in enumerate(temperature_info)}
            return temperatures
        except wmi.x_wmi:
            return {"c0": 0}
        except Exception:
            return {"c0": 0}
    else:
        try:
            output = subprocess.check_output("sensors", universal_newlines=True)
            temp_dict = {}
            for line in output.splitlines():
                if "°C" in line:
                    parts = line.split()
                    label = parts[0]
                    temp = round(float(parts[-2]), 2)
                    temp_dict[label] = temp
            return temp_dict
        except Exception:
            return {"c0": 0}

if __name__ == "__main__":
    system_info = get_system_info()
    print(json.dumps(system_info, indent=4))
