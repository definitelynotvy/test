import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, 
    TimeoutException, 
    WebDriverException
)
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import json

# Your cookie string
cookie_string = "SPC_T_ID=0R6FqrRjbyUO1L0FIDPeO0e0wMJI9G/Nx1y4vHbulllE8FcO5fMB+WXZ2eTRhj2gA1UvH1O6wx+vSg4j4ewJTepWp4DV0xbVGmB+sM+RptlsyiDZmIrmNz1QhXPlZiMwMGtMG+veMH8PrD3j22Ss+Bva0ZyxHkUZqw6nMnAbuns=;SPC_F=ZoeV5gF74pMOA028AQ98M04RpBv2uNXs;SPC_R_T_ID=0R6FqrRjbyUO1L0FIDPeO0e0wMJI9G/Nx1y4vHbulllE8FcO5fMB+WXZ2eTRhj2gA1UvH1O6wx+vSg4j4ewJTepWp4DV0xbVGmB+sM+RptlsyiDZmIrmNz1QhXPlZiMwMGtMG+veMH8PrD3j22Ss+Bva0ZyxHkUZqw6nMnAbuns=;SPC_SI=eTRhZwAAAABBT09OejA3OL4fBQAAAAAASjdSdkFHMjQ=;SPC_CDS_CHAT=2003c9ab-15db-44a9-955d-ac10f6f3647a;AC_CERT_D=U2FsdGVkX18axvhR11pj7WsCWSlNlGgEuxX9sSL8on7ZlckYm52P0qP6aoZlHFVeTSS4fW59EaXo8cnLnBqy1OMknaFBlKQlXJtgaOsRHZRw6NgqgsHyFBSR6+ND48zBXg1zb72MpYsEHV/YGnmQod0AdNyyP1Iu48uBUjOlAo3XdiFu/R0LdoKgRSEiwnlzZ6ITlxKSu8Zy2PgvvtClkuDdxq2UYZLnUvmxmBisvHMI6gp4cPoHtmMeoK2IhWP11k3O+YSYggakgTvve67A1SUWFC9CnTlJYGzUwHqnteTqnos6sJcvTFhXLze2jIJLdPqiY+lUA1A2eQsXDOnaIUE/bk/G7QjNfNmac2WJU6jVdlRfLwi0z5Bt8cLd65Vi34LwB/0QPHOev0Nr+qMEe+6fQvhLkapmCyL1uEqvNJTxNp+2fJGSrCKbf3yeau6nqJL7z0JNdZ2jMvZI+n/3Ke1MjBCj4szBOUjsZskEmmPz20mamwlAYOQBd6S0ZcD5nAGjYH2+1zlRa6OK/k+DA3zg9K2VL5XzbmMsIu6ZWcADcPK6jPS6e2FIF4uOSnxgg6wkiV9a6IxGjHNZ6+8zG9y9Gr5f616aL08jP6lhw0y/tOGjOQznpfPvAjj7/zHrVAjkbt4srAwyIlAYOzxQ9hfFjRCrKmleZOxh4Tah3+BxvMeBlzMVRUXuI9JdFFwDaMURvir4EGb2YzXw48rXfe2YKq7eXRhtX+UO0repgac0dtLlncCeR0xsZtQ2NxsComChZE+2YSg4M1Y1jiOb8BLlOtPxfuLUP7K5aV7f5pcblH0cgAdS3h1IqrRBe+nXysGK5bLZbBN6nuq/DENBtP9XlQhwq1MoiAjcsy3hzkEyV2SXuXZ2r/xCAQJXDL+Ob6miQtV9CrFlRV2DURxJP2RfcTqmxwPsVzlWeHVkc59HFuNVml9RHMmpPxh2ucFfhOPLm7JwIjyBiBVLxmxYI1RjwP1MPlv+5oeFjhoUmW3tiIsi8U2YT9iiE/Ll6lbw8BdzkKsDWE8mTs7v5dBf4DwaMSAHkdC1MhzH+yN4ZsMcVISTnzMlxtEHpQR3VfK4hzqJKsN7alBBwd5BdNPszg==;SPC_EC=.SjdwMkJQN2pWSHFiZVhLb6FbZDhUt22wvPiSug0OXYoJjyTEr88NfNGInNeXZ3KTPsvG8fSpR7NKK3xA5SOQq2/Ep/gUQIm4tf1Sz71Mm73bmyGy4zfXtXnWmABp7iHQJz/euASK06U26+7pqJ+/Dancnx4GPYNqDl05PaVlhmZ2zuNsRK6fkKJlHPtNpmIArJvyw2YrI3xvrkwNtj7WypAHNtAGxyAazYICGdhejVU=;__LOCALE__null=VN;_QPWSDCXHZQA=ca182b85-12e5-46af-c26e-fe6fea0b9192;_sapid=39b61973814c4f143cebd57180e99699b4245d16abc59581608e727a;csrftoken=VlExMWjfJd7aHrwfhpVC1DqORx4zTZ1l;ext_pgvwcount=1;REC7iLP4Q=7f9759b6-9b73-4ae8-9d06-0b413148e3aa;REC_T_ID=abaeffe7-d267-11ee-aa01-b6f4b4988612;SPC_CLIENTID=Wm9lVjVnRjc0cE1Pqfjjgbxxvrblveex;SPC_IA=1;SPC_R_T_IV=Mnd4ZHVJTG93U2YzY2xBcw==;SPC_SEC_SI=v1-VWZoZUFJQ29SSFh6cWxmcHHNurMmYngo+EloyEX0X3+vc0q1daV+G/xR8khdMzYbbkGIFYSkPMz554mtBKVrM6sdj3AHwL6fnyEzyckf+Wc=;SPC_ST=.SjdwMkJQN2pWSHFiZVhLb6FbZDhUt22wvPiSug0OXYoJjyTEr88NfNGInNeXZ3KTPsvG8fSpR7NKK3xA5SOQq2/Ep/gUQIm4tf1Sz71Mm73bmyGy4zfXtXnWmABp7iHQJz/euASK06U26+7pqJ+/Dancnx4GPYNqDl05PaVlhmZ2zuNsRK6fkKJlHPtNpmIArJvyw2YrI3xvrkwNtj7WypAHNtAGxyAazYICGdhejVU=;SPC_T_IV=Mnd4ZHVJTG93U2YzY2xBcw==;SPC_U=183314148" 


# Set up Chrome options
options = Options()
options.add_argument("--start-maximized")
# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Open Shopee website
driver.get("https://shopee.vn")
time.sleep(3)  # Allow page to load

# Parse and add cookies
cookies = cookie_string.split('; ')
for cookie in cookies:
    try:
        name, value = cookie.split('=', 1)
        cookie_dict = {'name': name, 'value': value, 'path': '/'}
        driver.add_cookie(cookie_dict)
    except Exception as e:
        print(f"Failed to add cookie: {cookie} - {e}")

# Refresh the page to apply cookies
driver.refresh()
time.sleep(5)

print("Cookies added successfully!")
driver.quit()