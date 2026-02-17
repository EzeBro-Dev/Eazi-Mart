from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from .models import User, SellerProfile, UserProfile, Address
from .serializer import (UserRegistrationSerializer, UserSerializer, SellerProfileSerializer, UserProfileSerializer , AddressSerializer)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        UserProfile.objects.create(user=user)

        if user.is_seller:
            SellerProfile.objects.create(user=user)

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class SellerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = SellerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.seller_profile
        

class AddressListCreate(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.addresses.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.addresses.all()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_verification_email(request):
    user = request.user

    if not user.is_seller:
        return Response(
            {'error': 'User is not registered as a seller'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        seller_profile = user.seller_profile
    except SellerProfile.DoesNotExist:
        return Response(
            {'error': 'Seller profile does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Set KYC to pending
    seller_profile.kyc_status = 'pending'
    seller_profile.save()

    # OPTIONAL: Send email
    send_mail(
        subject='KYC Verification Submitted',
        message='Your KYC documents have been submitted and are under review.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return Response(
        {'message': 'Verification request submitted successfully'},
        status=status.HTTP_200_OK
    )