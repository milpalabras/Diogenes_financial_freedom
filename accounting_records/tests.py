from django.test import TestCase
from.models import Account, Category
from django.contrib.auth.models import User

class AccountTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):        
        cls.user = User.objects.create_user(username='test', password='test')

    def setUp(self):
        Account.objects.create(name="test", amount=1000, owner=self.user)

    def test_account(self):
        account = Account.objects.get(name="test")
        self.assertEqual(account.name, 'test')
        self.assertEqual(account.amount, 1000)
        self.assertEqual(account.owner.username, 'test')
        self.assertEqual(self.user.accounts.all()[0].name, 'test')


class CategoryTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='test')

    
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', category_type='F', owner=self.user)

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_parent(self):
        child_category = Category.objects.create(name='child category', category_type='F', owner=self.user, parent=self.category)         
        self.assertEqual(child_category.get_parent(), self.category)
        self.assertEqual(list(child_category.get_ancestors()), [self.category])

    def test_category_children(self):
        child_category = Category.objects.create(name='Child Category', category_type='F', owner=self.user)
        self.category.children.add(child_category)
        self.assertEqual(list(self.category.get_children()), [child_category])

    def test_category_all_children(self):
        child_category = Category.objects.create(name='Child Category', category_type='F', owner=self.user, parent=self.category)
        grandchild_category = Category.objects.create(name='Grandchild Category', category_type='F', owner=self.user, parent=child_category)        
        self.assertEqual(list(self.category.get_all_children()), [self.category, child_category, grandchild_category])

    def test_category_all_children_id(self):
        child_category = Category.objects.create(name='Child Category', category_type='F', owner=self.user, parent=self.category)
        grandchild_category = Category.objects.create(name='Grandchild Category', category_type='F', owner=self.user, parent=child_category)        
        self.assertEqual(list(self.category.get_all_children_id()), [ self.category.id,child_category.id, grandchild_category.id])

    def test_category_all_children_count(self):
        child_category = Category.objects.create(name='Child Category', category_type='F', owner=self.user, parent=self.category)
        grandchild_category = Category.objects.create(name='Grandchild Category', category_type='F', owner=self.user, parent=child_category)        
        self.assertEqual(self.category.get_descendant_count(), 2)

    def test_category_get_next_sibling(self):
        child_category_1 = Category.objects.create(name='Child Category', category_type='F', owner=self.user, parent=self.category)
        child_category_2 = Category.objects.create(name='Grandchild Category', category_type='F', owner=self.user, parent=self.category)        
        self.assertEqual(child_category_1.get_next_sibling(), child_category_2)