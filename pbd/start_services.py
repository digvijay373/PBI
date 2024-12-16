import subprocess
import sys
import time

def run_django():
    return subprocess.Popen([
        sys.executable,
        "manage.py",
        "runserver"
    ])

def run_streamlit(port):
    return subprocess.Popen([
        sys.executable,
        "-m", "streamlit",
        "run",
        "app.py",
        "--server.port",
        str(port)
    ])

def run_nginx():
    return subprocess.Popen([
        "nginx",
        "-c",
        "C:/nginx/conf/nginx.conf"
    ])

if __name__ == "__main__":
    ports = [8501, 8502, 8503, 8504, 8505, 8506]
    processes = []

    # Start Django
    django_process = run_django()
    processes.append(django_process)
    time.sleep(2)

    # Start Streamlit instances
    for port in ports:
        process = run_streamlit(port)
        processes.append(process)
        print(f"Started Streamlit instance on port {port}")
        time.sleep(2)

    # Start NGINX
    nginx_process = run_nginx()
    processes.append(nginx_process)
    print("Started NGINX")

    try:
        print("All services running. Press Ctrl+C to stop...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping all services...")
        for process in processes:
            process.terminate()