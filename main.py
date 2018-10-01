# -*- coding: utf-8 -*-

import os
from utils import log, get_plants
from farmbot import FarmBot
from geometry import Circle, Point3D


def get_parameters():
    """
    Get parameters

    :return: Farmware parameters (radius, speed, steps)
    :rtype: tuple
    """
    try:
        sp = int(os.environ.get('watering_tool_speed', '800'))
        st = int(os.environ.get('watering_tool_steps', '8'))
    except ValueError:
        raise Exception('Wrong parameters format')
    if sp < 1:
        raise Exception('Speed ( > 1 )')
    if st < 2:
        raise Exception('Steps ( > 2 )')

    return sp, st


if __name__ == '__main__':
    log('Started', 'debug')

    try:
        speed, steps = get_parameters()

        log('Speed: {0}, Steps: {1}'.format(speed, steps), 'debug')

        path = []
        for plant in get_plants():
            path.extend(Circle(Point3D(plant['x'], plant['y'], plant['z']), plant['radius'] * 2, steps).points)

        farmbot = FarmBot()

        current_position = farmbot.position
        log('Current position: ' + str(current_position), 'debug')

        log('Movements to do: {0}'.format(len(path)), 'debug')

        for position in path:
            farmbot.move(position, speed)

    except Exception as ex:
        log('Error --> {0}'.format(ex), 'error')

    log('Finished', 'debug')
