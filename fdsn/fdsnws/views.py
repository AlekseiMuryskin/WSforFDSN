from django.shortcuts import render
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from django.http import HttpResponse
import os, sys
import zipfile



def GetFileName(st,format):
    filename = "GSRAS_"
    filename=filename+str(st[0].stats['network'])+"_"
    filename=filename+str(st[0].stats['station'])
    if 'css' not in format:
        filename=filename+".msd"
    return filename

def ListFilterW(lst):
    lst2=[]
    for i in lst:
        if ".w" in i:
            lst2.append(i)
    return lst2
# Create your views here.

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True




def main_page(request):
    return render(request,'fdsnws/main_page.html',{})

def dataselect(request):
    if request.method =="POST":
        try:
            client = Client("http://172.20.1.37:8090")
            t = UTCDateTime("2022-02-01T00:00:00")
            starttime = request.POST['starttime']
            endtime = request.POST['endtime']
            startdate = request.POST['startdate']
            enddate = request.POST['enddate']
            starttime = UTCDateTime(startdate + "T" + starttime)
            endtime = UTCDateTime(enddate + "T" + endtime)
            if len(request.POST['network'])>0:
                net = request.POST['network']
            else:
                net="*"
            if len(request.POST['station']) > 0:
                sta = request.POST['station']
            else:
                sta = "*"
            if len(request.POST['location']) > 0:
                loc = request.POST['location']
            else:
                loc = "*"
            if len(request.POST['channel']) > 0:
                ch = request.POST['channel']
            else:
                ch = "*"

            nodata = request.POST['nodata']
            st = client.get_waveforms(net, sta, loc, ch, starttime, endtime,attach_response=True)
            FName=GetFileName(st,request.POST['format'])
            st.write(FName,format="MSEED")


            if 'css3'in request.POST['format']:
                if 'win' in sys.platform:
                    os.system("wavetapc -d=w {}".format(FName))
                else:
                    os.system("./waveTapc -d=w {}".format(FName))

                flist=ListFilterW(os.listdir())
                with zipfile.ZipFile('{}.zip'.format(FName), 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for obj in flist:
                        zipf.write(obj)

                response = HttpResponse(open(FName+".zip",'rb'))
                response['Content-Type'] = 'application/zip'
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(FName+".zip")
                for obj in flist:
                    os.remove(obj)
                os.remove(FName+".zip")
            else:
                response = HttpResponse(open(FName,'rb'))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(FName)

            os.remove(FName)
            return response
        except:
            return render(request,'fdsnws/error.html',{"message":"Error! введите корректные данные"})
    return render(request,'fdsnws/dataselect.html',{})

def station(request):
    if request.method == "POST":
        try:
            try:
                startdate = UTCDateTime(request.POST['startdate'])
                enddate = UTCDateTime(request.POST['enddate'])
            except:
                startdate=UTCDateTime(2000,1,1)
                enddate=UTCDateTime().now()

            if len(request.POST['network']) > 0:
                net = request.POST['network']
            else:
                net = "*"
            if len(request.POST['station']) > 0:
                sta = request.POST['station']
            else:
                sta = "*"
            if len(request.POST['location']) > 0:
                loc = request.POST['location']
            else:
                loc = "*"
            if len(request.POST['channel']) > 0:
                ch = request.POST['channel']
            else:
                ch = "*"
            loc1=request.POST['location1']
            if 'box' in loc1:
                minlat=request.POST['minlatitude']
                maxlat = request.POST['maxlatitude']
                minlon = request.POST['minlongitude']
                maxlon = request.POST['maxlongitude']
            elif 'cir' in loc1:
                lat=request.POST['latitude']
                lon=request.POST['longitude']
                minrad=request.POST['minradius']
                maxrad=request.POST['maxradius']
            else:
                pass
            form=request.POST['format']
            nodata = request.POST['nodata']
            level=request.POST['level']

            client = Client("http://172.20.1.37:8090")


            inv=client.get_stations(network=net,station=sta,location=loc,channel=ch,starttime=startdate,endtime=enddate,level=level)

            if 'box' in loc1:
                inv=client.get_stations(network=net,station=sta,location=loc,channel=ch,starttime=startdate,endtime=enddate,level=level, minlatitude=minlat,maxlatitude=maxlat,
                                        minlongitude=minlon,maxlongitude=maxlon)

            if 'cir' in loc1:
                inv=client.get_stations(network=net,station=sta,location=loc,channel=ch,starttime=startdate,endtime=enddate,level=level,
                                        longitude=lon,latitude=lat,minradius=minrad,maxradius=maxrad)


            inv.write("GSRAS_inv.xml",format="STATIONXML")
            response = HttpResponse(open("GSRAS_inv.xml","r",encoding="utf-8"))
            if "XML" in form:
                response['Content-Type'] = 'text/xml'
            else:
                response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename="GSRAS_inv.xml"'
            os.remove("GSRAS_inv.xml")
            return response
        except:
            return render(request, 'fdsnws/error.html', {"message": "Error! введите корректные данные"})

    return render(request,'fdsnws/station.html',{})





