from django.test import TestCase
from django.urls import reverse, resolve
from home.views import index,watchlist,add_to_watchlist,randomrec, award_my_badge, award_tickets

# Create your tests here.

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