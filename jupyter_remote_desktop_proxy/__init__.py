import os
import shlex
from shutil import which

HERE = os.path.dirname(os.path.abspath(__file__))


def setup_desktop():
    vncserver = which('vncserver')

    with open(vncserver) as vncserver_file:
        is_turbovnc = "turbovnc" in vncserver_file.read().casefold()

    # {unix_socket} is expanded by jupyter-server-proxy
    websockify_args = ['--unix-target', "{unix_socket}"]
    vnc_args = [vncserver, '-rfbunixpath', "{unix_socket}", '-rfbport', '-1']
    if is_turbovnc:
        # turbovnc doesn't handle being passed -rfbport -1, but turbovnc also
        # defaults to not opening a TCP port which is what we want to ensure
        vnc_args = [vncserver, '-noserverkeymap', '-rfbunixpath', "{unix_socket}"]

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
            '{port}',
        ]
        + websockify_args
        + ['--', '/bin/sh', '-c', f'cd {os.getcwd()} && {vnc_command}'],
        'timeout': 30,
        'mappath': {'/': '/vnc.html'},
        'new_browser_window': True,
        "unix_socket": True,
    }
