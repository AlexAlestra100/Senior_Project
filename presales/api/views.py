from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from collections import OrderedDict
from management.models import *
from itertools import chain
from .helper import *
from .serializers import *
import requests
import json

results = 5

@csrf_exempt
@api_view(['POST'])
def addActivity(request):
    if(request.method == 'POST'):
        activity = json.loads(request.body)

        #Check if activity already exists
        if(searchActivity(activity)):
            return HttpResponse("Activity already exists", status=409)

        #add activity type
        request_activity_Type = ActivityType.objects.get(type_ID=activity['activity_Type'])

        date1 = datetime.fromisoformat(activity['oneDateTime'].split('.')[0] + '+00:00')
        
        #create a new activity
        newActivity = Activity(
            opportunity_ID=activity['opportunity_ID'], 
            account_ID = activity['account_ID'], 
            location = activity['location'], 
            activity_Type = request_activity_Type,
            activity_Level = activity['activity_Level'], 
            oneDateTime=date1,
            status = activity['status'], 
            flag=activity['flag']
        )

        newActivity.save()

        #add member_ID to the activity
        member = activity['createdByMember']
        if(type(member) != list):
            member = [member]
        member = searchMember(member)
        member = member[0]
        newActivity.createdByMember = Member.objects.get(member_ID=member)
        newActivity.save()

        #add members to the activity
        if("members" in activity):
            members = activity['members']
            if(type(members) != list):
                members = [members]
            members = searchMember(members)
            for member in members:
                newActivity.members.add(Member.objects.get(member_ID=member))
            newActivity.save()

        #add activeManager to the activity
        if("activeManager" in activity):
            activeManager = activity['activeManager']
            if(type(activeManager) != list):
                activeManager = [activeManager]
            activeManager = searchMember(activeManager)
            for member in activeManager:
                newActivity.activeManager = Member.objects.get(member_ID=member)
            newActivity.save()

        #add product_ID to the activity
        products = activity['products']
        arrP = searchProducttoAdd(products)
        for p in arrP:
            newActivity.products.add(p)
        newActivity.save()

        #set selectedDateTime if necessary
        if((not activity['twoDateTime']) and (not activity['twoDateTime'])):
            newActivity.selectedDateTime = date1
        else:
            if(activity['twoDateTime']):
                newActivity.twoDateTime = activity['twoDateTime']

            if(activity['threeDateTime']):
                newActivity.threeDateTime = activity['threeDateTime']

        newActivity.save()

        if('notes' in activity):
            newNote = Note(
                activity=newActivity,
                member=newActivity.createdByMember,
                note_text=activity['notes']
            )

            newNote.save()

        return HttpResponse(json.dumps({'POST Success': 'True'}), content_type='application/json')

@csrf_exempt
@api_view(['GET', 'PATCH', 'POST', 'DELETE']) 
def getActivity(request, activityID):
    if(activityID == 'types'):
        if(request.method =='GET'):
            activity_Type = ActivityType.objects.all()
            serializer = ActivityTypeSerializer(activity_Type, many=True)
            return Response(serializer.data)
        elif(request.method == 'POST'):
            activity_Type = json.loads(request.body)
            if(ActivityType.objects.filter(name=activity_Type['name']).exists()):
                return HttpResponse("Activity type already exists", status=409)
            new_activity_Type = ActivityType(name=activity_Type['name'])
            new_activity_Type.save()
            return HttpResponse(json.dumps({'POST Success': 'True'}), content_type='application/json')
        elif(request.method == 'DELETE'):
            activity_Type = json.loads(request.body)
            activity_Type = ActivityType.objects.get(type_ID=activity_Type['type_ID'])
            activity_Type.delete()
            return HttpResponse(json.dumps({'DELETE Success': 'True'}), content_type='application/json')
    else:
        if(request.method == 'GET'):
            try:
                activity = Activity.objects.filter(activity_ID=activityID)
                serializer = ActivitySerializer(activity, many=True)

                return Response(serializer.data[0])
            
            except:
                return Response(status=204)

        elif(request.method == 'PATCH'):
            activity_patch = json.loads(request.body)

            updateActivity = Activity.objects.get(activity_ID=activityID)

            #check to see if the json contains a members
            if('members' in activity_patch):
                members = activity_patch['members']

                #remove members from the update activity if they do not exist in the memberForm
                for m in updateActivity.members.all():
                    if(m.external_member_ID not in members):
                        updateActivity.members.remove(m)

                arrM = searchMember(members)
                for m in arrM:
                    updateActivity.members.add(m)
                
                updateActivity.save()

            if('members' in activity_patch):
                #if the leadMember is not in the memberForm, remove it
                if('leadMember' in activity_patch):
                    leadM = Member.objects.get(external_member_ID=activity_patch['leadMember'])
                if(not 'leadMember' in activity_patch or leadM not in updateActivity.members.all()):
                    updateActivity.leadMember = None
                    updateActivity.save()
                elif('leadMember' in activity_patch):
                    member = [activity_patch['leadMember']]
                    memberID = searchMember(member)
                    updateActivity.leadMember = Member.objects.filter(member_ID=memberID[0])[0]
                    updateActivity.save()
            
            if("activeManager" in activity_patch):
                activeManager = activity_patch['activeManager']
                if(type(activeManager) != list):
                    activeManager = [activeManager]
                activeManager = searchMember(activeManager)
                for member in activeManager:
                    updateActivity.activeManager = Member.objects.get(member_ID=member)
                updateActivity.save()

            if('status' in activity_patch):
                updateActivity.status = activity_patch['status']
                updateActivity.save()

            if('flag' in activity_patch):
                updateActivity.flag = activity_patch['flag']
                updateActivity.save()

            if('oneDateTime' in activity_patch):
                oneDateTime = activity_patch['oneDateTime'].split(".")[0]
                updateActivity.oneDateTime = oneDateTime
                updateActivity.save()

            if('twoDateTime' in activity_patch):
                twoDateTime = activity_patch['twoDateTime'].split(".")[0]
                updateActivity.twoDateTime = twoDateTime
                updateActivity.save()

            if('threeDateTime' in activity_patch):
                threeDateTime = activity_patch['threeDateTime'].split(".")[0]
                updateActivity.threeDateTime = threeDateTime
                updateActivity.save()

            if('selectedDateTime' in activity_patch):
                selectedDateTime = activity_patch['selectedDateTime'].split(".")[0]
                updateActivity.selectedDateTime = selectedDateTime
                updateActivity.save()

            return HttpResponse(json.dumps({'PATCH Success': 'True'}), content_type='application/json')
            
@api_view(['GET'])
def getActivities(request):
    query = Activity.objects.all()
    
    if(request.GET.get('opportunity_ID') or request.GET.get('activeManager') or request.GET.get('account_ID') or request.GET.get('createdByMember') or request.GET.get('members') or request.GET.get('products') or request.GET.get('status') or request.GET.get('flag')):
        #query whatever is passed in
        new_query = Activity.objects.none()

        if(request.GET.get('opportunity_ID')):
            new_query |= query.filter(opportunity_ID=request.GET.get('opportunity_ID'))
        if(request.GET.get('account_ID')):
            new_query |= query.filter(account_ID=request.GET.get('account_ID'))
        if(request.GET.get('createdByMember')):
            new_query |= query.filter(createdByMember=request.GET.get('createdByMember'))
        if(request.GET.get('activeManager')):
            new_query |= query.filter(createdByMember=request.GET.get('activeManager'))
        if(request.GET.get('members')):
            new_query |= query.filter(members=request.GET.get('members'))
        if(request.GET.get('products')):
            new_query |= query.filter(products=request.GET.get('products'))
        if(request.GET.get('status')):
            new_query |= query.filter(status=request.GET.get('status'))
        if(request.GET.get('flag')):
            new_query |= query.filter(flag=request.GET.get('flag'))

        #serialize the query
        serializer = ActivitySerializer(new_query, many=True)
        return Response(serializer.data)
    else:
        serializer = ActivitySerializer(query, many=True)

        return Response(serializer.data)

@api_view(['GET'])
def getActiveActvivities(request):
    #get all activities with the status of accapt, reschedule, schedule, and request
    activities = Activity.objects.filter(status__in=['Accept', 'Reschedule', 'Schedule', 'Request'])
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAcceptedActivities(request):
    activities = Activity.objects.filter(status__in=['Accept', 'Scheduled'])
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRequestActivities(request):
    activities = Activity.objects.filter(status__in=['Reschedule', 'Request'])
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPastActivities(request):
    activities = Activity.objects.filter(status__in=['Cancel', 'Expire', 'Complete'])
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSuggestedMembers(request, activityID):
    #get the activity
    activity = Activity.objects.get(activity_ID=activityID)
    oID = activity.opportunity_ID
    aID = activity.account_ID
    date1 = activity.oneDateTime
    if(activity.twoDateTime != None):
        date2 = activity.twoDateTime
    else:
        date2 = None
    if(activity.threeDateTime != None):
        date3 = activity.threeDateTime
    else:
        date3 = None

    prod = []
    for p in activity.products.all():
        prod.append(str(p))

    if(len(prod) == 0):
        prodW = 0
    else:
        prodW = .25 / len(prod)

    avaW = .25
    oppW = .3
    accW = .2
    total = 0

    allmembers = Member.objects.filter(user_role__name='Presales Member')
    serializers = MemberSerializer(allmembers, many=True)
    members = serializers.data

    for m in members:
        aS = False
        avaAmount = avaW
        memID = Member.objects.filter(external_member_ID=m['external_member_ID'])

        #get all activity that the member is assigned to that have the status of accept, reschedule, or schedule
        memAct = Activity.objects.filter(
            members=memID[0], 
            status__in=['Request', 'Accept', 'Reschedule', 'Schedule']
        )

        aList = []

        #then see if any of the oneDateTime is within the hour of this activity
        for a in memAct:
            if(str(a) != str(activityID) and a.selectedDateTime != None):
                if(isWithinAnHour(a.selectedDateTime, date1)):
                    #add just the activity ID to aList
                    aList.append(a.activity_ID)
                    avaAmount = 0
                    aS = True
                if(date2):
                    if(isWithinAnHour(a.selectedDateTime, date2)):
                        aList.append(a.activity_ID)
                        avaAmount = 0
                        aS = True
                if(date3):
                    if(isWithinAnHour(a.selectedDateTime, date3)):
                        aList.append(a.activity_ID)
                        avaAmount = 0
                        aS = True

        aList = Activity.objects.filter(activity_ID__in=aList)

        if(avaAmount == 0):
            conflicts = SimpleActivitySerializer(aList, many=True).data
            m.update({'Conflicts': conflicts})

        #get the count of how manny activity the member is appart of
        oAmount = Activity.objects.filter(opportunity_ID=oID, members=memID[0]).count()
        if(oAmount > 0):
            oAmount = oppW
        aAmount = Activity.objects.filter(account_ID=aID, members=memID[0]).count()
        if(aAmount > 0):
            aAmount = accW
        pAmount = 0
        
        #see if the proficiency is the same as the activity
        prof = list(memID[0].proficiency.all())
        print(prof)
        #make prof into a list
        prof = [str(p)[:-2] for p in prof]

        total = 0
        for p in prof:
            if(p in prod):
                total += 1
                pAmount += prodW
        
        total = oAmount + aAmount + pAmount + avaAmount
        
        m.update(
        {
            "Conflict Status": aS,
            "Opportunity Weight": oAmount, 
            "Account Weight": aAmount, 
            "Product Weight": pAmount, 
            "Availablity": avaAmount, 
            "Total Percentage": total
        })

    #sort the members by the weight
    members = sorted(
        members, 
        key=lambda k: k['Opportunity Weight'] + k['Account Weight'] + k['Product Weight'] + k['Availablity'] + k['Total Percentage'], 
        reverse=True
    )

    #remove all members that have a product weight of 0
    members = [m for m in members if m['Product Weight'] != 0]

    return Response(members)

# add in the account look up and opportunity look up as well.
@api_view(['GET'])
def getMembers(request):
    if(request.method == 'GET'):
        # account = request.GET.get('account')
        # opportunity = request.GET.get('opportunity')
        role = request.GET.get('role')

        if(role):
            members = Member.objects.filter(user_role__name=role)
        else:
            members = Member.objects.all()

        serializers = MemberSerializer(members, many=True)
        return Response(serializers.data)

#FIX PROFICIENCY
@csrf_exempt
@api_view(['GET', 'DELETE', 'POST', 'PATCH'])
def getMember(request, id):
    if(request.method == 'POST'):
        data = request.data

        if(Member.objects.filter(external_member_ID=id).exists()):
            return HttpResponse("Member already exists", status=409)
        
        #get the role ID
        role = UserRole.objects.get(name=data['user_role'])
        #create the memeber
        member = Member(
            external_member_ID = id,
            user_role = role,
        )
        member.save()

        if("proficiency" in data):
            #get the proficiency ID's
            prof = searchProficiency(data['proficiency'])
            
            for p in prof:
                member.proficiency.add(p)
                member.save()

        return HttpResponse(json.dumps({'POST Success': 'True'}), content_type='application/json')

    elif(request.method == 'GET'):
        member = Member.objects.filter(external_member_ID=id)
        serializer = MemberSerializer(member, many=True)
        return Response(serializer.data[0])

    elif(request.method == 'DELETE'):
        member = Member.objects.get(external_member_ID=id)
        member.delete()
        return HttpResponse(json.dumps({'DELETE Success': 'True'}), content_type='application/json')

    elif(request.method == 'PATCH'):
        data = request.data
        #get the member
        member = Member.objects.get(external_member_ID=id)

        # FIX change proficiencies to accept json object array
        if("proficiency" in data):
            #get the proficiency ID's
            prof = searchProficiency(data['proficiency'])
    
            for p in prof:
                member.proficiency.add(p)
                member.save()

            for p in member.proficiency.all().values_list('proficiency_ID', flat=True):
                if(p not in prof):
                    member.proficiency.remove(p)
                    member.save()
        if("role" in data):
            #get the role ID
            role = UserRole.objects.get(name=data['role'])
            member.user_role = role
            member.save()

        return HttpResponse(json.dumps({'PATCH Success': 'True'}), content_type='application/json')

@api_view(['GET'])
def getMemberActivities(request, id):
    memID = Member.objects.filter(external_member_ID=id)[0]
    actsM = Activity.objects.filter(members=memID)
    actsL = Activity.objects.filter(createdByMember=memID)
    acts = set(actsM | actsL)
    serializers = serializers = ActivitySerializer(acts, many=True)

    return Response(serializers.data)

@csrf_exempt
@api_view(['GET', 'POST', 'PATCH'])
def getProducts(request):
    if(request.method == 'GET'):
        if(request.GET.get('available')):
            products = Product.objects.filter(available=request.GET.get('available'))
            serializers = ProductSerializer(products, many=True)
            return Response(serializers.data)
        else:
            products = Product.objects.all()
            serializers = ProductSerializer(products, many=True)
            return Response(serializers.data)
    elif(request.method == 'POST'):
        product = json.loads(request.body)

        if(Product.objects.filter(name=product['name']).exists()):
            return HttpResponse("Product already exists", status=409)
        
        searchProducttoCreate(product)
        return HttpResponse(json.dumps({'POST Success': 'True'}), content_type='application/json')
    elif(request.method == 'PATCH'):
        data = request.data
        product = Product.objects.get(product_ID=data['product_ID'])
        if("name" in data):
            product.name = data['name']
            product.save()
        if("external_product_ID" in data):
            product.external_product_ID = data['external_product_ID']
            product.save()
        if("available" in data):
            product.available = data['available']
            product.save()
        return HttpResponse(json.dumps({'PATCH Success': 'True'}), content_type='application/json')

@csrf_exempt
@api_view(['PATCH', 'DELETE'])
def getActivityNote(request, noteID):
    if(request.method == 'DELETE'):
        note = Note.objects.get(note_ID=noteID)
        note.delete()
        return HttpResponse(json.dumps({'DELETE Success': 'True'}), content_type='application/json')
    elif(request.method == 'PATCH'):
        jForm = json.loads(request.body)
        note = Note.objects.get(note_ID=noteID)
        note.note_text = jForm['note_text']
        note.save()
        return HttpResponse(json.dumps({'PATCH Success': 'True'}), content_type='application/json')

@csrf_exempt
@api_view(['GET', 'POST'])
def getActivityNotes(request, activityID):
    if(request.method == 'GET'):
        notes = Note.objects.filter(activity=activityID)
        serializers = NoteSerializer(notes, many=True)
        return Response(serializers.data)
    elif(request.method == 'POST'):
        note = json.loads(request.body)

        if(Note.objects.filter(activity=activityID, note_text=note['note_text']).exists()):
            return HttpResponse("Note already exists", status=409)
        
        memberID = searchMember([note['member']])[0]

        act = Activity.objects.get(activity_ID=activityID)
        mem = Member.objects.get(member_ID=memberID)
        newNote = Note(member = mem, note_text = note['note_text'], activity = act)
        newNote.save()
        return HttpResponse(json.dumps(note), content_type="application/json")

@csrf_exempt
@api_view(['GET', 'POST'])
def getUserRoles(request):
    if(request.method =='GET'):
        user_roles = UserRole.objects.all()
        serializer = UserRolesSerializer(user_roles, many=True)
        return Response(serializer.data)
    elif(request.method == 'POST'):
        user_role = json.loads(request.body)
        if(UserRole.objects.filter(name=user_role['name']).exists()):
            return HttpResponse("User role already exists", status=409)
        new_user_role = UserRole(name=user_role['name'])
        new_user_role.save()
        return HttpResponse(json.dumps({'POST Success': 'True'}), content_type='application/json')

#Display and send a notification in dashboard
def sendNotification():
    url = "https://scs-4d-dev-ed.my.salesforce.com/services/data/v46.0/actions/standard/customNotificationAction"

    data = {
        'inputs': [{
               'customNotifTypeId': '0ML5f000000brbbGAA',
               'recipientIds' : ['0055f000002968SAAQ'],
               'title': 'test',
               'body': 'This is a custom notification.',
               'targetId': '0065f000003swZ9AAI'
               }]
            }

    headers = {
        "Authorization": "Bearer 00D5f000003H4cm!ASAAQJKTo8flvPbaKObo_i6Dvajk4cc_YM9nLSyJd0YYPEv0YrlSpiXaEbXNz617RS.UdsiL2XfbBIyuBE9ANpMkVp8ye0KH",
        "Content-Type": "application/json"
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r