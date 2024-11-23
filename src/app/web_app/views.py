from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Person
from .serializers import PersonSerializer


@csrf_exempt
def persons_api(request, id=None):
    if request.method == 'GET':
        if id:
            try:
                person = Person.objects.get(id=id)
                person_serializer = PersonSerializer(person)
                return JsonResponse(person_serializer.data, safe=False, status=status.HTTP_200_OK)
            except Person.DoesNotExist:
                return JsonResponse({'message': 'Person does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            persons = Person.objects.all()
            person_serializer = PersonSerializer(persons, many=True)
            return JsonResponse(person_serializer.data, safe=False, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        try:
            new_person = JSONParser().parse(request)
        except:
            return JsonResponse({'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        person_serializer = PersonSerializer(data=new_person)
        if person_serializer.is_valid():
            res = person_serializer.save()
            return HttpResponse(
                headers={'Location': f"/api/v1/persons/{res.id}"},
                status=status.HTTP_201_CREATED
            )
        else:
            return JsonResponse({'message': 'Person serializer error'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        try:
            upd_person = JSONParser().parse(request)
        except:
            return JsonResponse({'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            person = Person.objects.get(id=id)
        except Person.DoesNotExist:
            return JsonResponse({'message': 'Person does not exist'}, status=status.HTTP_404_NOT_FOUND)
        person_serializer = PersonSerializer(person, data=upd_person, partial=True)
        if person_serializer.is_valid():
            person_serializer.save()
            return JsonResponse(person_serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'Person serializer error'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            person = Person.objects.get(id=id)
        except Person.DoesNotExist:
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        person.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)