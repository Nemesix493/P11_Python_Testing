from locust import HttpUser, task

from tests.run_test_server import clubs, competitions

class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        response = self.client.get('')
    
    @task(2)
    def clubs_point(self):
        response = self.client.get('/clubs-points')
    
    @task
    def show_summary(self):
        response = self.client.post(
            '/showSummary',
            data = {
                'email': clubs[0]['email']
            }
        )
    
    @task
    def purchase_places(self):
        response = self.client.post(
            '/purchasePlaces',
            data = {
                'club': clubs[0]['name'],
                'competition': competitions[0]['name'],
                'numberOfPlaces': 1
            }
        )