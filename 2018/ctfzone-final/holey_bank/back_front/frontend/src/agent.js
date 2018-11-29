import superagentPromise from 'superagent-promise';
import _superagent from 'superagent';

const superagent = superagentPromise(_superagent, global.Promise);

const API_ROOT = '/api';

const handleErrors = err => {
  /*if (err && err.response && err.response.status === 401) {
    authStore.logout();
  }*/
  return err;
};

const tokenPlugin = req => {
  /*if (commonStore.token) {
    req.set('authorization', `Token ${commonStore.token}`);
  }*/
};

const responseBody = res => res.body;

const requests = {
  del: url =>
    superagent
      .del(`${API_ROOT}${url}`)
      .use(tokenPlugin)
      .end(handleErrors)
      .then(responseBody),
  get: url =>
    superagent
      .get(`${API_ROOT}${url}`)
      .use(tokenPlugin)
      .end(handleErrors)
      .then(responseBody),
  put: (url, body) =>
    superagent
      .put(`${API_ROOT}${url}`, body)
      .use(tokenPlugin)
      .end(handleErrors)
      .then(responseBody),
  post: (url, body) =>
    superagent
      .post(`${API_ROOT}${url}`, body)
      .use(tokenPlugin)
      .end(handleErrors)
      .then(responseBody),
};

const Session = {
  login: (username, password) =>
    requests.post('/session/', { username, password }),
  logout: () =>
    requests.del('/session/')
};

const User = {
  current: () =>
    requests.get('/user/'),
  new: ( username, password, firstname, lastname, passport, residence ) =>
    requests.put('/user/', { username, password, firstname, lastname, passport, residence }),
  edit: ( userInfo ) =>
    requests.post('/user/', { userInfo }),
};

const Account = {
  current: () =>
    requests.get('/processing/'),
  new: () =>
    requests.put('/processing/'),
};

const PaymentA2A = {
  new: ( to, comment, sum ) =>
    requests.post('/processing/a2a', { to, comment, sum }),
};

const PaymentC2C = {
  new: ( from, to, comment, sum ) =>
    requests.post('/processing/c2c', { from, to, comment, sum }),
};

const PaymentA2C = {
  new: ( to, comment, sum ) =>
    requests.post('/processing/a2c', { to, comment, sum }),
};

const PaymentC2A = {
  new: ( from, comment, sum ) =>
    requests.post('/processing/c2a', { from, comment, sum }),
};

const Payment = {
  history: () =>
    requests.get('/processing/full_history'),
};

const MapMarkers = {
  get: () =>
    requests.get('/user/nearby'),
};

export default {
  Session,
  User,
  Account,
  PaymentA2A,
  PaymentC2A,
  PaymentA2C,
  PaymentC2C,
  Payment,
  MapMarkers,
};