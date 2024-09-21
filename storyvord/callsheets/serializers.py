from rest_framework import serializers
from .models import *
import requests
from django.conf import settings
from datetime import datetime, timedelta

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {'call_sheet': {'required': False}}

# class ScenesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Scenes
#         fields = '__all__'
#         extra_kwargs = {'call_sheet': {'required': False}}

# class CharactersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Characters
#         fields = '__all__'
#         extra_kwargs = {'call_sheet': {'required': False}}

# class ExtrasSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Extras
#         fields = '__all__'
#         extra_kwargs = {'call_sheet': {'required': False}}

# class DepartmentInstructionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DepartmentInstructions
#         fields = '__all__'
#         extra_kwargs = {'call_sheet': {'required': False}}

class CallTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallTime
        fields = '__all__'
        extra_kwargs = {'call_sheet': {'required': False}}

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'
        extra_kwargs = {'call_sheet': {'required': False}}

class CallSheetSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, required=False)
    # scenes = ScenesSerializer(many=True, required=False)
    # characters = CharactersSerializer(many=True, required=False)
    # extras = ExtrasSerializer(many=True, required=False)
    # department_instructions = DepartmentInstructionsSerializer(many=True, required=False)
    call_time = CallTimeSerializer(required=False, many= True)
    weather = WeatherSerializer(many=True, required=False)

    class Meta:
        model = CallSheet
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['events'] = EventSerializer(instance.events.all(), many=True).data
        ret['call_time'] = CallTimeSerializer(instance.call_time.all(), many=True).data
        # ret['scenes'] = ScenesSerializer(instance.scenes.all(), many=True).data
        # ret['characters'] = CharactersSerializer(instance.characters.all(), many=True).data
        # ret['extras'] = ExtrasSerializer(instance.extras.all(), many=True).data
        # ret['department_instructions'] = DepartmentInstructionsSerializer(instance.department_instructions.all(), many=True).data
        ret['weather'] = WeatherSerializer(instance.weather.all(), many=True).data
        return ret

    def create(self, validated_data):
        events_data = validated_data.pop('events', [])
        call_time_data = validated_data.pop('call_time', [])
        # scenes_data = validated_data.pop('scenes', [])
        # characters_data = validated_data.pop('characters', [])
        # extras_data = validated_data.pop('extras', [])
        # department_instructions_data = validated_data.pop('department_instructions', [])

        location = validated_data.get('location')

        geoapify_api_key = getattr(settings, 'GEOAPIFY_API_KEY')
        geoapify_url = f"https://api.geoapify.com/v1/geocode/search?text={location}&apiKey={geoapify_api_key}"
        geoapify_response = requests.get(geoapify_url)
        geoapify_data = geoapify_response.json()

        lat = geoapify_data['features'][0]['geometry']['coordinates'][1]
        lon = geoapify_data['features'][0]['geometry']['coordinates'][0]

        weatherapi_key = getattr(settings, 'WEATHERAPI_API_KEY')
        date = validated_data.get('date')

        
        today = datetime.today().date()

        if date <= today + timedelta(days=14):
            weatherapi_url = f"http://api.weatherapi.com/v1/current.json?key={weatherapi_key}&q={lat},{lon}"
        elif today + timedelta(days=14) < date <= today + timedelta(days=300):
            weatherapi_url = f"http://api.weatherapi.com/v1/future.json?key={weatherapi_key}&q={lat},{lon}&dt={date}"
        else:
            raise ValueError("Date must be within 14 to 300 days from today.")

        weatherapi_response = requests.get(weatherapi_url)
        weather_data = weatherapi_response.json()
        

        if 'forecast' in weather_data and 'forecastday' in weather_data['forecast']:
            forecast = weather_data['forecast']['forecastday'][0]['day']
            temperature = forecast.get('avgtemp_c', 0)
            conditions = forecast['condition']['text']
        else:
            temperature = 0
            conditions = "Weather data unavailable"

        call_sheet = CallSheet.objects.create(**validated_data)

        for event_data in events_data:
            Event.objects.create(call_sheet=call_sheet, **event_data)

        for call_time_data in call_time_data:
            CallTime.objects.create(call_sheet=call_sheet, **call_time_data)
        # for scene_data in scenes_data:
        #     Scenes.objects.create(call_sheet=call_sheet, **scene_data)
        # for character_data in characters_data:
        #     Characters.objects.create(call_sheet=call_sheet, **character_data)
        # for extra_data in extras_data:
        #     Extras.objects.create(call_sheet=call_sheet, **extra_data)
        # for instruction_data in department_instructions_data:
        #     DepartmentInstructions.objects.create(call_sheet=call_sheet, **instruction_data)

        Weather.objects.create(
            call_sheet=call_sheet,
            temperature=temperature,
            conditions=conditions
        )

        return call_sheet

    def update(self, instance, validated_data):
        events_data = validated_data.pop('events', [])
        call_time_data = validated_data.pop('call_time', [])
        # scenes_data = validated_data.pop('scenes', [])
        # characters_data = validated_data.pop('characters', [])
        # extras_data = validated_data.pop('extras', [])
        # department_instructions_data = validated_data.pop('department_instructions', [])
        weather_data = validated_data.pop('weather', [])

        # Update CallSheet instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create related models
        self.update_related_models(Event, events_data, instance)
        self.update_related_models(CallTime, call_time_data, instance)
        # self.update_related_models(Scenes, scenes_data, instance)
        # self.update_related_models(Characters, characters_data, instance)
        # self.update_related_models(Extras, extras_data, instance)
        # self.update_related_models(DepartmentInstructions, department_instructions_data, instance)
        self.update_related_models(Weather, weather_data, instance)

        return instance

    def update_related_models(self, model_class, data, call_sheet):
        existing_ids = set(item.id for item in model_class.objects.filter(call_sheet=call_sheet))
        data_ids = set(item.get('id') for item in data if item.get('id'))

        # Delete old items not present in the new data
        to_delete = existing_ids - data_ids
        if to_delete:
            model_class.objects.filter(id__in=to_delete).delete()

        # Update or create new items
        for item_data in data:
            item_id = item_data.get('id')
            if item_id:
                item = model_class.objects.get(id=item_id)
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                item.save()
            else:
                model_class.objects.create(call_sheet=call_sheet, **item_data)