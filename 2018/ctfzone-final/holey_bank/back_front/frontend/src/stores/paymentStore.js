import { observable, action, decorate } from 'mobx';
import agent from '../agent';
import AccountStore from './accountStore';

class PaymentStore {
  pageLoaded = false;

  history = [

  ];

  setPageLoadingStatus(isLoaded) {
    this.pageLoaded = isLoaded;
  }

  async createPayment (from, fromType, to, toType, comment, sum) {
    let result = null;
    if ( fromType === 'Card' && toType === 'Card' )
    {
      result = await agent.PaymentC2C.new(from, to, comment, sum)
        .then(action(() => {
        }))
        .catch(action(err => {
          throw err.response.body.message;
        }))
        .finally(action(() => {
        }));
    }
    else if ( fromType === 'Card' && toType === 'Account' ) {
      result = await agent.PaymentC2A.new(from, comment, sum)
        .then(action(() => {
        }))
        .catch(action(err => {
          throw err.response.body.message;
        }))
        .finally(action(() => {
        }));
    }
    else if ( fromType === 'Account' && toType === 'Card' ) {
      result = await agent.PaymentA2C.new(to, comment, sum)
        .then(action(() => {
        }))
        .catch(action(err => {
          throw err.response.body.message;
        }))
        .finally(action(() => {
        }));
    }
    else if ( fromType === 'Account' && toType === 'Account' ) {
      result = await agent.PaymentA2A.new(to, comment, sum)
        .then(action(() => {
        }))
        .catch(action(err => {
          throw err.response.body.message;
        }))
        .finally(action(() => {
        }));
    }
    await AccountStore.getAccountInfo();
    return result;
  }

  getHistory () {
    return agent.Payment.history()
      .then(action((data) => {
        this.history = data.data.history.reverse();
      }))
      .catch(action(err => {
        throw err.response.body.message;
      }))
      .finally(action(() => {
        this.setPageLoadingStatus(true);
      }));
  }
}
decorate(PaymentStore, {
  pageLoaded: observable,
  setPageLoadingStatus: action,
  createPayment: action,
  getHistory: action,
});

export default new PaymentStore();
