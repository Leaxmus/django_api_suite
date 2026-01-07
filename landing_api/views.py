from django.shortcuts import render

# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Firebase Admin SDK
from firebase_admin import db

# Python
from datetime import datetime


class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "usuarios"

    def get(self, request):
        ref = db.reference(self.collection_name)
        data = ref.get()

        return Response(
            {
                "data": data,
                "timestamp": datetime.utcnow()
            },
            status=status.HTTP_200_OK
        )
    def post(self, request):
        data = request.data

        if not data:
            return Response(
                {"error": "No data provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ref = db.reference(self.collection_name)

        # push() crea un ID único automáticamente
        new_record = ref.push({
            **data,
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
