#!flask/bin/python

from flask import Blueprint, request

RestAPI = Blueprint('RestAPI', __name__, template_folder='templates')

@RestAPI.route('/devices/<device_id>', methods=['GET'])
def get_devices(device_id):
    assert device_id == request.view_args['device_id']
    print("get_devices")

@RestAPI.route('/devices/<device_id>/get', methods=['GET'])
def get_device_value(device_id):
    assert device_id == request.view_args['device_id']
    print("get_device_value")

@RestAPI.route('/devices/<device_id>/set', methods=['POST'])
def set_device_value(device_id):
    assert device_id == request.view_args['device_id']
    print("set_device_value")

@RestAPI.route('/devices/<device_id>', methods=['DELETE'])
def delete_device(device_id):
    assert device_id == request.view_args['device_id']
    print("delete_device")

@RestAPI.route('/devices/<device_id>', methods=['POST'])
def create_device(device_id):
    assert device_id == request.view_args['device_id']
    print("create_device")

@RestAPI.route('/devices/<device_id>', methods=['PUT'])
def update_device(device_id):
    assert device_id == request.view_args['device_id']
    print("ispremium")