import logging

from kafka_connect import KafkaConnect

from util import config

host=config.get('kafka-connect','host')
port=int(config.get('kafka-connect','port'))
scheme=config.get('kafka-connect','scheme')
print('CDC-kafka:%s://%s:%s'%(scheme,host,port))

connect = KafkaConnect(host, port, scheme)
print(connect.api.version)

def create_connector(name,config):
    logging.info('create_connector(%s,%s)',name,config)
    connect.connectors[name] = config

def update_connetcor_property(connector_name,prop_name,value):
    logging.info('update_connetcor_property(%s,%s,%s)',connector_name,prop_name,value)
    connector = connect.connectors[connector_name]
    connector.config[prop_name] = value

def list_connectors():
    logging.info('list_connectors')
    return list(map(lambda c: c.name, connect.connectors))

def restart_connectors_tasks():
    logging.info('restart_connectors_tasks')
    for connector in connect.connectors:
        for task in connector.tasks:
            task.restart()

def delete_connector(name):
    logging.info('delete_connector(%s)',name)
    del connect.connectors[name]
