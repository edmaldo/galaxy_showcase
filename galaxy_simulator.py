import tkinter as tk
from random import randint, uniform, random
import math


# scale (radio bubble diameter) in light-years:
SCALE = 150

# number of advanced civilizations from the Drake question:
NUM_CIVS = 15600000

root = tk.Tk()
root.title("Milky Way Galaxy")
c = tk.Canvas(root, width=1000, height=800, bg='black')
c.grid()
c.configure(scrollregion=(-500, -400, 500, 400))

DISC_RADIUS = 50000
DISC_HEIGHT = 1000
DISC_VOL = math.pi * DISC_RADIUS**2 * DISC_HEIGHT


def scale_galaxy():
    """Scale galaxy dimensions based on radio bubble size (scale)."""
    disc_radius_scaled = round(DISC_RADIUS / SCALE)
    bubble_vol = 4/3 * math.pi * (SCALE/2)**3
    disc_vol_scaled = DISC_VOL/bubble_vol
    return disc_radius_scaled, disc_vol_scaled


def detect_prob(disc_vol_scaled):
    """Calculate probability of galactic civilization detecting each other."""
    ratio = NUM_CIVS / disc_vol_scaled
    if ratio < 0.002:
        detection_prob = 0
    elif ratio >= 5:
        detection_prob = 1
    else:
        detection_prob = -0.004747 * ratio**4 + 0.06681 + ratio**3 - 0.3605 * \
                        ratio**2 + 0.9215 * ratio + 0.00826
    return round(detection_prob, 3)


def random_polar_coordinates(disc_radius_scaled):
    """Generate unifrom random (x, y) point within a disc for 2D display."""
    r = random()
    theta = uniform(0, 2 * math.pi)
    x = round(math.sqrt(r) * math.cos(theta) * disc_radius_scaled)
    y = round(math.sqrt(r) * math.sin(theta) * disc_radius_scaled)
    return x, y


def spirals(b, r, rot_fac, fuz_fac, arm):
    """Build spiral arms for tkinter display using logarithmic spiral formula.

    :param b: arbitrary constant in logarithmic spiral equation
    :param r: scaled galactic disc radius
    :param rot_fac: rotation factor
    :param fuz_fac: random shift in star position in arm, applied to 'fuzz' variable
    :param arm: spiral arm (0 = main arm, 1 = trailing stars)
    """

    spiral_stars = []
    fuzz = int(0.030 * abs(r))
    theta_max_degrees = 520
    for i in range(theta_max_degrees):
        theta = math.radians(i)
        x = r * math.exp(b * theta) * math.cos(theta + math.pi * rot_fac)\
            + randint(-fuzz, fuzz) * fuz_fac
        y = r * math.exp(b * theta) * math.sin(theta + math.pi * rot_fac)\
            + randint(-fuzz, fuzz) * fuz_fac
        spiral_stars.append((x, y))
    for x, y in spiral_stars:
        if arm == 0 and int(x % 2) == 0:
            c.create_oval(x-2, y-2, x+2, y+2, fill='white', outline='')
        elif arm == 0 and int(x % 2) != 0:
            c.create_oval(x-1, y-1, x+1, y+1, fill='white', outline='')
        elif arm == 1:
            c.create_oval(x, y, x, y, fill='white', outline='')


def star_haze(disc_radius_scaled, density):
    """Randomly distribute faint tkinter stars in galactic disc.

    :param disc_radius_scaled: galactic disc radius scaled to radio bubble diameter
    :param density: multiplier to vary number of stars posted
    """

    for i in range(0, disc_radius_scaled * density):
        x, y = random_polar_coordinates(disc_radius_scaled)
        c.create_text(x, y, fill='white', font=('Helvetica', '7'), text='.')


def main():
    """Calculate detection probability and post galaxy display and statistics."""
    disc_radius_scaled, disc_vol_scaled = scale_galaxy()
    detection_prob = detect_prob(disc_vol_scaled)

    spirals(b=-0.3, r=disc_radius_scaled, rot_fac=2, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=disc_radius_scaled, rot_fac=1.91, fuz_fac=1.5, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=2, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=2.09, fuz_fac=1.5, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.5, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.4, fuz_fac=1.5, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.5, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.6, fuz_fac=1.5, arm=1)
    star_haze(disc_radius_scaled, density=8)

    c.create_text(-455, -360, fill='white', anchor='w',
                  text='One Pixel = {} LY'.format(SCALE))
    c.create_text(-455, -330, fill='white', anchor='w',
                  text='Radio Bubble Diameter = {} LY'.format(SCALE))
    c.create_text(-455, -300, fill='white', anchor='w',
                  text='Probability of detection for {:,} civilizations = {}'
                  .format(NUM_CIVS, detection_prob))

    if SCALE == 225:
        c.create_rectangle(115, 75, 116, 76, fill='red', outline='')
        c.create_text(118, 72, fill='red', anchor='w',
                      text="<------------ Earth's Radio Bubble")

    root.mainloop()


if __name__ == '__main__':
    main()