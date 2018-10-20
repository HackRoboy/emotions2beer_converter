#!/usr/bin/env python
import rospy
import time

channels = 4
leds_num = 36
mode = 0


def write_pixels(pixels):
    # image is a list of size 4*36
    with open('/dev/matrixio_everloop', 'wb') as bin_file:
        bin_file.write(bytearray(pixels))
    bin_file.close()


def set_color(red, green, blue, white):
    color_array = []
    for x in range(0,35):
        color_array += [red, green, blue, white]
    write_pixels(color_array)


def turn_off(self):
    self.write_pixels([0]*self.channels*self.leds_num)


def dimming_puls(duration=0):
    # mode 1
    # dims in & out changing colors
    brightness = 50
    half_brightness = 0#int(100 / 2)
    # leds_num = 36
    pixels  = [0, 0, 0, half_brightness] * leds_num
    count = 0
    d = 1
    pos = 0
    color = [0,0,0,half_brightness]
    start = time.time()
    while mode == 1:
        if duration != 0 and time.time() - start>duration:
            break
        #color = [0,0,0,half_brightness]
        pixels = color * leds_num
        write_pixels(pixels)
        # self.show(pixels)
        time.sleep(0.02)
        if count!=1 and (count-1)%brightness==0:
            d = -d
        if(count-1)%(2*brightness) == 0:
        #    print "CHANGED COLOR"
            if pos == 3:
                pos = 0
            else:
                pos += 1
        half_brightness += d
        count += abs(d)
        color = [0]*4
        color[pos] = half_brightness
        # pixels = pixels[-2:] + pixels[:-2]


def tail_clock(duration=0):
    # mode 2
    brightness = 3
    tail = 30
    led = 0
    #print "duration: ",duration
    start = time.time()
    while mode == 2:
        if duration != 0 and time.time()-start > duration:
            break
        intensity = brightness
        pixels = [0] * channels * leds_num
        if led > 35 or led < 0:
            led=0
        for l in range(led-tail,led):
            intensity += 4
            pixels[l*channels+3]=intensity
        write_pixels(pixels)
        led += 1
        time.sleep(0.02)


if __name__ == "__main__":
    mode = 1
    dimming_puls(8)

    mode = 2
    tail_clock(8)
