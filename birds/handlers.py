import json
import datetime
from PIL import Image
from ru.travelfood.simple_ui import SimpleSQLProvider as sqlClass

def init_on_start(hashMap,_files=None,_data=None):
    """
    Соединение с БД и создание таблиц
    """
    hashMap.put("SQLConnectDatabase","birds.DB")
    # основная таблица с данными о птицах
    hashMap.put("SQLExec",json.dumps({"query":"create table IF NOT EXISTS Birds(id integer primary key autoincrement, name text, feather_color text, img_path text)","params":""}))
    # таблица с данными о птицах которых я видел
    hashMap.put("SQLExec",json.dumps({"query":"create table IF NOT EXISTS SeenBirds(id integer primary key autoincrement, bird_id integer, seen_date text, seen_count integer)","params":""}))
    return hashMap

def add_bird_screen(hashMap,_files=None,_data=None):
    """
    Переход на экран добавления новой птицы.
    """
    # Очистим поля от остаточных значений
    hashMap.put("name","")
    hashMap.put("feather_color","")
    hashMap.put("pic_bird","")
    hashMap.put("title_add_edit","Добавить в БД")
    hashMap.put("title_h1","Добавление новой птицы")
    hashMap.put("ShowScreen","Добавление птицы")  

    return hashMap
      
def btn_back_on_press(hashMap,_files=None,_data=None):
    """
    Обработчик кнопки назад. Возврат к списку птиц
    """
    hashMap.put("ShowScreen","Список птиц")

    return hashMap

def get_if_exist(hashMap, field):
    if hashMap.containsKey(field):
            res =hashMap.get(field)
    else:
            res =""
    return res

def btn_add_to_db_on_press(hashMap,_files=None,_data=None):
    """
    Обработчик добавления/редактирования птицы в БД.
    """
    action = get_if_exist(hashMap, "title_add_edit")
    name = hashMap.get('name')
    feather_color = hashMap.get("feather_color")
    img_path = get_if_exist(hashMap, "pic_bird")
    bird_id = hashMap.get("id")
    params = f"{name},{feather_color},{img_path}"

    if action=="Изменить":
        query = "UPDATE Birds SET name = ?, feather_color = ?, img_path = ? WHERE id = ?"
        params += f",{bird_id}"
        success_msg = "Успешно изменено!"
    elif action=="Добавить в БД":
        query = "insert into Birds(name,feather_color,img_path) values(?,?,?)"
        success_msg = "Успешно добавлено!"

    if name != "" and feather_color != "":
        sql = sqlClass()
        success=sql.SQLExec(query, str(params))

        if success:    
            hashMap.put("toast", success_msg)
            if action=="Добавить в БД":
                hashMap.put('name',"")
                hashMap.put('feather_color',"")
                hashMap.put('pic_bird',"")
    else:
        hashMap.put("toast","Поля не должны быть пустыми!")
        
    return hashMap

def btn_edit_on_press(hashMap,_files=None,_data=None):
    """
    Обработчик изменения надписей полей.
    """
    hashMap.put("title_add_edit","Изменить")
    hashMap.put("title_h1","Изменение данных птицы")
    hashMap.put("ShowScreen","Добавление птицы")
    
    return hashMap

def btn_delete_on_press(hashMap,_files=None,_data=None):
    """
    Обработчик кнопки удаления птицы из БД. И возврат в список птиц.
    """
    bird_id = hashMap.get("id")
    sql = sqlClass()
    success = sql.SQLExec("DELETE FROM Birds WHERE id=?", bird_id)

    if success:
        hashMap.put("toast", "Удаление прошло успешно")
    else:
        hashMap.put("toast", "Не удалось удалить элемент из БД")

    hashMap.put("ShowScreen","Список птиц")

    return hashMap

def btn_pic_on_press(hashMap,_files=None,_data=None):
    """
    Обработчик кнопки выбора картинки.
    """
    image_file = str(hashMap.get("photo_path")) # "переменная"+"_path" - сюда помещается путь к полученной фотографии
    hashMap.put("pic_bird","~" + image_file) 

    # сделаем фотку - квадратной
    image = Image.open(image_file)
    im = image.resize((900,900))
    im.save(image_file)

    return hashMap

def birds_record_on_start(hashMap,_files=None,_data=None):
    """
    Инициализация переменных для локального хранения картинки, а также сжатие и размер
    """
    hashMap.put("mm_local","")
    hashMap.put("mm_compression","70")
    hashMap.put("mm_size","50")
    
    return hashMap

def customcards_on_open(hashMap,_files=None,_data=None):
    """
    Формирование списка карточек
    """
    hashMap.put("mm_local","")
    hashMap.put("mm_compression","70")
    hashMap.put("mm_size","50")

    j = { "customcards":         {
            
            "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
            {
                "type": "LinearLayout",
                "orientation": "horizontal",
                "height": "wrap_content",
                "width": "match_parent",
                "weight": "0",
                "Elements": [
                {
                "type": "Picture",
                "show_by_condition": "",
                "Value": "@pic_bird",
                "NoRefresh": False,
                "document_type": "",
                "mask": "",
                "Variable": "",
                "TextSize": "16",
                "TextColor": "#DB7093",
                "TextBold": True,
                "TextItalic": False,
                "BackgroundColor": "",
                "width": 200,
                "height": 100,
                "weight": 1
                },
                {
                "type": "LinearLayout",
                "orientation": "vertical",
                "height": "wrap_content",
                "width": "match_parent",
                "weight": "1",
                "Elements": [
                {
                    "type": "TextView",
                    "show_by_condition": "",
                    "Value": "@name",
                    "NoRefresh": False,
                    "document_type": "",
                    "mask": "",
                    "TextSize": "27",
                    "TextBold": True,
                    "Variable": ""
                },
                {
                    "type": "TextView",
                    "show_by_condition": "",
                    "Value": "@feather_color",
                    "NoRefresh": False,
                    "document_type": "",
                    "mask": "",
                    "TextSize": "25",
                    "TextItalic": True,
                    "Variable": ""
                }
                ]
                }
                ]
            },
            {
                "type": "TextView",
                "show_by_condition": "",
                "Value": "@id",
                "NoRefresh": False,
                "document_type": "",
                "mask": "",
                "Variable": "",
                "TextSize": "-1",
                "TextColor": "#6F9393",
                "TextBold": False,
                "TextItalic": True,
                "BackgroundColor": "",
                "width": "wrap_content",
                "height": "wrap_content",
                "weight": 0
            }
            ]
        }

    }
    }
   
    sql = sqlClass()
    res = sql.SQLQuery("select * from Birds","")

    records = json.loads(res)
    
    j["customcards"]["cardsdata"]=[]
    for record in records:
        id_card = str(record['id'])
        c =  {
        "key": id_card,
        "pic_bird": "" if record["img_path"] is None or record["img_path"] == "" else record['img_path'],
        "id": "ID: "+ id_card,
        "name": record['name'],
        "feather_color": record['feather_color'],
      }
        j["customcards"]["cardsdata"].append(c)

    hashMap.put("cards",json.dumps(j,ensure_ascii=False).encode('utf8').decode())
    
    return hashMap

def customcards_touch(hashMap,_files=None,_data=None):
    """
    Обработчик нажатия на карточку. Переход в карточку птицы.
    """
    selected_card = hashMap.get("selected_card_key") 
    
    sql = sqlClass()
    res = sql.SQLQuery(f"select * from Birds where id={selected_card}","")

    records = json.loads(res)
    if records:
        record = records[0]
        hashMap.put("id", str(record["id"]))
        hashMap.put("name", record["name"])
        hashMap.put("feather_color", record["feather_color"])
        hashMap.put("pic_bird", "" if record["img_path"] == "" else record["img_path"])

    hashMap.put("ShowScreen","Карточка птицы")

    return hashMap

def btn_seen_on_press(hashMap,_files=None,_data=None):
    """
    Обработчик кнопки "Видел". Увеличивает количество нажатий для выбранной птицы в глобальной переменной.
    """
    bird_id = hashMap.get("id")
    if get_if_exist(hashMap, "_seen_birds") != "":
        seen_birds = json.loads(hashMap.get("_seen_birds"))
    else:
        hashMap.put("_seen_birds",json.dumps({}))
        seen_birds={}

    seen_birds[bird_id] = seen_birds.get(bird_id, 0) + 1
    hashMap.put("_seen_birds", json.dumps(seen_birds))
    hashMap.put("toast", f"Птица помечена как виденная {seen_birds[bird_id]} раз")

    return hashMap

def seen_birds_on_open(hashMap,_files=None,_data=None):
    """
    Формирование списка карточек увиденных птиц
    """
    hashMap.put("mm_local","")
    hashMap.put("mm_compression","70")
    hashMap.put("mm_size","50")

    j = { "customcards":         {
            
            "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
            {
                "type": "LinearLayout",
                "orientation": "horizontal",
                "height": "wrap_content",
                "width": "match_parent",
                "weight": "0",
                "Elements": [
                {
                "type": "Picture",
                "show_by_condition": "",
                "Value": "@pic_bird",
                "NoRefresh": False,
                "document_type": "",
                "mask": "",
                "Variable": "",
                "TextSize": "16",
                "TextColor": "#DB7093",
                "TextBold": True,
                "TextItalic": False,
                "BackgroundColor": "",
                "width": 200,
                "height": 100,
                "weight": 1
                },
                {
                "type": "LinearLayout",
                "orientation": "vertical",
                "height": "wrap_content",
                "width": "match_parent",
                "weight": "1",
                "Elements": [
                {
                    "type": "TextView",
                    "show_by_condition": "",
                    "Value": "@seen_date",
                    "NoRefresh": False,
                    "document_type": "",
                    "mask": "",
                    "TextSize": "27",
                    "TextItalic": True,
                    "Variable": ""
                },
                {
                    "type": "TextView",
                    "show_by_condition": "",
                    "Value": "@name",
                    "NoRefresh": False,
                    "document_type": "",
                    "mask": "",
                    "TextSize": "27",
                    "TextBold": True,
                    "Variable": ""
                },
                {
                    "type": "TextView",
                    "show_by_condition": "",
                    "Value": "@seen_count",
                    "NoRefresh": False,
                    "document_type": "",
                    "mask": "",
                    "TextSize": "25",
                    "TextItalic": True,
                    "Variable": ""
                }
                ]
                }
                ]
            },
            {
                "type": "TextView",
                "show_by_condition": "",
                "Value": "@id",
                "NoRefresh": False,
                "document_type": "",
                "mask": "",
                "Variable": "",
                "TextSize": "-1",
                "TextColor": "#6F9393",
                "TextBold": False,
                "TextItalic": True,
                "BackgroundColor": "",
                "width": "wrap_content",
                "height": "wrap_content",
                "weight": 0
            }
            ]
        }

    }
    }
   
    sql = sqlClass()
    # получаем недостающие поля соядинением с основной таблицей
    res = sql.SQLQuery("""SELECT SeenBirds.bird_id, SeenBirds.seen_date, SeenBirds.seen_count, Birds.name, 
                        Birds.img_path FROM SeenBirds JOIN Birds ON SeenBirds.bird_id = Birds.id""","")

    records = json.loads(res)
    
    j["customcards"]["cardsdata"]=[]
    for record in records:
        id_card = str(record['bird_id'])
        c =  {
        "key": id_card,
        "pic_bird": "" if record["img_path"] is None or record["img_path"] == "" else record['img_path'],
        "id": "ID: "+ id_card,
        "name": record['name'],
        "seen_date": record['seen_date'],
        "seen_count": f"Увидено: {record['seen_count']} раз",
      }
        j["customcards"]["cardsdata"].append(c)

    hashMap.put("seen_birds_cards",json.dumps(j,ensure_ascii=False).encode('utf8').decode())
    
    return hashMap

def add_seen_birds_on_press(hashMap,_files=None,_data=None):
    """
    Обработчик кнопки "+". Создает записи в таблице SeenBirds для всех увиденных птиц из глобальной переменной.
    """
    if get_if_exist(hashMap, "_seen_birds") != "":
        seen_birds = json.loads(hashMap.get("_seen_birds"))
        sql = sqlClass()
        for bird_id, seen_count in seen_birds.items():
            seen_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            success = sql.SQLExec("insert into SeenBirds(bird_id,seen_date,seen_count) values(?,?,?)", bird_id + "," + seen_date + "," + str(seen_count))
            if success:
                hashMap.put("toast", "Успешно добавлено в список виденных птиц!")
            else:
                hashMap.put("toast", "Не удалось добавить в список виденных птиц!")
        hashMap.put("_seen_birds", "{}")  # очищаем список виденных птиц после добавления в базу данных
    else:
        hashMap.put("toast", "Нет птиц для добавления!")
   
    return hashMap
