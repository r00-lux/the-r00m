from rest_framework import serializers
from profiles import models


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ('id', 'username', 'password')

        # Modify password to be write-only so that user cannot get hash.
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
        user = models.Profile.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'))

        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')

        # Modify user_profile to be read-only.
        extra_kwargs = {'user_profile': {'read_only': True}}
