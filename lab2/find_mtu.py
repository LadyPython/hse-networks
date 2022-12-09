import subprocess
import click


class FindMinMTU:
    def __init__(self, host: str):
        self.host = host

        self._low_mtu = 0
        self._high_mtu = 100000

    def check_mtu_packet_size(self, packet_size, timeout=50) -> bool:
        command = f'ping -M do -c 1 -s {packet_size} -w {timeout} {self.host}'
        print('.', end='')
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             shell=True)
        for line in iter(p.stdout.readline, b''):
            line = line.decode(encoding='utf-8')
            if 'Message too long' in line or '100.0% packet loss' in line or 'packet size too large' in line:
                return False
        code = p.wait()
        return code == 0

    def find_min_mtu(self):
        print('progress:', end='')
        while self._high_mtu - self._low_mtu > 1:
            middle_mtu = (self._high_mtu + self._low_mtu) // 2
            if self.check_mtu_packet_size(middle_mtu):
                self._low_mtu = middle_mtu
            else:
                self._high_mtu = middle_mtu
        return self._low_mtu


@click.command()
@click.option("--host", required=True, type=str)
def main(host):
    f = FindMinMTU(host)
    print(f"finished\nmin MTU: {f.find_min_mtu()} bytes (excluding headers)")


main()
