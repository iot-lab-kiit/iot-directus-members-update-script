import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from drive import Drive
from fix import image_ids


def make_date(d):
    return datetime.strptime(d, '%m/%d/%y')


df = pd.read_excel('IoT Lab Data.xlsx', sheet_name='Sheet1')


URL = 'http://13.232.181.16'
TOKEN = 'AJyRPfsNhrq66N0q8PD2FpYdlGuh7lvT'

# response = requests.get(URL + '/items/teams',
#                         auth=HTTPBasicAuth('admin@iot.in', 'iitk@#'))

gdrive = Drive()
id_index = -1

for member in df.itertuples():
    id_index += 1
    try:
        gid = image_ids[id_index]
        gdrive.download(gid, str(member.roll) + '.jpeg')
        img_name = str(member.roll) + '.jpeg'
        avatar_file = open(img_name, 'rb')
        files = [('file', (img_name, avatar_file, 'image/jpeg'))]
        response = requests.request("POST", URL + '/files', files=files)      
        image_data = response.json()
        image_id = image_data['data']['id']
        print(image_id)
        data = {
            'id': member.roll,
            'status': 'published',
            'name': member.name,
            'email': member.email,
            'phone_number': member.phone_number,
            'whatsapp_number': member.whatsapp_number,
            'year': member.year,
            'domain': member.domain,
            'dob': str(member.dob),
            'branch': member.branch,
            'position': member.position,
            'about': member.about,
            'linkedin': member.linkedIn,
            'github': member.github,
            'avatar': image_id
        }

        response = requests.post(URL + '/items/teams', json=data)
        print(str(member.roll), ' -> ', response)
        # print(response.json())
    except:
        with open('error.txt', 'a') as f:
            f.write(str(member) + '\n\n')
    with open('success.txt', 'a') as f:
        f.write(str(member) + '\n')

