from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from Mve.models import MvModel
from Mve.serializers import MvSerializer
import math
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
# Create your views here.
class CustomPage(PageNumberPagination):
    page_size_query_param = 'page_size'  # Set the query parameter for page size
    max_page_size = 100

class Mvl(generics.GenericAPIView):
    serializer_class = MvSerializer
    queryset = MvModel.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['genre', 'director']

    def get(self, request):
        # notes = MvModel.objects.all()
        notes = self.filter_queryset(self.get_queryset())
        paginator = CustomPage()
        paginated_notes = paginator.paginate_queryset(notes, request)
        serializer = self.serializer_class(paginated_notes, many=True)
        # print(type(paginator.get_paginated_response(serializer.data)))
        return paginator.get_paginated_response(serializer.data)
    # def get(self, request):
    #     # notes = MvModel.objects.all()
    #     notes = self.filter_queryset(self.get_queryset())
    #     if request.GET.get('form_size'):
    #         paginator = CustomPage()
    #         paginated_notes = paginator.paginate_queryset(notes, request)
    #         serializer = self.serializer_class(paginated_notes, many=True)
    #         return paginator.get_paginated_response(serializer.data)
   
    #     else:
    #         serializer = self.serializer_class(MvModel.objects.all(),many=True)
    #         return Response({"status": "success", "data": {"note": serializer.data}}, status=status.HTTP_200_OK)

        # print(type(paginator.get_paginated_response(serializer.data)))
        

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MvDetail(generics.GenericAPIView):
# queryset = NoteModel.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = MvSerializer
    def get_mv(self, pk):
        try:
            return MvModel.objects.get(pk=pk)
        except:
            return None
    def get(self, request, pk):
        rec = self.get_mv(pk=pk)
        if rec == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(rec)
        return Response({"status": "success", "data": {"note": serializer.data}})
    def patch(self, request, pk):
        rec = self.get_mv(pk)
        if rec == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            rec, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            # serializer.validated_data['updatedAt'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        rec = self.get_mv(pk)
        if rec == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
        rec.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)