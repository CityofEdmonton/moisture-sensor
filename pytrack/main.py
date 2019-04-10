from network import LoRa
import machine
import utime
import socket
import binascii
import struct
from L76GNSS import L76GNSS
from pytrack import Pytrack

# package header, B: 1 byte for deviceID, I: 1 byte for int
_LORA_PKG_FORMAT = "BIII"
DEVICE_ID = 0x01

# LoRa constants
FREQ = 90310000
DEV_ADDR = '<DEVICE ADDRESS>'
NWK_SWKEY = '<NETWORK SESSION KEY>'
APP_SWKEY = '<APP SESSION KEY>'

READING_FREQ_IN_MIN = 0.16

def setup_adc():
    adc = machine.ADC()
    adc.init(bits=12)
    sensor = adc.channel(pin='P19', attn=machine.ADC.ATTN_11DB)
    return sensor

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

def format_gps_for_lora(gps_object):
    lat = gps_object.coordinates()[0]
    long = gps_object.coordinates()[1]

    if(lat is not None and long is not None):
        lat = int(lat * 100000)
        long = int(long * 10000 * -1)
    else:
        lat = 0
        long = 0

    print("Lat: {0}, Long: {1}".format(lat,long))    
    return (lat, long)

def send_message(sensor_reading, gps_object):
    print('sending message')
    lora_socket = create_lora_socket()
    formatted_gps_object = format_gps_for_lora(gps_object)
    pkt = struct.pack(_LORA_PKG_FORMAT, DEVICE_ID, sensor_reading, formatted_gps_object[0], formatted_gps_object[1])
    try:
        lora_socket.send(pkt)
    except Exception as e:
        print(e)
    
def read_sensor(sensor):
    # take multiple readings and take the average to get a more reliable reading
    print('Reading sensor...')
    READING_DELAY_IN_S = 0.25
    NUM_READINGS = 10

    total = 0

    for i in range(0, NUM_READINGS):
        utime.sleep(READING_DELAY_IN_S)
        sensor_reading = sensor.value()
        print('Moisture value: {0}'.format(sensor.value()))
        total += sensor_reading

    average_reading = int(total/NUM_READINGS)
    print('Average value: {0}'.format(average_reading))

    return average_reading

def setup_gps():
    py = Pytrack()
    l76 = L76GNSS(py, timeout=30)

    return l76

def main():

    gps = setup_gps()

    # setup lopy4 pins
    sensor = setup_adc()

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

    sensor_reading = read_sensor(sensor)
    send_message(sensor_reading, gps)
    utime.sleep(1)
    lora.nvram_save()
    machine.deepsleep(int(READING_FREQ_IN_MIN*60*1000))



if __name__ == '__main__':
    main()
