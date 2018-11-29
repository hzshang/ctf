import { observable, action, decorate } from 'mobx';
import agent from '../agent';
import CommonStore from './commonStore';

class UserStore {
  userInfo = {
  };

  getUserInfo() {
    return agent.User.current()
      .then(action(({ user_info }) => {
        if ('full_name' in user_info)
          this.userInfo['full_name'] = user_info['full_name'];
        if ('residence' in user_info)
          this.userInfo['residence'] = user_info['residence'];
        if ('passport_number' in user_info)
          this.userInfo['passport'] = user_info['passport_number'];
        CommonStore.setIsLogged(true);
      }))
      .catch(action(err => {
        throw err.response.body.message;
      }))
      .finally(action(() => {
        CommonStore.setAppLoaded();
      }));
  }

  async createNewUser(username, password, first_name, last_name, passport, residence) {
    let isError = false;
    let result = await agent.User.new(username, password, first_name, last_name, passport, residence)
      .then(action(() => {
      }))
      .catch(action(err => {
        isError = true;
        throw err.response.body.message;
      }))
      .finally(action(() => {
        if ( isError )
          CommonStore.setAppLoaded();
      }));
    if ( !isError )
      await CommonStore.login(username, password);
    return result;
  }

}
decorate(UserStore, {
  userInfo: observable.struct,
  getUserInfo: action,
  createNewUser: action,
});

export default new UserStore();
