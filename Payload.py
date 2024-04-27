import os
import platform
import socket
import nmap

def get_linux_distribution():
    try:
        # Ouvrir le fichier /etc/os-release et lire les informations
        with open('/etc/os-release', 'r') as f:
            lines = f.readlines()
            distribution_info = {}
            for line in lines:
                parts = line.strip().split('=')
                if len(parts) == 2:
                    distribution_info[parts[0]] = parts[1].strip('"')
            return distribution_info.get('PRETTY_NAME', 'Unknown')
    except Exception as e:
        print("Erreur lors de la récupération de la distribution Linux:", e)
        return 'Unknown'


def get_service_name(port):
    try:
        # Utilisez la fonction socket.getservbyport pour obtenir le nom du service
        service_name = socket.getservbyport(port)
        return service_name
    except Exception as e:
        print("Erreur lors de la récupération du nom du service:", e)
        return None

def get_open_ports(ip):
    try:
        nm = nmap.PortScanner()
        nm.scan(ip, arguments='-p-')
        open_ports = nm[ip]['tcp'].keys()
        return open_ports
    except Exception as e:
        print("Erreur lors de la récupération des ports ouverts:", e)
        return []

def get_host_info():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        hostname = socket.gethostname()
        os_version = platform.platform()
        os_type = platform.system()
        if os_type == 'Linux':
            distribution = get_linux_distribution()
            if distribution:
                os_type += " " + " ".join(distribution)
        return ip, hostname, os_version, os_type
    except Exception as e:
        print("Erreur lors de la récupération des informations d'hôte:", e)
        return None, None, None, None

if __name__ == "__main__":
    ip, hostname, os_version, os_type = get_host_info()
    if ip and hostname and os_version and os_type:
        print("Adresse IP de l'hôte:", ip)
        print("Hostname de l'hôte:", hostname)
        print("Version du système d'exploitation:", os_version)
        print("Type de système d'exploitation:", os_type)

        open_ports = get_open_ports(ip)
        if open_ports:
            print("\nPorts ouverts:")
            for port in open_ports:
                service_name = get_service_name(int(port))
                print("Port:", port, "(Service:", service_name, ")")
