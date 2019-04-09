from network import LoRa
import machine
import utime
import socket
import binascii
import struct

# package header, B: 1 byte for deviceID, I: 1 byte for int
_LORA_PKG_FORMAT = "BI"
DEVICE_ID = 0x01

# LoRa constants
FREQ = 90310000
DEV_ADDR = '26021345'
NWK_SWKEY = 'B005F2A05084CBF0CBD38003161F4AC2'
APP_SWKEY = '8CB2F240C6080A064ACE12A95F9F29E4'

READING_FREQ_IN_MIN = 1

def setup_adc():
    adc = machine.ADC()
    adc.init(bits=12)
    sensor = adc.channel(pin='P13', attn=machine.ADC.ATTN_11DB)
    return sensor


def setup_power_pin():
    power = machine.Pin('P19', machine.Pin.OUT)
    power.value(0)
    return power


def setup_single_lora_channel(lora):
    # remove all the channels
    for channel in range(0, 72):
        lora.remove_channel(channel)
    # set all channels to the same frequency
    for channel in range(0, 8):
        lora.add_channel(channel, frequency=903100000, dr_min=0, dr_max=3)

    return lora

def join_via_abp(lora):
    # create an ABP authentication params
    dev_addr_in_bytes = struct.unpack(">l", binascii.unhexlify(DEV_ADDR))[0]
    nwk_swkey_in_bytes = binascii.unhexlify(NWK_SWKEY)
    app_swkey_in_bytes = binascii.unhexlify(APP_SWKEY)
    
    # join a network using ABP (Activation By Personalization)
    lora.join(activation=LoRa.ABP, auth=(dev_addr_in_bytes, nwk_swkey_in_bytes, app_swkey_in_bytes))


def create_lora_socket():
    lora_socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    lora_socket.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)
    lora_socket.setblocking(False)
    return lora_socket

def send_message(sensor_reading):
    print('sending message')
    lora_socket = create_lora_socket()
    pkt = struct.pack(_LORA_PKG_FORMAT, DEVICE_ID, sensor_reading)
    try:
        lora_socket.send(pkt)
    except Exception as e:
        print(e)
    
def read_sensor(sensor, power_pin):
    # take multiple readings and take the average to get a more reliable reading
    print('reading sensor')
    READING_DELAY_IN_S = 1
    NUM_READINGS = 10

    total = 0

    for i in range(0, NUM_READINGS):
        power_pin.value(1)
        utime.sleep(READING_DELAY_IN_S)
        sensor_reading = sensor.value()
        print('Moisture value: {0}'.format(sensor.value()))
        total += sensor_reading
        power_pin.value(0)

    average_reading = int(total/NUM_READINGS)
    
    return average_reading


def main():
    
    # setup lopy4 pins
    sensor = setup_adc()
    power = setup_power_pin()

    #intialize lora object
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)
    lora = setup_single_lora_channel(lora)
    lora.nvram_restore()

    if not lora.has_joined():
        join_via_abp(lora)
        while not lora.has_joined():
            utime.sleep(2.5)
            print('Not yet joined...')
        print('Join successful!')

    sensor_reading = read_sensor(sensor, power)
    send_message(sensor_reading)
    utime.sleep(1)
    lora.nvram_save()
    machine.deepsleep(int(READING_FREQ_IN_MIN*60*1000))



if __name__ == '__main__':
    main()
