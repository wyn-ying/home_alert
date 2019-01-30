import json
import time
import os
import requests
import ConfigParser

class facepp:
    def __init__(self):
        Config = ConfigParser.ConfigParser()
        Config.read('settings.conf')
        self.key = Config.get('facepp','key')
        self.secret = Config.get('facepp','secret')
        self.faceset_token = Config.get('facepp','facesettoken')
        self.face_id = Config.get('facepp','faceid')

    def set_faceset(self):
        url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/create'
        params = {
                'api_key':self.key,
                'api_secret':self.secret,
                }
        response = requests.post(url, data = params)
        req_dict = response.json()
        print("[DEBUG] set_faceset: %s"%req_dict)
        return req_dict


    def get_faceset(self):
        url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getfacesets'
        params = {
                'api_key':self.key,
                'api_secret':self.secret,
                }
        response = requests.post(url, data = params)
        req_dict = response.json()
        print("[DEBUG] get_faceset: %s"%req_dict)
        return req_dict


    def update_faceset(self):
        url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/update'
        params = {
                'api_key':self.key,
                'api_secret':self.secret,
                'faceset_token':self.faceset_token,
                'new_outer_id':'homemate',
                }
        response = requests.post(url, data = params)
        req_dict = response.json()
        print("[DEBUG] update_faceset: %s"%req_dict)
        return req_dict


    def detect_face(self, filepath):
        url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
        files = {'image_file': open(filepath, 'rb')}
        params = {
                'api_key':self.key,
                'api_secret':self.secret,
                }
        response = requests.post(url, data = params, files = files)
        req_dict = response.json()
        print('[DEBUG] detect_face: %s'%req_dict)
        return req_dict


    def set_face_userid(self, face_token, user_id):
        url = 'https://api-cn.faceplusplus.com/facepp/v3/face/setuserid'
        params = {
                'api_key':self.key,
                'api_secret':self.secret,
                'face_token':face_token,
                'user_id':user_id
                }
        response = requests.post(url, data = params)
        req_dict = response.json()
        print('[DEBUG] set_face_userid: %s'%req_dict)
        return req_dict


    def add_face(self, filepath, user_id, face_token=None, faceset_id='homemate'):
        if face_token is None:
            image = self.detect_face(filepath)
            face_token = image['faces'][0]['face_token']
        url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/addface'
        params = {
                'api_key':self.key,
                'api_secret':self.secret,
                'outer_id':faceset_id,
                'face_tokens':face_token,
                }
        response = requests.post(url, data = params)
        req_dict = response.json()
        print('[DEBUG] add_face: %s'%req_dict)

        self.set_face_userid(face_token, user_id)
        
        return req_dict


    def face_search(self, image_file, faceset_id='homemate'):
        url = 'https://api-cn.faceplusplus.com/facepp/v3/search'
        files = {'image_file': open(image_file, 'rb')}
        params = {
                'api_key':self.key,
                'api_secret':self.secret,
                'outer_id':faceset_id,
                }
        response = requests.post(url, data = params, files = files)
        req_dict = response.json()
        print('[DEBUG] face_search: %s'%req_dict)
        return req_dict


    def is_homemate(self, image_file, faceset_id='homemate'):
        req_dict = self.face_search(image_file, faceset_id)
        if 'results' not in req_dict.keys():
            print('\n[INFO] this face is failed to search with face ++.')
            return None
        user = req_dict["results"][0]["user_id"] 
        confidence = req_dict["results"][0]["confidence"]
        threshold = req_dict["thresholds"]["1e-4"]
        is_homemate = confidence >= threshold
        print('\n[INFO] this face is searched as %s, is homemate: %s, confidence: %s, 1e-4 threshold: %s'%(user, is_homemate, confidence, threshold))
        if user in ("ying", "wu") and is_homemate:
            return True
        else:
            return False

if __name__ == '__main__':
    f = facepp()
    # req_dict = f.set_faceset()
    # with open('faceset.txt', 'w') as f:
    #     json.dump(req_dict, f)

    # f.get_faceset()

    # f.update_faceset()
    
    # f.add_face('dataset/User.1.1.jpg', 'ying')
    # f.add_face('dataset/User.1.1.jpg', 'ying', f.face_id)
    # f.set_face_userid(f.face_id, 'ying')

    # for n in (2,3,4):
    #     for i in xrange(1,31):
    #         filepath = 'dataset/User.%d.%d.jpg'%(n,i) 
    #         print('now file: %s\n\n'%filepath)
    #         user_id = 'ying' if n in (1, 3) else 'wu'
    #         f.add_face(filepath, user_id)
    #         time.sleep(1.2)


    # f.face_search("dataset/User.1.15.jpg") ## 96.9
    # f.face_search("keychain.1.jpg") ## 82.0
    # f.face_search("dataset/User.2.15.jpg") ## 97.2
    # f.face_search("keychain.2.jpg") ## 87.4
    # f.face_search("keychain.jpg") ## 61.3
    # f.face_search("other.1.jpg") ## 52.3
    # f.face_search("other.2.jpg") ## 48.4
    f.is_homemate("dataset/User.2.28.jpg")
