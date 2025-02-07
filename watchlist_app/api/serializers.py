from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watchlist',)
        # fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = WatchList
        fields = "__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"














# from rest_framework import serializers
# from watchlist_app.models import WatchList,StreamPlatform,Review


# class ReviewSerializer(serializers.ModelSerializer):
#     review_user=serializers.StringRelatedField(read_only=True)
#     class Meta:
#         model=Review
#         fields="__all__"

# class WatchListSerializer(serializers.ModelSerializer):
#     # reviews = ReviewSerializer(many=True, read_only=True)
#     platform = serializers.CharField(source='platform.name')

#     class Meta:
#         model = WatchList
#         fields = "__all__"

# class StreamPlatformSerializer(serializers.ModelSerializer):
#     watchlist=WatchListSerializer(many=True,read_only=True)
#     class Meta:
#         model=StreamPlatform
#         fields="__all__"
#         # extra_kwargs = {
#         #     'url': {'view_name': 'streamdetail'}  # Ensure the view name matches
#         # }

# #user defined validator
# # def name_length(value):
# #     if len(value)<2:
# #         raise serializers.ValidationError("Name is too short")

# # class MovieSerializer(serializers.Serializer):
# #     id=serializers.IntegerField(read_only=True)
# #     name=serializers.CharField(validators=[name_length])
# #     description=serializers.CharField()
# #     active=serializers.BooleanField()
# #     def create(self, validated_data):
# #         return Movie.objects.create(**validated_data)
    
# #     def update(self,instance,validated_data):
# #         instance.name=validated_data.get('name',instance.name)
# #         instance.description=validated_data.get('description',instance.description)
# #         instance.active=validated_data.get('active',instance.active)
# #         instance.save()
# #         return instance
# #     #This is object level validator
# #     def validate(self,data):
# #         if data['name']==data['description']:
# #             raise serializers.ValidationError("name and description cant be same")
#     #this is field level VALIDATOR
#     # def validate_name(self,value):  this we can also do by another method by calling direct a defined function on name  (name_length)
#     #     if len(value)<2:
#     #         raise serializers.ValidationError("Name is too short")
#     #     else:
#     #         return value