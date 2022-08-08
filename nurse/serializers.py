from datetime import datetime
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(
            max_length=None, use_url=True
        )

    class Meta:
        model = User
        fields = ["id", "first_name", "email", "last_name", "city", "state", "address", "lat", "long", "picture", "phoneNumber", "isNurse"]


class UserBasicSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(
            max_length=None, use_url=True
        )

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "picture"]


class NurseQualificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Qualification
        fields = "__all__"

class NurseReviewSerializer(serializers.ModelSerializer):
    user_from = UserBasicSerializer()
    user_to = UserBasicSerializer()

    class Meta:
        model = Review
        fields = "__all__"
        depth = 1

class NurseSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    rating = serializers.SerializerMethodField("get_rating")

    class Meta:
        model = Nurse
        fields = "__all__"
        depth = 1

    def get_rating(self, obj):
        return obj.nurse_rating

class NearbyNurseSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    qualification = serializers.SerializerMethodField('get_qualification')
    reviews = serializers.SerializerMethodField('get_reviews')

    class Meta:
        model = Nurse
        fields = "__all__"
        depth = 1

    def get_qualification(self, obj):
        data = Qualification.objects.filter(nurse=obj)
        if data.count() > 0: return list(data.values())
        else: return []
    
    def get_reviews(self, obj):
        data = Review.objects.filter(user_to=obj.user)
        serializer = NurseReviewSerializer(data, many=True)
        return serializer.data

class SearchNurseSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Nurse
        fields = "__all__"
        depth = 1

class MessageSerializer(serializers.ModelSerializer):
    user_from = UserSerializer()
    user_to = UserSerializer()

    class Meta:
        model = Message
        fields = "__all__"
        depth = 1

class CreateMessageSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Message
        fields = "__all__"

class CreateReviewSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Review
        fields = "__all__"

class GetReviewSerializer(serializers.ModelSerializer):
    user_to = serializers.SerializerMethodField("get_nurse_user")
    user_from = UserSerializer()
    create_at = serializers.SerializerMethodField("format_date")

    class Meta:
        model = Review
        fields = "__all__"
        depth = 1

    def get_nurse_user(self, obj):
        nurse = Nurse.objects.get(user=obj.user_to)
        serializer = NurseSerializer(nurse)
        return serializer.data

    def format_date(self, obj):
        return datetime.date(obj.create_at)

class QualificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Qualification
        fields = "__all__"

class MessagesUser(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = "__all__"