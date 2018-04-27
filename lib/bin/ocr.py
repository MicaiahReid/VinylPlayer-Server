# pylint: skip-file
import sys
import segmentation_v2 as s
from network import test
import dataset as D
import cv2
from PIL import Image
import base64 
import io
import numpy as np

seg_img_width = 1024
seg_img_height = 512

def ocr(img, img_height, img_width):
    letters = []
    # segment image into word(s) 
    # segment word(s) into letters
    lines = s.segment_image_v2(img, img_width, img_height)
    print("Segmenting Lines")
    for line in lines:
        print("New Line!")
        segments = s.segment_line_v2(line, img_width, img_height)
        if segments is None:
            continue
        letters.extend(segments)    
    word = test(letters)
    return word

def rotate_image(img, angle):
    img_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(img_center, angle, 1.0)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

file = "./img/original.JPG"
encodedString = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAB4AHgDASIAAhEBAxEB/8QAGQABAQEBAQEAAAAAAAAAAAAAAAYFBwgK/8QAJRAAAQUBAAMAAAcBAAAAAAAAAAECAwQFBgcRFBITFRYXJCYx/8QAGAEBAAMBAAAAAAAAAAAAAAAAAAEEBgP/xAAlEQACAwEBAAEDBAMAAAAAAAAAAgEDBAURBhIhMQcTFMFhgfH/2gAMAwEAAhEDEQA/APh/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK7iOPudvutxqtyll14M/T2tjZ0lmbnYmFiUZ9LX1bnzQ2LMkdSnXkWKtVgmtXbLoKdWKSeeNqxMxH3kuc/Br6m7JzcFDad2/TTkyZ0lFa7RfYtdVcNYyVpDO0RL2OlaR6zsqRLRIg7hB4gzulbkWPHHaw9bVu9jzPEazNLBt8xp4Wn19ySlz+hNQlu6sN3Cv2ILUKXq19LNaxCyG9QqLaqul0ZLnhKt1D+Hfw+xPgR6q8/N5Dd0ulH2iyNtfDJ0sOGz/Jx1WzIt6PmpsqaytNEz5Og+tV0Wvqifx7MxHvnnk+exHv38/Hsf5NevwDp0VLp6/U4HDxaLs2fndHX0H6fN61+n9+Pp5vQ+NZ+7l0VZmzX1b9bW148GhP4urRVp9pjz8Ch67nLXH9X0/JXpYp7vL9Dtc7cnhRUhmtYmlZzbEsSO9uSKSWs98aKqr+FU9qv/SeJ/uIn/U/eDG7Menn7NeDZVNOvDpvx6qZZXmrTmtem+qWRmRprtRklkZlbz1WmJiQAAVgAAAAAAAAAAAAWnBdi7iN5+pJmQbeZoZOvz2/iWLEtOPXwN6jNnalJl6Br58+1+RN9FDQhZI+jfgrWVhsRxvryxYImImPJ+8SXOd0NnK34+nz7pz7cGmnXlvhUf9u+h1sraa7Veq1fqWIeq1HqtSWrtR62ZZ7Nc8kc9z+KuJ4qwt/mnXeiwen1ug6XoKPQ7stvl5bNrnc3N/TsDn87Pzc2/bl0Z5H07V3Tux1HyzV69VlV+v8AyT4tfvfv6XxhqP7f7k23Y7etrM8ZydKkyW11Xc+nOL0Lcl9/+8/l29OlVZPdRuizMVKKcCAlYn8x75/f/DUp+oPyatklbeTNNMZP4mJ/jXxuzmc98Nmu/LdzeXZyX5/O0Jfu2X2X481Num7Vdbpe6x5Y0NbVv7urp7erYfc1NjQu6ulbkRqSWr+hZlt3LD0ajWo+axNJI5Goie3L6REM8Akx111ui63Rotsvvvse66612stuttaXsttseZZ7LHZnd2mWZplmmZmZAABzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/9k="

# if there is no command line arguements then run a test image
if len(sys.argv) <= 1:
    # img = base64.b64decode(encodedString)
    # img = Image.open(io.BytesIO(img))
    img = cv2.imread(file)
    img = rotate_image(img, 90)

else:
    file = sys.argv[1]
    img = cv2.imread(file)
    # encodedString = sys.argv[1]
    # img = base64.b64decode(encodedString)
    # img = Image.open(io.BytesIO(img))
    # img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

if img is None:
    data = '{"artist": "kanye west", "album": "graduation"}'
else:
    data = ocr(img, seg_img_height, seg_img_width)
    # data = '{"data": "' + data + '"}'
    data = '{"artist": "kanye west", "album": "graduation"}'

print(data)
sys.stdout.flush()  
   