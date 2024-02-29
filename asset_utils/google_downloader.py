import sys
import requests
import json

class CloudUtils():
    def download_file_from_google_drive(self, file_id, destination):
        URL = "https://docs.google.com/uc?export=download&confirm=1"

        session = requests.Session()

        response = session.get(URL, params={"id": file_id}, stream=True)
        token = self.get_confirm_token(response)

        if token:
            params = {"id": file_id, "confirm": token}
            response = session.get(URL, params=params, stream=True)

        self.save_response_content(response, destination)


    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value

        return None


    def save_response_content(self, response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)


    def download(self,file,dest):
        if len(sys.argv) >= 3:
            file_id = sys.argv[1]
            destination = sys.argv[2]
        else:
            file_id = file
            destination = dest
        print(f"dowload {file_id} to {destination}")
        self.download_file_from_google_drive(file_id, destination)


if __name__ == "__main__":
    aux = CloudUtils()

    with open("asset_info.json","r") as file:
        data = json.load(file)

    #file_id = data["asset1"]["link"]
    dest = "C:/Users/carlo/Desktop/python4production/WEEK3/production_assets"
    for asset in data.values():
        aux.download(asset["link"],dest+"/{}".format(asset["name"]))
