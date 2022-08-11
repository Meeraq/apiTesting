
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from api.views import getCourses,addCourses,getLearners,addLearners,getBatches,addBatches,getcoach,addcoach,getfaculty,addfaculty

class TestUrls(SimpleTestCase):

    def test_course_url_is_resolved(self):
        url = reverse('get_course')
        self.assertEquals(resolve(url).func, getCourses)


    def test_add_course_url_is_resolved(self):
        url = reverse('add_course')
        self.assertEquals(resolve(url).func, addCourses)


    def test_learner_url_is_resolved(self):
        url = reverse('get_learner')
        self.assertEquals(resolve(url).func, getLearners)


    def test_add_learner_url_is_resolved(self):
        url = reverse('add_learner')
        self.assertEquals(resolve(url).func, addLearners)

    def test_batch_url_is_resolved(self):
        url = reverse('get_batch')
        self.assertEquals(resolve(url).func, getBatches)


    def test_add_batch_url_is_resolved(self):
        url = reverse('add_batch')
        self.assertEquals(resolve(url).func,addBatches)

    def test_coach_url_is_resolved(self):
        url = reverse('get_coaches')
        self.assertEquals(resolve(url).func, getcoach)


    def test_add_coach_url_is_resolved(self):
        url = reverse('add_coaches')
        self.assertEquals(resolve(url).func,addcoach)

    def test_faculty_url_is_resolved(self):
        url = reverse('get_faculty')
        self.assertEquals(resolve(url).func, getfaculty)


    def test_add_faculty_url_is_resolved(self):
        url = reverse('add_faculty')
        self.assertEquals(resolve(url).func,addfaculty)


