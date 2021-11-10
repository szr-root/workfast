# import json
# import requests
#
#
# def get_token(env='test'):
#     if env == 'test':
#         url = 'https://dev-nas.apiteamn.com/api/login'
#         pay_load = {
#             'username': "admin",
#             'password': "WP-nas2018"
#         }
#     else:
#         url = 'https://nas.apiteamn.com/api/login'
#         pay_load = {
#             'username': "nancy",
#             'password': "H_HNZ8r6gw"
#         }
#     headers = {
#         'Accept': 'application / json'
#     }
#     resp = requests.request('post', url=url, headers=headers, data=json.dumps(pay_load), cert=(
#                 '/Users/woop/client/nas-client-cert.pem',
#                 '/Users/woop/client/nas-client-key.pem'))
#     respj = resp.json()
#     return 'Bearer ' + respj['data']['token']
#
#
# def get_share_account(token, uid, env='test'):
#     if env == 'test':
#         url = 'https://dev-nas.apiteamn.com/api/profile/' + uid + '/shared_account'
#     else:
#         url = 'https://nas.apiteamn.com/api/profile/' + uid + '/shared_account'
#     headers = {
#         'Accept': 'application / json',
#         'Authorization': token
#     }
#     resp = requests.request('get', url=url, headers=headers, cert=(
#         '/Users/woop/client/nas-client-cert.pem',
#         '/Users/woop/client/nas-client-key.pem'))
#     respj = resp.json()
#     _ids = list()
#     for _ in respj['data']['accounts']:
#         if _['status'] == 5:
#             _ids.append(_['id'])
#     return _ids
#
#
# def make_normal(token, _id, env='test'):
#     if env == 'test':
#         url = 'https://dev-nas.apiteamn.com/api/user/' + _id + '/1'
#     else:
#         url = 'https://nas.apiteamn.com/api/user/' + _id + '/1'
#     headers = {
#         'Accept': 'application / json',
#         'Authorization': token
#     }
#     pay_load = {
#         'current_status': 5,
#         'reason': 'null'}
#     resp = requests.request('post', url=url, headers=headers, data=json.dumps(pay_load), cert=(
#                 '/Users/woop/client/nas-client-cert.pem',
#                 '/Users/woop/client/nas-client-key.pem'))
#     respj = resp.json()
#     return respj
#
#
# auth = get_token('test')     # test/prod
# ids = get_share_account(auth, '611e1b53935e8dded0b6b2e5') + ['611e1b53935e8dded0b6b2e5']
# for _id in ids:
#     print(make_normal(auth, _id))
