from rest_framework import serializers

from apps.common.serializers import SportSerializer, MuscleSerializer, ExerciseTypeSerializer, LawVersionSerializer, \
    ServiceSerializer, TariffSerializer


class VersionFilterSerializer(serializers.Serializer):
    type = serializers.RegexField(r'^plain|html$', default='plain')

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        return instance

    def create(self, validated_data):  # pragma: no cover
        raise NotImplementedError


class VersionDataSerializer(serializers.Serializer):  # pragma: no cover
    """Used just for documentation"""

    services = ServiceSerializer(many=True, required=True)
    tariffs = TariffSerializer(many=True, required=True)
    sports = SportSerializer(many=True, required=False)
    exercise_types = ExerciseTypeSerializer(many=True, required=False)
    muscles = MuscleSerializer(many=True, required=False)
    workout_day_types = serializers.ListField(required=False)
    event_types = serializers.ListField(required=False)
    intensities = serializers.ListField(required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class Meta:
        fields = ('services', 'sports', 'exercise_types', 'muscles', 'workout_day_types', 'event_types', 'intensities')


class VersionSerializer(serializers.Serializer):  # pragma: no cover
    """Used just for documentation"""

    name = serializers.CharField(required=True)
    version = serializers.CharField(required=True)
    data = VersionDataSerializer(required=True)
    legal_documents = LawVersionSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class Meta:
        fields = ('name', 'version', 'data')
