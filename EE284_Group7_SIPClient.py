'''
EE284 VoIP Networks
Project1: SIP_Client Code
Authors :	Prakhar Pandit	(SID:010714795)
			Ronak Borad		(SID:010752170)
			Hardik Patel	(SID:010744968)
Info    : This program acts as a SIP client.
Features: 	1. Register
			2. Call to any URI
			3. Unregister
'''

#Adding required libraries. 

import pjsua as sip
import sys
import time

def log_cb(level, str, len):
	print(str),

#Creating Instance for AccountCallback

class AccountCallbackInstace(sip.AccountCallback):
	
	def __init__ (self,account):
		sip.AccountCallback.__init__(self, account)

#Class to call at a given URI

class SRCallCallback(sip.CallCallback):

    def __init__(self, call):
        sip.CallCallback.__init__(self, call)
 
    def on_state(self):
        print("Call is :", self.call.info().state_text),
        print("last code :", self.call.info().last_code),
        print("(" + self.call.info().last_reason + ")")
        
        #return if call is disconnected

        if (self.call.info().state_text == 'DISCONNCTD'):
        	print 'Press anykey to Unregister.....'
        	return

	
try:

	#Creating instance and Initializing SIP library...

	sip_lib = sip.Lib()
	sip_lib.init(log_cfg = sip.LogConfig(level=3, callback=log_cb))

	#creating Transport Object Instance...

	client_IP = raw_input('Enter Client IP address :')

	transpot_socket = sip.TransportConfig()
	transpot_socket.port = 5060
	transpot_socket.bound_addr = client_IP
	print('Binding IP ' + client_IP + 'to default port no 5060.....'),
	transport_bind = sip_lib.create_transport(sip.TransportType.UDP,transpot_socket)
	
	print('OK')

	#Starting SIP libraries

	sip_lib.start()
	sip_lib.set_null_snd_dev()

	#Starting Registering Process

	r_IP=raw_input("Enter IP address of the Server: ")
	r_name=raw_input("Enter Username: ")
	r_pwd=raw_input("Enter Password: ")
	print 'Setting same display name as user name.....'
	r_Dname=r_name

	print 'Staring Registration.....'
	account_conf = sip.AccountConfig(domain = r_IP, username = r_name, password =r_pwd, display = r_Dname, proxy = 'sip:%s:5060' % r_IP)
	account_conf.id ="sip:%s" % (r_name)
	account_conf.reg_uri ='sip:%s:%s' % (r_IP,transpot_socket.port)
	account_callback = AccountCallbackInstace(account_conf)
	acc = sip_lib.create_account(account_conf,cb=account_callback)

	#Setting value to Accountcallback class

	acc.set_callback(account_callback)
	print('Status= ',acc.info().reg_status,'(' + acc.info().reg_reason + ')')
	time.sleep(5)
	print 'Registration is Complete....'

	#Calling
	
	c_ID = raw_input('Enter UID to make call : ')
	print 'Calling %s.....' % (c_ID)
	s_URI = 'sip:%s@%s:%s' % (c_ID,r_IP,transpot_socket.port)
	call = acc.make_call(s_URI, SRCallCallback(acc))

	#Destroying instance and unregistering
	
	
	input = sys.stdin.readline().rstrip('\r\n')
	print 'Unregistering.....'
	time.sleep(2)
	sip_lib.destroy()
	time.sleep(2)
	sip_lib= None
	sys.exit(1)

#Handling Execption

except sip.Error, err:
	print 'Initializations Error', err
	sip_lib.destroy()