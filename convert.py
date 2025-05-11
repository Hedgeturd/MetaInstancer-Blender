import math
import struct

SCALING_FACTOR = 255 / math.pi  # 255 is max uint8, math.pi is the max value in radians

class Header():
    HEADER_FORMAT = ">IIIIIIII"  # Big-endian: 8 unsigned 32-bit integers
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    INSTANCE_FORMAT = ">fffBBBBhhBBBB"
    INSTANCE_SIZE = struct.calcsize(INSTANCE_FORMAT)

class Convert():
    def to_uint8(value):
        """Convert radians to uint8 (range: 0 to 255)."""
        # Scale the value and clamp it to the uint8 range
        uint8_value = int((value + math.pi) * SCALING_FACTOR)  # Convert negative to positive by adding pi
        return max(min(uint8_value, 255), 0)  # Ensure it's within the uint8 range

    def to_int16(value):
        """Convert radians to int16 (-32768 to 32767)."""
        int16_value = int((value / math.pi) * 32767)  # Scale radians (-π to π) to int16 range
        return max(min(int16_value, 32767), -32768)  # Clamp to int16 range