from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import configparser
import datetime
import json
import os
import re
import time
import vix
import sys


app = Flask(__name__)
api = Api(app)
cors = CORS(app)


# def abort_if_todo_doesnt_exist(todo_id):
#     if todo_id not in TODOS:
#         abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('path')
parser.add_argument('vm')
parser.add_argument('snapshot')

root_nv = r'\\svr-rum-net-04\new_versions'
root_host_test = r'D:\Testing\Test-1'
root_guest_test = r'c:\Test'
root_report = r'\\rum-cherezov-dt\!Reports'


def make_job_ini_file(_dct, _ini):
    config = configparser.ConfigParser()
    config.read_dict(_dct)

    with open(_ini, 'w', encoding='ASCII') as fi:
        config.write(fi)


def make_cfg_dict(_setup, _name, _report, _vm):
    _dct = {'DEFAULT': {}}
    patt = r'(.*-.*)-(\d\d\d\d)(_x64)*__git--(.*)$'
    matches = re.search(patt, _name)
    if matches:
        wd = r"%s\%s-setup\%s\%s-%s" % (root_report, matches.group(2), matches.group(1), datetime.date.today(), _vm)
        _dct['DEFAULT']['path'] = _setup
        _dct['DEFAULT']['workingdir'] = wd
        _dct['DEFAULT']['done'] = '0'
    else:
        print('No matches in name')
        sys.exit(1)
    return _dct


class SingleTask(Resource):
    host = vix.VixHost(service_provider=3)

    def get(self):
        return {'message': 'no'}

    def post(self):
        args = parser.parse_args()
        print(args)
        vm_name = args.vm.replace('.vmx', '')
        snapshot_path = r'd:\images\%s\%s' % (vm_name, args.vm)
        # setup_path = args.path.replace('/', '\\')
        setup_path = args.path
        name_setup = os.path.basename(setup_path)

        _d = make_cfg_dict(setup_path, name_setup, root_report, vm_name)
        make_job_ini_file(_d, os.path.join(root_host_test, 'cfg.ini'))

        vm = self.host.open_vm(snapshot_path)
        work_snapshot = vm.snapshot_get_named(args.snapshot)
        vm.snapshot_revert(work_snapshot)

        vm.power_on(launch_gui=True)

        vm.wait_for_tools(timeout=90)
        while True:
            try:
                vm.login(username='Tester', password='t', require_interactive=True)
                break
            except vix.VixError as e:
                if e.VIX_E_INTERACTIVE_SESSION_NOT_PRESENT == 3034:
                    time.sleep(5)
                else:
                    print(e)
                    sys.exit(1)

        vm.copy_host_to_guest(host_path=root_host_test, guest_path=root_guest_test)
        vm.proc_run(program_name=r'C:\Windows\System32\schtasks.exe', command_line=r'/run /tn "StartJob"')

        # time.sleep(5)
        return {'messageOk': "Ok"}


class GetCfg(Resource):
    def get(self):
        with open('snap_dct.json') as fi:
            cfg = json.load(fi)
        return cfg


api.add_resource(SingleTask, '/api/single')
api.add_resource(GetCfg, '/api/cfg')


if __name__ == '__main__':
    app.run(debug=True)