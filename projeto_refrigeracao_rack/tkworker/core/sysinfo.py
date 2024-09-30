import psutil
import platform
import json

def get_system_info() -> dict:
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    memory_info = psutil.virtual_memory()
    pc_clock = {}
    pc_temp = get_cpu_temperature()
    pc_usage = {f"c{i}": psutil.cpu_percent(interval=1, percpu=True)[i] for i in range(psutil.cpu_count())}
    
    if cpu_freq:
        pc_clock = {f"c{i}": int(freq.current) for i, freq in enumerate(psutil.cpu_freq(percpu=True)) if freq is not None}

    system_info = {
        "cpu": {
            "clock": int(cpu_freq.current) if cpu_freq else 0,
            "temp": max(pc_temp.values) if pc_temp else 0,
            "usage": cpu_usage,
            "pc_clock": pc_clock,
            "pc_temp": pc_temp,
            "pc_usage": pc_usage
        },
        "memory": {
            "total_size": int((memory_info.total / 1024) / 1024),
            "used": int((memory_info.used / 1024) / 1024),
            "free": int((memory_info.available / 1024) / 1024),
            "frequency": cpu_freq.max if cpu_freq else 0
        }
    }

    return system_info

def get_cpu_temperature():
    if platform.system() == "Windows":    
        import wmi
        
        try:
            w = wmi.WMI(namespace="root\\wmi")
            temperature_info = w.MSAcpi_ThermalZone()
            temperatures = {f"c{i}": temp.CurrentTemperature / 10.0 - 273.15 for i, temp in enumerate(temperature_info)}
            
            return temperatures
        
        except wmi.x_wmi:
            print("Classe MSAcpi_ThermalZone não encontrada.")
       
            return {}
       
        except Exception as e:
            print(f"Erro ao obter temperatura: {e}")
       
            return {}
    else:
        try:
            cores = {}
            sensors = psutil.sensors_temperatures()
            
            for i in range(1, len(sensors["coretemp"])):
                cores[f'c[{i -1}]'] = int(sensors["coretemp"][i][1])
            
            return cores
        except Exception as e:
            print(f"Erro ao ler sensores: {e}")
            return {}


if __name__ == "__main__":
    system_info = get_system_info()
    print(json.dumps(system_info, indent=4))
