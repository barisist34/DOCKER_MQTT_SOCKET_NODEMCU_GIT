import serial
import serial.tools.list_ports
import time

comport=list(serial.tools.list_ports.comports())[0][0]
print(f"comport: {comport}")
time.sleep(2) 
print("arduino serial nesnesi oluşturuluyor şimdi...")
# arduino = serial.Serial(port=comport,  baudrate=9600, timeout=2,stopbits=serial.STOPBITS_ONE)
# arduino = serial.Serial(port=comport,  baudrate=9600, timeout=0.2,dsrdtr=None)dsrdtr=True
# arduino = serial.Serial(port=comport,  baudrate=9600, timeout=0.2,dsrdtr=True)
arduino = serial.Serial()
arduino.port=comport
arduino.baudrate=9600
# arduino.timeout=1
# arduino.setDTR(False)
arduino.setDTR(True)
arduino.open()
print(f"arduino serial nesnesi: {arduino}")
time.sleep(1) 
# arduino.reset_input_buffer()
# arduino.reset_output_buffer()
# time.sleep(2)  #250203  veri göndermeden önce (write() öncesi) django tarafında input buffer temizleyelim********************
# arduino.reset_input_buffer()
time.sleep(1) 
write_sayi=arduino.write(bytes("all",  'utf-8')) #butun config göster
# write_sayi=arduino.write(bytes("name",  'utf-8')) #butun config göster
# write_sayi=arduino.write(bytes("abcd",  'utf-8')) #butun config göster
# arduino.write(bytes("v",  'utf-8')) #butun config göster
# arduino.write(bytes("asd",  'utf-8')) #butun config göster
print(f"arduino.write uzunluk: {write_sayi}")
time.sleep(1)
# data = arduino.read(5)
# data = arduino.readline()
# data = arduino.readline()[4:]
# print(f"type arduino.readline(): {type(data)}")
# data = arduino.readline().decode('utf_8')
data_read=arduino.readline()
index_suslu_parantez=data_read.index(b"{")
print(f"index_suslu_parantez: {index_suslu_parantez}")
# data = data_read[4:].decode('utf_8')
data = data_read[index_suslu_parantez:].decode('utf_8')
print(f"arduino.readline():{data}, type: {type(data)}")
# arduino.close()