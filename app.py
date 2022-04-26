from peewee import *
from flask import Flask, jsonify, request
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('legos', user='stacey', password='',
                        host='localhost', port=5432)

db.connect()

class BaseModel(Model):
    class Meta:
        database = db


class Sets(BaseModel):
    name = CharField()
    mini_figures = IntegerField()
    pieces = IntegerField()
    age = IntegerField()


db.create_tables([Sets])
db.drop_tables([Sets])
db.create_tables([Sets])

Sets(name='Rocket Launch Center', mini_figures='7', pieces='1010', age='7').save()
Sets(name='Vespa 125', mini_figures='0', pieces='1107', age='18').save()
Sets(name='Harry Potter Hogwarts Magical Trunk',
     mini_figures='6', pieces='603', age='8').save()
Sets(name='1970 Ferrari 512 M', mini_figures='1', pieces='291', age='8').save()
Sets(name='Peach\'s Castle Expansion Set',
     mini_figures='4', pieces='1216', age='8').save()
Sets(name='Colosseum', mini_figures='0', pieces='9036', age='18').save()
Sets(name='The Globe', mini_figures='1', pieces='2585', age='18').save()
Sets(name='Sonic the Hedgehog - Green Hill Zone',
     mini_figures='1', pieces='1125', age='18').save()
Sets(name='Ferrari 488 GTE', mini_figures='0', pieces='1682', age='18').save()
Sets(name='The Disney Castle', mini_figures='5', pieces='4080', age='16').save()


app = Flask(__name__)


@app.route('/lego', methods=['GET', 'POST'])
@app.route('/lego/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Sets.get(Sets.id == id)))
        else:
            legoList = []
            for unit in Sets.select():
                legoList.append(model_to_dict(unit))
            return jsonify(legoList)

    if request.method == 'PUT':
        data = request.get_json()
        Sets.update(data).where(Sets.id == id).execute()
        return ("updated")

    if request.method == 'POST':
        new_unit = dict_to_model(Sets, request.get_json())
        new_unit.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        Sets.delete().where(Sets.id == id).execute()
        return ("It's been deleted!")


app.run(debug=True, port=9000)
