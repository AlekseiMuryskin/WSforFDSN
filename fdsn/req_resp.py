import requests

param={
    'startdate':'2022-02-01',
    'starttime':'00:00',
    'enddate':'2022-02-01',
    'endtime':'00:07',
    'network':'II',
    'station':'ARTI',
    'location':'00',
    'channel':'BHZ',
    'format':'miniseed'
}

resp = requests.post("http://127.0.0.1:8000/dataselect/", data=param)

with open('resp.msd','wb') as f:
    f.write(resp.content)


