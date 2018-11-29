import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import { Provider } from 'mobx-react';

import { BrowserRouter } from 'react-router-dom';
import {configure} from "mobx"

import commonStore from './stores/commonStore';
import userStore from './stores/userStore';
import accountStore from './stores/accountStore';
import paymentStore from './stores/paymentStore';

import App from './pages/App';

const stores = {
  commonStore,
  userStore,
  accountStore,
  paymentStore,
};

configure({enforceActions: 'observed'});

ReactDOM.render(
  <Provider {...stores}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </Provider>
  , document.getElementById('root'));