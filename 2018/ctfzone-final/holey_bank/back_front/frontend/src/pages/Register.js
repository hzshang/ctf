import React, { Component } from 'react';

import { Row, Col, Layout } from 'antd';

import RegisterForm from './forms/RegisterForm';

const { Footer, Content } = Layout;

class LoginPage extends Component {
  render() {
    return (
      <div>
        <Layout style={{height:"100vh"}}>
          <Content className="center-vertical-horizontal">
            <div style={{ background: '#fff', padding: 24, minHeight: 280, minWidth: 360, maxWidth: 360 }}>
              <RegisterForm />
            </div>
          </Content>
        </Layout>
      </div>
    );
  }
}

export default LoginPage;
