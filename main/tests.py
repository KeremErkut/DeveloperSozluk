from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Topic, Entry
from .forms import EntryForm

User = get_user_model()


class TopicModelTest(TestCase):
    """Test suite for the Topic model."""

    def setUp(self):
        # Create a test user and topic for all tests in this class
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.topic = Topic.objects.create(title='Test Topic', created_by=self.user)

    def test_topic_creation(self):
        """Test that a topic can be created successfully."""
        self.assertEqual(self.topic.title, 'Test Topic')
        self.assertEqual(self.topic.created_by, self.user)
        self.assertIsNotNone(self.topic.created_at)

    def test_topic_str_representation(self):
        """Test the string representation of a topic."""
        self.assertEqual(str(self.topic), 'Test Topic')


class EntryModelTest(TestCase):
    """Test suite for the Entry model."""

    def setUp(self):
        # Create a test user and topic for entry tests
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.topic = Topic.objects.create(title='Another Test Topic', created_by=self.user)
        self.entry = Entry.objects.create(content='This is a test entry content.', author=self.user, topic=self.topic)

    def test_entry_creation(self):
        """Test that an entry can be created successfully and linked correctly."""
        self.assertEqual(self.entry.content, 'This is a test entry content.')
        self.assertEqual(self.entry.author, self.user)
        self.assertEqual(self.entry.topic, self.topic)

    def test_entry_str_representation(self):
        """Test the string representation of an entry."""
        self.assertTrue(len(str(self.entry)) <= 50)


class ViewTest(TestCase):
    """Test suite for the views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        # Login the client with the test user to access protected views
        self.client.login(username='testuser', password='password123')
        self.topic = Topic.objects.create(title='Test View Topic', created_by=self.user)
        self.entry = Entry.objects.create(content='Entry for topic detail.', author=self.user, topic=self.topic)

    def test_home_view(self):
        """Test that the home view returns a 200 status code and uses the correct template."""
        # Use a new client for unauthenticated tests
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')
        self.assertIn('page_obj', response.context)

    def test_topic_detail_view(self):
        """Test the topic detail view with a valid topic."""
        response = self.client.get(reverse('topic_detail', args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/topic_detail.html')
        self.assertEqual(response.context['topic'], self.topic)
        self.assertIn(self.entry, response.context['page_obj'])

    def test_topic_detail_view_not_found(self):
        """Test that an invalid topic id returns a 404."""
        response = self.client.get(reverse('topic_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_search_view(self):
        """Test that the search view can find topics."""
        response = self.client.get(reverse('search'), {'q': 'Test View'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/search_results.html')
        self.assertEqual(len(response.context['results']), 1)
        self.assertEqual(response.context['results'][0], self.topic)

    def test_protected_view_redirects_unauthenticated_user(self):
        """Test that a protected view redirects unauthenticated users to the login page."""
        # Use a new client for unauthenticated tests
        client = Client()
        response = client.get(reverse('create_topic'), follow=True)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('create_topic'))


class FormTest(TestCase):
    """Test suite for the forms."""

    def test_entry_form_valid_data(self):
        """Test that the entry form is valid with correct data."""
        form_data = {'content': 'This is a valid entry content.'}
        form = EntryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_entry_form_invalid_data(self):
        """Test that the entry form is invalid with missing data."""
        form_data = {}  # Empty data
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

