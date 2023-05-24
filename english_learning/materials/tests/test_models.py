from django.test import TestCase
from ..models import UserProfile, User, Commens


class ModelsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create(first_name='User', username='naya', last_name='lsnm' )
        Commens.objects.create(user=User.objects.get(id=1), is_published=True, comment='comment from inside')
        UserProfile.objects.create(user=User.objects.get(id=1), phone='0987654321', is_approved=True)
       
    def test_phone_lable(self):
        user = UserProfile.objects.get(id=1)
        field_label = user.phone
        self.assertEqual(field_label, '0987654321')

    def test_phone_max_length(self):
        user = UserProfile.objects.get(id=1)
        max_length = user._meta.get_field('phone').max_length
        self.assertEqual(max_length, 13)

    def test_is_uprroved(self):
        user = UserProfile.objects.get(id=1)
        is_approved = user.is_approved
        self.assertTrue(is_approved)
    
    def test_comments_is_published(self):
        coment = Commens.objects.get(id=1)
        is_published = coment.is_published
        self.assertTrue(is_published)
