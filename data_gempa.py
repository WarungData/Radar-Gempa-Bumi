'''
Ini adalah penampil gempa bumi setelah kejadian yang saya rasakan
pada 2 Agustus 2019 ada gempa di Indonesia. M 6.9 - 102km WSW of Tugu Hilir, Indonesia
di 7.267°S 104.825°E, kedalaman 52.8 km.

Masih terlalu kasar untuk persiapan pengembangan
notifikasi dan pemberitahuan pra gempa..

Semoga bermanfaat.

_drat_

'''


import json
import pandas as pd
import numpy as np
import urllib.request


#
# Untuk mengambil data gempa di situs informasi gempa usgs
#
class Data_GempaBumi():

    def __init__():
        pass

    def getDataFile():
        try:
            with open("gempabumi.json", 'r') as f:
                data = f.read()
        except FileNotFoundError:
            return None
        except:
            print("[-] File error!")
            return None
        return json.loads(data)

    # Ambil data dari website
    def ambilDataWeb(urlData):
        print(urlData)
        try:
            alamatWebGempa = urllib.request.urlopen(urlData)
        except urllib.error.URLError as e:
            msg = "\n [-] Error dari website - " + str(e.code) + " - " + str(e.reason) + " dari\n" + urlData
            if e.code == 400:
                msg = msg + "\n[-] Kesalahan ini terjadi karena data terlalu besar."
            msg=msg + "\n[-] Silahkan salin alamat url dan buka manual di browser.\n\n"

            print(msg)
            return None
        if (alamatWebGempa.getcode() == 200):
            data = alamatWebGempa.read()

            # pengambilan data json
            try:
                theJSON = json.loads(data)

                # tulis json ke file
                with open("gempabumi.json", "w") as f:
                    json.dump(theJSON, f)
                f.close()
                return theJSON
            except:
                print("[-] File error dari server, tidak dapat mengambil data di halaman  - " +
                      str(urlData))
                return None
        else:
            print("[-] Terjadi kesalahan di server, tidak dapat mengambil hasil" +
                  str(alamatWebGempa.getcode()))
            return None

    def loadDict(JSONData):
        eDict = {}
        row = 0
        for i in JSONData["features"]:
            eDict[row] = {}
            eDict[row]["_idName"] = i["id"]
            eDict[row]["mag"] = i["properties"]["mag"]
            eDict[row]["place"] = i["properties"]["place"]
            eDict[row]["time"] = i["properties"]["time"]
            eDict[row]["tz"] = i["properties"]["tz"]
            eDict[row]["urlName"] = i["properties"]["url"]
            eDict[row]["felt"] = i["properties"]["felt"]
            eDict[row]["alert"] = i["properties"]["alert"]
            eDict[row]["shakeMap"] = i["properties"]["mmi"]
            eDict[row]["lon"] = i["geometry"]["coordinates"][0]
            eDict[row]["lat"] = i["geometry"]["coordinates"][1]
            eDict[row]["depth"] = i["geometry"]["coordinates"][2]
            row += 1

        list = pd.DataFrame.from_records(eDict).T
        try:
            list.sort_values(by=['mag', 'alert'], inplace=True,
                             ascending=[False, True])
        except:
            print("[-] List kosong..")
        list.reset_index(drop=True, inplace=True)

        # retList = [list.columns.values.tolist()] + list.values.tolist()
        return list.values.tolist()

    def loadHeaderInfo(JSONData):
        headerInfo = {}
        headerInfo["timeStamp"] = JSONData["metadata"]["generated"]
        headerInfo["url"] = JSONData["metadata"]["url"]
        headerInfo["title"] = JSONData["metadata"]["title"]
        headerInfo["count"] = JSONData["metadata"]["count"]
        return headerInfo

def ambilDataBaru(self, timeString):

    global urlData
    # print(urlData)
    x = urlData.find('summary/')
    y = urlData.find('.geojson')
    # print(urlData[x+8:y])
    urlData = str(urlData.replace(urlData[x+8:y], timeString, 1))
    print(urlData)


def main():

    # alamat json tempat data gempa
    urlData = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
    print(Data_GempaBumi.ambilDataWeb(urlData))


# START
if __name__ == "__main__":
    main()
