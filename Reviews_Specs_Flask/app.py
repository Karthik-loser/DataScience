from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def reviews():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})
            reviews = []
            for commentbox in commentboxes:
                try:
                    #name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    name = 'No Name'

                try:
                    #rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text


                except:
                    rating = 'No Rating'

                try:
                    #commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    #custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
            return render_template('reviews.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            #return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

@app.route('/specs',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def specs():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","+")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding = 'utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            specsboxes = prod_html.find_all('div', {'class': '_3k-BhJ'})
            subheaders = []
            contents = []
            headers = []
            dictionary = {}
            for i in specsboxes:
                header = []
                subheader = []
                content = []
                try :
                    header = i.div.text
                except :
                    header = "No Header"
                headers.append(header)
                dictionary = {key: None for key in headers}
                dictionary1 = {}
                for j in i.table.tbody:
                    # print(j.td.text)
                    # print(j.ul.li.text)
                    subheader.append(j.text)
                    try :
                        dictionary1[j.td.text] = j.ul.li.text
                    except :
                        dictionary1[j.td.text] = "No Content"
                # print(dictionary)
                # dictionary = {key: dictionary1 for key in headers}
                contents.append(dictionary1)
            # print(contents)
            for key in dictionary:
                try :
                    index = list(dictionary).index(key)
                # print(index)
                    dictionary[key] = contents[index]
                except:
                    dictionary[key] = "No Information"
            #print(dictionary)
            # print(specsboxes[i].table.tr.td)
            # print(specsboxes[i].table.tr.ul.li.text)
            # print(dictionary1)
            # print(dictionary[i])
            # print(contents)
            # print(subheaders)

            #print(headers)
            #print(contents)
            # print(subheaders)
            return render_template('specs.html',dictionary=dictionary )
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)
	#app.run(debug=True)
