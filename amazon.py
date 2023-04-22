import requests
import pandas as pd
from bs4 import BeautifulSoup

# Using WEBSHARE.IO proxy for this project
# proxy_credential = http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_ADDRESS}:{PROXY_PORT}

proxies = {
    'http' : "http://",
    'https' : "http://"
}

# response = requests.get('https://ipinfo.io/json', proxies=proxies)
# print(response.json())
reviewList = []
# Create soup - get all content from website using proxy
def create_soup(reviewUrl):
    proxies = {
    'http' : "http://ucdcfrki-rotate:xrx5i8i3yztw@p.webshare.io:80",
    'https' : "http://ucdcfrki-rotate:xrx5i8i3yztw@p.webshare.io:80"
    }
    # response = requests.get(reviewUrl)
    response = requests.get(reviewUrl, proxies=proxies)
    soup = BeautifulSoup(response.text, "html.parser")
    print("Soup Created ✔✔✔✔✔✔✔✔✔✔✔✔✔✔✔✔✔✔✔✔✔")
    return soup

# review counter - how many reviews there
def review_counter(reviewUrl):
    soup = create_soup(reviewUrl)
    counter = soup.find('div', {'data-hook':'cr-filter-info-review-rating-count'})
    reviewNum = counter.text.strip().split(', ')[1].split(" ")[0]

    # if string value contains a comma
    if "," in reviewNum:
        reviewNum = reviewNum.replace(",","")
    return int(reviewNum)


# extract review 
def extract_review(reviewUrl):
    soup = create_soup(reviewUrl)
    reviews = soup.findAll('div',{'data-hook': "review"})

    for review in reviews:
        review_dict = {
            "Product Title" : soup.title.text.replace("Amazon.in:Customer reviews:","").strip(),
            "Review Title" : review.find('a', {'data-hook':"review-title"}).text.strip(),
            "Review Body" : review.find('span', {'data-hook':"review-body"}).text.strip(),
            "Rating" : review.find('i', {'data-hook':"review-star-rating"}).text.strip(),
            
        }
        reviewList.append(review_dict)
    

# Main 
def main():
    productUrl = "https://www.amazon.in/Samsung-Galaxy-Prime-Light-Blue/dp/B0BD3T6MGJ/ref=asc_df_B0BD3T6Z1D"
    # replace dp to product-reviews on url
    reviewUrl = productUrl.replace("dp", "product-reviews") + "?pageNumber=" 

    reviewNum = review_counter(reviewUrl+str(1))
    pageNum = int(reviewNum)//10
    print("Number of Pages : ",pageNum)

    for page in range(1, pageNum+1):
        print(f"Running for Page {page}📝📝📝....")
        pageUrl = reviewUrl + str(page)
        print(pageUrl)
        extract_review(pageUrl)

    print(reviewList)
    # create dataset using review list
    df = pd.DataFrame(reviewList)
    df.to_excel('amazon_reviews.xlsx', index=False)

main()