# _*_ coding = utf-8 _*_
# Здесь реализовано Rest Api для работы с сетью и websocket для работы с фронтом
# Общее про curl: https://curl.haxx.se/docs/httpscripting.html
# Curl cheatsheet: https://devhints.io/curl
# Полезная инфа про socketio: https://davidwalsh.name/websocket
# Про flask-socketio: https://flask-socketio.readthedocs.io/en/latest/
# Для тестирования сервера: https://chrome.google.com/webstore/detail/socketio-tester/cgmimdpepcncnjgclhnhghdooepibakm
# В целом про websocket: https://www.fullstackpython.com/websockets.html
# Про virtualenv для студентов: http://docs.python-guide.org/en/latest/dev/virtualenvs/
# TODO: реализовать работу с элементами
# TODO: реализовать работу с ботами (регистрация, местоположение)
# TODO: выводить статистику (сколько ботов, сколько состояний, связей, страниц)
# TODO: реализовать тестовый поток событий

from flask import Flask, request, render_template
from flask_restplus import Resource, Api, fields
from flask_socketio import SocketIO, emit
import time
from flask_cors import CORS
from network import Network
import json

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
net = Network('network.db')
startserver = time.time();
ns = api.namespace('todos', description='TODO operations')


class NetworkApi(Resource):

    node = api.model('Node', {
        'url': fields.String,
        'title': fields.String,
        'id': fields.Integer,
        'has_bug': fields.Boolean,
    })

    link = api.model('Link', {
        'source': fields.Integer,
        'target': fields.Integer,
        'key': fields.Integer
    })

    graph = api.model('Graph', {
        'nodes': fields.List(fields.Nested(node)),
        'links': fields.List(fields.Nested(link))
    })

    model = api.model('Model', {
        'directed': fields.Boolean,
        'multigraph': fields.Boolean,
        'nodes': fields.List(fields.Nested(node)),
        'links': fields.List(fields.Nested(link))
    })

    @api.response(code=200, description='Network', model=model)
    def get(self):
        """Возвращает граф из БД с базовой информацией"""
        return net.json()

class StateApi(Resource):

    @api.doc(params={'id': 'идментификатор состояния'})
    @api.doc(params={'state_hash': 'хэш скриншота страницы'})
    def get(self):
        """Возвращает метаданные о состоянии по идентификатору"""
        if 'id' in request.args:
            return net.get_state(state_id=request.args['id'])
        elif 'state_hash' in request.args:
            return net.get_state(state_hash=request.args['state_hash'])

    @api.doc(params={
        'url': 'полный URL страницы',
        'title': 'заголовок страницы',
        'screenshot': 'скриншот страницы в base64',
        'console': '{все записи из консоли в формате json',
        'http_requests': 'HTTP запросы в формате HAR',
        'state_hash': 'хэш страницы из скриншота',
        'has_bug': 'имеется ли в этом состоянии ошибка',
    })
    @api.response(200, 'id')
    def post(self):
        json_data = request.get_json(force=True)
        # TODO: возвращает id+перенос строки, нужно разобраться почему он добавляется
        state_id = net.add_state(**json_data)
        data = {
                'url': json_data['url'],
                'title': json_data['title'],
                'id': str(state_id)
        }
      #  with app.app_context():
       #     socketio.emit('state', json.dumps(data), broadcast=True)
        return str(state_id)

class TransitionApi(Resource):

    def get(self):
        """Возвращает метаданные перехода по id"""
        return net.get_transition(request.args['id'])

    @api.doc(params={
        'source': 'id состояния из которого переходим',
        'target': 'id состояния в которое попадаем',
        'action': 'выполняемое действие, click, type, etc,',
    })
    def post(self):
        """Добавление нового перехода"""
        json_data = request.get_json(force=True)
        transition_id = net.add_transition(**json_data)
        json_input = {"transition": [json_data],"state": [net.get_state(json_data['target'])]}
        with app.app_context():
            socketio.emit('transition', json_input, broadcast=True)
        return str(transition_id)


class States(Resource):
    def get(self):
        """Статистика по ботам"""
        json_input = {#'bots': len(net.get_bots_id()),
                      'states': len(net.get_states_id()),
                      'edges': len(net.get_edges_id()),
                      'bugs': net.get_bugs_num(),
                      'date':int(startserver),
                     }
        return json_input

    #json_input = json.dumps({"transition": [json_data], "state": [net.get_state(json_data['target'])]})
    #return pass

api.add_resource(NetworkApi, '/network')
api.add_resource(States, '/stats')
api.add_resource(StateApi, '/state')
api.add_resource(TransitionApi, '/transition')


@app.route('/index.html')
def index():
    """Выдача клиентской визуализации"""
    # with app.app_context():
    #     socketio.emit('test', 'Ali is OK', broadcast=True)
    return render_template('index.html')

def on_aaa_response(*args):
    print('on_aaa_response', args)

@socketio.on('connect', namespace='/test')
def test_connect(message):
    emit('my response', {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5556, host='0.0.0.0')
