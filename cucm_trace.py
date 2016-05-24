#!/usr/bin/env python
import ssl
import sys
import xml
from SOAPpy import WSDL
from base64 import b64encode
print sys.version

from M2Crypto import SSL, httpslib

context = SSL.Context("sslv3")

# Disable certificate checking
context.set_verify(0, depth = 0)

connection = httpslib.HTTPSConnection("10.66.90.65", 8443, ssl_context=context)


# Hack (!!!) for disabling host name check <CN> == <expected host name>.
# Will affect any future SSL connections made by M2Crypto!
SSL.Connection.postConnectionCheck = None

userAndPass = b64encode(b"a:a").decode("ascii")
headers = { 'Authorization' : 'Basic %s' %  userAndPass }
connection.request('GET', '/realtimeservice', headers=headers)
res = connection.getresponse()
data = res.read()
print data

#wsdlFile = 'https://10.66.90.65:8443/logcollectionservice2/services/LogCollectionPortTypeService?wsdl'
wsdlFile = 'https://10.66.90.65:8443/realtimeservice2/services/RISService70??wsdl'
server = WSDL.Proxy(wsdlFile)
server.config.dumpSOAPOut = 1
server.config.dumpSOAPIn = 1
print server.methods.keys()
