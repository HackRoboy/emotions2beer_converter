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
        for l in range(led-tail, led):
            intensity += 4
            pixels[l*channels+3]=intensity
        write_pixels(pixels)
        led += 1
        time.sleep(0.02)


def light_face():
    brightness = 50

    pixels = [0, 0, 0, 0] * leds_num
    face_array = [3, 4, 5, 13, 14, 15, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

    for i in face_array:
        pixels[i*4 -1 ] = brightness

    write_pixels(pixels)


def dimm_face(duration=0):
    # mode 1
    # dims in & out changing colors
    brightness = 50
    half_brightness = 0  # int(100 / 2)
    # leds_num = 36
    pixels = [0, 0, 0, half_brightness] * leds_num
    count = 0
    d = 1
    pos = 0
    color = [0, 0, 0, half_brightness]
    start = time.time()
    while mode == 3:
        if duration != 0 and time.time() - start > duration:
            break
        # color = [0,0,0,half_brightness]
        pixels = [0, 0, 0, 0]
        for i in range(1, leds_num):
            if i in [3, 4, 5, 13, 14, 15, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]:
                pixels += color
            else:
                pixels += [0, 0, 0, 0]
        write_pixels(pixels)
        # self.show(pixels)
        time.sleep(0.02)
        if count != 1 and (count - 1) % brightness == 0:
            d = -d
        if (count - 1) % (2 * brightness) == 0:
            #    print "CHANGED COLOR"
            if pos == 3:
                pos = 0
            else:
                pos += 1
        half_brightness += d
        count += abs(d)
        color = [0] * 4
        color[pos] = half_brightness
        # pixels = pixels[-2:] + pixels[:-2]


def count_and_light():
    # mode 3
    # dims in & out changing colors
    brightness = 50

    # for anz leds_num
    # light up one led
    # meaning set the brightness of one leds to brightness
    # all others should be 0
    for i in range(leds_num):
        pixels = [0, 0, 0, 0] * leds_num
        pixels[i*4-1] = brightness
        write_pixels(pixels)
        print "pixel ", i
        time.sleep(1)


def pulsing_arrow(point_led, duration=8, color=3):
    # mode 2
    brightness = 50
    tail = 30
    led_r = point_led
    led_l = point_led
    # print "duration: ",duration
    start = time.time()
    # while mode == 2:
    #     if duration != 0 and time.time() - start > duration:
    #         break
    #     intensity = brightness
    #     pixels = [0] * channels * leds_num
    #     if led > 35 or led < 0:
    #         led = 0
    #     for l in range(led - tail, led):
    #         intensity += 4
    #         pixels[l * channels + 3] = intensity
    #     write_pixels(pixels)
    #     led += 1
    #     time.sleep(0.02)
    clockwise_r = True
    clockwise_l = True

    allowed_l = list()
    for i in range(1, 6):
        allowed_l.append(point_led - i)

    # map them to our range
    for i in range(len(allowed_l)):
        if allowed_l[i] < 0:
            allowed_l[i] = 36 + allowed_l[i]

    for i in range(len(allowed_l)):
        if allowed_l[i] > 35:
            allowed_l[i] = allowed_l[i] - 36
    print "allowed_l: ", allowed_l

    allowed_r = list()
    for i in range(1, 6):
        allowed_r.append(point_led + i)

    # map them to our range
    for i in range(len(allowed_r)):
        if allowed_r[i] < 0:
            allowed_r[i] = 36 + allowed_r[i]

    for i in range(len(allowed_r)):
        if allowed_r[i] > 35:
            allowed_r[i] = allowed_r[i] - 36
    print "allowed_r: ", allowed_r

    forbidden_l = list()
    for i in range(0, 36):
        if i not in allowed_l:
            forbidden_l.append(i)

    forbidden_r = list()
    for i in range(0, 36):
        if i not in allowed_r:
            forbidden_r.append(i)

    while mode == 4:
        if duration != 0 and time.time() - start > duration:
            break

        if led_l == 36:
            led_l = 0
        if led_r == 36:
            led_r = 0
        print "led_l: ", led_l
        print "led_r: ", led_r
        print "clockwise_l, ", clockwise_l
        print "clockwise_r, ", clockwise_r

        pixels = [0] * channels * leds_num
        pixels[led_r * channels + color] = brightness
        pixels[led_l * channels + color] = brightness

        write_pixels(pixels)

        if led_l in forbidden_l:
            clockwise_l = not clockwise_l

        if led_r in forbidden_r:
            clockwise_r = not clockwise_r

        if led_r == 0 and not clockwise_r:
            led_r = 36

        if led_l == 0 and not clockwise_l:
            led_l = 36

        if clockwise_r:
            led_r += 1
        else:
            led_r -= 1

        if clockwise_l:
            led_l += 1
        else:
            led_l -= 1

        time.sleep(0.05)


if __name__ == "__main__":
    # mode = 1
    # dimming_puls(8)
    #
    # mode = 2
    # tail_clock(8)
    #
    # # 3 4 5  13 14 15 32 - 21
    #
    # mode = 0
    # count_and_light()

    mode = 4
    pulsing_arrow(30, 8)

