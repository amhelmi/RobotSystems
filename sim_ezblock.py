class _Basic_class(object):
    _class_name = '_Basic_class'
    DEBUG_LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL,
              }
    DEBUG_NAMES = ['critical', 'error', 'warning', 'info', 'debug']

    def __init__(self):
        pass

    @property
    def debug(self):
        return 0

    @debug.setter
    def debug(self, debug):
    	pass

    def run_command(self, cmd):
        return 0, 1

    def map(self, x, in_min, in_max, out_min, out_max):
        return 0


class Servo(_Basic_class):
    MAX_PW = 2500
    MIN_PW = 500
    _freq = 50
    def __init__(self, pwm):
        pass

    # angle ranges -90 to 90 degrees
    def angle(self, angle):
    	pass


class Pin(_Basic_class):
    OUT = GPIO.OUT
    IN = GPIO.IN
    IRQ_FALLING = GPIO.FALLING
    IRQ_RISING = GPIO.RISING
    IRQ_RISING_FALLING = GPIO.BOTH
    PULL_UP = GPIO.PUD_UP
    PULL_DOWN = GPIO.PUD_DOWN
    PULL_NONE = None

    _dict = {
        "BOARD_TYPE": 12,
    }

    _dict_1 = {
        "D0":  17,
        "D1":  18,
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25,
        "D7":  4,
        "D8":  5,
        "D9":  6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  19,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 21,
    }

    _dict_2 = {
        "D0":  17,
        "D1":   4, # Changed
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25, # Removed
        "D7":   4, # Removed
        "D8":   5, # Removed
        "D9":   6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  25, # Changed
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST":  5, # Changed
    }

    def __init__(self, *value):
        pass

        
    def check_board_type(self):
    	pass

    def init(self, mode, pull=PULL_NONE):
    	pass

    def dict(self, *_dict):
    	pass

    def __call__(self, value):
        return 0

    def value(self, *value):
    	return 0

    def on(self):
        return 0

    def off(self):
        return 0

    def high(self):
        return 0

    def low(self):
        return 0

    def mode(self, *value):
    	pass

    def pull(self, *value):
        return 0

    def irq(self, handler=None, trigger=None, bouncetime=200):
    	pass

    def name(self):
        return 0

    def names(self):
        return 0

    class cpu(object):
        GPIO17 = 17
        GPIO18 = 18
        GPIO27 = 27
        GPIO22 = 22
        GPIO23 = 23
        GPIO24 = 24
        GPIO25 = 25
        GPIO26 = 26
        GPIO4  = 4
        GPIO5  = 5
        GPIO6  = 6
        GPIO12 = 12
        GPIO13 = 13
        GPIO19 = 19
        GPIO16 = 16
        GPIO26 = 26
        GPIO20 = 20
        GPIO21 = 21

        def __init__(self):
            pass


class I2C(_Basic_class):
    MASTER = 0
    SLAVE  = 1
    RETRY = 5

    def __init__(self, *args, **kargs):
        pass

    def _i2c_write_byte(self, addr, data):
        return 0

    def _i2c_write_byte_data(self, addr, reg, data):
        return 0
    
    def _i2c_write_word_data(self, addr, reg, data):
        return 0
    
    def _i2c_write_i2c_block_data(self, addr, reg, data):
        return 0

    def _i2c_read_byte(self, addr):
        return 0

    def _i2c_read_i2c_block_data(self, addr, reg, num):
        return 0

    def is_ready(self, addr):
    	return 0

    def scan(self):
        return 0

    def send(self, send, addr, timeout=0):
        pass

    def recv(self, recv, addr=0x00, timeout=0):
    	pass

    def mem_write(self, data, addr, memaddr, timeout=5000, addr_size=8): #memaddr match to chn
    	pass
    
    def mem_read(self, data, addr, memaddr, timeout=5000, addr_size=8):
    	return 0
    
    def readfrom_mem_into(self, addr, memaddr, buf):
    	return 0

    def writeto_mem(self, addr, memaddr, data):
        pass

class PWM(I2C):
    REG_CHN = 0x20
    REG_FRE = 0x30
    REG_PSC = 0x40
    REG_ARR = 0x44

    ADDR = 0x14

    CLOCK = 72000000

    def __init__(self, channel, debug="critical"):
        pass

    def i2c_write(self, reg, value):
    	pass

    def freq(self, *freq):
    	pass

    def prescaler(self, *prescaler):
    	pass

    def period(self, *arr):
    	pass

    def pulse_width(self, *pulse_width):
    	pass

    def pulse_width_percent(self, *pulse_width_percent):
    	pass
        

class ADC(I2C):
    def __init__(self, chn):
    	pass
        
    def read(self):
    	return 0

    def read_voltage(self):
        return 0
        