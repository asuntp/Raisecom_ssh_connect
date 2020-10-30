import paramiko
import time
import socket
from pprint import pprint


def raisecom_command(
    ip,
    username,
    password,
    enable,
    commands,
    max_bytes=50000,
):
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cl.connect(
        hostname=ip,
        username=username,
        password=password,
        look_for_keys=False,
        allow_agent=False,
    )
    with cl.invoke_shell() as ssh:
        ssh.send("enable\n")
        ssh.send(f"{enable}\n")
        time.sleep(1)
        ssh.send("terminal length 0\n")
        time.sleep(1)
        ssh.recv(max_bytes)

        result = {}
        for command in commands:
            ssh.send(f"{command}\n")
            ssh.settimeout(2)
            output = ""

            while True:
                try:
                    part = ssh.recv(max_bytes).decode("utf-8")
                    output += part
                    time.sleep(0.5)
                except socket.timeout:
                    break
            result[command] = output

        return result


if __name__ == "__main__":

    port = 3
    ip_swich = "172.17.16.17"

    commands = [
                f"show interface port {port}",
                f"sh mac-address-table l2-address port {port}",
                "sh ip dhcp snooping binding",
                "sh ip arp-inspection binding",
                f"test cable-diagnostics port-list {port}",
                f"show cable-diagnostics port-list {port}",
                ]
    result = raisecom_command(ip_swich, "admin", "Iyzufdjkit,yfz7", "raisecom", commands)
    pprint(result, width=200)