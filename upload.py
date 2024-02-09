import requests

# URL = 'http://13.232.181.16'

img_name = str(20051362) + '.jpeg'
# avatar_file = open(img_name, 'rb')
# files = [('file', (img_name, open(img_name, 'rb')))]
# response = requests.request("POST", URL + '/files', files=files)
# print(response.json())


import requests

url = "http://13.232.181.16/files"

files=[
  ('file',(img_name,open('/home/harshraj/IoT Lab KiiT/iot-directus-update/20051362.jpeg','rb'),'image/jpeg'))
]


 = requests.request("POST", url, files=files)

print(response.text)