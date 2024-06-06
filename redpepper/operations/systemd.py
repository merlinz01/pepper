import subprocess

from redpepper.operations import Operation, Result


class Running(Operation):

    _no_changes_text = "The service is already running."

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"systemd.Running({self.name})"

    def test(self, agent):
        cmd = ["systemctl", "is-active", self.name]
        p = subprocess.run(cmd)
        return p.returncode == 0

    def run(self, agent):
        result = Result(self)
        cmd = ["systemctl", "start", self.name]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if result.check_completed_process(p).succeeded:
            result.changed = True
        return result


class Enabled(Operation):

    _no_changes_text = "The service is already enabled."

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"systemd.Enabled({self.name})"

    def test(self, agent):
        cmd = ["systemctl", "is-enabled", self.name]
        p = subprocess.run(cmd)
        return p.returncode == 0

    def run(self, agent):
        result = Result(self)
        cmd = ["systemctl", "enable", self.name]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if result.check_completed_process(p).succeeded:
            result.changed = True
        return result