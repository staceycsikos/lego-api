from peewee import *
from flask import Flask, jsonify, request
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('daiul39605bhds', user="iuequlwttmnjxu", password="fa56a1a7759d77d10c1c082c6beced0b560132ad02fe59839a1f27e2dbf26ab9",
                        host='ec2-3-223-213-207.compute-1.amazonaws.com', port=5432)

db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Sets(BaseModel):
    name = CharField()
    mini_figures = IntegerField()
    pieces = IntegerField()
    age = IntegerField()
    creator_id = IntegerField()


class Creator(BaseModel):
    name = CharField()
    age = IntegerField()


db.create_tables([Sets])
db.drop_tables([Sets])
db.create_tables([Sets])

Sets(name='Rocket Launch Center', mini_figures=7,
     pieces=1010, age=7, creator_id=1).save()
Sets(name='Vespa 125', mini_figures=0, pieces=1107, age=18, creator_id=2).save()
Sets(name='Harry Potter Hogwarts Magical Trunk',
     mini_figures=6, pieces=603, age=8, creator_id=1).save()
Sets(name='1970 Ferrari 512 M', mini_figures=1,
     pieces=291, age=8, creator_id=3).save()
Sets(name='Peach\'s Castle Expansion Set',
     mini_figures=4, pieces=1216, age=8, creator_id=4).save()
Sets(name='Colosseum', mini_figures=0, pieces=9036, age=18, creator_id=1).save()
Sets(name='The Globe', mini_figures=1, pieces=2585, age=18, creator_id=2).save()
Sets(name='Sonic the Hedgehog - Green Hill Zone',
     mini_figures=1, pieces=1125, age=18, creator_id=4).save()
Sets(name='Ferrari 488 GTE', mini_figures=0,
     pieces=1682, age=18, creator_id=3).save()
Sets(name='The Disney Castle', mini_figures=5,
     pieces=4080, age=16, creator_id=4).save()

db.create_tables([Creator])
db.drop_tables([Creator])
db.create_tables([Creator])

Creator(name='Stejci', age=29).save()
Creator(name='H', age=32).save()
Creator(name='Iffato', age=35).save()
Creator(name='Lucas', age=5).save()

app = Flask(__name__)


@app.route('/lego', methods=['GET', 'POST'])
@app.route('/lego/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Sets.get(Sets.id == id)))
        else:
            lego_list = []
            for unit in Sets.select():
                lego_list.append(model_to_dict(unit))
            return jsonify(lego_list)

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


@app.route('/creator', methods=['GET', 'POST'])
@app.route('/creator/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpointer(id=None):
    if request.method == 'GET':
        if id:
            sets = Sets.select().where(Sets.creator_id == id).execute()
            jsets = []
            for set in sets:
                jsets.append(model_to_dict(set))
            creator = model_to_dict(Creator.get_by_id(id))

            return jsonify({'creator': creator, 'sets': jsets})
        else:
            creator_list = []
            for unit in Creator.select():
                creator_list.append(model_to_dict(unit))
            return jsonify(creator_list)
    if request.method == 'PUT':
        data = request.get_json()
        Creator.update(data).where(Creator.id == id).execute()
        return ("updated")

    if request.method == 'POST':
        new_unit = dict_to_model(Creator, request.get_json())
        new_unit.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        Creator.delete().where(Creator.id == id).execute()
        return jsonify({"Deleted?": "It's been deleted!"})


app.run(debug=True, host="0.0.0.0")
