from rest_framework import serializers
from .models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.is_active:
            raise serializers.ValidationError("User is not active")
        
        token, created = Token.objects.get_or_create(user=user)
        
        data['token'] = token
        data['user'] = user
        
        return data
    

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'password1', 'password2']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
        
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password1']
        )
        user.is_active = True
        user.set_password(validated_data['password1'])
        user.save()
        
        token, created = Token.objects.get_or_create(user=user)
        validated_data['token'] = token
        validated_data['user'] = user
        
        return validated_data
    

class UserSrializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name',"email"]
        read_only_fields = ['email',]

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        ref_name = 'UserChangePasswordSerializer'

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError(
                {
                    "confirm_password": "New password and confirmation password do not match."
                }
            )

        return attrs


class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def send_otp_email(self, user, otp):
        send_mail(
            subject='رمز التحقق',
            message=f'رمز التحقق هو: {otp}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )


    def validate(self, data):
        email = data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            return {"success": False, "message": "user not found"}
        
        user.generate_otp()
        self.send_otp_email(user, user.otp)
        return {"success": True, "message": "OTP sent successfully"}


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')
        
        user = User.objects.filter(email=email).first()
        if not user:
            return {"success": False, "message": "user not found"}

        is_valid, message = user.verify_otp(otp)
        return {"success": is_valid, "message": message}
    

class ResetPasswordWithOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password != confirm_password:
            return {"success": False, "message": "Passwords do not match"}

        user = User.objects.filter(email=email).first()
        if not user:
            return {"success": False, "message": "user not found"}

        is_valid, message = user.verify_otp(otp, remove_otp=True)
        if not is_valid:
            return {"success": False, "message": message}

        user.set_password(new_password)
        user.save()

        return {"success": True, "message": "Password reset successfully"}