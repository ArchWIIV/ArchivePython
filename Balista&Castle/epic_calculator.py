import math
from PIL import Image


class Vector:
    x = 0.0
    y = 0.0

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def normalized(self):
        return self / abs(self)

    def turned(self, angle_rads):
        return Vector(self.x * math.cos(angle_rads) - self.y * math.sin(angle_rads),
                      self.x * math.sin(angle_rads) + self.y * math.cos(angle_rads))


class CalculationResult:

    def __init__(self, position, velocity, time, image, mass, pixels_per_meter):
        self.position = position
        self.x = position.x
        self.velocity = abs(velocity)
        self.angle = math.degrees(math.atan(velocity.y / velocity.x))
        self.time = time
        self.image = image
        self.mass = mass
        self.pixels_per_meter = pixels_per_meter

    def save_image(self, path):
        file = open(path, 'wb')
        self.image.save(file)
        file.close()

    def calculate_damage(self, multiplier):
        return self.mass * self.velocity * multiplier

    def draw_castle(self, x1, x2):
        x1 *= self.pixels_per_meter
        x2 *= self.pixels_per_meter

        for j in range(6):
            for i in range(x1, x2 + 1):
                self.image.putpixel((i + 1023, 1023 - j), 0)

    def __str__(self):
        return "Projectile landed at " + str(int(self.x)) + " m, with a speed of " + str(int(self.velocity))\
               + " m/s,\n angle of " + str(int(abs(self.angle))) + ", impulse of " + str(int(self.mass * self.velocity))\
               + " and it took it " + str(self.time) + " seconds."


def air_density(pressure, T, humidity):
    vapour_pressure = humidity * 6.1078 * math.pow(10, ((7.5 * T - 2048.625) / (T - 35.85))) * 100
    dry_pressure = pressure - vapour_pressure
    density = (dry_pressure / (287.058 * T)) + (vapour_pressure / (461.495 * T))
    return clamp(density, 10000, 0)


def f_air(pressure, T, humidity, V, S, air_speed):
    total_speed = air_speed - V
    return total_speed.normalized() * 0.3 * S * ((air_density(pressure, T, humidity) * abs(total_speed) * abs(total_speed)) / 2)


def clamp(v, mx=2047, mn=0):
    return min(max(mn, v), mx)


def calculate(pressure, T, humidity, mass, radius, start_impulse, angle, wind_x, pixels_per_meter=1, deltaTime=0.001):

    wind = Vector(wind_x, 0)
    time = 0

    img = Image.new("1", (2048, 1024), 1)

    pos = Vector(0, 0)
    velocity = Vector(start_impulse / mass, 0).turned(math.radians(angle))

    while pos.y >= 0:
        time += deltaTime

        velocity.y -= 9.8 * deltaTime
        velocity += f_air(pressure, T, humidity, velocity, radius * radius * math.pi, wind) / mass * deltaTime

        pos = pos + velocity * deltaTime

        img.putpixel((clamp(int(pos.x * pixels_per_meter) + 1024), 1023 - clamp(int(pos.y * pixels_per_meter), 1023, 0)), 0)

    return CalculationResult(pos, velocity, time, img, mass, pixels_per_meter)


def hg_to_p(val):
    return 133.322 * val


def c_to_k(val):
    return val + 273.15