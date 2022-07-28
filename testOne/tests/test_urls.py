


from django.test import SimpleTestCase
from django.urls import reverse,resolve
from api.views import getCourses,addCourses,getLearners,addLearners

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


