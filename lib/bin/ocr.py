import sys
import segmentation as seg
import dataset as D
import layers
import cv2

def ocr(img, img_height, img_width):
    seg.segment(img, img_height, img_width)
    return "Running OCR Was Succesful"


file = "./img/ciare_likeaboy_0002.JPG"
encoded = "iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAIAAAC2BqGFAAAAA3NCSVQICAjb4U/gAAAEhUlEQVR4\nnO3aTYhbVRjG8ec99yuTTDKZsfPRkenYQou0lUqLraIUHBRduHKhOxcuRNwIguheUHGruHOpIIo7\nQd21IEWwVEtRa6l1SjuO03GS Uxu7rnnuEjaWkVQiu/trc9/kw8S7s0vL4eTS6TZbIL995miT D/\nEqGVIrRShFaK0EoRWilCK0VopQitFKGVIrRShFaK0EoRWilCK0VopQitFKGVIrRStyd0LgBgDeL8\n pNeijod4DaD9oI4hzVIcohHxSINB jiYVyR1mFhR765xAN/GVLj4I08jPFD9cm6D5dc5/Ta5ZPB\nahqaXBC6wbsKKahUKoUd/CaSG24GTSB5bfLBR5q7LriNFfTuaIw8PXXPXZ3oVOdKVvREFX38f1x/\neCsZqiZ8tDIzGzV6Pv9hfek4rmyE3gCRl1fvvN9v2WeWP7PWWeOwjqmhxlvTR5 d33rbn7cmTHKb\nSzGrZWkmOvTwwE4z/OaOuelKY95vBtXkiel9u7vJN52lzOBobeapcMfzy8e6eZZGJnAegt9cd0G6\nz43u 3zlXComNyhqlS7NROcCA3lx  EL7aXXW1 nIQKPj9pn39k 93i68nF 8UBt8njn8kpgQ5Fq\nho0Ywz3kIj8uL4Szh/bGY1 6li9ujS7NrsM4PzY0vCcefbd9uhvBC6zBYrr xfrPj1VnQ0hYSRZ8\np5pBPHoBqhnWEiQ5tiRfQzaWh67QHV5poK2YejLU7XbbvmccQjfYRVzstcfiCHC9ja273bDxzhkX\neJcLKhbWoBbEY4iXnHUG4gv7vKWBNuJXbbcWV8YlMoA1SANkAWbD oLveMGJdHF229QOGwEuDRyA\nNERiMVedadnuKWkbV j5F3nwf5M1WF1fO2naL9cO1HuSC5LMH7HNJ6u7Pt2YF29OpIvfov3KxJHd\nm1HFAkCth4Px Av1/R 0vusE3pki99FSlr/t5mJi5xrD9TcmHmpu2u/Xfq0kycH69Cdr595rn7HG\niEctjF aPnyvHzm//MulINsTNXc2tn24evb91hmYIPceMF6KGezSQAPwAuMQm C 0Zm9MrKVZ19t\nLvzUa cCL9d/K 6vTjwQT0YmaGWdY1uXFrPNYq9y9CsTdD/xyMQnXhxgDQI/UO5D9x/2DAwQ5ega\nH3m5FaBLs4  ljMIvVgDAKHDn1beNACucluDQApclm ofND94e0P6bUVo3 /f Uo8MgF4gffwR9f\nU2Dlgwb 1m4wyFcXiv5rbgVllGh7V/YIrRShlSK0UoRWitBKEVopQitFaKUIrRShlSK0UoRWitBK\nEVopQitFaKUIrRShlSK0UoRWitBKEVopQitFaKUIrRShlSK0UoRWitBKEVopQitFaKUIrRShlSK0\nUoRWitBKEVopQitFaKUIrRShlSK0UoRWitBKEVopQitFaKUIrRShlSK0UoRWitBKEVopQitFaKUI\nrRShlSK0UoRWitBKEVopQitFaKUIrRShlSK0UoRWitBKEVopQitFaKUIrRShlSK0UoRWitBKEVop\nQitFaKUIrRShlfodF8d1EwKsUz4AAAAASUVORK5CYI"

# if there is no command line arguements then run a test image
if len(sys.argv) <= 1:
    img = cv2.imread(file)
    img_height = 512
    img_width = 1024
else:
    encodedImage = sys.argv[1]
    img = cv2.imread(encodedImage)
    img_height = sys.argv[2]
    img_width = sys.argv[3]

if img is None:
    print(encodedImage)
    sys.stdout.flush()
    sys.exit()
else:
    data = ocr(img, img_height, img_width)
    print("Hello from the ocr file")
    sys.stdout.flush()
    sys.exit()