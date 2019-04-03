from network import LoRa
import machine
import utime
import socket
import binascii
import struct

# package header, B: 1 byte for deviceID, I: 1 byte for int
_LORA_PKG_FORMAT = "BI"
DEVICE_ID = 0x01


def setup_adc():
    adc = machine.ADC()
    adc.init(bits=12)
    sensor = adc.channel(pin='P13', attn=machine.ADC.ATTN_11DB)
    return sensor


def setup_power_pin():
    power = machine.Pin('P19', machine.Pin.OUT)
    power.value(0)
    return power


def setup_single_lora_channel():
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)
    # remove all the channels
    for channel in range(0, 72):
        lora.remove_channel(channel)
    # set all channels to the same frequency (must be before sending the OTAA join request)
    for channel in range(0, 8):
        lora.add_channel(channel, frequency=903100000, dr_min=0, dr_max=3)

    join_abp(lora)


def join_abp(lora):
    # create an ABP authentication params
    dev_addr = struct.unpack(">l", binascii.unhexlify('26021345'))[0]
    nwk_swkey = binascii.unhexlify('B005F2A05084CBF0CBD38003161F4AC2')
    app_swkey = binascii.unhexlify('8CB2F240C6080A064ACE12A95F9F29E4')
    # join a network using ABP (Activation By Personalization)
    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))


def create_lora_socket():
    lora_socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    lora_socket.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)
    lora_socket.setblocking(False)
    return lora_socket


def read_sensor(sensor, power_pin):
    power_pin.value(1)
    utime.sleep(5)
    return sensor.value()


def main():
    sensor = setup_adc()
    power = setup_power_pin()
    setup_single_lora_channel()
    lora_socket = create_lora_socket()

    while True:
        sensor_reading = read_sensor(sensor, power)
        pkt = struct.pack(_LORA_PKG_FORMAT, DEVICE_ID, sensor_reading)
        print(pkt)
        lora_socket.send(pkt)
        power.value(0)


if __name__ == '__main__':
    main()
