import pytest
import requests
import json

@pytest.fixture
def supply_url():
	return "https://stagingapi.autographamt.com"


@pytest.fixture
def get_adm_accessToken():
	email = "alex@yopmail.com"
	password = "1189"
	url = "https://stagingapi.autographamt.com/v1/auth"
	data = {'email':email,
			'password':password}
	resp = requests.post(url, data=data)
	respobj = json.loads(resp.text)
	token = respobj['accessToken']

	return token

@pytest.fixture
def get_supAdmin_accessToken():
	email = 'savitha.mark@bridgeconn.com'
	password = '221189'
	url = "https://stagingapi.autographamt.com/v1/auth"
	data = {'email':email,
			'password':password}
	resp = requests.post(url, data=data)
	respobj = json.loads(resp.text)
	token = respobj['accessToken']

	return token

@pytest.fixture
def get_trans_accessToken():
	email = 'ag2@yopmail.com'
	password = '1189'
	url = "https://stagingapi.autographamt.com/v1/auth"
	data = {'email':email,
			'password':password}
	resp = requests.post(url, data=data)
	respobj = json.loads(resp.text)
	token = respobj['accessToken']

	return token

@pytest.fixture
def get_supAdmin_accessToken():
	email = 'savitha.mark@bridgeconn.com'
	password = '221189'
	url = "https://stagingapi.autographamt.com/v1/auth"
	data = {'email':email,
			'password':password}
	resp = requests.post(url, data=data)
	respobj = json.loads(resp.text)
	token = respobj['accessToken']

	return token


def check_login(url,email,password):
	url = url + "/v1/auth" 
	data = {'email':email,
			'password':password}
	resp = requests.post(url, data=data)
	return resp

def test_firstpage_load():
	url = "https://staging.autographamt.com"
	resp = requests.get(url)
	assert resp.status_code == 200, resp.text
	
## POST method with access  for Organization aprovals

@pytest.mark.parametrize('org_id, verified',[('org_id','verified')])
def test_Orgapprovalsup(supply_url,get_supAdmin_accessToken,org_id, verified):
	url = supply_url + '/v1/autographamt/approvals/organisations'
	data = {'organisationId':org_id,
			'verified':verified
			}
	resp = requests.post(url,data=json.dumps(data),headers={'Authorization': 'bearer {}'.format(get_supAdmin_accessToken)})
	j = json.loads(resp.text)
	print(j)
	assert resp.status_code == 200, resp.text
	assert j['success'] == False, str(j)
	assert j['message'] == "Server error", str(j)

@pytest.mark.parametrize('org_id, verified',[('org_id','verified')])
def test_Orgapprovalad(supply_url,get_adm_accessToken,org_id, verified):
	url = supply_url + '/v1/autographamt/approvals/organisations'
	data = {'organisationId':org_id,
			'verified':verified
			}
	resp = requests.post(url,data=json.dumps(data),headers={'Authorization': 'bearer {}'.format(get_adm_accessToken)})
	j = json.loads(resp.text)
	assert resp.status_code == 200, resp.text
	assert j['success'] == False, str(j)
	assert j['message'] == "Unauthorized", str(j)

# @pytest.mark.parametrize(('org_id, verified',[('org_id','verified')])
# def test_Orgapprovaltr(supply_url,get_trans_accessToken,org_id, verified):
# 	url = supply_url + '/v1/autographamt/approvals/organisations'
# 	data = {'organisationId':org_id,
# 			'verified':verified
# 			}
# 	resp = requests.post(url,data=json.dumps(data),headers={'Authorization': 'bearer {}'.format(get_trans_accessToken)})
# 	j = json.loads(resp.text)
# 	print(j)
# 	assert resp.status_code == 200, resp.text
# 	assert j['success'] == True, str(j)
# 	assert j['message'] == "Role Updated", str(j)
@pytest.mark.parametrize('org_id, verified',[('org_id','verified')])
def test_Orgapprovalsupc(supply_url,get_supAdmin_accessToken,org_id, verified):
	url = supply_url + '/v1/autographamt/approvals/organisations'
	data = {'organisationId':org_id,
			'verified':verified
			}
	resp = requests.post(url,data=json.dumps(data),headers={'Authorization': 'bearer {}'.format(get_supAdmin_accessToken)})
	j = json.loads(resp.text)
	print(j)
	assert resp.status_code == 200, resp.text
	assert j['success'] == True, str(j)
	assert j['message'] == "Role Updated", str(j)

@pytest.mark.parametrize('org_id, verified',[('org_id','verified')])
def test_Orgapprovaladc(supply_url,get_adm_accessToken,org_id, verified):
	url = supply_url + '/v1/autographamt/approvals/organisations'
	data = {'organisationId':org_id,
			'verified':verified
			}
	resp = requests.post(url,data=json.dumps(data),headers={'Authorization': 'bearer {}'.format(get_adm_accessToken)})
	j = json.loads(resp.text)
	assert resp.status_code == 200, resp.text
	assert j['success'] == True, str(j)
	assert j['message'] == "Role Updated", str(j)
