
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from api.views import getcoach,addcoach,getAdminRequestData

class TestUrls(SimpleTestCase):



    def test_coach_url_is_resolved(self):
        url = reverse('get_coaches')
        self.assertEquals(resolve(url).func, getcoach)


    def test_add_coach_url_is_resolved(self):
        url = reverse('add_coaches')
        self.assertEquals(resolve(url).func,addcoach)

    def test_get_admin_request_url(self):
        url = reverse('get_admin_request')
        self.assertEquals(resolve(url).func,getAdminRequestData)
    
    