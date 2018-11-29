import re
import unittest
from pyramid import testing
from pyramid.request import Request


class TestCORS(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

        self.config.registry.settings.update({
            'cors.Access-Control-Allow-Origin': '*'
        })

        self.config.include('pyramid_cors')

        # This should come first to intercept preflight requests
        self.config.add_cors_preflight_handler()

        # add a test view
        def view(request):
            return 'Hello'

        self.config.add_view(view, name='cors', cors=True, renderer='json', request_method='POST')
        self.config.add_view(view, name='nocors', renderer='json', request_method='GET')

    def tearDown(self):
        del self.config
        testing.tearDown()

    def test_deriver_registered(self):
        from pyramid.interfaces import IViewDerivers

        derivers = self.config.registry.getUtility(IViewDerivers)
        dlist = {d for (d, _) in derivers.sorted()}
        self.assertIn('cors_view', dlist)

    def test_default_headers(self):
        origin = 'http://example.com'
        app = self.config.make_wsgi_app()
        request = Request.blank('/cors', base_url=origin)
        request.method = 'POST'
        request.headers['Origin'] = origin
        response = request.get_response(app)
        self.assertTrue(response.headers.get('Access-Control-Allow-Methods'))
        self.assertTrue(response.headers.get('Access-Control-Allow-Headers'))
        self.assertTrue(response.headers.get('Access-Control-Allow-Origin'))
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], '*')

    def test_preflight_default_headers(self):
        origin = 'http://example.com'
        app = self.config.make_wsgi_app()
        request = Request.blank('/cors', base_url=origin)
        request.method = 'OPTIONS'
        request.headers['Origin'] = origin
        request.headers['Access-Control-Request-Method'] = 'GET'
        response = request.get_response(app)
        self.assertTrue(response.headers.get('Access-Control-Allow-Methods'))
        self.assertTrue(response.headers.get('Access-Control-Allow-Headers'))
        self.assertTrue(response.headers.get('Access-Control-Allow-Origin'))
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], '*')

    def test_preflight_allowed_origins_ok(self):
        origin = 'http://example.com'
        self.config.registry.settings['cors.allowed_origins'] = re.compile('http://example.com')
        app = self.config.make_wsgi_app()
        request = Request.blank('/cors', base_url=origin)
        request.method = 'OPTIONS'
        request.headers['Origin'] = origin
        request.headers['Access-Control-Request-Method'] = 'GET'
        response = request.get_response(app)
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], 'http://example.com')

    def test_preflight_allowed_origins_fail(self):
        origin = 'http://example.org'
        self.config.registry.settings['cors.allowed_origins'] = re.compile('http://example.com')
        app = self.config.make_wsgi_app()
        request = Request.blank('/cors', base_url=origin)
        request.method = 'OPTIONS'
        request.headers['Origin'] = origin
        request.headers['Access-Control-Request-Method'] = 'GET'
        response = request.get_response(app)
        self.assertNotIn('Access-Control-Allow-Origin', response.headers)

    def test_preflight_allowed_sub_domain_ok(self):
        origin = 'http://sub.example.com'
        self.config.registry.settings['cors.allowed_origins'] = re.compile('http://.*example.com')
        app = self.config.make_wsgi_app()
        request = Request.blank('/cors', base_url=origin)
        request.method = 'OPTIONS'
        request.headers['Origin'] = origin
        request.headers['Access-Control-Request-Method'] = 'GET'
        response = request.get_response(app)
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], 'http://sub.example.com')

    def test_preflight_allowed_sub_domain_fail(self):
        origin = 'http://sub.example.com'
        self.config.registry.settings['cors.allowed_origins'] = re.compile('http://example.com')
        app = self.config.make_wsgi_app()
        request = Request.blank('/cors', base_url=origin)
        request.method = 'OPTIONS'
        request.headers['Origin'] = origin
        request.headers['Access-Control-Request-Method'] = 'GET'
        response = request.get_response(app)
        self.assertNotIn('Access-Control-Allow-Origin', response.headers)

    def test_nocors_view_preflight(self):
        origin = 'http://example.com'
        app = self.config.make_wsgi_app()
        request = Request.blank('/nocors', base_url=origin)
        request.method = 'OPTIONS'
        request.headers['Origin'] = origin
        request.headers['Access-Control-Request-Method'] = 'GET'
        response = request.get_response(app)
        self.assertIn('Access-Control-Allow-Methods', response.headers)
        self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')

    def test_nocors_view(self):
        origin = 'http://example.com'
        app = self.config.make_wsgi_app()
        request = Request.blank('/nocors', base_url=origin)
        request.method = 'GET'
        request.headers['Origin'] = origin
        response = request.get_response(app)
        self.assertNotIn('Access-Control-Allow-Methods', response.headers)
        self.assertNotIn('Access-Control-Allow-Origin', response.headers)

    def test_no_origin(self):
        origin = 'http://example.com'
        app = self.config.make_wsgi_app()
        request = Request.blank('/cors', base_url=origin)
        request.method = 'POST'
        response = request.get_response(app)
        self.assertNotIn('Access-Control-Allow-Methods', response.headers)
        self.assertNotIn('Access-Control-Allow-Origin', response.headers)
