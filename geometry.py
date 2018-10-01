# -*- coding: utf-8 -*-

import math


class Point3D:
    """
    Position in 3D space
    """

    def __init__(self, x, y, z=0):
        """
        Constructor

        >>> position = Point3D(0, 0, 0)

        :param x: Position on X axis
        :type x: int|float

        :param y: Position on Y axis
        :type y: int|float

        :param z: Position on Z axis
        :type z: int|float
        """
        self.__x = x
        self.__y = y
        self.__z = z

    @property
    def x(self):
        """
        Get position on X axis

        :return: Position on X axis
        :rtype: int|float
        """
        return self.__x

    @property
    def y(self):
        """
        Get position on Y axis

        :return: Position on Y axis
        :rtype: int|float
        """
        return self.__y

    @property
    def z(self):
        """
        Get position on Z axis

        :return: Position on Z axis
        :rtype: int|float
        """
        return self.__z

    def equals_on_xy(self, other):
        """
        Test equality on x y axis

        :return: True if equals on x y, else False
        :rtype: bool
        """
        if isinstance(other, Point3D):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def project_on_xy(self, angle, distance):
        """
        Get projection of point in x y axis

        :param angle: Angle (rad)
        :type angle: int|float
        :param distance: Distance
        :type distance: int|float
        :return: Projection of current
        :rtype: Point3D
        """
        return Point3D(
            self.x + distance * math.cos(angle),
            self.y + distance * math.sin(angle),
            self.z
        )

    def __eq__(self, other):
        """
        Test equality

        :param other: Other object
        :return: True if other object equal current, else False
        :rtype: bool
        """
        return self.equals_on_xy(other) and self.z == other.z

    def __sub__(self, other):
        """
        Current coordinates minus other coordinates

        :param other: Other
        :return: Current coordinates minus other coordinates
        :rtype: Point3D
        """
        if not isinstance(other, Point3D):
            raise Exception('Point3D object expected')

        return Point3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __repr__(self):
        """
        Get representation of object

        :return: Representation of object
        :rtype: str
        """
        return 'Point3D' + str(self)

    def __str__(self):
        """
        Get string representation

        :return: String representation of current
        :rtype: str
        """
        return '({0}, {1}, {2})'.format(self.x, self.y, self.z)


class Square:
    """
    Square
    """

    def __init__(self, center, size):
        """
        Constructor

        :param center: Center of square
        :type center: Point3D
        :param size: Size of square
        :type size: float
        """
        self.__center = center
        self.__size = size
        self.__points = ()
        self.__create_points()

    @property
    def center(self):
        """
        Get center of square

        :return: Center of square
        :rtype: Point3D
        """
        return self.__center

    @property
    def size(self):
        """
        Get size of square

        :return: Size of square
        :rtype: int
        """
        return self.__size

    @property
    def points(self):
        """
        Get points of square

        :return: Points of square
        :rtype: tuple
        """
        return self.__points

    def __create_points(self):
        """
        Create points form center and size
        """
        half_size = self.size / 2
        self.__points = (
            Point3D(self.center.x - half_size, self.center.y + half_size, self.center.z),
            Point3D(self.center.x + half_size, self.center.y + half_size, self.center.z),
            Point3D(self.center.x + half_size, self.center.y - half_size, self.center.z),
            Point3D(self.center.x - half_size, self.center.y - half_size, self.center.z)
        )

    def contains(self, other):
        """
        Check if other is inside current

        :param other: Other
        :type other: object
        :return: True if object is inside current, else False
        :rtype: bool
        """
        if not isinstance(other, Point3D):
            raise Exception('Point3D object expected')

        half_size = self.size / 2

        return (self.center.x - half_size <= other.x <= self.center.x + half_size) \
               and (self.center.y - half_size <= other.y <= self.center.y + half_size) \
               and self.center.z == other.z


class Circle:
    """
    Circle
    """

    def __init__(self, center, radius, steps):
        """
        Constructor

        :param center: Center
        :type center: Point3D
        :param radius: Radius
        :type radius: int|float
        :param steps: Number of steps ( >= 1 )
        :type steps: int|float
        """
        self.__steps = steps
        self.__center = center
        self.__radius = radius
        self.__points = ()
        self.__create_points()

    @property
    def center(self):
        """
        Get center of circle

        :return: Center of circle
        :rtype: Point3D
        """
        return self.__center

    @property
    def steps(self):
        """
        Get number of steps

        :return: Number of steps
        :rtype: int|float
        """
        return self.__steps

    @property
    def radius(self):
        """
        Get radius

        :return: Radius
        :rtype: int|float
        """
        return self.__radius

    @property
    def points(self):
        """
        Get points of circle

        :return: Points of circle
        :rtype: tuple
        """
        return self.__points

    def __create_points(self):
        """
        Create points from center and radius
        """
        result = []

        current_angle = 0
        part = (2 * math.pi) / self.__steps

        while current_angle < 2 * math.pi:
            result.append(self.center.project_on_xy(current_angle, self.radius))

            current_angle += part

        self.__points = tuple(result)