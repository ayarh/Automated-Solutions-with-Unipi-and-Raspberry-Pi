import redis
 import logging
 from jsonrpclib import Server
 from time import sleep
 s = Server (" http ://192.168.137.3/ rpc")
 redis_client = redis . Redis ()

 global estdemarre
 global aru
 global DI # DigitalInputs inputs de 4 a 12. {0 ,1 ,2 ,3} existent mais ne sont pas utiles dans cette liste
 DI =[]
 DI = [0 for i in range (13) ]
 estdemarre = 0
 global vehicule_number
 global kilometrage
 global parkingspot


 ## Connecting to the database

 ## importing ’mysql . connector ’ as mysql for convenient
 import mysql . connector as mysql

 ## connecting to the database using ’connect () ’ method
 ## it takes 3 required parameters ’host ’, ’user ’, ’passwd ’
 db = mysql . connect (
 host = " localhost ",
 user = " userex ",
 passwd = "mdp ",
 database =" Test "
 )
 cursor = db . cursor ()

 # configure logging
 logging . basicConfig (
 format =’%( asctime )s %( levelname )s: %( message )s’,
 datefmt =’%Y -%m -%d %H:%M:%S’,
level = logging . INFO
 )
 def NoARU () : # verifie si il y a des arrets d’urgences
 arug = s . input_get_value (1) # arret urgence
 au1 = s . input_get_value (2) # arret urgence compresseur 1
 au2 = s . input_get_value (3) # arret urgence compresseur 2
 return not ( arug and au1 and au2 )

 def Inpulsion ( numero , duree ) : # Cree une inuplsion au relai avec son numero et sa duree
 s . relay_set ( numero ,1)
 sleep ( duree )
 s . relay_set ( numero ,0)

 def RoutineDemarrage () : # routine de demarrage descompresseurs
 global aru
global estdemarre
if aru := NoARU () :
 sleep (5)
 Inpulsion (1 ,1) # inpulsion de demarrage du
compresseur 1
 sleep (15)
 Inpulsion (2 ,1)# inpulsion de demarrage du
compresseur 2
 estdemarre = 1

 def RoutineExtinxion () : # Routine d’extinxion des compresseurs
global estdemarre
 Inpulsion (3 ,1) # inpulsion d’extinxion du compresseur 1
 sleep (1)
 Inpulsion (4 ,1) # inpulsion d’extinxion du compresseur 1
 estdemarre = 0

 def ReadInputs () : # Lis les DI non ARU
 global DI
 for i in range (4 ,13) : #[de 4 a 12]
 DI [ i ] = s . input_get_value ( i )

 def process_message ( message ) :
 logging . info (’Received new message from Redis queue ’)
 data = message . decode (’utf -8 ’)
 vehicule_number , kilometrage , parkingspot = data . split (’,’)
cursor . execute ( f’INSERT INTO infos (km ,Nplace , Nvehicule )
VALUES ({ kilometrage } ,{ parkingspot } ,{ vehicule_number });’)
db . commit ()
try:
s . relay_set (int( parkingspot ) , 1)
logging . info ( f" Relay { parkingspot } turned on")
except Exception as e :
logging . error ( f" Error turning on relay { parkingspot}: {e}")
pubsub = redis_client . pubsub ()
pubsub . subscribe (’ parking_data ’)
while True :
try:
message = pubsub . get_message ()
except redis . ConnectionError :
 # Do reconnection attempts here such as sleeping and retrying
 pubsub = redis . pubsub ()
 pubsub . subscribe (’ parking_data ’)
if message :
 print ( message )
 print ( type ( message ) )
 if message [’type ’]== ’message ’: ## verifie si le message est bien un message
process_message ( message [’data ’])
 # do something withthe message
 else :
 print ("pas de message ")
 sleep (0.05) # be nice to the system :)
db . close ()
