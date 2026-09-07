from rest_framework.test import APITestCase
from .models import PortfolioProject
from django.test.utils import CaptureQueriesContext
from django.db import connection
from .models import TechStack
from django.core.cache import cache
from .models import ApiPlaygroundLog

# Create your tests here.
class HealthCheckTest(APITestCase):
    def test_health_check_returns_200_ok(self):
        url = '/api/v1/health/'

        response = self.client.get(url)

        self.assertEqual(response.status_code,200)

        self.assertEqual(response.data['status'], 'healthy')

    def test_project_list_returns_200_ok(self):
        url = '/api/v1/projects/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertIn('results', response.data)

class ProjectListPublishedFilterTest(APITestCase):
    def setUp(self):
        self.published = PortfolioProject.objects.create(
            title='Published Projects',
            slug = 'published-projects',
            description = 'visible',
            is_published = True,
        )
        self.unpublished = PortfolioProject.objects.create(
            title='Unpublished Project',
            slug='unpublished-project',
            description='hidden',
            is_published=False,
        )

    def test_list_excludes_unpublished_projects(self):
        response = self.client.get('/api/v1/projects/')
        self.assertEqual(response.status_code, 200)

        slug = [p['slug'] for p in response.data['results']]
        
        self.assertIn('published-projects', slug)
        self.assertNotIn('unpublished-projects', slug)

    def test_search_matches_title(self):
        response = self.client.get('/api/v1/projects/', {'search':'Published'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'] ,1)

    def test_pagination_page_size_and_next_link(self):
        for i in range(6):
            PortfolioProject.objects.create(
                title=f"Bulk Project {i}",
                slug=f"bulk-project-{i}",
                description="Testing pagination",
                is_published=True
            )
        response = self.client.get('/api/v1/projects/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 5)

        self.assertIsNotNone(response.data['next'])



class ProjectDetailTest(APITestCase):
    def setUp(self):
        self.project = PortfolioProject.objects.create(
            title = "Detail Project",
            slug = "detail-project",
            description="Testing the detail view",
            is_published = True
        )

    def test_valid_slug_returns_200(self):
        response = self.client.get(f'/api/v1/projects/{self.project.slug}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "Detail Project")

    def test_invalid_slug_returns_404(self):
        response = self.client.get(f'/api/v1/projects/this-fake-slug-does-bot-exist/')
        self.assertEqual(response.status_code, 404)

# Query count regression test
class QueryCountTest(APITestCase):
    def setUp(self):
        # Arranging tech stack and like to thier projects
        tech = TechStack.objects.create(name='Django', category='Backend')
        for i in range(5):
            p = PortfolioProject.objects.create(
                title=f'P{i}', slug=f'p{i}',
                description='x', 
                is_published=True
            )
            p.tech_stacks.add(tech)

    def test_project_list_query_count_stays_flat(self):
        # Tracking database hits during GET request.
            with CaptureQueriesContext(connection) as ctx:
                self.client.get('/api/v1/projects/')

            self.assertLessEqual(len(ctx.captured_queries), 4)
            
# Testing Throttling
class ApiPlaygroundTest(APITestCase):
    def tearDown(self):
        cache.clear()

    def  test_valid_api_playground(self):
        response = self.client.post('/api/v1/playground/echo/', {'message': 'test1'}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('received_message'),'test1')


    def test_invalide_post_returns_400(self):
        response = self.client.post('/api/v1/playground/echo/', {}, format = 'json')

        self.assertEqual(response.status_code, 400)


    def test_logs_request_to_database(self):
        
        self.client.post('/api/v1/playground/echo/', {'message': 'hi'}, format='json')
        self.assertEqual(ApiPlaygroundLog.objects.count(), 1)
        log = ApiPlaygroundLog.objects.first()
        self.assertIsNotNone(log.ip_hash)
        self.assertGreaterEqual(log.latency_ms, 0)

class PlaygroundThrottleTest(APITestCase):
    def setUp(self):
        cache.clear()  # throttle counts persist in cache across tests
    def test_exceeds_rate_limit_returns_429(self):
        for _ in range(5):  # matches settings.py: 'playground_echo': '5/min'
            response = self.client.post('/api/v1/playground/echo/', {'message': 'hi'}, format='json')
            self.assertEqual(response.status_code, 200)

        sixth = self.client.post('/api/v1/playground/echo/', {'message': 'hi'}, format='json')
        self.assertEqual(sixth.status_code, 429)


class CorsHeadersTest(APITestCase):
    def test_allowed_origin_receives_cors_header(self):
        response = self.client.get('/api/v1/health/', HTTP_ORIGIN='http://localhost:5500')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Access-Control-Allow-Origin'), 'http://localhost:5500')

    def test_disallowed_origin_omits_cors_headers(self):
        response = self.client.get('/api/v1/health/', HTTP_ORIGIN='http://unauthorized-domain.com')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.has_header('Access-Control-Allow-Origin'))


class ErrorResponseTest(APITestCase):
    def test_404_returns_frontend_friendly_json(self):
        response = self.client.get('/api/v1/projects/this-slug-does-not-exist/')
        self.assertEqual(response.status_code, 404)

        self.assertEqual(response['Content-Type'],'application/json')

        self.assertIn('detail', response.json())