# importing Flask and other modules
from flask import Flask , request , render_template , redirect ,
url_for import redis
 redis_client = redis . Redis ( host =’ 192.168.137.3 ’, port =6379)

 # Flask constructor
 app = Flask ( __name__ , template_folder =’.’)
 global vehicule_number
 global parkingspot
 global kilometrage

 #app = Flask ( __name__ )
 # A decorator used to tell the application
 # which URL is associated function
 @app . route (’/’, methods =["GET ", " POST "])
 def test () :
 if request . method == " POST ":
# getting input with name = fname in HTML form
 vehicule_number = request . form . get (" vehicule -
number_form ")
 # getting input with name = lname in HTML form
kilometrage = request . form . get (" kilometrage_form ")
 parkingspot = request . form . get (’spot ’, False )

 print ("le kilometrage : " + str( kilometrage ) ) # marche
 print ("le numero de vehicule : "+str( vehicule_number ) )
 print ("la place de parking : "+str( parkingspot ) )
 return redirect (’/ valider . html ? kilometrage ={}&
vehicule_number ={}& parkingspot ={} ’. format ( kilometrage ,
vehicule_number , parkingspot ) )

 return render_template (" webapp . html ")


 @app . route (’/ valider . html ’, methods =["GET ", " POST "])
 def valider () :
 print (" Validation ")
 kilometrage = request . args . get (’kilometrage ’)
 vehicule_number = request . args . get (’ vehicule_number ’)
 parkingspot = request . args . get (’parkingspot ’)
 if request . method == " POST ":
 # getting input with name = fname in HTML form
 print (" POST ")
 bon = request . form . get ("bon")
 print ( bon )
 if bon == " true ":
 while True :
 try :
 data = ’{} ,{} ,{} ’. format ( vehicule_number ,
kilometrage , parkingspot )
 rcvd = redis_client . publish (’ parking_data ’
, data )
 print (" Data published successfully ")
 if rcvd >0:
 break
 except redis . ConnectionError :
 pass
 # handle reconnect attempts
 else :
 print ("Non valide ")
return redirect ( url_for (’test ’) )
 return render_template (" valider . html ", hkilometrage =
kilometrage , hvehicule_number = vehicule_number , hparkingspot
= parkingspot )

 if __name__ == ’__main__ ’:
 print (" passe ")
 app . run ( host =" 0.0.0.0 ", port =5000 , debug = True )
