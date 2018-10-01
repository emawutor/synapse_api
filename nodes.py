from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, TransferForm
import requests
import datetime



# initializing api
client_id = 'client_id'  # client id
client_secret = 'client_secret'  # client secret
fingerprint = 'da2e11ae7cc239fe9bb0dd07cc57f257'
ip_address = 'ip_address'   # user IP
headers = {
    'X-SP-GATEWAY': client_id + '|' + client_secret,
    'X-SP-USER-IP': ip_address,
    'X-SP-USER': '|' + fingerprint
}

baseURL = 'https://uat-api.synapsefi.com/v3.1'


app = Flask(__name__)

app.config['SECRET_KEY'] = '589aa70fbccae7791668ddb8c287a866'

@app.route("/")

# fetching all users
@app.route('/users')
def users():
    URL = baseURL+'/users'
    response = requests.get(URL, headers=headers).json()
    users = response['users']

    return render_template('users.html', users=users)

#noedes
@app.route('/users/<user_id>')
def nodes(user_id):
    URLT = baseURL + '/users/' + user_id
    resp = requests.get(URLT, headers=headers).json()
    refreshToken = resp['refresh_token']
    oauthURL = baseURL + '/oauth/' + user_id
    oauthResp = requests.post(oauthURL, headers=headers, json={'refresh_token': refreshToken}).json()
    oauthKey = oauthResp['oauth_key']
    headers['X-SP-USER'] = oauthKey + '|' + fingerprint
    URL = baseURL + '/users/' + user_id+'/nodes'
    resp = requests.get(URL, headers=headers).json()
    nodes = resp['nodes']
    return render_template('nodes.html', nodes=nodes, user_id=user_id)

#nodes
@app.route('/users/<user_id>/nodes/<node_id>/trans', methods=['GET','POST'])
def trans(user_id, node_id):

    URL = baseURL+'/users'
    response = requests.get(URL, headers=headers).json()
    users = response['users']

    form = TransferForm()
    legal_names = [ (user['_id'], user['legal_names'][0]) for user in users ]

    form.to.choices = legal_names
    # form.sender.choices = [(node_id,node_id)]

    if form.validate_on_submit():
      POSTURL = baseURL + '/users/' + user_id + '/nodes/' + node_id + '/trans'
      to = {'type': form.network.data, 'id': str(form.to.data)}
      amount = {'amount':form.amount.data, 'currency':form.currency.data}
      extra = {'ip': ip_address}
      headers["Content-Type"] = "application/json"
      resp = requests.post(POSTURL, headers=headers, json={'to':to, 'amount':amount, 'extra':extra}).json()

      return redirect(url_for('users'))

    URL = baseURL + '/users/' + user_id + '/nodes/' + node_id + '/trans'
    resp = requests.get(URL, headers=headers).json()
    trans = resp['trans']


    return render_template('trans.html', form=form, trans=trans)

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
      flash(f'Account created for {form.username.data}!', 'success')
      return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
      if form.username.data == '' and form.password.data == '':
        flash('You have been logged in!', 'success')
        return redirect(url_for('home'))
      else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
  app.run(debug=True)


