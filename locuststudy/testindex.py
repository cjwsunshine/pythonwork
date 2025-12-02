from locust import HttpUser,TaskSet, task

class testindex(TaskSet):
    @task
    def getIndex(self):
        self.client.get("/html/html-tutorial.html")
        print("here")
class WebSite(HttpUser):
    task_set = testindex
    min_wait = 1000
    max_wait =2000