# windows setup

- https://stackoverflow.com/a/26374992
- use remmina & freerdp (for arch, install both)
- https://medium.com/@johann_78792/getting-started-with-bloombergs-python-desktop-api-5fd083b4193a
- need to get around 729 error with logging in (because rdp is blocked). need to login automatically on boot
  - see https://docs.microsoft.com/en-us/sysinternals/downloads/autologon
  - https://serverfault.com/questions/579615/auto-login-to-aws-ec2-instance-running-windows-on-startup
  - try teamviewer, see what happens: https://www.techradar.com/news/best-remote-desktop-software
- teamviewer works :)
  - set resolution to 1920x1080 (display settings)
  - maybe make the workstation have [these requirements](https://assets.bbhub.io/professional/sites/10/Bloomberg-User-Workstation-Requirements.pdf)
  - just run autologin script (https://serverfault.com/a/840563) and remove ctrl-alt-delete thing (https://serverfault.com/a/911298)
  - maybe figure out a way to use a static ip address for the ec2 instance
  - install blpapi using conda (because otherwise you need the c++ sdk)
  - port 8194 is where the data is sent
  - https://www.tomshardware.com/news/how-to-open-firewall-ports-in-windows-10,36451.html
  - 5938
  - allow ping: https://stackoverflow.com/a/42777521/8623391
  - need to figure out how to open ports. first need to make sure it's working locally
