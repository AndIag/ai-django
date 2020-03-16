from rest_framework import serializers


class WeekYearSerializer(serializers.Serializer):
    week = serializers.IntegerField(default=None)
    year = serializers.IntegerField(default=None)

    def update(self, instance, validated_data):
        instance.week = validated_data.get('week', instance.week)
        instance.year = validated_data.get('year', instance.year)
        return instance

    def create(self, validated_data):  # pragma: no cover
        raise NotImplementedError


class PeriodSerializer(WeekYearSerializer):
    date = serializers.DateField(default=None)
    day = serializers.IntegerField(default=None)
    month = serializers.IntegerField(default=None)

    def update(self, instance, validated_data):
        instance = super(PeriodSerializer).update(instance, validated_data)
        instance.date = validated_data.get('date', instance.date)
        instance.day = validated_data.get('day', instance.day)
        instance.month = validated_data.get('month', instance.month)
        return instance

    def create(self, validated_data):  # pragma: no cover
        raise NotImplementedError
