import React from 'react';
import { Route, Redirect, Switch } from 'react-router';
import { inject, observer } from 'mobx-react';

import Account from './pages/Account';
import Error from './pages/Error';
import Payment from './pages/Payment';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';

const LoggedOnlyRoute = inject('commonStore')(observer(({commonStore, ...rest}) => {
  return commonStore.isLogged === true
    ? <Route {...rest} />
    : <Redirect to='/login' />
}));

const NonLoggedOnlyRoute = inject('commonStore')(observer(({commonStore, ...rest}) => {
  return commonStore.isLogged === false
    ? <Route {...rest} />
    : <Redirect to='/' />
}));

const Routes = props => {
  return (
      <div>
        <Switch>
          <LoggedOnlyRoute exact path="/" component={Account}/>
          <LoggedOnlyRoute exact path="/payment" component={Payment}/>
          <LoggedOnlyRoute exact path="/profile" component={Profile}/>
          <NonLoggedOnlyRoute exact path="/login" component={Login}/>
          <NonLoggedOnlyRoute exact path="/register" component={Register}/>
          <Route component={Error}/>
        </Switch>
      </div>
  )
};

export default Routes