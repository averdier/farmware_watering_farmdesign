# -*- coding: utf-8 -*-

import uuid
from time import time, sleep
from .api import send_celery_script, log, get_resource
from .geometry import Point3D


def prepare_move_absolute_script(position, speed):
    return {
        'kind': 'rpc_request',
        'args': {
            'label': 'farmware_circle_' + str(uuid.uuid4())
        },
        'body': [{
            'kind': 'move_absolute',
            'args': {
                'location': {
                    'kind': 'coordinate',
                    'args': {
                        'x': position.x,
                        'y': position.y,
                        'z': position.z
                    }
                },
                'offset': {
                    'kind': 'coordinate',
                    'args': {
                        'x': 0,
                        'y': 0,
                        'z': 0
                    }
                },
                'speed': speed
            }
        }]
    }


class FarmBot:

    @property
    def position(self):
        response = get_resource('/api/v1/bot/state')
        if response.status_code != 200:
            raise RuntimeError('Unable to get position')

        data = response.json()['location_data']['position']

        return Point3D(data['x'], data['y'], data['z'])

    def move(self, position, speed, tolerance, timeout):
        target = Point3D(
            int(position.x),
            int(position.y),
            int(position.z)
        )

        log('target position: ' + str(target), 'debug')

        celery_move_script = prepare_move_absolute_script(target, speed)

        current_position = self.position
        send_celery_script(celery_move_script)

        t0 = time()
        while not target == current_position:
            new_position = self.position

            if new_position == current_position:
                if new_position.is_near(target, tolerance):
                    break

                else:
                    t1 = time()

                    if t1 - t0 > timeout:
                        if not new_position.is_near(target, tolerance):
                            raise RuntimeError('Movement timeout')
                        else:
                            break

            else:
                current_position = new_position
                t0 = time()

            sleep(0.5)

