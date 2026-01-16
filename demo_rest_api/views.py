from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

data_list = []

data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False})

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request, item_id=None):
        active_items = [item for item in data_list if item.get('is_active', False)]

        if not active_items:
            return Response(
                {'message': 'No hay registros activos.'},
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request, item_id=None):
        data = request.data.copy()

        if not data.get('name') or not data.get('email'):
            return Response(
                {'message': 'Los campos name y email son obligatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_item = {
            'id': str(uuid.uuid4()),
            'name': data['name'],
            'email': data['email'],
            'is_active': True
        }

        data_list.append(new_item)

        return Response(
            {'message': 'Dato guardado exitosamente.', 'data': new_item},
            status=status.HTTP_201_CREATED
        )

    def put(self, request, item_id):
        data = request.data.copy()

        for item in data_list:
            if item['id'] == str(item_id):
                if not data.get('name') or not data.get('email'):
                    return Response(
                        {'message': 'PUT requiere name y email.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                item['name'] = data['name']
                item['email'] = data['email']
                item['is_active'] = data.get('is_active', item['is_active'])

                return Response(
                    {'message': 'Registro actualizado completamente.', 'data': item},
                    status=status.HTTP_200_OK
                )

        return Response(
            {'message': 'Registro no encontrado.'},
            status=status.HTTP_404_NOT_FOUND
        )

    def patch(self, request, item_id):
        data = request.data.copy()

        for item in data_list:
            if item['id'] == str(item_id):
                item['name'] = data.get('name', item['name'])
                item['email'] = data.get('email', item['email'])
                item['is_active'] = data.get('is_active', item['is_active'])

                return Response(
                    {'message': 'Registro actualizado parcialmente.', 'data': item},
                    status=status.HTTP_200_OK
                )

        return Response(
            {'message': 'Registro no encontrado.'},
            status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request, item_id):
        for item in data_list:
            if item['id'] == str(item_id):
                item['is_active'] = False
                return Response(
                    {'message': 'Registro desactivado correctamente.'},
                    status=status.HTTP_200_OK
                )

        return Response(
            {'message': 'Registro no encontrado.'},
            status=status.HTTP_404_NOT_FOUND
        )
