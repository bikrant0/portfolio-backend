from rest_framework.test import APITestCase
from .models import PortfolioProject
from django.test.utils import CaptureQueriesContext
from django.db import connection
from .models import TechStack


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

        slugs = [p['slug'] for p in response.data['results']]
        
        self.assertIn('published-projects', slugs)
        self.assertNotIn('unpublished-projects', slugs)

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
            p = PortfolioProject.objects.create(title=f'P{i}', slug=f'p{i}', description='x', is_published=True
            )
            p.tech.stacks.add(tech)

        def test_project_list_query_count_stays_flat(self):
        # Tracking database hits during GET request.
            with CaptureQueriesContext(connection) as ctx:
                self.create.get('/api/v1/projects/')

            self.assertLessEqual(len(ctx.captured_queries), 4)

            with self.assertNumQueries(3):
                self.client.get('/api/v1/projects/')


