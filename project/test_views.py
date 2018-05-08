from django.contrib.auth.models import User

from django.test import TestCase, Client

from django.core.urlresolvers import reverse

from .models import Project

TEST_USER_NAME  = 'test_user'
TEST_USER_EMAIL = 'test_user@nothere.com'
TEST_USER_PW    = 'test_user_pw'

TEST_PROJECT_FULLNAME = 'TEST PROJECT #1 FULL NAME'
TEST_PROJECT_DESCRIPTION_1 = ''
TEST_PROJECT_DESCRIPTION_2 = 'New description'

class Project_View_Test_Client(TestCase):
    def test_Project_All_Public(self):
        c = Client()
        response = c.get( reverse('project:all_public') )
        self.assertEqual( response.status_code, 200 )

    def test_Search_Project_Page_is_200(self):
        c = Client()
        response = c.get( reverse('project:search_public') )
        self.assertContains(response, '0 found.', status_code=200 )

    def test_Project_Index(self):
        c = Client()
        response = c.get( reverse('project:index') )
        self.assertContains(response, 'Please, log in to see your projects.', status_code=200 )

    def test_Long_Long(self):
        # no projects here
        self.assertEqual( Project.objects.count(), 0 )

        # create user
        if not User.objects.filter( username = TEST_USER_NAME ).exists():
            test_user = User.objects.create_user( username = TEST_USER_NAME, password = TEST_USER_PW )

        c = Client()
        # check for project search page is available for anon
        response = c.get( reverse('project:search_public'), { 'fullname' : TEST_PROJECT_FULLNAME } )
        self.assertContains(response, '0 found.', status_code=200 )

        # log in
        res = c.login( username = TEST_USER_NAME, password = TEST_USER_PW )
        self.assertTrue( res )

        # create new project with post
        response = c.post( reverse('project:project_add'), { 'fullname' : TEST_PROJECT_FULLNAME, 'description' : TEST_PROJECT_DESCRIPTION_1, } )
        # we are redirected to new project page
        self.assertEqual( response.status_code, 302 )

        # check project is created
        self.assertEqual( Project.objects.count(), 1 )
        test_project_1 = Project.objects.get(id=1)
        self.assertEqual( response.url, test_project_1.get_absolute_url() )
        self.assertEqual( test_project_1.fullname, TEST_PROJECT_FULLNAME )
        self.assertEqual( test_project_1.description, TEST_PROJECT_DESCRIPTION_1 )
        self.assertTrue( test_project_1.is_member( test_user ) )

        # check - new project is available in search page
        response = c.get( reverse('project:search_public'), { 'fullname' : TEST_PROJECT_FULLNAME } )
        self.assertContains(response, '1 found.', status_code=200 )

        response = c.get( reverse('project:search_public'), { 'fullname' : '-no-', 'description' : '-no-' } )
        self.assertContains(response, '0 found.', status_code=200 )

        # check - project page is available
        response = c.get( reverse('project:project_view', args = (1,) ) )
        self.assertContains(response, TEST_PROJECT_FULLNAME, status_code=200 )

        # check - project history page is available
        response = c.get( reverse('project:project_history', args = (1,) ) )
        self.assertContains(response, TEST_PROJECT_FULLNAME, status_code=200 )

        # check - project milestone list page is available
        response = c.get( reverse('project:project_view_milestones', args = (1,) ) )
        self.assertContains(response, TEST_PROJECT_FULLNAME, status_code=200 )

        # check form posting from edit page - set new description
        response = c.post( reverse('project:project_edit', args = (1,)), { 'fullname' : TEST_PROJECT_FULLNAME, 'description' : TEST_PROJECT_DESCRIPTION_2, } )
        self.assertEqual(response.status_code, 302 )
        test_project_1.refresh_from_db()

        self.assertEqual( test_project_1.description, TEST_PROJECT_DESCRIPTION_2 )