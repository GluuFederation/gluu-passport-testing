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

print('trying to turn off droplet named %s' % name )
for droplet in droplets:
    if droplet['name'] == name:
        droplet_id = droplet['id']
        print('turning off droplet id %s' % droplet_id)
        aut.turnoff_droplet(droplet_id)
        print('destroying droplet id %s' % droplet_id)
        aut.destroy_droplet(droplet_id)
