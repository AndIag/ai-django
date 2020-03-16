from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    def __init__(self, *args, **kwargs):
        # Set 'image' field source, defaults to 'image'
        if hasattr(kwargs, 'source'):
            self.fields['image'] = serializers.ImageField(source=kwargs.pop('source'))

        super(ImageSerializer, self).__init__(*args, **kwargs)

    class Meta:
        fields = ('image',)


class ImageThumbnailSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(source='image.thumbnail')

    class Meta:
        fields = ('id', 'image', 'thumbnail')


class ImageListSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False))

    def create(self, validated_data):
        return [self.Meta.model.objects.create(image=i, **self.context) for i in validated_data.pop('images', [])]

    def update(self, instance, validated_data):  # pragma: no cover
        raise NotImplementedError

    class Meta:
        model = None
        fields = ('images',)


class VideoListSerializer(serializers.Serializer):
    videos = serializers.ListField(child=serializers.CharField(max_length=500))

    def create(self, validated_data):
        return [self.Meta.model.objects.create(video=v, **self.context) for v in validated_data.pop('videos', [])]

    def update(self, instance, validated_data):  # pragma: no cover
        raise NotImplementedError

    class Meta:
        model = None
        fields = ('videos',)
