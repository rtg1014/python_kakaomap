from flask import Flask, render_template, request
import requests
import folium

app = Flask(__name__)

def search_places(keyword, kakao_api_key):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
    params = {"query": keyword}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data.get("documents", [])

def create_map(places_data):
    if not places_data:
        return None

    map_center = (places_data[0]["y"], places_data[0]["x"])
    map = folium.Map(location=map_center, zoom_start=16, width=500, height=400)

    for place in places_data:
        marker = folium.Marker(location=(place["y"], place["x"]), popup=place["place_name"])
        map.add_child(marker)

    return map._repr_html_()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        keyword = request.form["keyword"]
        kakao_api_key = "YOUR_KAKAO_API_KEY"  # 발급받은 카카오 API 키 입력
        places_data = search_places(keyword, kakao_api_key)

        map_result = create_map(places_data)

        return render_template("index.html", keyword=keyword, map_result=map_result, places_data=places_data)
    
    return render_template("index.html", keyword="", map_result=None, places_data=None)

if __name__ == "__main__":
    app.run(debug=True)