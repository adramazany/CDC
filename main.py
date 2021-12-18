import logging

from flask import Flask, json, request
from service import kafka
import json

#########################################
# Initialize
#########################################
companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]
api = Flask(__name__)
logging.getLogger().setLevel(logging.INFO)

#########################################
# APIs
#########################################
@api.route('/', methods=['GET'])
def help():
  return "<a href='companies'>companies</a>" \
         "<hr/>" \
         "<a href='connectors/list'>connectors/list</a>" \
         "<hr/>" \
         "<form action='/connectors/create' method='POST'>" \
         "name:<input type='text' name='name' value='mysql_localhost_kafka_source'/><br/>" \
         "config:<textarea name='config'>" \
         '{"name":"mysql_localhost_kafka_source","config":{"connector.class":"io.debezium.connector.mysql.MySqlConnector","database.hostname":"localhost","database.port":"3306","database.user":"test","database.password":"test","table.whitelist":"test.test","database.history.kafka.bootstrap.servers":"localhost:9092","database.history.kafka.topic":"t_test","include.schema.changes":"false","transforms":"unwrap,extractkey","transforms.unwrap.type":"io.debezium.transforms.ExtractNewRecordState","transforms.extractkey.type":"org.apache.kafka.connect.transforms.ExtractField$Key","transforms.extractkey":"id","key.convertter":"org.apache.kafka.connect.storage.StringConverter","value.convertter":"io.confluent.connect.avro.AvroConverter"}}' \
         "</textarea><br/>" \
         "<input type='submit' value='Create Connector'/>" \
         "</form>" \
         "<hr/>" \
         ""

@api.route('/companies', methods=['GET'])
def get_companies():
  return json.dumps(companies)

@api.route('/connectors/list', methods=['GET'])
def connectors_list():
    return str( kafka.list_connectors() )

@api.route('/connectors/create', methods=['POST'])
def connectors_create():
    name=request.form.get('name')
    config=json.loads(request.form.get('config'))
    return str( kafka.create_connector(name,config) )

@api.route('/test', methods=['GET'])
def test():
    fp = open("connectors/test.json")
    return json.load(fp)


#########################################
# main
#########################################
if __name__ == '__main__':
    api.run()
