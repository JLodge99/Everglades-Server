import json
import os

config_dir = os.path.abspath('config')
with open(os.path.join(config_dir, "Loadout0.json")) as fid:
    loadout = json.load(fid)\

print(loadout['Squads'][0]['ReconInfo']['Type'])

# 0: ['active', 3, '0.38'],
# 1: ['active', 3, '0.45'],
# 3: ['active', 3, '1.20'],
# 4: ['active', 2, '2.30'],
# 5: ['active', 3, '0.40'],
# 6: ['active', 3, '2.20'],
# 7: ['active', 1, '1.13'],
# 8: ['active', 3, '1.08'],
# 9: ['active', 3, '0.77'],
# 11: ['passive', 3]
sensor_config = {}
for i in range(12):
    hasRecon = False
    for unit in loadout['Squads'][i]['Squad']:
        if 'recon' in unit.values():
            hasRecon = True
    if hasRecon:
        sensorinfo = []
        sensorinfo.append(loadout['Squads'][i]['ReconInfo']['Type'])
        sensorinfo.append(loadout['Squads'][i]['ReconInfo']['Range'])
        sensorinfo.append(loadout['Squads'][i]['ReconInfo']['Wavelength'])
        sensor_config[i] = sensorinfo
print(sensor_config)
