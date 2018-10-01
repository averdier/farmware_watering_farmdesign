# -*- coding: utf-8 -*-

import uuid
from time import time, sleep
from utils import send_celery_script, log, get_resource
from geometry import Point3D, Square


class FarmBot:
    """
    FarmBot
    """

    @property
    def position(self):
        """
        Get position of FarmBot

        :return: Position of Farmbot
        :rtype: Point3D
        """
        response = get_resource('/api/v1/bot/state')
        if response.status_code != 200:
            raise RuntimeError('Unable to get position')

        data = response.json()['location_data']['position']

        return Point3D(data['x'], data['y'], data['z'])

    def move(self, target, speed, tolerance=2, timeout=10):
        """
        Move FarmBot to position

        :param target: Target position
        :type target: Point3D
        :param speed: Speed of movement
        :type speed: int
        :param tolerance: Position tolerance
        :type tolerance: int|float
        :param timeout: Movement timeout
        :type timeout: int
        """
        log('target position: ' + str(target), 'debug')
        possible_area = Square(target, tolerance)

        celery_move_script = {
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
                            'x': target.x,
                            'y': target.y,
                            'z': target.z
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

        t0 = time()
        send_celery_script(celery_move_script)
        current_position = self.position

        secure = 0
        while not target.equals_on_xy(current_position):

            if secure > 120: # 120 sc security
                raise RuntimeError('Movement Timeout')

            secure += 1

            new_position = self.position

            if current_position.equals_on_xy(new_position):

                if new_position.equals_on_xy(target):
                    break

                else:
                    t1 = time()

                    if t1 - t0 > timeout:

                        if not possible_area.contains(new_position):
                            raise RuntimeError('Movement Timeout')
                        else:
                            break

            else:
                current_position = new_position
                t0 = time()

            sleep(1)

        log('FarmBot successfully moved to ' + str(target), 'debug')