import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep

class enviarMail:
	
	ano="2024"
	subject = "Factura cota " + ano
	corpoMsg ='''Anexo acompañamos a factura da túa cota de Entidade deste ano.\n
Se o pago é por PayPal verás que o vencemento está indicado segundo o\n
teu plan de PayPal.\n
Unha aperta\n
--\n
Nome emisario <email@emisario.com>'''
	emisor_email = "email@emisario.com"
	receptor_email = "recepctor@receptor.com"
	password = "contrasinaldoemailemisor"
	fiche_PDF ="factura_.pdf" 
	#input("Type your password and press enter:")

	# Create a multipart message and set headers
	message = MIMEMultipart()
	def __init__():
		
		
	def __init__(self,emaildestino,ficheiro):
		self.message = MIMEMultipart()
		self.receptor_email=emaildestino
		self.fiche_PDF=ficheiro
		self.message["From"] = self.emisor_email
		self.message["To"] = self.receptor_email
		self.message["Subject"] = self.subject
		self.message["Bcc"] = self.receptor_email  # Recommended for mass emails
		# Add body to email
		self.message.attach(MIMEText(self.corpoMsg, "plain"))
	
	
	def enviar(self):
		# Open PDF file in binary mode
	
		with open(self.fiche_PDF, "rb") as attachment:
			# Add file as application/octet-stream
			# Email client can usually download this automatically as attachment
			part = MIMEBase("application", "octet-stream")
			
			part.set_payload(attachment.read())
			
			
			# Encode file in ASCII characters to send by email    
			encoders.encode_base64(part)

		# Add header as key/value pair to attachment part
			part.add_header(
							"Content-Disposition",
							f"attachment; filename= {self.fiche_PDF}",
							)

		# Add attachment to message and convert message to string
		self.message.attach(part)
		textoMsg = self.message.as_string()
	
		# Log in to server using secure context and send email
		context = ssl.create_default_context()
		
		with smtplib.SMTP_SSL("servidorsmtp.org", 465, context=context) as server:
			server.login(self.emisor_email,self.password)
			server.sendmail(self.emisor_email,self.receptor_email, textoMsg)
			#print("envio a: "+ self.receptor_email +" de parte de: "+ self.emisor_email + " co texto: [" +textoMsg +"]")
			sleep(2)

#***************************************************************************************************************


class leerFactEmail:
	nomeFicheiro =""
	lista=[]
	numsocios=0
	correo=""
	factura=""
	PDFS=[]
	
	def __init__(self):
		print("Objecto sen parametros")
		self.nomeFicheiro="fact_email.txt"
	
	def __init__(self,fiche,lista):
		self.nomeFicheiro=fiche
		self.PDFS=lista
		print("Parametro enviado :"+ fiche)
	
	def leer(self):
		
		if self.nomeFicheiro!="" :
			#leemos arquivo
			with open(self.nomeFicheiro, 'r') as fichero:
				linea = fichero.read()
				self.lista= linea.split("\n")

				#gardamos numero de socios
				self.numsocios=len(self.lista)
		else:
			print("Necesaria ruta a ficheiro de socios")
		
	def enviarCorreo(self):
		print("Iniciando envio")
		
		for i in range(self.numsocios):
			if self.lista[i]!="":
				#print(i , lista[i])
				dim=self.lista[i].split("	")
				self.factura=dim[0]
				self.correo=dim[1]
				fiche_pdf=self.PDFS[i]
				
				e=enviarMail(self.correo,fiche_pdf)
				e.enviar()
				

# ********************************************************************************************************************

class leerPDF:
	ficheiro ="lista.txt "
	lista=[]
	numPDF=0
	correo=""
	factura=""
	PDF=""
	
	def __init__():
		self.ficheiro="Sen_ficheiro.txt"
		print("Sen parametro:")
		
	def __init__(self, fiche):
		self.ficheiro=fiche
		print("Con parametro :"+fiche)

	def leer(self):
		
		#leemos arquivo
		
		with open(self.ficheiro, 'r') as fichero:
			linea = fichero.read()
			self.lista= linea.split("\n")

		#gardamos numero de socios
		self.numPDF=len(self.lista)
		return self.lista
		

#************************************************************************************************************
#leeemos a lista de pdf a enviar
p= leerPDF("lista.txt")
pdfs=p.leer()
#leemos a relacion factura con o emial
soc = leerFactEmail("fact_email.txt",pdfs)
soc.leer()
#enviamos correo a socios
soc.enviarCorreo()








