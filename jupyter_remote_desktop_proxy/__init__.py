import os
import shlex
from shutil import which

HERE = os.path.dirname(os.path.abspath(__file__))


def setup_desktop():
    vncserver = which('vncserver')

    vnc_args = [vncserver]

    if not os.path.exists(os.path.expanduser('~/.vnc/xstartup')):
        vnc_args.extend(['-xstartup', os.path.join(HERE, 'share/xstartup')])

    vnc_command = shlex.join(
        vnc_args
        + [
            '-geometry',
            '1680x1050',
            '-SecurityTypes',
            'None',
            '-fg',
            ':1',
        ]
    )

    return {
        'command': [
            'websockify',
            '--web',
            os.path.join(HERE, 'share/web/noVNC-1.2.0'),
            '--heartbeat',
            '30',
            '5901',
        ]
        + ['--', '/bin/sh', '-c', f'cd {os.getcwd()} && {vnc_command}'],
        'port': 5901,
        'timeout': 30,
        'mappath': {'/': '/vnc_lite.html'},
        'new_browser_window': True,
    }
