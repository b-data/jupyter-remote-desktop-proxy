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
            '1920x1080',
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
            os.path.join(HERE, 'share/web/noVNC'),
            '--heartbeat',
            '30',
            'localhost:5901',
        ]
        + ['--', '/bin/sh', '-c', f'cd {os.getcwd()} && {vnc_command}'],
        'port': 5901,
        'timeout': 30,
        'mappath': {'/': '/vnc.html'},
        "launcher_entry": {
            "title": "QGIS Desktop",
            "icon_path": "/usr/local/share/icons/hicolor/scalable/apps/qgis.svg"
        },
        'new_browser_window': True,
    }
