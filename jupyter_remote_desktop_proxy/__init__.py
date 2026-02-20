import os
import shlex
from shutil import which

HERE = os.path.dirname(os.path.abspath(__file__))


def setup_desktop():
    vncserver = which('vncserver')

    with open(vncserver) as vncserver_file:
        is_turbovnc = "turbovnc" in vncserver_file.read().casefold()

    if is_turbovnc:
        vnc_args = [vncserver, '-noserverkeymap', '-localhost', '-rfbport', '{port}']
    else:
        vnc_args = [vncserver, '-rfbport', '{port}']

    xstartup = os.getenv("JUPYTER_REMOTE_DESKTOP_PROXY_XSTARTUP")
    if not xstartup and not os.path.exists(os.path.expanduser('~/.vnc/xstartup')):
        xstartup = os.path.join(HERE, 'share/xstartup')
    if xstartup:
        vnc_args.extend(['-xstartup', xstartup])

    vnc_command = shlex.join(
        vnc_args
        + [
            '-geometry',
            '1920x1080',
            '-SecurityTypes',
            'None',
            '-fg',
        ]
    )

    return {
        'command': [
            'websockify',
            '--web',
            os.path.join(HERE, 'share/web/noVNC'),
            '--heartbeat',
            '30',
            'localhost:{port}',
        ]
        + ['--', '/bin/sh', '-c', f'cd {os.getcwd()} && {vnc_command}'],
        'timeout': 30,
        'mappath': {'/': '/vnc.html'},
        "launcher_entry": {
            "title": "QGIS Desktop",
            "icon_path": "/usr/local/share/icons/hicolor/scalable/apps/qgis.svg"
        },
        'new_browser_window': True,
    }
