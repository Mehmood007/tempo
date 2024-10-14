from locust import HttpUser, between, task


class FastAPIUser(HttpUser):
    wait_time = between(0.1, 0.5)

    def on_start(self):
        # Authenticate and store the access token
        response = self.client.post(
            '/token',
            data={'username': 'testuser1', 'password': 'securepassword'},
        )
        if response.status_code == 200:
            self.token = response.json().get('access_token')
        else:
            self.token = None

    @task
    def get_friends(self):
        self.client.get(
            '/friends', headers={'Authorization': f'Bearer {self.token}'}
        )

    @task
    def get_non_friends(self):
        self.client.get(
            '/not-friends', headers={'Authorization': f'Bearer {self.token}'}
        )

    @task
    def get_health_check(self):
        self.client.get('/')
