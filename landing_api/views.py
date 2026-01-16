from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from firebase_admin import db

from datetime import datetime


class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "usuarios"

    def get(self, request, item_id=None):
        """Obtiene todos los registros o uno específico por ID"""
        ref = db.reference(self.collection_name)
        
        if item_id:
            record_ref = ref.child(item_id)
            data = record_ref.get()
            
            if data is None:
                return Response(
                    {"error": "Registro no encontrado"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(
                {
                    "id": item_id,
                    "data": data
                },
                status=status.HTTP_200_OK
            )
        
        data = ref.get()

        return Response(
            {
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            },
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        """Crea un nuevo registro"""
        data = request.data

        if not data:
            return Response(
                {"error": "No data provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ref = db.reference(self.collection_name)

        new_record = ref.push({
            **data,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat()
        })

        return Response(
            {
                "message": "Record created successfully",
                "id": new_record.key,
                "data": data
            },
            status=status.HTTP_201_CREATED
        )
    
    def put(self, request, item_id):
        """Reemplaza completamente los datos de un registro, excepto el ID"""

        data = request.data

        required_fields = {"nombre", "correo", "edad", "is_active"}

        if not data:
            return Response(
                {"error": "No data provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        missing_fields = required_fields - data.keys()
        if missing_fields:
            return Response(
                {
                    "error": "Campos requeridos faltantes",
                    "missing_fields": list(missing_fields)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        ref = db.reference(f"{self.collection_name}/{item_id}")
        current = ref.get()

        if current is None:
            return Response(
                {"error": "Registro no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        sanitized_data = {
            "nombre": data["nombre"],
            "correo": data["correo"],
            "edad": data["edad"],
            "updated_at": datetime.utcnow().isoformat()
        }

        ref.set(sanitized_data)

        return Response(
            {
                "message": "Registro actualizado completamente",
                "id": item_id,
                "data": sanitized_data
            },
            status=status.HTTP_200_OK
        )


    def patch(self, request, item_id):
        """Actualiza parcialmente los campos de un registro"""
        data = request.data
        
        if not data:
            return Response(
                {"error": "No data provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ref = db.reference(f"{self.collection_name}/{item_id}")
        
        existing_data = ref.get()
        if existing_data is None:
            return Response(
                {"error": "Registro no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        ref.update({
            **data,
            "updated_at": datetime.utcnow().isoformat()
        })
        
        return Response(
            {
                "message": "Registro actualizado parcialmente",
                "id": item_id,
                "data": data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, item_id):
        """Elimina lógicamente un registro (soft delete)"""
        ref = db.reference(f"{self.collection_name}/{item_id}")
        
        existing_data = ref.get()
        if existing_data is None:
            return Response(
                {"error": "Registro no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        ref.update({
            "is_active": False,
            "deleted_at": datetime.utcnow().isoformat()
        })
        
        return Response(
            {
                "message": "Registro eliminado correctamente",
                "id": item_id
            },
            status=status.HTTP_200_OK
        )
