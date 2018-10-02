# -*- coding: utf-8 -*-

import os
from utils.farmbot import FarmBot
from utils.geometry import Circle, Point3D
from utils.api import log, get_plants


def get_parameters():
    """
    Get parameters

    :return: Farmware parameters (radius, speed, steps)
    :rtype: tuple
    """
    try:
        sp = int(os.environ.get('watering_tool_speed', '800'))
        st = int(os.environ.get('watering_tool_steps', '8'))
        tl = int(os.environ.get('watering_tool_tolerance', '8'))

    except ValueError:
        raise Exception('Wrong parameters format')
    if sp < 1:
        raise Exception('Speed ( > 1 )')
    if st < 2:
        raise Exception('Steps ( > 2 )')
    if tl < 1:
        raise Exception('Tolerance ( > 1)')

    return sp, st, tl


if __name__ == '__main__':
    log('Started', 'debug')

    try:
        speed, steps, tolerance = get_parameters()

        log('Speed: {0}, Steps: {1}, Tolerance {2}'.format(speed, steps, tolerance), 'debug')

        path = []
        for plant in get_plants():
            path.extend(Circle(Point3D(plant['x'], plant['y'], plant['z']), plant['radius'] * 2, steps).points)

        farmbot = FarmBot()

        current_position = farmbot.position
        log('Current position: ' + str(current_position), 'debug')

        log('Movements to do: {0}'.format(len(path)), 'debug')

        for position in path:
            farmbot.move(position, speed, tolerance, 10)

    except Exception as ex:
        log('Error --> {0}'.format(ex), 'error')

    log('Finished', 'debug')
