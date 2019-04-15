#include "ALS31300.h"

ALS31300::ALS31300(I2C *i2c) {
    i2c_ = i2c;
}

void ALS31300::setup() {
    write(CUSTOMER_ACCESS_REG,CUSTOMER_ACCESS_CODE);
}

void ALS31300::setLoopMode(LOOP_MODE loop_mode) {
    switch(loop_mode) {
        case LOOP_MODE::SINGLE_LOOP :

            break;

        case LOOP_MODE::FAST_LOOP  :

            break;

        case LOOP_MODE::FULL_LOOP :

            break;
    }
}

//todo: might be able to avoid resending reg to read from if the current read addr. is tracked
int ALS31300::read(int reg){
    i2c_->start();
    i2c_->write((ALS31300_ADDRESS << 1) & 0xFE); // Slave Address with write bit set => 0
    i2c_->write(reg);
    i2c_->stop();

    wait_us(2);
    i2c_->start();
    // Slave Address with read bit set => 1
    i2c_->write((ALS31300_ADDRESS << 1) | 0x01);

    int rx = i2c_->read(1) << 24;
    rx += i2c_->read(1) << 16;
    rx += i2c_->read(1) << 8;
    rx += i2c_->read(0);

    i2c_->stop();
    wait_us(2);
    return rx;
}

bool ALS31300::write(int reg, uint32_t data){
    i2c_->start();
    i2c_->write((ALS31300_ADDRESS << 1) & 0xFE);

    i2c_->write(reg);
    i2c_->write((char)(data >> 24));
    i2c_->write((char)(data >> 16));
    i2c_->write((char)(data >> 8));
    i2c_->write((char)(data));

    wait_us(2);
    i2c_->stop();
    wait_us(2);
    return true;
}

// Read the X, Y, Z values from Register 0x28 and 0x29
// eight times. No loop mode is used.
//
//void ALS31300::readALS31300ADC(int busAddress)
//{
//    uint32_t value0x27;
//    // Read the register the I2C loop mode is in
////    uint16_t error = read(busAddress, 0x27, value0x27);
//
//    unsigned char* tmp = readALS31300(0x27);
//    uint32_t value0x27 = tmp << 24;
//    value0x27 += tmp << 16;
//    value0x27 += tmp << 8;
//    value0x27 += tmp;
//
//    // I2C loop mode is in bits 2 and 3 so mask them out
//    // and set them to the no loop mode
//    value0x27 = (value0x27 & 0xFFFFFFF3) | (0x0 << 2);
//
//
//
//    // Write the new values to the register the I2C loop mode is in
//    error = write(busAddress, 0x27, value0x27);
//    if (error != kNOERROR)
//    {
//        Serial.print("Unable to write to the ALS31300. error = ");
//        Serial.println(error);
//        return;
//    }
////
////    for (int count = 0; count < 8; ++count)
////    {
////        // Write the address that is going to be read from the ALS31300
////        Wire.beginTransmission(busAddress);
////        Wire.write(0x28);
////        uint16_t error = Wire.endTransmission(false);
////
////        // The ALS31300 accepted the address
////        if (error == kNOERROR)
////        {
////            // Start the read and request 8 bytes
////            // which are the contents of register 0x28 and 0x29
////            Wire.requestFrom(busAddress, 8);
////
////            // Read the first 4 bytes which are the contents of register 0x28
////            uint32_t value0x28 = Wire.read() << 24;
////            value0x28 += Wire.read() << 16;
////            value0x28 += Wire.read() << 8;
////            value0x28 += Wire.read();
////
////            // Read the next 4 bytes which are the contents of register 0x29
////            uint32_t value0x29 = Wire.read() << 24;
////            value0x29 += Wire.read() << 16;
////            value0x29 += Wire.read() << 8;
////            value0x29 += Wire.read();
////
////            // Take the most significant byte of each axis from register 0x28 and combine it with the least
////            // significant 4 bits of each axis from register 0x29, then sign extend the 12th bit.
////            int x = SignExtendBitfield(((value0x28 >> 20) & 0x0FF0) | ((value0x29 >> 16) & 0x0F), 12);
////            int y = SignExtendBitfield(((value0x28 >> 12) & 0x0FF0) | ((value0x29 >> 12) & 0x0F), 12);
////            int z = SignExtendBitfield(((value0x28 >> 4) & 0x0FF0) | ((value0x29 >> 8) & 0x0F), 12);
////
////            // Display the values of x, y and z
////            Serial.print("Count, X, Y, Z = ");
////            Serial.print(count);
////            Serial.print(", ");
////            Serial.print(x);
////            Serial.print(", ");
////            Serial.print(y);
////            Serial.print(", ");
////            Serial.println(z);
////
////            // Look at the datasheet for the sensitivity of the part used.
////            // In this case, full scale range is 500 gauss, other sensitivities
////            // are 1000 gauss and 2000 gauss
////            float mx = (float)x / 4.0;
////            float my = (float)y / 4.0;
////            float mz = (float)z / 4.0;
////
////            Serial.print("MX, MY, MZ = ");
////            Serial.print(mx);
////            Serial.print(", ");
////            Serial.print(my);
////            Serial.print(", ");
////            Serial.print(mz);
////            Serial.println(" Gauss");
////
////            // Convert the X, Y and Z values into radians
////            float rx = (float)x / 4096.0 * M_TWOPI;
////            float ry = (float)y / 4096.0 * M_TWOPI;
////            float rz = (float)z / 4096.0 * M_TWOPI;
////
////            // Use a four quadrant Arc Tan to convert 2
////            // axis to an angle (which is in radians) then
////            // convert the angle from radians to degrees
////            // for display.
////            float angleXY = atan2f(ry, rx) * 180.0 / M_PI;
////            float angleXZ = atan2f(rz, rx) * 180.0 / M_PI;
////            float angleYZ = atan2f(rz, ry) * 180.0 / M_PI;
////
////            Serial.print("angleXY, angleXZ, angleYZ = ");
////            Serial.print(angleXY);
////            Serial.print(", ");
////            Serial.print(angleXZ);
////            Serial.print(", ");
////            Serial.print(angleYZ);
////            Serial.println(" Degrees");
////        }
////        else
////        {
////            Serial.print("Unable to read the ALS31300. error = ");
////            Serial.println(error);
////            break;
////        }
////    }
//}
//
//// Read the X, Y, Z 8 bit values from Register 0x28
//// eight times quickly using the fast loop mode.
////
//void ALS31300::readALS31300ADC_FastLoop(int busAddress)
//{
////    uint32_t value0x27;
////
////    // Read the register the I2C loop mode is in
////    uint16_t error = read(busAddress, 0x27, value0x27);
////    if (error != kNOERROR)
////    {
////        Serial.print("Unable to read from the ALS31300. error = ");
////        Serial.println(error);
////        return;
////    }
////
////    // I2C loop mode is in bits 2 and 3 so mask them out
////    // and set them to the fast loop mode
////    single
////    value0x27 = (value0x27 & 0xFFFFFFF3) | (0x0 << 2);
////    //fast loop
////    value0x27 = (value0x27 & 0xFFFFFFF3) | (0x1 << 2);
////
////    // Write the new values to the register the I2C loop mode is in
////    error = write(busAddress, 0x27, value0x27);
////    if (error != kNOERROR)
////    {
////        Serial.print("Unable to write to the ALS31300. error = ");
////        Serial.println(error);
////    }
////
////    // Write the register address that is going to be read from the ALS31300 (0x28)
////    Wire.beginTransmission(busAddress);
////    Wire.write(0x28);
////    error = Wire.endTransmission(false);
////
////    // The ALS31300 accepted the address
////    if (error == kNOERROR)
////    {
////        int x;
////        int y;
////        int z;
////
////        // Eight times is arbitrary, there is no limit. What is being demonstrated
////        // is that once the address is set to 0x28, all reads will be from 0x28 until the
////        // register address is changed or the loop mode is changed.
////        for (int count = 0; count < 8; ++count)
////        {
////            // Start the read and request 4 bytes
////            // which is the contents of register 0x28
////            Wire.requestFrom(busAddress, 4);
////
////            // Read the first 4 bytes which are the contents of register 0x28
////            // and sign extend the 8th bit
////            x = SignExtendBitfield(Wire.read(), 8);
////            y = SignExtendBitfield(Wire.read(), 8);
////            z = SignExtendBitfield(Wire.read(), 8);
////            Wire.read();    // Temperature and flags not used
////
////            // Display the values of x, y and z
////            Serial.print("Count, X, Y, Z = ");
////            Serial.print(count);
////            Serial.print(", ");
////            Serial.print(x);
////            Serial.print(", ");
////            Serial.print(y);
////            Serial.print(", ");
////            Serial.println(z);
////
////            // Convert the X, Y and Z values into radians
////            float rx = (float)x / 256.0 * M_TWOPI;
////            float ry = (float)y / 256.0 * M_TWOPI;
////            float rz = (float)z / 256.0 * M_TWOPI;
////
////            // Use a four quadrant Arc Tan to convert 2
////            // axis to an angle (which is in radians) then
////            // convert the angle from radians to degrees
////            // for display.
////            float angleXY = atan2f(ry, rx) * 180.0 / M_PI;
////            float angleXZ = atan2f(rz, rx) * 180.0 / M_PI;
////            float angleYZ = atan2f(rz, ry) * 180.0 / M_PI;
////
////            Serial.print("angleXY, angleXZ, angleYZ = ");
////            Serial.print(angleXY);
////            Serial.print(", ");
////            Serial.print(angleXZ);
////            Serial.print(", ");
////            Serial.print(angleYZ);
////            Serial.println(" Degrees");
////        }
////    }
////    else
////    {
////        Serial.print("Unable to read the ALS31300. error = ");
////        Serial.println(error);
////    }
//}
//
//// Read the X, Y, Z 12 bit values from Register 0x28 and 0x29
//// eight times quickly using the full loop mode.
////
//void ALS31300::readALS31300ADC_FullLoop(int busAddress)
//{
////    uint32_t value0x27;
////
////    // Read the register the I2C loop mode is in
////    uint16_t error = read(busAddress, 0x27, value0x27);
////    if (error != kNOERROR)
////    {
////        Serial.print("Unable to read from the ALS31300. error = ");
////        Serial.println(error);
////        return;
////    }
////
////    // I2C loop mode is in bits 2 and 3 so mask them out
////    // and set them to the full loop mode
////    single
////    value0x27 = (value0x27 & 0xFFFFFFF3) | (0x0 << 2);
////    //fast loop
////    value0x27 = (value0x27 & 0xFFFFFFF3) | (0x1 << 2);
////    full loop
////    value0x27 = (value0x27 & 0xFFFFFFF3) | (0x2 << 2);
////
////    // Write the new values to the register the I2C loop mode is in
////    error = write(busAddress, 0x27, value0x27);
////    if (error != kNOERROR)
////    {
////        Serial.print("Unable to write to the ALS31300. error = ");
////        Serial.println(error);
////        return;
////    }
////
////    // Write the address that is going to be read from the ALS31300
////    Wire.beginTransmission(busAddress);
////    Wire.write(0x28);
////    error = Wire.endTransmission(false);
////
////    // The ALS31300 accepted the address
////    if (error == kNOERROR)
////    {
////        int x;
////        int y;
////        int z;
////
////        // Eight times is arbitrary, there is no limit. What is being demonstrated
////        // is that once the address is set to 0x28, the first four bytes read will be from 0x28
////        // and the next four will be from 0x29 after that it starts all over at 0x28
////        // until the register address is changed or the loop mode is changed.
////        for (int count = 0; count < 8; ++count)
////        {
////            // Start the read and request 8 bytes
////            // which is the contents of register 0x28 and 0x29
////            Wire.requestFrom(busAddress, 8);
////
////            // Read the first 4 bytes which are the contents of register 0x28
////            x = Wire.read() << 4;
////            y = Wire.read() << 4;
////            z = Wire.read() << 4;
////            Wire.read();    // Temperature and flags not used
////
////            // Read the next 4 bytes which are the contents of register 0x29
////            Wire.read();    // Upper byte not used
////            x |= Wire.read() & 0x0F;
////            byte d = Wire.read();
////            y |= (d >> 4) & 0x0F;
////            z |= d & 0x0F;
////            Wire.read();    // Temperature not used
////
////            // Sign extend the 12th bit for x, y and z.
////            x = SignExtendBitfield((uint32_t)x, 12);
////            y = SignExtendBitfield((uint32_t)y, 12);
////            z = SignExtendBitfield((uint32_t)z, 12);
////
////            // Display the values of x, y and z
////            Serial.print("Count, X, Y, Z = ");
////            Serial.print(count);
////            Serial.print(", ");
////            Serial.print(x);
////            Serial.print(", ");
////            Serial.print(y);
////            Serial.print(", ");
////            Serial.println(z);
////
////            // Convert the X, Y and Z values into radians
////            float rx = (float)x / 4096.0 * M_TWOPI;
////            float ry = (float)y / 4096.0 * M_TWOPI;
////            float rz = (float)z / 4096.0 * M_TWOPI;
////
////            // Use a four quadrant Arc Tan to convert 2
////            // axis to an angle (which is in radians) then
////            // convert the angle from radians to degrees
////            // for display.
////            float angleXY = atan2f(ry, rx) * 180.0 / M_PI;
////            float angleXZ = atan2f(rz, rx) * 180.0 / M_PI;
////            float angleYZ = atan2f(rz, ry) * 180.0 / M_PI;
////
////            Serial.print("angleXY, angleXZ, angleYZ = ");
////            Serial.print(angleXY);
////            Serial.print(", ");
////            Serial.print(angleXZ);
////            Serial.print(", ");
////            Serial.print(angleYZ);
////            Serial.println(" Degrees");
////        }
////    }
////    else
////    {
////        Serial.print("Unable to read the ALS31300. error = ");
////        Serial.println(error);
////    }
//}
//
//// Using I2C, read 32 bits of data from the address on the device at the bus address
////
//uint16_t ALS31300::read(int busAddress, uint8_t address, uint32_t& value)
//{
////    // Write the address that is to be read to the device
////    Wire.beginTransmission(busAddress);
////    Wire.write(address);
////    int error = Wire.endTransmission(false);
////
////    // if the device accepted the address,
////    // request 4 bytes from the device
////    // and then read them, MSB first
////    if (error == kNOERROR)
////    {
////        Wire.requestFrom(busAddress, 4);
////        value = Wire.read() << 24;
////        value += Wire.read() << 16;
////        value += Wire.read() << 8;
////        value += Wire.read();
////    }
////
////    return error;
//    return 0;
//}
//
//// Using I2C, write 32 bit data to an address to the device at the bus address
////
//uint16_t ALS31300::write(int busAddress, uint8_t address, uint32_t value)
//{
////    // Write the address that is to be written to the device
////    // and then the 4 bytes of data, MSB first
////    Wire.beginTransmission(busAddress);
////    Wire.write(address);
////    Wire.write((byte)(value >> 24));
////    Wire.write((byte)(value >> 16));
////    Wire.write((byte)(value >> 8));
////    Wire.write((byte)(value));
////    return Wire.endTransmission();
//    return 0;
//}


// Sign extend a right justified value
//
long ALS31300::SignExtendBitfield(uint32_t data, int width) {
    long x = (long)data;
    long mask = 1L << (width - 1);

    if (width < 32) {
        x = x & ((1 << width) - 1); // make sure the upper bits are zero
    }

    return (long)((x ^ mask) - mask);
}

constexpr char hexmap[] = {'0', '1', '2', '3', '4', '5', '6', '7',
                           '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};

std::string ALS31300::hexStr(unsigned char *data, int len) {
    std::string s((unsigned)len * 2, ' ');
    for (int i = 0; i < len; ++i) {
        s[2 * i]     = hexmap[(data[i] & 0xF0) >> 4];
        s[2 * i + 1] = hexmap[data[i] & 0x0F];
    }
    return s;
}