import cv2
import numpy as np
import json
import base64
import requests
from requests.models import Response


class BlogCRAFTAPI:
    def __init__(
        self,
        url:str,
        api_key:str,
    ):
        self.url = url
        self.api_key = api_key
    
    @property
    def headers(self) -> str:
        return {"x-api-key": self.api_key}
    
    def inference(
        self,
        image:np.ndarray,
    ) -> list[list[int]]:
        """画像から文字領域検出

        Args:
            image (np.ndarray): _description_
            spacing (int, optional): _description_. Defaults to 10.

        Returns:
            list[list[int]]: _description_
        """
        result, image = cv2.imencode(".png", image)
        if not result:
            return []
        
        try:
            data = json.dumps({
                "image_bytes": base64.b64encode(image.tobytes()).decode("utf8"),
            })
            
            response:Response = requests.post(self.url, headers=self.headers, data=data)
            
            content = response.json()
            
            if content["statusCode"] == 200:
                bboxes:list[list[int]] = content["body"]["bboxes"]
                return bboxes
            else:
                return[]
        except Exception as e:
            return []


def my_app(url:str, api_key:str, image_path:str):
    blog_craft = BlogCRAFTAPI(url, api_key)
    
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    bboxes = blog_craft.inference(image)
    
    for idx, bbox in enumerate(bboxes):
        cv2.rectangle(image, bbox[:2], bbox[2:], (0, 255, 0), 1)
        cv2.putText(image, str(idx), (bbox[0]+1, bbox[1]+1), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(idx), bbox[:2], cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
    
    cv2.imshow("", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    cv2.waitKey()


if __name__ == "__main__":
    pass
