from django.test import TestCase
from django.shortcuts import reverse
from agents.models import Agent
from users.models import User, UserProfile
from .models import Lead



def create_agent():
    user = User.objects.create(username="ironman", password="djangocrm123")
    userProfile = UserProfile.objects.create(user=user)
    agent = Agent.objects.create(organisation=userProfile)
    return agent
    

class LeadModelTest(TestCase):
    
    def setUp(self):
        Lead.objects.create(
            first_name="dare", last_name="devil", 
            age="28", agent=create_agent()
        )
    
    def test_lead_creation(self):
        lead = Lead.objects.filter(first_name="dare")
        self.assertIs(lead.exists(), True)


class ViewTest(TestCase):
    
    def test_get(self):
        response = self.client.get(reverse("landing-page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing.html")
