import subprocess
import psutil
import platform

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def get_model():
    return run_command(['sysctl', 'hw.model']).split(': ')[1]

def get_cpu():
    return run_command(['sysctl', '-n', 'machdep.cpu.brand_string'])

def get_ram():
    ram_bytes = psutil.virtual_memory().total
    ram_gb = ram_bytes / (1024 ** 3)
    return f"{ram_gb:.2f} GB"

def get_serial_number():
    result = run_command(['system_profiler', 'SPHardwareDataType'])
    for line in result.split('\n'):
        if 'Serial Number' in line:
            return line.split(': ')[1].strip()
    return "Not Available :("

def get_storage():
    result = run_command(['diskutil', 'info', '/'])
    for line in result.split('\n'):
        if 'Volume Total Space' in line:
            return line.split(': ')[1].strip()
    return "Not Available :("

def get_os_version():
    return platform.mac_ver()[0]

def get_machine_info():
    return platform.machine()

def get_python_version():
    return platform.python_version()

def get_system_profiler_data(data_type):
    result = run_command(['system_profiler', data_type])
    data = {}
    for line in result.split('\n'):
        if ': ' in line:
            key, value = line.split(': ', 1)
            data[key.strip()] = value.strip()
    return data

def main():
    model = get_model()
    cpu = get_cpu()
    ram = get_ram()
    serial_number = get_serial_number()
    storage = get_storage()
    os_version = get_os_version()
    machine_info = get_machine_info()
    python_version = get_python_version()

    hardware_data = get_system_profiler_data('SPHardwareDataType')
    memory_data = get_system_profiler_data('SPMemoryDataType')
    network_data = get_system_profiler_data('SPNetworkDataType')
    software_data = get_system_profiler_data('SPSoftwareDataType')

    print("Mac Detailed Information")
    print("------------------------")
    print(f"Model: {model}")
    print(f"CPU: {cpu}")
    print(f"RAM: {ram}")
    print(f"Serial Number: {serial_number}")
    print(f"Storage: {storage}")
    print(f"OS Version: {os_version}")
    print(f"Machine Info: {machine_info}")
    print(f"Python Version: {python_version}")
    print("\nHardware Data:")
    for key, value in hardware_data.items():
        print(f"{key}: {value}")
    print("\nMemory Data:")
    for key, value in memory_data.items():
        print(f"{key}: {value}")
    print("\nNetwork Data:")
    for key, value in network_data.items():
        print(f"{key}: {value}")
    print("\nSoftware Data:")
    for key, value in software_data.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
