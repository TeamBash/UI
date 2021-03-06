from django.shortcuts import render,render_to_response,redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
import httplib2
import httplib
import urllib
import urllib2
import json
import copy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

#for keeping track of the user
userid=None


stationCodeDict = {'Aberdeen, SD ': 'KVBX', 'Tulsa, OK': 'KSGF', 'Milwaukee, WI': 'KAMX',
                       'Columbus AFB, MS': 'KCLE', 'Rapid City, SD': 'KGYX',
                       'El Paso, TX': 'KDYX', 'Bismarck, ND': 'KBMX', 'Caribou, ME': 'KCXX', 'Sioux Falls, SD': 'KNKX',
                       'Paducah, KY': 'KLNX', 'San Joaquin Valley, CA': 'KDAX', 'Amarillo, TX': 'KAMA',
                       'Tallahassee, FL': 'PHKI',
                       'Duluth, MN': 'KDDC', 'Dyess AFB, TX': 'KDOX', 'Atlanta, GA': 'KFFC', 'Maxwell AFB, AL': 'KLVX',
                       'Biorka Island/Sitka, AK': 'KBGM', 'Great Falls, MT': 'KMVX', 'Kansas City, MO': 'KJKL',
                       'Brownsville, TX': 'KFCX',
                       'Wakefield, VA': 'KCCX', 'Montague/Ft Drum, NY': 'KMPX', 'Hastings, NE': 'KTFX',
                       'Salt Lake City, UT': 'KRAX',
                       'Omaha, NE': 'FAA', 'Jackson, KY': 'KHGX', 'Northwest Florida/Eglin AFB, FL': 'KLIX',
                       'Spokane, WA': 'FAA',
                       'Dodge City, KS': 'KDMX', 'Tampa Bay, FL': 'FAA', 'North Platte, NE': 'KMHX',
                       'Albuquerque, NM': 'KVBX',
                       'Ft Worth, TX': 'KFDR', 'Grand Junction, CO': 'KGGW', 'Houston, TX': 'KGSP',
                       'Medford, OR': 'KLBB',
                       'Sterling, VA': 'KFSD', 'Shreveport, LA': 'KEWX', 'Marquette, MI': 'KVTX',
                       'Oklahoma City, OK': 'PAEC',
                       'Bethel, AK': 'PABC', 'Pocatello, ID': 'KPAH', 'Charleston, WV': 'KICX', 'Des Moines IA': 'KCRP',
                       'Blacksburg, VA': 'KBIS', 'Goodland, KS': 'KFWS', 'Eureka, CA': 'KEYX', 'Columbia, SC': 'KILN',
                       'Kamuela/Kohala, HI': 'KIND', 'Greer, SC': 'KGRR', 'Cannon AFB, NM': 'KBUF',
                       'Pendleton, OR': 'KIWX',
                       'Mobile, AL': 'KMAF', 'Corpus Christi, TX': 'KCAE', 'Boston, MA': 'NWS', 'Billings, MT': 'FAA',
                       'Holloman AFB, NM': 'KGRB', 'Laughlin AFB, TX': 'KARX', 'Cincinnati/Wilmington, OH': 'KCYS',
                       'Memphis, TN': 'KMXX',
                       'Northern Indiana/North Webster, IN': 'KOHX', 'State College, PA': 'KSHV', 'Molokai, HI': 'KMKX',
                       'Andersen AFB, Guam': 'PGUA', 'Fairbanks/Pedro Dome, AK': 'KBHX', 'Melbourne, FL': 'KMQT',
                       'Cedar City, UT': 'KFDX', 'Lincoln, IL': 'KLCH', 'San Juan, PR': 'KMTX',
                       'Birmingham, AL': 'PACG',
                       'Jackson, MS': 'KHTX', 'Little Rock, AR': 'KESX', 'Minot AFB, ND': 'FAA', 'Detroit, MI': 'KFTG',
                       'Seattle, WA': 'NWS', 'Flagstaff, AZ': 'KVWX', 'Ft Rucker, AL': 'KSRX', 'Wilmington, NC': 'KTLH',
                       'La Crosse, WI': 'KBYX', 'Topeka, KS': 'PHWA', 'Indianapolis, IN': 'KHDX',
                       'Sacramento, CA': 'KDVN',
                       'San Diego, CA': 'KJGX', 'Pittsburgh, PA': 'KOAX', 'San Antonio, TX': 'KRIW',
                       'Evansville, IN': 'KEPZ',
                       'Wichita, KS': 'KLWX', 'Gaylord, MI': 'KHPX', 'Raleigh/Durham, NC': 'KSFX',
                       'Green Bay, WI': 'KGJX',
                       'King Salmon, AK': 'PHKM', 'Anchorage/Kenai, AK': 'PAHG', 'Philadelphia, PA': 'KEVX',
                       'Louisville, KY': 'KILX',
                       'Santa Ana Mountains, CA': 'KSJT', 'Phoenix, AZ': 'KTLX', 'Key West, FL': 'KDGX',
                       'Portland, OR': 'KDIX',
                       'Buffalo, NY': 'KBOX', 'Cheyenne, WY': 'KCLX', 'Lake Charles, LA': 'PAKC',
                       'Burlington, VT': 'KBRO',
                       'Cleveland, OH': 'KLOT', 'Midland/Odessa, TX': 'KNQA', 'Glasgow, MT': 'KEOX',
                       'Tucson, AZ': 'KOTX',
                       'Nome, AK': 'KVAX', 'Dover AFB, DE': 'KDTX', 'Moody AFB, GA': 'KMBX', 'St Louis, MO': 'KATX',
                       'Springfield, MO': 'KSOX', 'Lubbock, TX': 'KLZK', 'San Angelo, TX': 'KUDX', 'Albany, NY': 'KENX',
                       'Ft Campbell, KY': 'KFSX', 'Minneapolis, MN': 'PAIH', 'South Kauai, HI': 'KHNX',
                       'Las Vegas, NV': 'KMRX',
                       'Yuma, AZ': 'KTBW', 'Binghamton, NY': 'KBLX', 'Knoxville/Morristown, TN': 'KEAX',
                       'Frederick/Altus AFB, OK': 'FAA',
                       'Los Angeles, CA': 'KDFX', 'Middleton Island, AK': 'KMLB', 'Grand Rapids, MI': 'KGLD',
                       'Robins AFB, GA': 'KPUX',
                       'Nashville, TN': 'PHMO', 'Miami, FL': 'KMAX', 'New Orleans, LA': 'KTYX',
                       'Vandenberg AFB, CA': 'KLSX',
                       'Morehead City, NC': 'KMOB', 'Fort Smith, AR': 'PAPD', 'Riverton, WY': 'KRTX',
                       'Denver, CO': 'KGWX',
                       'Edwards AFB, CA': 'KDLH', 'Pueblo, CO': 'KIWA', 'Quad Cities/Davenport, IA': 'KPBZ',
                       'Charleston, SC': 'KCBW',
                       'Chicago, IL': 'KRLX', 'Portland, ME': 'KPDT', 'South Shore, HI': 'TJUA',
                       'Huntsville/Hytop, AL': 'KUEX',
                       'Beale AFB, CA': 'KBBX', 'Grand Forks, ND': 'KAPX'}

stationList1 = ['Albany, NY', 'Albuquerque, NM', 'Amarillo, TX', 'Anchorage/Kenai, AK', 'Andersen AFB, Guam',
                'Atlanta, GA', 'Beale AFB, CA', 'Bethel, AK', 'Billings, MT', 'Binghamton, NY',
                'Biorka Island/Sitka, AK', 'Birmingham, AL', 'Bismarck, ND', 'Blacksburg, VA', 'Boston, MA',
                'Brownsville, TX', 'Buffalo, NY', 'Burlington, VT', 'Cannon AFB, NM', 'Caribou, ME', 'Cedar City, UT',
                'Charleston, SC', 'Charleston, WV', 'Cheyenne, WY', 'Chicago, IL', 'Cincinnati/Wilmington, OH',
                'Cleveland, OH', 'Columbia, SC', 'Columbus AFB, MS', 'Corpus Christi, TX', 'Denver, CO',
                'Des Moines IA', 'Detroit, MI', 'Dodge City, KS', 'Dover AFB, DE', 'Duluth, MN', 'Dyess AFB, TX',
                'Edwards AFB, CA', 'El Paso, TX', 'Eureka, CA', 'Evansville, IN', 'Fairbanks/Pedro Dome, AK',
                'Flagstaff, AZ', 'Fort Smith, AR', 'Frederick/Altus AFB, OK', 'Ft Campbell, KY', 'Ft Rucker, AL',
                'Ft Worth, TX', 'Gaylord, MI', 'Glasgow, MT', 'Goodland, KS', 'Grand Forks, ND', 'Grand Junction, CO',
                'Grand Rapids, MI', 'Great Falls, MT', 'Green Bay, WI', 'Greer, SC', 'Hastings, NE', 'Holloman AFB, NM',
                'Houston, TX', 'Huntsville/Hytop, AL', 'Indianapolis, IN', 'Jackson, KY', 'Jackson, MS',
                'Kamuela/Kohala, HI', 'Kansas City, MO', 'Key West, FL', 'King Salmon, AK', 'Knoxville/Morristown, TN',
                'La Crosse, WI', 'Lake Charles, LA', 'Las Vegas, NV', 'Laughlin AFB, TX', 'Lincoln, IL',
                'Little Rock, AR', 'Los Angeles, CA', 'Louisville, KY', 'Lubbock, TX', 'Marquette, MI',
                'Maxwell AFB, AL', 'Medford, OR', 'Melbourne, FL', 'Memphis, TN', 'Miami, FL', 'Middleton Island, AK',
                'Midland/Odessa, TX', 'Milwaukee, WI', 'Minneapolis, MN', 'Minot AFB, ND', 'Mobile, AL', 'Molokai, HI',
                'Montague/Ft Drum, NY', 'Moody AFB, GA', 'Morehead City, NC', 'Nashville, TN', 'New Orleans, LA',
                'Nome, AK', 'North Platte, NE', 'Northern Indiana/North Webster, IN', 'Northwest Florida/Eglin AFB, FL',
                'Oklahoma City, OK', 'Omaha, NE', 'Paducah, KY', 'Pendleton, OR', 'Philadelphia, PA', 'Phoenix, AZ',
                'Pittsburgh, PA', 'Pocatello, ID', 'Portland, ME', 'Portland, OR', 'Pueblo, CO',
                'Quad Cities/Davenport, IA', 'Raleigh/Durham, NC', 'Rapid City, SD', 'Riverton, WY', 'Robins AFB, GA',
                'Sacramento, CA', 'Salt Lake City, UT', 'San Angelo, TX', 'San Antonio, TX', 'San Diego, CA',
                'San Joaquin Valley, CA', 'San Juan, PR', 'Santa Ana Mountains, CA', 'Seattle, WA', 'Shreveport, LA',
                'Sioux Falls, SD', 'South Kauai, HI', 'South Shore, HI', 'Spokane, WA', 'Springfield, MO',
                'St Louis, MO', 'State College, PA', 'Sterling, VA', 'Tallahassee, FL', 'Tampa Bay, FL', 'Topeka, KS',
                'Tucson, AZ', 'Tulsa, OK', 'Vandenberg AFB, CA', 'Wakefield, VA', 'Wichita, KS', 'Wilmington, NC',
                'Yuma, AZ']
stationList = ['KABR', 'KENX', 'KABX', 'KAMA', 'PAHG', 'PGUA', 'KFFC', 'KBBX', 'PABC', 'FAA', 'KBLX', 'KBGM', 'PACG',
               'KBMX', 'KBIS',
               'NWS', 'KFCX', 'KBOX', 'KBRO', 'KBUF', 'KCXX', 'KFDX', 'KCBW', 'KICX', 'KCLX', 'KRLX', 'KCYS', 'KLOT',
               'KILN',
               'KCLE', 'KCAE', 'KGWX', 'KCRP', 'KFTG', 'KDMX', 'KDTX', 'KDDC', 'KDOX', 'KDLH', 'KDYX', 'KEYX', 'KEPZ',
               'KBHX',
               'KVWX', 'PAPD', 'FAA', 'KFSX', 'KSRX', 'KFDR', 'KHPX', 'KEOX', 'KFWS', 'KAPX', 'KGGW', 'KGLD', 'KMVX',
               'KGJX',
               'KGRR', 'KTFX', 'KGRB', 'KGSP', 'KUEX', 'KHDX', 'KHGX', 'KHTX', 'KIND', 'KJKL', 'KDGX', 'PHKM', 'KEAX',
               'KBYX',
               'PAKC', 'KMRX', 'KARX', 'KLCH', 'KESX', 'KDFX', 'KILX', 'KLZK', 'KVTX', 'KLVX', 'KLBB', 'KMQT', 'KMXX',
               'KMAX',
               'KMLB', 'KNQA', 'KAMX', 'PAIH', 'FAA', 'KMAF', 'KMKX', 'KMPX', 'KMBX', 'KMOB', 'PHMO', 'KTYX', 'KVAX',
               'KMHX',
               'KOHX', 'KLIX', 'PAEC', 'FAA', 'KLNX', 'KIWX', 'KEVX', 'KTLX', 'KOAX', 'KPAH', 'KPDT', 'KDIX', 'KIWA',
               'KPBZ',
               'KSFX', 'KGYX', 'KRTX', 'KPUX', 'KDVN', 'KRAX', 'KUDX', 'KRIW', 'KJGX', 'KDAX', 'KMTX', 'KSJT', 'NWS',
               'KEWX',
               'KNKX', 'KHNX', 'TJUA', 'FAA', 'KSOX', 'KATX', 'KSHV', 'KFSD', 'PHKI', 'FAA', 'PHWA', 'KOTX', 'KSGF',
               'KLSX',
               'KCCX', 'KLWX', 'KTLH', 'KTBW', 'KTWX', 'KEMX', 'KINX', 'KVBX', 'KAKQ', 'KICT', 'KLTX', 'KYUX']


def login(request):
    context = RequestContext(request, {'request': request, 'user': request.user})
    return render_to_response('Login/login.html', context_instance=context)

def start_here(request):
    return render_to_response('SampleWeb/home.html', context_instance={})

def home(request):
    context = RequestContext(request, {'request': request, 'user': request.user})
    return render_to_response('Login/weatherForm.html',context_instance=context)

def disconnect(request):
    logout(request)

def logout(request):
    auth_logout(request)
    return redirect('/')

def login(request) :
    return render(request, 'Login/login.html', {})

def setUid(uid):
    print("SET IS ALREADY TAKEN")
    global userid
    userid = uid

def getUid():
    return userid

def loginAPI(request):
    print("I am scre")
    h = httplib2.Http()
    context = {
        "useremail" : str(request.user.email),
    }
    resp, content = h.request(
        uri='http://52.25.123.69:8888/createUser',
        method='POST',
        headers={'Content-Type': 'application/json; charset=UTF-8'},
        body=json.dumps(request.user.email),
    )
    if resp['status'] == '401':
        return render(request, 'Login/401.html', {})
    #userid = content
    setUid(content)

    return redirect('Login:weatherForm')
    #return weatherForm(request)

def weatherForm(request, context={}):
    global userid

    if not userid:
        return redirect('start_here')
    print("sdfsfsfdsdf")

    day =[]
    for i in range(1,31):
        if i<10:
            day.append('0'+str(i))
        else:
            day.append(str(i))
    h = httplib2.Http()
    #context{
    #    "useremail": str(request.user.email),
    #}
    resp, content = h.request(
        # uri='http://52.25.123.69:8888/loginUser',
        uri='http://52.25.123.69:8888/createUser',
        method='POST',
        headers={'Content-Type': 'application/json; charset=UTF-8'},
        body=json.dumps(request.user.email),
    )
    if resp['status'] == '401':
        return render(request, 'Login/401.html', {})

    context.update({'year' : range(1991,2017), 'day':day , 'station':stationList1})
    return render(request, 'Login/weatherForm.html', context=context)


def hit(request):
    global userid
    h = httplib2.Http()
    context = {
        "useremail": str(request.user.email),
    }
    resp, content = h.request(
        # uri='http://52.25.123.69:8888/loginUser',
        uri='http://52.25.123.69:8888/createUser',
        method='POST',
        headers={'Content-Type': 'application/json; charset=UTF-8'},
        body=json.dumps(request.user.email),
    )
    if resp['status'] == '401':
        return render(request, 'Login/401.html', {})
    userid = content
    print("FALSEI"*10,userid)
    day=[]
    for i in range(1, 31):
        if i < 10:
            day.append('0' + str(i))
        else:
            day.append(str(i))
    stationCode =''
    if request.method == 'POST':
        print(request.POST)
        for key in stationCodeDict.keys():
            if  str(request.POST['station']) in key:
                stationCode = stationCodeDict[key]
                break
        h = httplib2.Http()
        print("about to request")
        response, content= h.request("http://52.25.123.69:8888/dataIngestor/"+str(userid)+"/"+str(request.POST['year'])+'/'+str(request.POST['month'])+'/'+str(request.POST['day'])+'/'+stationCode+'/')
        print(response)
        if content == 'false':
            return render(request, 'Login/falseForecast.html')
        elif response['status']=='206':
            return render(request, 'Login/206.html')
        elif response['status']=='404':
            return render(request, 'Login/404.html')
        elif response['status'] == '500':
            return render(request, 'Login/500.html')
        else:
            #return render(request, 'Login/weatherForm.html', context={'picture' : response})
            return render(request, 'Login/weatherForm.html', context = {'year' : range(1991,2017), 'day':day , 'station':stationList1, "content":"Job Created!!!", 'show_button':True})
            #return redirect('weatherForm')
            #return HttpResponseRedirect(reverse('Login:weatherForm', args=(userid,)))
def result(request):
    if '404' in request.body:
        return render(request, 'Login/404.html',)
    else:
        return render(request, 'Login/Result.html' )

def getStats(request):
    #body = urllib.urlencode(context)
    h = httplib2.Http()
    #context = {'content': {'jobname': []} }

    resp, content = h.request("http://52.25.123.69:8888/registry/displayData/"+str(userid), method="GET")
    content= {'weather_data':json.loads(content), 'hello':'world'}
    return render(request, 'Login/stats.html', context=content)

def getJob(request):
    class Task:
        def __init__(self):
            self.tasks = [] # list of tuples, tuple[0] is status, tuple[1] is a list of urls
            self.job_name = None


    h = httplib2.Http()
    task_objects = []

    response, content = h.request("http://52.25.123.69:8888/jobsapi/getJobDetails/"+str(userid), method="GET")
    loaded = json.loads(content)
    for dic in loaded:
        task = Task()
        task.job_name = dic['jobName']
        list_dics = dic['taskResultsBeans']
        for result_dic in list_dics:
            task.tasks.append((result_dic['scheduleStatus'], result_dic['imageUrls']))
        task_objects.append(task)

    content = {'tasks': task_objects, 'hello': 'world'}

    return render(request, 'Login/jobDetails.html', context=content)

def restart(request):
    h = httplib2.Http()
    #print("REACHESresp")
    # context = {'content': {'jobname': []} }
    if request.method == 'GET':
        job_name = request.GET['job_name']
        #request.POST = {'job_name': job_name}
        request.GET = {}
        print("REACHESresp",job_name)
        print("http://52.25.123.69:8888/jobsapi/restartJob/"+str(userid)+"/")
        #resp, content = h.request("http://52.25.123.69:8888/jobsapi/restartJob/"+str(userid)+"/", method="POST")
        resp, content = h.request("http://52.25.123.69:8888/jobsapi/restartJob/" + str(userid) + "/"+job_name+"/", method="GET")
    print(resp)
    return redirect('Login:getJob')