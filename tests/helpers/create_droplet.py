from pydoautomator import Automator, Droplet
import os

digital_ocean_token = os.getenv("DO_TOKEN")

aut = Automator(digital_ocean_token)

# requires ENV
name = os.getenv('DROPLET_HOST')
floating = os.getenv('FLOATING_IP')
snapshot = os.getenv('SNAPSHOT_ID')


droplet_data = {
    "name": name,
    "region": "nyc1",
    "size": "s-8vcpu-16gb",
    "image": snapshot,
    "ssh_keys": [28792503, 28790914],
    "private_networking": True,
    "monitoring": True
}

droplet = Droplet(**droplet_data)

droplet_id = aut.create_droplet_from_snapshot(droplet)

action_status = aut.assign_floating_ip_to_droplet(floating, droplet_id)

if action_status == 'completed':
    print('floating_ip assigned to droplet!')
