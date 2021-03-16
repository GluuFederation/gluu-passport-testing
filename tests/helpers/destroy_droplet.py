import ipdb
from pydoautomator import Automator
import os

digital_ocean_token = os.getenv("DO_TOKEN")

# requires ENV
name = os.getenv('DROPLET_HOST')
floating = os.getenv('FLOATING_IP')
snapshot = os.getenv('SNAPSHOT_ID')


aut = Automator(digital_ocean_token)

droplets = aut.get_all_droplets()

for droplet in droplets:
    print('trying to turn off droplet named %s' % name )
    if droplet['name'] == name:
        aut.turnoff_droplet(droplet['id'])
        print('destroying droplet id' % droplet['id'])
        aut.destroy_droplet(droplet['id'])
