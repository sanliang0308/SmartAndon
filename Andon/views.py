from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

import requests
import json

QIO = True

# Create your views here.
from django.db.models import Count
from Andon.models import Concern
from Andon.models import NotifyRelationship
from Andon.models import Issue
from Andon.models import Acknowledgement
from Andon.models import SupportPersonnel

def validatePOST(view):
	def wrap(request, *args, **kwargs):
		if request.method != 'POST':
			return HttpResponseRedirect(reverse('Andon:InvaildAccess'))
		else:
			return view(request, *args, **kwargs)
	return wrap

def InvaildAccess(request):
	return HttpResponse('Invaild Access!')

@validatePOST
def sendNotification(request):
	station_id = request.POST['station_id']
	concern_id = request.POST['concern_id']
	concern = Concern.objects.get(id = concern_id)
	recipient_email = []
	recipient_phoneNo = []
	relations = NotifyRelationship.objects.all().filter(concern = concern)
	for relation in relations:
		recipient_email.append(relation.supportPersonnel.email)
		recipient_phoneNo.append(relation.supportPersonnel.phoneNo)
	request.session['ErrMsg'] = None
	try:
		issue = Issue.objects.all().filter(workstation_id = station_id, acked = 0)
		if issue.count() == 0:
			issue = Issue(workstation_id = station_id, concern = concern)
			issue.save()
		timestamp = issue.issue_raised_timestamp
		try:
			sendMail(station_id, recipient_email, concern, timestamp)
		except Exception as e:
			request.session['ErrMsg'] = str(e)
			# return HttpResponse(e)
		try:
			sendSMS(station_id, recipient_email, concern, timestamp)
		except Exception as e:
			request.session['ErrMsg'] = str(e)
			# return HttpResponse(e)
		return HttpResponseRedirect(reverse('Andon:index'))
	except Exception as e:
		request.session['ErrMsg'] = str(e)
		return HttpResponse(e)
	return HttpResponseRedirect(reverse('Andon:index'))

def sendMail(station_id, recipient_email, concern_name, timestamp):
	if QIO:
		url = 'http://10.228.240.51:3000/MMservices/Email'
	else:
		url = 'http://127.0.0.1:3000/MMservices/Email'
	TO = recipient_email
	SUBJECT = '%s Raised on Station ID: %s' % (concern_name, station_id)
	TEXT = '%s Raised on Station ID: %s @ %s' % (concern_name, station_id, timestamp)
	data = {
		"recipient": TO,
		"subject": SUBJECT,
		"body": TEXT
	}
	data_json = json.dumps(data)
	headers = {'Content-type': 'application/json'}
	response = requests.post(url, data = data_json, headers = headers)

def sendSMS(request, station_id, number, concern_name, timestamp):
	if QIO:
		url = 'http://10.228.240.51:3000/MMservices/SMS'
	else:
		url = 'http://127.0.0.1:3000/MMservices/SMS'
	TO = [number]
	SUBJECT = '%s Raised on Station ID: %s @ %s' % (concern_name, station_id, timestamp)
	data = {
		"number": TO,
		"message": SUBJECT
	}
	data_json = json.dumps(data)
	headers = {'Content-type': 'application/json'}
	response = requests.post(url, data = data_json, headers = headers)
	return HttpResponse(response)

def testnotify(request):
	# if QIO:
	# 	url = 'http://10.228.240.51:3000/MMservices/Email'
	# else:
	# 	url = 'http://127.0.0.1:3000/MMservices/Email'
	# TO = ['fenghao@ntu.edu.sg', 'RRERT4.2@gmail.com']
	# SUBJECT = '%s Raised on Station ID: %s' % (1, 2)
	# TEXT = '%s Raised on Station ID: %s @ %s' % (1, 2, 3)
	# data = {
	# 	"recipient": TO,
	# 	"subject": SUBJECT,
	# 	"body": TEXT
	# }
	# data_json = json.dumps(data)
	# headers = {'Content-type': 'application/json'}
	# response = requests.post(url, data = data_json, headers = headers)
	if QIO:
		url = 'http://10.228.240.51:3000/MMservices/SMS'
	else:
		url = 'http://127.0.0.1:3000/MMservices/SMS'
	TO = [96220394, 88766323]
	SUBJECT = '%s Raised on Station ID: %s @ %s' % (1, 2, 3)
	data = {
		"number": TO,
		"message": SUBJECT
	}
	data_json = json.dumps(data)
	headers = {'Content-type': 'application/json'}
	response = requests.post(url, data = data_json, headers = headers)
	return HttpResponse(response)

def index(request):
	ErrMsg = None
	if request.session.has_key('ErrMsg'):
		ErrMsg = request.session['ErrMsg']
	return render(request, 'index.html', {'title': 'HomePage', 'Concerns': Concern.objects.all().filter(parent_id = 1).exclude(id = 1), 'Issues': Issue.objects.filter(acked = 0), 'ErrMsg': ErrMsg})

def subIndex(request):
	if request.method == 'GET' and 'parent_id' in request.GET:
		parent_id = request.GET['parent_id']
	if parent_id is not None and parent_id != '':
		return render(request, 'subIndex.html', {'title': 'HomePage', 'Concerns': Concern.objects.filter(parent_id = parent_id), 'ParentConcern': Concern.objects.get(id = parent_id)})

def notify(request):
	if request.method == 'GET' and 'cid' in request.GET:
		return render(request, 'notify.html', {'cid': request.GET['cid']})

@validatePOST
def acknowledgement(request):
	UID = request.POST['UID']
	station_id = request.POST['station_id']
	issue = Issue.objects.filter(acked = 0).filter(workstation_id = station_id)
	if issue.count() == 1:
		issue = issue[0]
		supportPersonnel = SupportPersonnel.objects.filter(uid = UID)
	if supportPersonnel.count() == 1:
		supportPersonnel = supportPersonnel[0]
		acknowledgement = Acknowledgement(issue = issue, supportPersonnel = supportPersonnel)
		acknowledgement.save()
		issue.acked = 1
		issue.save()
	return HttpResponseRedirect(reverse('Andon:index'))

def Dashboard(request):
	issues = Issue.objects.all()
	TotalIssues = issues.count()
	acknowledgements = Acknowledgement.objects.all()
	TotalSolvedIssues = acknowledgements.count()
	TotalIssuesByConcern = []
	parent_id_list = Concern.objects.values('parent_id').all().distinct()
	concerns = Concern.objects.exclude(id__in = parent_id_list).annotate(count_issue = Count('issue'))
	for concern in concerns:
		count_issue = concern.count_issue
		if count_issue > 5:
			status = "BAD"
			color = "red"
		elif count_issue > 2:
			status = "NORMAL"
			color = "orange"
		elif count_issue > 0:
			status = "GOOD"
			color = "blue"
		else:
			status = "GREAT"
			color = "green"
		issue = {'name': concern.name, 'count_issue': count_issue, 'color': color, 'status': status}
		TotalIssuesByConcern.append(issue)
	SolvedIssuesBySupportPersonnel = SupportPersonnel.objects.annotate(count_acknowledgement = Count('acknowledgement'))
	total_supportpersonnel = SupportPersonnel.objects.all().count()	
	total_concern = Concern.objects.all().count() - 1
	current_issue = Issue.objects.filter(acked = 0).count()
	return render(request, 'Dashboard.html', {'title': 'Dashboard', 'TotalIssues': TotalIssues, 'TotalSolvedIssues': TotalSolvedIssues,
		'TotalIssuesByConcern': TotalIssuesByConcern, 'SolvedIssuesBySupportPersonnel': SolvedIssuesBySupportPersonnel, 
		'total_supportpersonnel':total_supportpersonnel, 'total_concern': total_concern, 'current_issue': current_issue})

def viewConcern(request):
	Root_Concerns = Concern.objects.filter(parent_id = 1).exclude(id = 1)
	Concerns = []
	index = 1
	for Root_Concern in Root_Concerns:
		if Root_Concern.has_child():
			Concerns.append({'index': index, 'name': Root_Concern.name, 'created_timestamp': Root_Concern.created_timestamp, 'z_index': Root_Concern.z_index, 'has_child': Root_Concern.has_child, 'count_issue': '-'})
			concerns = Concern.objects.filter(parent_id = Root_Concern.id).exclude(id = 1).annotate(count_issue = Count('issue'))
			index = index + 1
			for concern in concerns:
				Concerns.append({'index': index, 'name': concern.name, 'created_timestamp': concern.created_timestamp, 'z_index': concern.z_index, 'has_child': concern.has_child, 'count_issue': concern.count_issue})	
				index = index + 1
		else:
			count_issue = Issue.objects.filter(concern = Root_Concern).count()
			Concerns.append({'index': index, 'name': Root_Concern.name, 'created_timestamp': Root_Concern.created_timestamp, 'z_index': Root_Concern.z_index, 'has_child': Root_Concern.has_child, 'count_issue': count_issue})
			index = index + 1
	return render(request, 'ViewConcern.html', {'title': 'Concern View', 'Concerns': Concerns})

def viewSupportPersonnel(request):
	SupportPersonnels = SupportPersonnel.objects.all()
	return render(request, 'ViewSupportPersonnel.html', {'title': 'View Support Personnel', 'SupportPersonnels': SupportPersonnels})

def viewIssue(request):
	Issues = Issue.objects.all()
	return render(request, 'ViewIssue.html', {'title': 'View Issue', 'Issues': Issues})

def viewAcknowledgement(request):
	Acknowledgements = Acknowledgement.objects.all()
	return render(request, 'ViewAcknowledgement.html', {'title': 'View Acknowledgement', 'Acknowledgements': Acknowledgements})