import React, { Component } from 'react';
import '../App.css';
import { withRouter } from 'react-router-dom';
import { inject, observer } from 'mobx-react';
import Routes from '../routes.js';
import { Spin, Row, Col } from 'antd'

import TopMenu from './TopMenu';

class App extends Component {

  componentDidMount() {
    this.props.userStore.getUserInfo();
  }

  render() {
    if (this.props.commonStore.appLoaded) {
      return (
        <div>
          <TopMenu />
          <Routes/>
        </div>
      );
    }
    else
    {
      return (
        <div>
          <div style={{ padding: '30px 0px 0px 0px' }}>
          </div>
          <Row>
            <Col span={11} />
            <Col span={2}><Spin size="large" /></Col>
            <Col span={11} />
          </Row>
        </div>
      )
    }
  }
}

//export default App;
export default inject('commonStore', 'userStore', 'accountStore')(
  withRouter(observer(App))
);
