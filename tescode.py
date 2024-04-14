def int_to_6_digit_hex(my_integer):
    # Convert integer to 6-digit hexadecimal (with '0x' prefix)
    hex_value = hex(my_integer)[2:].zfill(6)  # Remove '0x' and zero-fill to 6 digits

    # Split into three 2-digit values
    hex_parts = [hex_value[i:i+2] for i in range(0, 6, 2)]
    print('Hex Parts', hex_parts)

    # Create a bytearray
    my_bytearray = bytearray.fromhex(''.join(hex_parts))

    return my_bytearray

# Example usage
my_integer = 16384
result_bytearray = int_to_6_digit_hex(my_integer)

print(f"Original integer: {my_integer}")
print(f"6-digit hexadecimal value: {result_bytearray.hex()}")
print(f"Bytearray: {result_bytearray}")
