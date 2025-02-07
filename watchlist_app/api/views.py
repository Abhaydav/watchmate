from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from watchlist_app.api  import pagination, permissions, serializers, throttling
from watchlist_app.models import Review, StreamPlatform, WatchList


class UserReview(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(
            watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (
                watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    throttle_classes = [throttling.ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle, AnonRateThrottle]
    throttle_scope = 'review-detail'


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]


class WatchListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = serializers.WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = serializers.WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)












# from django.shortcuts import get_object_or_404
# from rest_framework import status
# from rest_framework import viewsets
# from rest_framework import filters
# from rest_framework.exceptions import ValidationError
# from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

# from rest_framework.decorators import api_view,APIView
# from rest_framework import mixins
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
# from django_filters.rest_framework import DjangoFilterBackend

# from watchlist_app.api.pagination import WatchListPagination,WatchListLOPagination,WatchListCPagination
# from watchlist_app.api.permissions import AdminOrReadOnly,RevieUserOrReadOnly
# from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
# from watchlist_app.models import WatchList,StreamPlatform,Review
# from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle
 

# class UserReview(generics.ListAPIView):
#     # queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#     # permission_classes=[IsAuthenticated]
#     # throttle_classes=[ReviewListThrottle]
#     # def get_queryset(self):
#     #     username=self.kwargs['username']
#     #     return Review.objects.filter(review_user__username=username)
#     def get_queryset(self):
#         username=self.request.query_params.get('username',None)
#         return Review.objects.filter(review_user__username=username)
        

# class StreamPlatformVS(viewsets.ModelViewSet):
#     queryset=StreamPlatform.objects.all()
#     serializer_class=StreamPlatformSerializer


# # class StreamPlatformVS(viewsets.ViewSet):
# #     def list(self, request):
# #         queryset = StreamPlatform.objects.all()
# #         serializer = StreamPlatformSerializer(queryset, many=True)
# #         return Response(serializer.data)

# #     def retrieve(self, request, pk=None):
# #         queryset = StreamPlatform.objects.all()
# #         user = get_object_or_404(queryset, pk=pk)
# #         serializer = StreamPlatformSerializer(user)
# #         return Response(serializer.data)
    
# #     def create(self,request):
# #         serializer=StreamPlatformSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         else: 
# #             return Response(serializer.errors)

# class ReviewCreate(generics.CreateAPIView):
#     serializer_class=ReviewSerializer
#     throttle_classes=[ReviewCreateThrottle]
#     def get_queryset(self):
#         return Review.objects.all()
#     def perform_create(self, serializer):
#         pk=self.kwargs.get('pk')
#         watchlist=WatchList.objects.get(pk=pk)
#         review_user=self.request.user
#         review_queryset=Review.objects.filter(watchlist=watchlist,review_user=review_user)
#         if review_queryset.exists():
#             raise ValidationError("you have already reviewed this ")
        
#         if watchlist.number_rating==0:
#             watchlist.avg_rating=serializer.validated_data['rating']
#         else:
#             watchlist.number_rating=(watchlist.avg_rating + serializer.validated_data['rating'])
        
#         watchlist.number_rating=watchlist.number_rating +1
#         watchlist.save()
        
#         serializer.save(watchlist=watchlist,review_user=review_user)

# #concrete view class
# class ReviewList(generics.ListAPIView):
#     # queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#     # permission_classes=[IsAuthenticated]
#     throttle_classes=[ReviewListThrottle]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['review_user__username', 'active']
#     def get_queryset(self):
#         pk=self.kwargs['pk']
#         return Review.objects.filter(watchlist=pk)

# class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#     permission_classes=[RevieUserOrReadOnly]
#     throttle_classes=[UserRateThrottle,AnonRateThrottle]

# #mixins and generic api view classes
# # class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
# #     queryset = Review.objects.all()
# #     serializer_class = ReviewSerializer
# #     def get(self, request, *args, **kwargs):
# #         return self.retrieve(request, *args, **kwargs)

# # class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
# #     queryset = Review.objects.all()
# #     serializer_class = ReviewSerializer

# #     def get(self, request, *args, **kwargs):
# #         return self.list(request, *args, **kwargs)

# #     def post(self, request, *args, **kwargs):
# #         return self.create(request, *args, **kwargs)

# class WatchList(generics.ListAPIView):
#     queryset=WatchList.objects.all()
#     serializer_class=WatchListSerializer
#     # pagination_class=WatchListPagination
#     # pagination_class=WatchListLOPagination
#     pagination_class=WatchListCPagination
#     # filter_backends = [filters.SearchFilter]
#     # search_fields = ['title','=platform__name']
    


# class WatchListAV(APIView):
#     def get(self,request):
#         movies=WatchList.objects.all()
#         serializer=WatchListSerializer(movies,many=True)
#         return Response(serializer.data)

#     def post(self,request):
#         serializer=WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
# class WatchDetailAV(APIView):
#     def get(self,request,pk):
#         try:
#             movie=WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
#         serializer=WatchListSerializer(movie)
#         return Response(serializer.data)
#     def put(self,request,pk):
#         movie=WatchList.objects.get(pk=pk)
#         serializer=WatchListSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request,pk):
#         movie=WatchList.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class StreamPlatformAV(APIView):
#     def get(self,request):
#         platform=StreamPlatform.objects.all()
#         serializer=StreamPlatformSerializer(platform,many=True,context={'request': request})
#         return Response(serializer.data)
#     def post(self,request):
#         serializer=StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# class StreamPlatformDetailAV(APIView):
#     def get(self,request,pk):
#         try:
#             movie=StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
#         serializer=StreamPlatformSerializer(movie,context={'request': request})
#         return Response(serializer.data)
#     def put(self,request,pk):
#         movie=StreamPlatform.objects.get(pk=pk)
#         serializer=StreamPlatformSerializer(movie,data=request.data,context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request,pk):
#         movie=StreamPlatform.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
















# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method =='GET':
#         movies=Movie.objects.all()
#         serializer=MovieSerializer(movies,many=True)
#         return Response(serializer.data)
#     if request.method =='POST':
#         serializer=MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,pk):
#     if request.method=='GET':
#         try:
#             movie=Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error':'Movie Not Found'},status=status.HTTP_404_NOT_FOUND)
#         serializer=MovieSerializer(movie)
#         return Response(serializer.data)
#     if request.method=='PUT':
#         movie=Movie.objects.get(pk=pk)
#         serializer=MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     if request.method=='DELETE':
#         movie=Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)