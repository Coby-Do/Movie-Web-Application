from django.test import TestCase

<<<<<<< Updated upstream
# Create your tests here.
=======
#Create your tests here.
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



class BadgeAndProfileTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.user)

    # Black-box Tests
    #
    # My cool-cam has to do with badge implementation, to create designiated badges
    # for users, each profile much be made. Therefore, I consider testing profiles as
    # a part of my cool-cam feature.
    #
    # 2. Tests user login success - ACCEPTANCE TEST
    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirection after successful login

    # 3. Tests user registration - ACCEPTANCE TERST
    def test_register_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'N3wP@ssw0rd!',
            'password2': 'N3wP@ssw0rd!',
        })
        self.assertEqual(response.status_code, 302)  # Redirection after successful registration

    # 4. Tests user logout - ACCEPTANCE TEST
    def test_logout_success(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirection after successful logout

    # White-box Tests

    # Tests badge creation - Provides coverage for the Badge model creation
    def test_create_badge(self):
        # Creating the badge
        badge = Badge.objects.create(name='Test Badge', description='Test Badge Description')

        # Testing if the badge exists
        self.assertEqual(badge.name, 'Test Badge')

    # Testing resetting badges - Provides branch and statement coverage for the reset_user_badges view
    def test_reset_badges(self):
        # Creating the badge and adding it to the user's profile
        badge = Badge.objects.create(name='Test Badge', description='Test Badge Description')
        self.user_profile.badges.add(badge)

        # Logging into the test client
        self.client.login(username='testuser', password='testpassword')

        # Sending a request to the rest_user_badges view
        response = self.client.post(reverse('reset_user_badges'))

        # Refresh the user_profile object to get updated data
        self.user_profile.refresh_from_db()

        # Checking to see if the badges has been reset
        self.assertEqual(self.user_profile.badges.count(), 0)
        self.assertEqual(response.status_code, 302)

    # Testing badge list to display badges - Provides statement coverage for badge_list view
    def test_badge_list_display(self):
        # Logging into the test client
        self.client.login(username='testuser', password='testpassword')

        # Creating the badges
        Badge.objects.create(name='Test Badge 1', description='Test Badge Description 1')
        Badge.objects.create(name='Test Badge 2', description='Test Badge Description 2')

        # Sending a request to the badge_list view
        response = self.client.get(reverse('badge_list'))
        self.assertEqual(response.status_code, 200)

        # Checking if the badges exist on the badge list display
        self.assertContains(response, 'Test Badge 1')
        self.assertContains(response, 'Test Badge 2')

    # Tests viewing profile - Provides statement coverage for profile view
    def test_view_profile(self):
        # Logging into the test client
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile', args=[self.user.username]))

        # Check if the response status code is successful
        self.assertEqual(response.status_code, 200)

        # Check if it contains the correct user's profile
        self.assertContains(response, self.user.username)

    # Testing number of movies watched - Provides statement coverage for UserProfile's movies_watched function
    def test_number_of_movies_watched(self):
        # Set the movies watched and save it to the user's profile
        self.user_profile.movies_watched = 2
        self.user_profile.save()

        # Get the user's profile from the database
        user_profile_from_db = UserProfile.objects.get(user=self.user)

        # Check if the movies_watched attribute matches the expected value
        self.assertEqual(user_profile_from_db.movies_watched, 2)

    # Testing earned badges displayed under 'Earned Badges' on profile page - Provides statement coverage for profile view when displaying earned badges
    def test_earned_badges_display(self):
        # Creating the badge
        badge = Badge.objects.create(name='Test Badge', description='Test Badge Description')

        # Add the badge to the user's profile
        self.user_profile.badges.add(badge)

        # Logging into the test client
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile', args=[self.user.username]))

        # Check if the badge is displayed
        self.assertContains(response, 'Test Badge')


    # Testing deleting badges - Provides statement coverage for the delete_badges view
    def test_delete_badges(self):
        # Creating the badges
        Badge.objects.create(name='Test Badge 1', description='Test Badge Description 1')
        Badge.objects.create(name='Test Badge 2', description='Test Badge Description 2')

        # Sending a request to the delete_badges view
        response = self.client.get(reverse('delete_badges'))

        # Check if the response status code is successful
        self.assertEqual(response.status_code, 200)

        # Check if all badges have been deleted from the database
        self.assertEqual(Badge.objects.count(), 0)

    # Testing Genre Enthusiast badge - Provides function coverage for GE badge from the check_badges function
    def test_genre_enthusiast_badge(self):
        # Create the Genre Enthusiast badge
        genre_enthusiast_badge = Badge.objects.create(
            name='Genre Enthusiast',
            description='Watched movies from 5 different genres.',
            badge_type='genres_watched',
            requirement=5
        )

        # Manually updating the user's profile for different genres and checking if the requirements are met
        self.user_profile.animated_movies_watched = 1
        self.user_profile.check_badges()
        self.user_profile.documentaries_watched = 1
        self.user_profile.check_badges()
        self.user_profile.action_movies_watched = 1
        self.user_profile.check_badges()
        self.user_profile.comedy_movies_watched = 1
        self.user_profile.check_badges()
        self.user_profile.romance_movies_watched = 1
        self.user_profile.check_badges()

        self.assertIn(genre_enthusiast_badge, self.user_profile.badges.all())

    # Integration Test

    # Testing badge creation, then checking if it's been displayed on the profile page
    #   This is a bottom-up integration because it's testing the individual units first,
    #   which are the Badge and UserProfile classes, then integrating them by testing
    #   the badge's creation, badge list display, and earned badges display.
    def test_badge_creation_and_display(self):
        # Logging into the test client
        self.client.login(username='testuser', password='testpassword')

        # Creating the badges
        badge1 = Badge.objects.create(name='Test Badge 1', description='Test Badge Description 1')
        badge2 = Badge.objects.create(name='Test Badge 2', description='Test Badge Description 2')

        # Testing badge display
        response = self.client.get(reverse('badge_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Badge 1')
        self.assertContains(response, 'Test Badge 2')

        # Adding the badges to the user's profile
        self.user_profile.badges.add(badge1)
        self.user_profile.badges.add(badge2)

        # Testing earned badges display on the profile page
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertContains(response, 'Test Badge 1')
        self.assertContains(response, 'Test Badge 2')

class ExtendedBadgeTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='usertest', password='testpassword')
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.user)

    # Acceptance Test
    # Tests partitions of test_romance_badge
    # Tests if romance movies watched below 5 (under requirement)
    def test_romance_badge_below_req(self):

        # Creates the romance enthusiast badge
        romance_enthusiast_badge = Badge.objects.create(
            name = 'Romance Enthusiast',
            description = 'Watched 5 Romance Movies.',
            badge_type = 'romance_movies_watched',
            requirement = 5
        )
        self.user_profile.romance_movies_watched = 4 # Sets romance movies watched to 4
        self.user_profile.check_badges()

        self.assertIn(romance_enthusiast_badge, self.user_profile.badges.all())  # Should not pass since below requirement for badge

    # Acceptance Test
    # Tests partitions of test_romance_badge
    # Tests if romance movies watched at 5 (requirement)
    def test_romance_badge_at_req(self):

        # Creates the romance enthusiast badge
        romance_enthusiast_badge = Badge.objects.create(
            name = 'Romance Enthusiast',
            description = 'Watched 5 Romance Movies.',
            badge_type = 'romance_movies_watched',
            requirement = 5
        )
        self.user_profile.romance_movies_watched = 5 # Sets romance movies watched to 5
        self.user_profile.check_badges()
        self.assertIn(romance_enthusiast_badge, self.user_profile.badges.all()) # Should pass assert

    # Acceptance Test
    # Tests partitions of test_romance_badge
    # Tests if romance movies watched at 6 (above requirement)
    def test_romance_badge_above_req(self):

        # Creates the romance enthusiast badge
        romance_enthusiast_badge = Badge.objects.create(
            name = 'Romance Enthusiast',
            description = 'Watched 5 Romance Movies.',
            badge_type = 'romance_movies_watched',
            requirement = 5
        )
        self.user_profile.romance_movies_watched = 6 # Sets romance movies watched to 6
        self.user_profile.check_badges()

        self.assertIn(romance_enthusiast_badge, self.user_profile.badges.all()) # Should pass assert


    # Whitebox Test. Provides branch coverage of function check_badges. Along with test_romance_badge_at_req, test_genre_enthusiast_badge (teammates test), test_documentaries_badge,
    # test_action_badge, test_movies_badge and test_comedy_badge provides 100% branch coverage.

    # def check_badges(self):
    #     newly_earned_badges = []
    #     badges = Badge.objects.all()
    #     genres_watched = self.update_genres_watched()
    #     for badge in badges:
    #         if badge.badge_type == 'movies_watched':
    #             if self.movies_watched >= badge.requirement and badge not in self.badges.all():
    #                 self.badges.add(badge)
    #                 newly_earned_badges.append(badge)
    #         elif badge.badge_type == 'genres_watched':
    #             if genres_watched >= badge.requirement and badge not in self.badges.all():
    #                 self.badges.add(badge)
    #                 newly_earned_badges.append(badge)
    #         elif badge.badge_type == 'animated_movies_watched':
    #             if self.animated_movies_watched >= badge.requirement and badge not in self.badges.all():
    #                 self.badges.add(badge)
    #                 newly_earned_badges.append(badge)
    #         elif badge.badge_type == 'documentaries_watched':
    #             if self.documentaries_watched >= badge.requirement and badge not in self.badges.all():
    #                 self.badges.add(badge)
    #                 newly_earned_badges.append(badge)
    #         elif badge.badge_type == 'action_movies_watched':
    #             if self.action_movies_watched >= badge.requirement and badge not in self.badges.all():
    #                 self.badges.add(badge)
    #                 newly_earned_badges.append(badge)
    #         elif badge.badge_type == 'comedy_movies_watched':
    #             if self.comedy_movies_watched >= badge.requirement and badge not in self.badges.all():
    #                 self.badges.add(badge)
    #                 newly_earned_badges.append(badge)
    #         elif badge.badge_type == 'romance_movies_watched':
    #             if self.romance_movies_watched >= badge.requirement and badge not in self.badges.all():
    #                 self.badges.add(badge)
    #                 newly_earned_badges.append(badge)
    #     self.save()
    #     return newly_earned_badges

    def test_animated_badge(self):
        # Creates animated badge
        animation_fan_badge = Badge.objects.create(
            name = 'Animation Fan',
            description = 'Watched 5 animated Movies.',
            badge_type = 'animated_movies_watched',
            requirement = 5
        )

        self.user_profile.animated_movies_watched = 5 # Sets romance movies to 5
        self.user_profile.check_badges()

        self.assertIn(animation_fan_badge, self.user_profile.badges.all()) # Should pass assert

    def test_documentaries_badge(self):
        # Creates documentary badge
        documentary_buff_badge = Badge.objects.create(
            name = 'Documentary Buff',
            description = 'Watched 3 documentaries.',
            badge_type = 'documentaries_watched',
            requirement = 3
        )

        self.user_profile.documentaries_watched = 3
        self.user_profile.check_badges()

        self.assertIn(documentary_buff_badge, self.user_profile.badges.all()) # Should pass assert

    def test_action_badge(self):
        # Creates action badge
        action_lover_badge = Badge.objects.create(
            name='Action Lover',
            description='Watched 5 action movies.',
            badge_type='action_movies_watched',
            requirement=5
        )

        self.user_profile.action_movies_watched = 5
        self.user_profile.check_badges()

        self.assertIn(action_lover_badge, self.user_profile.badges.all())  # Should pass assert

    def test_comedy_badge(self):
        # Creates comedy badge
        comedy_fan_badge = Badge.objects.create(
            name='Comedy Fan',
            description='Watched 5 comedy movies.',
            badge_type='comedy_movies_watched',
            requirement=5
        )

        self.user_profile.comedy_movies_watched = 5
        self.user_profile.check_badges()

        self.assertIn(comedy_fan_badge, self.user_profile.badges.all())  # Should pass assert

    def test_movies_badge(self):
        # Creates movies watched badge
        twenty_movies_watched_badge = Badge.object.create(
            name='20 Movies Watched',
            description='Watched 20 movies.',
            badge_type='movies_watched',
            requirement=20
        )
        self.user_profile.movies_watched = 20
        self.user_profile.check_badges()

        self.assertIn(twenty_movies_watched_badge, self.user_profile.badges.all()) # Should pass assert
>>>>>>> Stashed changes
