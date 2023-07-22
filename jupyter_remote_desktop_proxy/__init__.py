import os
import shlex
import tempfile
from shutil import which

HERE = os.path.dirname(os.path.abspath(__file__))


def setup_desktop():
    # make a secure temporary directory for sockets
    # This is only readable, writeable & searchable by our uid
    sockets_dir = tempfile.mkdtemp()
    sockets_path = os.path.join(sockets_dir, 'vnc-socket')
    vncserver = which('vncserver')

    vnc_command = ' '.join(
        shlex.quote(p)
        for p in (
            [
                vncserver,
                '-xstartup',
                os.path.join(HERE, 'share/xstartup'),
                '-geometry',
                '1680x1050',
                '-SecurityTypes',
                'None',
                '-fg',
            ]
        )
    )
    return {
        'command': [
            'websockify',
            '--web',
            os.path.join(HERE, 'share/web/noVNC-1.2.0'),
            '--heartbeat',
            '30',
            '{port}',
        ]
        + ['--', '/bin/sh', '-c', f'cd {os.getcwd()} && {vnc_command}'],
        'timeout': 30,
        'mappath': {'/': '/vnc_lite.html'},
        'new_browser_window': True,
    }
