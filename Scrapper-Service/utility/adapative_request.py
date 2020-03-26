import requests
import math

class AdaptiveRequest:
    def __init__(self):
        self.max_wait_time = 10
        self.num_fail = 0
        self.num_success = 0
    def get(self , link, **kwargs ):
        try:
            redirects = kwargs.get('redirects')
            if redirects and (redirects == True):
                res = requests.get(link , timeout = self.max_wait_time, allow_redirects=True)
            else:
                res = requests.get(link , timeout = self.max_wait_time)
            self.num_success +=1
            return res
        except (requests.HTTPError , requests.ConnectionError) as err:
            self.num_fail= self.num_fail+1
            if self.num_fail != self.num_success:
                self.max_wait_time = math.pow( 10 + 1/(self.num_success - self.num_fail) , self.num_fail)
            else:
                self.max_wait_time += 1
            raise err