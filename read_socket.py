import select, socket 

port = 2805  # where do you expect to get a msg?
liste = []

max_liste = 512

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.bind(('<broadcast>', port))
s.bind(("", port))

#def addpacket(value):
#  global liste
#  liste.insert(0,[value[1],value[2],value[3],value[8],value[4],value[5]])
#  for index, item in enumerate(liste):
#    if value[1] == item[0]:
#      #print index, item
#      i = index
#  print i
#  if i > (max_liste-1):
#    liste.pop(i)
#  return 0

def readSocket():
  packet = s.recv(80)
  #print packet
  getrennt = packet.split(',')
  if getrennt[0] == "$PISE" and getrennt[10] == "00.0*ff\n":
    print "Vehicle: "+getrennt[1]+", Latitude: "+getrennt[2]+", Longtitude: "+getrennt[3]+", Yaw: "+getrennt[8]+", Date: "+getrennt[4]+", Time: "+getrennt[5]
    #addpacket(getrennt)
    return getrennt
  else:
    print "paket corrupted"
    return 0
 
if __name__ == "__main__" :                                                                                                                                                
  while True:                                                                                                                                                              
    readSocket()
