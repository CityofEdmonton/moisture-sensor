function Decoder(bytes, port) {
    // Decode an uplink message from a buffer
    // (array) of bytes to an object of fields.
    var decoded = {};
    
    // moisture
    
    decoded.rawMoisture = bytes[4] + bytes[5]*256;
    var rawMoistureDec;
    if(decoded.rawMoisture > 1750){
      rawMoistureDec = 1;
    } else {
      rawMoistureDec = decoded.rawMoisture / 1750;
    }
    decoded.moisturePercent = rawMoistureDec * 100;
    
    if(decoded.rawMoisture >= 1300){
      decoded.moistureDescription = 'wet';
    } else if( decoded.rawMoisture >= 500 && decoded.rawMoisture < 1300) {
      decoded.moistureDescription = 'moist';
    } else {
      decoded.moistureDescription = 'dry';
    }
    
    var lat = bytes[8] + bytes[9] * 256 + bytes[10] * 65536 + bytes[11] * 4294967296;
    var long = bytes[12] + bytes[13] * 256  + bytes[14] * 65536  + bytes[15] * 4294967296;
    
    decoded.lat = lat / 100000;
    decoded.long = long / -10000;
    
    
    return decoded;
  }