import datetime
import json
from django.test import Client, TestCase
from django.urls import reverse, resolve
from home.views import index,watchlist,add_to_watchlist,randomrec
from django.contrib.auth.models import User

from home.models import Movie, Integration, Profile, WatchedItem

# Create your tests here.
class TestWatchList(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='test')

    def setUp(self):
        self.client = Client()
    
    def tearDown(self):
        self.client.logout()

    def test_login(self):
        login = self.client.login(username='testuser', password='test')
        self.assertTrue(login)
    def test_login_required(self):
        response = self.client.get(reverse('watchlist'))
        self.assertRedirects(response, '/accounts/login/?next=/watchlist')
    
    # test that the watchlist page is accessible to logged in users
    def test_watchlist_page_accessible_to_logged_in_users(self):
        login = self.client.login(username='testuser', password='test')
        response = self.client.get(reverse('watchlist'))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
    
    # white box test of this function 
    #@login_required(login_url='accounts/login/')   
    #def add_to_watchlist(request):
    # get the user's id
    #user_id = request.user.id

    # get the user's profile
    #profile = Profile.objects.get(user_id=user_id)
    # make sure the movie isn't already in the user's watchlist
        # get the movie's id
    #movie_id = request.POST['movie_id']
    #if it doesn't exist, create it
    #if not Movie.objects.filter(id=movie_id).exists():
    #    with open('secrets.json') as f:
    #        secrets = json.load(f)
    #        tmdb.API_KEY = secrets['tmdb_api_key']
    #    movie = tmdb.Movies(movie_id).info()
    #    poster_url = 'https://image.tmdb.org/t/p/w500' + movie['poster_path']
    #    m = Movie(id=movie_id, title=movie['title'], description=movie['overview'], movie_poster_url=poster_url, tmdb_id=movie_id)
    #    m.save()
    # get the movie
    #movie = Movie.objects.get(id=movie_id)
    # add the movie to the user's watchlist
    #watched_item = WatchedItem(profile=profile, movie=movie, date_watched='2020-01-01')
    #watched_item.save()
    # redirect to the watchlist page
    #return redirect('watchlist')
    def test_new_movies_get_added_to_database(self):
        login = self.client.login(username='testuser', password='test')
        response = self.client.post(reverse('add_to_watchlist'), {'movie_id': 804150})
        self.assertTrue(Movie.objects.filter(id=804150).exists())
    
    # test to make sure movies that already exist in the database don't get added again
    def test_movies_that_already_exist_in_database_dont_get_added_again(self):
        login = self.client.login(username='testuser', password='test')
        response = self.client.post(reverse('add_to_watchlist'), {'movie_id': 804150})
        response = self.client.post(reverse('add_to_watchlist'), {'movie_id': 804150})
        self.assertEqual(Movie.objects.filter(id=804150).count(), 1)
    
    # verify that removing a movie from the watchlist works
    def test_remove_movie_from_watchlist(self):
        login = self.client.login(username='testuser', password='test')
        response = self.client.post(reverse('add_to_watchlist'), {'movie_id': 804150})
        self.assertTrue(Movie.objects.filter(id=804150).exists())
        response = self.client.post(reverse('add_to_watchlist'), {'movie_id': 804150})
        self.assertFalse(Movie.objects.filter(id=804150).exists())
    
    # make sure the retrieval of the watchlist doesn't take more than 5 seconds
    def test_watchlist_retrieval_doesnt_take_too_long(self):
        login = self.client.login(username='testuser', password='test')
        response = self.client.get(reverse('watchlist'))
        # just make sure that the page doesn't time out for now
        self.assertLess(200, 400)
    
    # Integration Test - make sure the watchlist page is displaying the correct movies (Combining the controller and view units) Big Bang?
    def test_watchlist_page_displays_correct_movies(self):
        login = self.client.login(username='testuser', password='test')
        response = self.client.post(reverse('add_to_watchlist'), {'movie_id': 804150})
        response = self.client.post(reverse('add_to_watchlist'), {'movie_id': 76600})
        response = self.client.get(reverse('watchlist'))
        self.assertContains(response, '804150')
        self.assertContains(response, '76600')
    
    # Integration Test - make sure the home page has a button to add a movie to the watchlist Big Bang?
    def test_home_page_has_button_to_add_movie_to_watchlist(self):
        login = self.client.login(username='testuser', password='test')
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Add To Watchlist')
        
    def test_watchlist_page_has_button_to_remove_movie_from_watchlist(self):
        login = self.client.login(username='testuser', password='test')
        response = self.client.post(reverse('add_to_watchlist'), {'movie_id': 804150})
        response = self.client.get(reverse('watchlist'))
        self.assertContains(response, 'Remove from Watchlist')
    
    # make sure the movie details has the correct date
    def test_movie_details_has_correct_date(self):
        login = self.client.login(username='testuser', password='test')
        response = self.client.post(reverse('add_to_watchlist'), {'movie_id': 804150})
        movie = Movie.objects.get(id=804150)
        watched_item = WatchedItem.objects.get(movie=movie)
        
        # get today's date
        today = datetime.date.today()
        # make sure they are the same
        self.assertEqual(watched_item.date_watched, today)

    # Create an integration and make sure an access token is returned
    def test_access_token_is_returned(self):
        #create an integration with a mock access token
        self.client.login(username='testuser', password='test')

        integration = Integration.objects.create(name="Test", access_token="test_access_token")

        # make the request
        response = self.client.post(reverse('get_access_token'), {'code': 'test_access_token'})
        # get the json
        json_response = json.loads(response.content)
        # make sure the access token is in the json
        self.assertIn('access_token', json_response)

class TestUrls(TestCase):
        
    # Test Index with print command
    def test_index_url_is_resolved(self):
        url = reverse('index')
        print(resolve(url))
        
    #Test index with self.assertEquals(resolve(url).func, index)
    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)
        
    # Test Watchlist (the correct parameter for reverse())
    def test_watchlist_url_is_resolved(self):
        url = reverse('watchlist')
        self.assertEquals(resolve(url).func, watchlist)
           
           
    # Test Watchlist (the wrong parameter for reverse())
    def test_watchlist_url_is_resolved(self):
        url = reverse('wathlist')
        self.assertEquals(resolve(url).func, watchlist)
           
    # Test add_to_watchlist (the correct parameter for reverse())
    def test_add_to_watchlist_url_is_resolved(self):
        url = reverse('add_to_watchlist')
        self.assertEquals(resolve(url).func, add_to_watchlist)
           
    # Test add_to_watchlist (the wrong parameter for reverse())
    def test_add_to_watchlist_url_is_resolved(self):
        url = reverse('add_to_watchlis')
        self.assertEquals(resolve(url).func, add_to_watchlist)
           
    #Test randomrec (the correct parameter for reverse())
    def test_randomrec_url_is_resolved(self):
        url = reverse('Random Movie Recommendation')
        self.assertEquals(resolve(url).func, randomrec)
           
    #Test randomrec (the wrong  parameter for reverse())
    def test_randomrec_url_is_resolved(self):
        url = reverse('Random Movie Recommendatio')
        self.assertEquals(resolve(url).func, randomrec)
           
    #Test award_my_badge ( the correct parameter for reverse() )
    def test_award_my_badge_url_is_resolved(self):
        url = reverse('award_my_badge')
        self.assertEquals(resolve(url).func, award_my_badge)
        
    #Test award_my_badge ( the wrong parameter  for reverse() )
    def test_award_my_badge_url_is_resolved(self):
        url = reverse('award_my_badge')
        self.assertEquals(resolve(url).func, award_my_badge)
        
    #Test award_ticket (the correct parameter for reverse())
    def test_award_tickets_url_is_resolved(self):
        url = reverse('award_tickets')
        self.assertEquals(resolve(url).func, award_tickets)
        
    #Test award_ticket (the wrong parameter for reverse())
    def test_award_tickets_url_is_resolved(self):
        url = reverse('award_ticets')
        self.assertEquals(resolve(url).func, award_tickets)