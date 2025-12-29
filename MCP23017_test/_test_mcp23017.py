# Test MCP23017 as input port expander
# connected to I2C1

from machine import Pin, I2C
import time

# Scan addresses
print("External devices on I2C port 1, GPIO27(SCL), GPIO26(SDA)")
i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=100000)
addresses = i2c.scan()
for a in addresses:
    print(hex(a))

# Rudimentary class for the port expander
class MCP23017():

    def __init__(self, i2c, mcp_addr=0x20):
        self.addr = mcp_addr
        self.i2c = i2c
        
    def read_regs(self):
        # read all 22 registers and return list of values
        x = self.i2c.readfrom_mem(self.addr, 0, 22)
        x = list(x)
        return x
    
    def write_reg(self, reg_addr, value):
        # write value into reg_addr 
        self.i2c.writeto_mem(self.addr, reg_addr,  bytes([value]))
    
    def pullup_all(self):
        # Set pullups 100k for A and B port
        self.write_reg(0xc, 0xFF)
        self.write_reg(0xd, 0xFF)

    def read_A(self):
        # Read 8 bits on port A
        x = self.i2c.readfrom_mem(self.addr, 0x12 , 1)
        return x[0]
    
    def read_B(self):
        # Read 8 bits on port B
        x = self.i2c.readfrom_mem(self.addr, 0x13 , 1)
        return x[0]

    def enable_int_A(self):
        self.write_reg(0x04, 0xFF) 

    def enable_int_B(self):
        self.write_reg(0x05, 0xFF)
        
#-------------------------------------------------------
# TEST        
mcp = MCP23017(i2c)

print("Register values after powerup")
x = mcp.read_regs()
print(x)

print("Register values after switching on pullups:")
mcp.pullup_all()
x = mcp.read_regs()
print(x)

print("Enabling interrupts")
mcp.enable_int_A()
mcp.enable_int_B()

print("Reading A and B ports in loop, stop with Ctrl-C")
input("Start = <Enter>")

while True:
    a = mcp.read_A()
    b = mcp.read_B()
    print(hex(a),hex(b))
    time.sleep(0.05)
