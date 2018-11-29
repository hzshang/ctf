import { observable, action, decorate } from 'mobx';
import agent from '../agent';

class AccountStore {
  pageLoaded = false;

  accountInfo = {
  };

  cards = [
  ];

  mapMarkers = [

  ];

  getMapMarkers() {
    agent.MapMarkers.get()
      .then(action(({user_info}) => {
        const min_x = 0.600;
        const max_x = 0.850;
        const min_y = 0.400;
        const max_y = 0.800;
        this.mapMarkers = [];
        user_info['users'].map((user, idx) =>
          this.mapMarkers.push({
            x: 55 + min_x + Math.random() * (max_x - min_x),
            y: 37 + min_y + Math.random() * (max_y - min_y),
            id: user.id,
            username: user.username,
          })
        );
      }))
      .catch(action(err => {
        throw err.response.body.message;
      }))
      .finally(action(() => {
      }));
    //this.mapMarkers.push([55.700, 37.605, '1337', 'qew']);
    //this.mapMarkers.push([55.650, 37.605, '1338', 'aaa']);
    //this.mapMarkers.push([55.750, 37.605, '1339', 'bbb']);
    //this.mapMarkers.map((marker, idx) => console.log(marker));
    return null;
  }

  setPageLoadingStatus(isLoaded) {
    this.pageLoaded = isLoaded;
  }

  getAccountInfo() {
    return agent.Account.current()
      .then(action(({ data }) => {
        if (('account' in data) && ('id' in data['account']))
          this.accountInfo['id'] = data['account']['id'];
        if (('account' in data) && ('balance' in data['account']))
          this.accountInfo['balance'] = data['account']['balance'];
        if ('cards' in data)
          this.cards = data['cards'];
      }))
      .catch(action(err => {
        throw err.response.body.message;
      }))
      .finally(action(() => {
        this.setPageLoadingStatus(true);
      }));
  }

  createNewCard = async () => {
    await agent.Account.new()
      .then(action(() => {
      }))
      .catch(action(err => {
        throw err.response.body.message;
      }))
      .finally(action(() => {
      }));
    await this.getAccountInfo();
  }

}
decorate(AccountStore, {
  mapMarkers: observable,
  pageLoaded: observable,
  accountInfo: observable.struct,
  cards: observable,
  setPageLoadingStatus: action,
  getAccountInfo: action,
  createNewCard: action,
  getMapMarkers: action,
});

export default new AccountStore();
