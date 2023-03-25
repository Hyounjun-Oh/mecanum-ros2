from struct import *
spi_value = [0,0]
trans_value = [50, 100]
val_1 = int(trans_value[0])
val_2 = int(trans_value[1])
i = 0
for value in trans_value:
    spi_value[i] = pack('i',value)
    i +=1
    
print("value {0}, {1}".format(spi_value[0],spi_value[1])) 