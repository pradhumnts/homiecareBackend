from django.http import HttpResponse
from rest_framework import status
from nurse.client import check_verification, send_verification

from nurse.serializers import CreateMessageSerializer, CreateReviewSerializer, GetReviewSerializer, MessageSerializer, NearbyNurseSerializer, NurseSerializer, QualificationSerializer, SearchNurseSerializer
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.db.models import Max, Count

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 200  

# Create your views here.
def index(request):
    # users = User.objects.all()

    # for x in users:
    #     print(x.first_name)
    #     x.isNurse = True
    #     x.save()

    return HttpResponse("Data Uploaded!")

@api_view(['GET', 'POST'])
def nearby_nurses(request):
    if request.method == 'POST' and "lat" in request.data and "long" in request.data:
       
        try:
            user = Nurse.objects.filter(user__lat__lte=request.data["lat"], user__long__gte=request.data["long"])[:5]
            user2 = Nurse.objects.filter(user__lat__gte=request.data["lat"], user__long__lte=request.data["long"])[:5]

            nurse_list = user | user2
            data = []
            print(nurse_list)
            if len(nurse_list) > 0:
                serializer = NearbyNurseSerializer(nurse_list, many=True)
                data = serializer.data
            
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": e}, status=status.HTTP_404_NOT_FOUND)

    return Response({"data": "Invalid Request"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def nurse_profile(request):
    
    if request.method == 'POST' and "id" in request.data:
        try:
            user = Nurse.objects.get(id=request.data["id"])
            
            data = []
            
            if user:
                serializer = NearbyNurseSerializer(user)
                data = serializer.data
            
                return Response(data, status=status.HTTP_200_OK)

        except Nurse.DoesNotExist: return Response({"message": "Does Not Exist!"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"data": "Invalid Request"}, status=status.HTTP_404_NOT_FOUND)

class GetMessage(APIView):

    def post(self, request, format=None):
        user_from = User.objects.get(id=request.data["user_to_id"])
        user_to = User.objects.get(id=request.data["user_from_id"])

        messages_from = Message.objects.filter(user_from=user_from, user_to=user_to)
        messages_to = Message.objects.filter(user_to=user_from, user_from=user_to)

        messages = messages_from | messages_to

        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class AddMessage(APIView):
    
    def post(self, request, format=None):

        serializer = CreateMessageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddReview(APIView):
    
    def post(self, request, format=None):
        try:
            review = Review.objects.get(user_from=request.data["user_from"], user_to=request.data["user_to"])
        except Review.DoesNotExist:
            review = None
        
        if review: serializer = CreateReviewSerializer(data=request.data, instance=review)
        else: serializer = CreateReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetReview(APIView):
    
    def post(self, request, format=None):
        try:
            review = Review.objects.get(user_from=request.data["user_from"], user_to=request.data["user_to"])
            serializer = CreateReviewSerializer(review)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Review.DoesNotExist:
            review = None
            return Response({}, status=status.HTTP_200_OK)

class GetUserReviews(APIView):
    
    def post(self, request, format=None):
        try:
            review = Review.objects.filter(user_from__id=request.data["user_from"])
            serializer = GetReviewSerializer(review, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Review.DoesNotExist:
            review = None
            return Response({}, status=status.HTTP_200_OK)

class SearchNurse(generics.ListAPIView):
    queryset = Nurse.objects.all()
    serializer_class = NearbyNurseSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = StandardResultsSetPagination
    search_fields = ['user__first_name', 'user__phoneNumber']

class SearchNurseByLocation(generics.ListAPIView):
    queryset = Nurse.objects.all()
    serializer_class = NearbyNurseSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = StandardResultsSetPagination
    search_fields = ['user__city', 'user__address', 'user__state']

class GetNurseProfile(APIView):

    def post(self, request, format=None):
        try:
            user = User.objects.get(pk=request.data["id"])
            if Nurse.objects.filter(user__id=request.data["id"]).exists():
                nurse = Nurse.objects.get(user__id=request.data["id"])
            else:
                nurse = Nurse.objects.create(user=user)
            
            serializer = NurseSerializer(nurse)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            nurse = None
            return Response({"message": "Following Profile Does Not Exist!"}, status=status.HTTP_404_NOT_FOUND)

class GetNurseReviews(APIView):
    
    def post(self, request, format=None):
        try:
            review = Review.objects.filter(user_to__id=request.data["user_to"])
            
            serializer = GetReviewSerializer(review, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Review.DoesNotExist:
            review = None
            return Response({}, status=status.HTTP_200_OK)

class GetQualifications(APIView):

    def post(self, request, format=None):

        try:
            user = Nurse.objects.get(user__id=request.data["id"])

            qualifications = Qualification.objects.filter(nurse=user)

            serializer = QualificationSerializer(qualifications, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_200_OK)

class UpdateOrCreateQualifications(APIView):

    def post(self, request, format=None):

        try:
            nurse = Nurse.objects.get(user__id=request.data["user_id"])

            qualification = Qualification.objects.create(
                nurse=nurse,
                degree=request.data["degree"], 
                end_date_year=request.data["end_date_year"], 
                description=request.data["description"],
            )
                
            serializer = QualificationSerializer(qualification)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        try:
            qualification = Qualification.objects.get(id=request.data["qualification_id"])
            qualification.degree = request.data["degree"]
            qualification.end_date_year = request.data["end_date_year"]
            qualification.description = request.data["description"]
            qualification.save()
            serializer = QualificationSerializer(qualification)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)

class UpdateNurse(APIView): 
    
    def post(self, request, format=None):
        try:
            user = User.objects.get(id=request.data["id"])
            user.isNurse = True
            user.save()
        except User.DoesNotExist as e: return Response({"message": e}, status=status.HTTP_404_NOT_FOUND)
        try:
            nurse = Nurse.objects.get(user=user)
            nurse.convenience_fee = request.data["convenience_fee"]
            nurse.working_distance_in_kms = request.data["working_distance_in_kms"]
            nurse.description = request.data["description"]
            nurse.availability = request.data["availability"]
            nurse.alternate_phone = request.data["alternate_phone"]
            nurse.save()

        except Nurse.DoesNotExist:
            nurse = Nurse.objects.create(
                user=user, 
                convenience_fee=request.data["convenience_fee"], 
                working_distance_in_kms=request.data["working_distance_in_kms"], 
                description=request.data["description"], 
                availability=request.data["availability"], 
                alternate_phone=request.data["alternate_phone"]
            )
        except Exception as e:
            print(e)

        serializer = NurseSerializer(nurse)

        return Response(serializer.data, status=status.HTTP_200_OK)

class GetMessageUsersList(APIView):

    def post(self, request, format=None):
        if request.data["type"] and request.data["type"] == "patient":
            result = Message.objects.filter(user_from=request.data["id"]).values('user_to').annotate(the_count=Count('user_to')).annotate(latest_activity=Max('create_at'))
        else:
            result = Message.objects.filter(user_to=request.data["id"]).values('user_from').annotate(the_count=Count('user_from')).annotate(latest_activity=Max('create_at'))
        
        response = []

        for x in result.order_by('-latest_activity'):
            
            if request.data["type"] and request.data["type"] == "patient":
                user = User.objects.get(id=x["user_to"])
                latest = Message.objects.filter(user_from__id=request.data["id"], user_to__id=x["user_to"]).latest('create_at')
                unread = Message.objects.filter(user_to__id=request.data["id"], user_from__id=x["user_to"], seen=False).count()
            else:
                user = User.objects.get(id=x["user_from"])
                latest = Message.objects.filter(user_from__id=x["user_from"], user_to__id=request.data["id"]).latest('create_at')
                unread = Message.objects.filter(user_from__id=x["user_from"], user_to__id=request.data["id"], seen=False).count()
            
            print(unread)
            
            response.append({
                "user_id": user.id,
                "picture": user.picture.url if user.picture else None,
                "first_name": user.first_name,
                "recent_message": latest.text,
                "message_count": x["the_count"],
                "unread": unread
            })

        return Response(response, status=status.HTTP_200_OK)

class PushNotificationToken(APIView):

    def post(self, request, format=None):
        try:
            token = request.data["token"]
            user_id = request.data["id"]

            user = User.objects.get(id=user_id)
            
            PushNotificationToken.objects.create(user=user, token=token)
            
            return Response({}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        try:
            user_id = request.data["id"]

            token = PushNotificationToken.objects.get(user__id=user_id)
            
            return Response(token.token, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateMessageStatus(APIView):
    def post(self, request, format=None):
        try:
            if request.data["ids"]:
                ids = request.data["ids"]

                messages = Message.objects.filter(id__in=ids)
                
                for message in messages:
                    message.seen = True
                    message.save()

            return Response({}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)

class SendVerification(APIView):

    def post(self, request, format=None):

        if request.data["phoneNumber"]:
            if send_verification(request.data["phoneNumber"]) == "pending":
                return Response({}, status=status.HTTP_200_OK)

        return Response({"message": "something went wrong!"}, status=status.HTTP_400_BAD_REQUEST)

class CheckVerification(APIView):

    def post(self, request, format=None):
        if request.data["phoneNumber"] and request.data["code"]:
            try:
                user = User.objects.get(phoneNumber=request.data["phoneNumber"])
            except:
                user = None

            if check_verification(request.data["phoneNumber"], request.data["code"]) == "approved":
                return Response({}, status=status.HTTP_200_OK)

        return Response({"message": "something went wrong!"}, status=status.HTTP_400_BAD_REQUEST)
