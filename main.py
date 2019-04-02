import machine
import utime

adc = machine.ADC()
adc.init(bits=12)
sensor = adc.channel(pin='P13', attn= machine.ADC.ATTN_11DB)

power = machine.Pin('P19', machine.Pin.OUT)
power.value(0)

while True:
    power.value(1)
    utime.sleep(1)
    value = sensor.value()
    print(value)
    power.value(0)