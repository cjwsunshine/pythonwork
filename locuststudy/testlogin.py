from locust import HttpUser,TaskSet, task

class testlogin(TaskSet):
    @task
    def doLogin(self):
        self.client.get("/html/html-tutorial.html")
        print("here")
class WebSite(HttpUser):
    task_set = testlogin
    min_wait = 1000
    max_wait =2000