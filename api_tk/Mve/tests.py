# from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory,force_authenticate,APITestCase

from .models import MvModel
from .serializers import MvSerializer
from .views import MvDetail,Mvl
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

# class MvDetailTestCase(TestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.mv = MvModel.objects.create(title="Test Note",genre="some test",release_date="2023-07-06",director="surya")
#         self.url = f"/api/mv/{self.mv.pk}/"

#     def test_get_existing_mv(self):
#         request = self.factory.get(self.url)
#         view = MvDetail.as_view()
#         response = view(request, pk=self.mv.pk)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["status"], "success")
#         self.assertEqual(response.data["data"]["note"]["title"], "Test Note")

#     def test_get_nonexistent_mv(self):
#         request = self.factory.get("/api/mv/999/")
#         view = MvDetail.as_view()
#         response = view(request, pk=999)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data["status"], "fail")
#         self.assertEqual(
#             response.data["message"], "Note with Id: 999 not found"
#         )

#     def test_patch_existing_mv(self):
#         request = self.factory.patch(self.url, data={"title": "Updated Note"})
#         view = MvDetail.as_view()
#         response = view(request, pk=self.mv.pk)
#         print("response from request...",response)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["status"], "success")
#         self.assertEqual(
#             response.data["data"]["note"]["title"], "Updated Note"
#         )

#     def test_patch_nonexistent_mv(self):
#         request = self.factory.patch("/api/mv/999/", data={"title": "Updated Note"})
#         view = MvDetail.as_view()
#         response = view(request, pk=999)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data["status"], "fail")
#         self.assertEqual(
#             response.data["message"], "Note with Id: 999 not found"
#         )

#     def test_delete_existing_mv(self):
#         request = self.factory.delete(self.url)
#         view = MvDetail.as_view()
#         response = view(request, pk=self.mv.pk)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(MvModel.objects.filter(pk=self.mv.pk).exists())

#     def test_delete_nonexistent_mv(self):
#         request = self.factory.delete("/api/mv/999/")
#         view = MvDetail.as_view()
#         response = view(request, pk=999)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data["status"], "fail")
#         self.assertEqual(
#             response.data["message"], "Note with Id: 999 not found"
#         )

class MvDetailTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = AccessToken.for_user(self.user)
        self.mv = MvModel.objects.create(
            title="Test Note",
            genre="some test",
            release_date="2023-07-06",
            director="surya"
        )
        self.url = f"/api/mv/{self.mv.pk}/"
        self.url1 = f"/api/mv/"

    def test_get_existing_mv(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user, token=self.token)
        view = MvDetail.as_view()
        response = view(request, pk=self.mv.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["data"]["note"]["title"], "Test Note")

    def test_get_nonexistent_mv(self):
        request = self.factory.get("/api/mv/999/")
        force_authenticate(request, user=self.user, token=self.token)
        view = MvDetail.as_view()
        response = view(request, pk=999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["status"], "fail")
        self.assertEqual(response.data["message"], "Note with Id: 999 not found")

    def test_patch_existing_mv(self):
        request = self.factory.patch(self.url, data={"title": "Updated Note"})
        force_authenticate(request, user=self.user, token=self.token)
        view = MvDetail.as_view()
        response = view(request, pk=self.mv.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["data"]["note"]["title"], "Updated Note")

    def test_patch_nonexistent_mv(self):
        request = self.factory.patch("/api/mv/999/", data={"title": "Updated Note"})
        force_authenticate(request, user=self.user, token=self.token)
        view = MvDetail.as_view()
        response = view(request, pk=999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["status"], "fail")
        self.assertEqual(response.data["message"], "Note with Id: 999 not found")

    def test_delete_existing_mv(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, user=self.user, token=self.token)
        view = MvDetail.as_view()
        response = view(request, pk=self.mv.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MvModel.objects.filter(pk=self.mv.pk).exists())

    def test_delete_nonexistent_mv(self):
        request = self.factory.delete("/api/mv/999/")
        force_authenticate(request, user=self.user, token=self.token)
        view = MvDetail.as_view()
        response = view(request, pk=999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["status"], "fail")
        self.assertEqual(response.data["message"], "Note with Id: 999 not found")
    
    def test_mvl_api(self):
        request = self.factory.get(self.url1)
        force_authenticate(request,user=self.user,token=self.token)
        view = Mvl.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mvl_post_api(self):
        request = self.factory.post(self.url1,data={"title":"Test title","genre":"test","release_date":"2023-07-07","director":"test"})
        force_authenticate(request,user=self.user,token=self.token)
        view= Mvl.as_view()
        response = view(request)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"],"success")        

# class MovieTestCase(APITestCase):
#     def __init__(self):
#         self
#         self.url= f"/api/mv/"

#     def test_mvl_api(self):
#         request = self.factory.get(url)