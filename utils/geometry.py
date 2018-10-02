# -*- coding: utf-8 -*-

import math


class Point3D:

    def __init__(self, x, y, z=0):
        self.__x = x
        self.__y = y
        self.__z = z

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z

    def is_near(self, other, tolerance):
        if not isinstance(other, Point3D):
            raise Exception('Point3D object expected')

        return self.x - tolerance <= other.x <= self.x + tolerance \
               and self.y - tolerance <= other.y <= self.y + tolerance \
               and self.z - tolerance <= other.z <= self.z + tolerance

    def project_on_xy(self, angle, distance):
        return Point3D(
            self.x + distance * math.cos(angle),
            self.y + distance * math.sin(angle),
            self.z
        )

    def __eq__(self, other):
        if not isinstance(other, Point3D):
            raise Exception('Point3D object expected')

        return self.x == other.x and self.y == other.y and self.z == other.z

    def __sub__(self, other):
        if not isinstance(other, Point3D):
            raise Exception('Point3D object expected')

        return Point3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __repr__(self):
        return 'Point3D' + str(self)

    def __str__(self):
        return '({0}, {1}, {2})'.format(self.x, self.y, self.z)


class Circle:

    def __init__(self, center, radius, steps):
        self.__steps = steps
        self.__center = center
        self.__radius = radius
        self.__points = ()
        self.create_points()

    @property
    def center(self):
        return self.__center

    @property
    def steps(self):
        return self.__steps

    @property
    def radius(self):
        return self.__radius

    @property
    def points(self):
        return self.__points

    def create_points(self):
        result = []

        current_angle = 0
        part = (2 * math.pi) / self.__steps

        while current_angle < 2 * math.pi:
            result.append(self.center.project_on_xy(current_angle, self.radius))

            current_angle += part

        self.__points = tuple(result)
