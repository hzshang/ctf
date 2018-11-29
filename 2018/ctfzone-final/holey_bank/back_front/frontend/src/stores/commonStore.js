import { observable, action, decorate } from 'mobx';
import agent from '../agent';
import UserStore from './userStore';

class CommonStore {
  isLogged = false;
  inProgress = false;
  appLoaded = false;

  setAppLoaded() {
    this.appLoaded = true;
  }

  setIsLogged(isLogged) {
    this.isLogged = isLogged;
  }

  login(username, password) {
    this.inProgress = true;
    return agent.Session.login(username, password)
      .then(action(() => {
        UserStore.getUserInfo();
        // this.isLogged = true;
      }))
      .catch(action(err => {
        throw err.response.body.message;
      }))
      .finally(action(() => {
        this.inProgress = false;
      }));
  }

  logout() {
    this.isLogged = false;
    return agent.Session.logout()
      .then(action(() => {
        this.isLogged = false;
      }))
      .catch(action(err => {
        throw err.response.body.message;
      }))
  }
}
decorate(CommonStore, {
  isLogged: observable,
  inProgress: observable,
  appLoaded: observable,
  login: action,
  logout: action,
  changeIsLogged: action,
  setAppLoaded: action,
});

export default new CommonStore();
