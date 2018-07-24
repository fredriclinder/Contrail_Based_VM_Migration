#cloud-config

runcmd:
 - [ systemctl enable serial-getty@ttyS0.service ]
 - [ systemctl start serial-getty@ttyS0.service ]
