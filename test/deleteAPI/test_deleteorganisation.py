import pytest
import requests
import json

@pytest.fixture
def supply_url():
	return "https://stagingapi.autographamt.com"

#----------- admin role--------------#
@pytest.fixture
def get_adm_accessToken():
	email = "alex@yopmail.com"
	password = "1189"
	url = "https://stagingapi.autographamt.com/v1/auth"
	data = {'email':email,'password':password}
	resp = requests.post(url, data=data)
	respobj = json.loads(resp.text)
	token = respobj['accessToken']
	return token

#----------- su-admin role--------------#
@pytest.fixture
def get_supAdmin_accessToken():
	email = 'savitha.mark@bridgeconn.com'
	password = '221189'
	url = "https://stagingapi.autographamt.com/v1/auth"
	data = {'email':email,'password':password}
	resp = requests.post(url, data=data)
	respobj = json.loads(resp.text)
	token = respobj['accessToken']
	return token

#----------- normal role--------------#
@pytest.fixture
def get_trans_accessToken():
	email = 'ag2@yopmail.com'
	password = '1189'
	url = "https://stagingapi.autographamt.com/v1/auth"
	data = {'email':email,'password':password}
	resp = requests.post(url, data=data)
	respobj = json.loads(resp.text)
	token = respobj['accessToken']
	return token

#----------- deactivate using su-admin role --------------#
@pytest.mark.skip(reason="need to change the values")
@pytest.mark.parametrize('organisationId',[("31")])
def test_delete_Organisation_2(supply_url,get_supAdmin_accessToken,organisationId):
	url = supply_url + "/v1/autographamt/organisation/delete"
	data = {'organisationId':organisationId}
	resp = requests.delete(url,data=json.dumps(data),headers={'Authorization': 'bearer {}'.format(get_supAdmin_accessToken)})
	j = json.loads(resp.text)
	assert resp.status_code == 200
	assert j['message'] == "Deactivated organization and its projects."


#----------- deactivate using admin role --------------#
@pytest.mark.parametrize('organisationId',[("12")])
def test_delete_Organisation_3(supply_url,get_adm_accessToken,organisationId):
	url = supply_url + "/v1/autographamt/organisation/delete"
	data = {'organisationId':organisationId}
	resp = requests.delete(url,data=json.dumps(data),headers={'Authorization': 'bearer {}'.format(get_adm_accessToken)})
	j = json.loads(resp.text)
	assert resp.status_code == 200
	assert j['message'] == "UnAuthorized! Only a super admin can delete organizations."


#----------- deactivate using normal role --------------#
@pytest.mark.parametrize('organisationId',[("12")])
def test_delete_Organisation_4(supply_url,get_trans_accessToken,organisationId):
	url = supply_url + "/v1/autographamt/organisation/delete"
	data = {'organisationId':organisationId}
	resp = requests.delete(url,data=json.dumps(data),headers={'Authorization': 'bearer {}'.format(get_trans_accessToken)})
	j = json.loads(resp.text)
	assert resp.status_code == 200
	assert j['message'] == "UnAuthorized! Only a super admin can delete organizations."