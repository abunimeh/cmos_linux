from  django.shortcuts import render_to_response

def teams(request):
	return render_to_response('team.html')
