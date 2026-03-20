from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

character_map = {
    "806": "102000008.png",
    "306": "102000006.png",
    "906": "101000009.png",
    "2406": "101000016.png",
    "1003": "102000009.png",
    "2306": "102000016.png",
    "6306": "102000016.png",
    "7506": "101000053.png",
    "1306": "102000010.png",
    "2006": "102000014.png",
    "2106": "101000014.png",
    "2806": "101100018.png",
    "7206": "102000051.png",
    "7006": "101000049.png",
    "6906": "102000046.png",
    "6806": "102000045.png",
    "6706": "102000044.png",
    "6606": "101000028.png",
    "6506": "101000027.png",
    "6206": "102000041.png",
    "6006": "102000040.png",
    "5306": "101000026.png",
    "5806": "102000039.png",
    "5606": "101000025.png",
    "5706": "102000038.png",
    "5506": "102000037.png",
    "5406": "102000036.png",
    "5206": "102000034.png",
    "5006": "102000033.png",
    "4906": "102000032.png",
    "4606": "102000030.png",
    "4706": "102000031.png",
    "4506": "102000029.png",
    "4306": "102000028.png",
    "4006": "102000025.png",
    "4406": "101000022.png",
    "4106": "102000026.png",
    "3806": "102000024.png",
    "3506": "101000020.png",
    "3406": "102000022.png",
    "2906": "102000018.png",
    "206": "101000006.png",
    "1506": "102000012.png",
    "1406": "101000023.png",
    "2606": "101000017.png",
    "606": "101000008.png",
    "706": "102000007.png",
    "406": "102000005.png",
    "7106": "101000050.png",
    "1106": "101000010.png",
    "1706": "101000012.png",
    "1806": "102000013.png",
    "2206": "102000015.png",
    "2706": "102000017.png",
    "3106": "101000019.png",
    "3006": "102200019.png",
    "3306": "102000021.png",
    "4203": "102000005.png",
    "4806": "101000023.png",
    "3203": "102000012.png",
    "2506": "101000006.png",
    "22016": "102000015.png",
    "506": "101000007.png",
    "1906": "101000013.png",
    "7406": "102000052.png",
    "1206": "102000011.png",
    "106": "101000005.png"
}

name_to_id = {
    "Kla": "806",
    "Ford": "306",
    "Paloma": "906",
    "Notora": "2406",
    "Miguel": "1003",
    "Alvaro": "2306",
    "Awaken Alvaro": "6306",
    "Rin": "7506",
    "Antonio": "1306",
    "Joseph": "2006",
    "Shani": "2106",
    "Kapella": "2806",
    "Koda": "7206",
    "Kassie": "7006",
    "Kairos": "6906",
    "Ryden": "6806",
    "Ignis": "6706",
    "Suzy": "6606",
    "Sonia": "6506",
    "Orion": "6206",
    "Santino": "6006",
    "Luna": "5306",
    "Tatsuya": "5806",
    "Iris": "5606",
    "J.Biebs": "5706",
    "Homer": "5506",
    "Kenta": "5406",
    "Nairi": "5206",
    "Otho": "5006",
    "Leon": "4906",
    "Thiva": "4606",
    "Dimitri": "4706",
    "D-bee": "4506",
    "Maro": "4306",
    "Skyler": "4006",
    "Xayne": "4406",
    "Shirou": "4106",
    "Chrono": "3806",
    "Dasha": "3506",
    "K": "3406",
    "Luqueta": "2906",
    "Kelly": "206",
    "Hayato Yagami": "1506",
    "Moco": "1406",
    "Steffie": "2606",
    "Misha": "606",
    "Maxim": "706",
    "Andrew": "406",
    "Lila": "7106",
    "Caroline": "1106",
    "Laura": "1706",
    "Rafael": "1806",
    "Alok": "2206",
    "Jota": "2706",
    "Clu": "3106",
    "Wolfrahh": "3006",
    "Jai": "3306",
    "Awaken Andrew": "4203",
    "Awaken Moco": "4806",
    "Awaken Hayato": "3203",
    "Awaken Kelly": "2506",
    "Awaken Alok": "22016",
    "Nikita": "506",
    "A124": "1906",
    "Oscar": "7406",
    "Wukong": "1206",
    "Olivia": "106"
}

pngid_to_id = {}
for char_id, filename in character_map.items():
    pngid = filename.replace('.png', '')
    pngid_to_id[pngid] = char_id

@app.route('/item-info')
def item_info():
    try:
        item_id = request.args.get('id')
        
        if not item_id:
            return jsonify({"error": "Missing 'id' parameter"}), 400
        
        character_id = None
        avatar_id = None
        name = None
        
        if item_id.isdigit() and len(item_id) >= 3 and len(item_id) <= 6:
            if item_id in character_map:
                character_id = item_id
                avatar_id = character_map[item_id].replace('.png', '')
                for n, cid in name_to_id.items():
                    if cid == character_id:
                        name = n
                        break
        
        elif item_id.isdigit() and len(item_id) >= 8 and len(item_id) <= 11:
            if item_id in pngid_to_id:
                character_id = pngid_to_id[item_id]
                avatar_id = item_id
                for n, cid in name_to_id.items():
                    if cid == character_id:
                        name = n
                        break
        
        else:
            if item_id in name_to_id:
                character_id = name_to_id[item_id]
                name = item_id
                avatar_id = character_map[character_id].replace('.png', '')
            else:
                for n, cid in name_to_id.items():
                    if n.lower() == item_id.lower():
                        character_id = cid
                        name = n
                        avatar_id = character_map[character_id].replace('.png', '')
                        break
        
        if character_id and name and avatar_id:
            return jsonify({
                "Name": name,
                "Id": character_id,
                "AvatarId": avatar_id
            })
        else:
            return jsonify({"error": f"Item not found for id: {item_id}"}), 404
            
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

app = app