import React, { Component } from 'react';

import { Layout, Row, Col, Divider } from 'antd';

import UserInfoEditForm from './forms/UserInfoEditForm';
import UserPasswordEditForm from './forms/UserPasswordEditForm';

const { Footer, Content } = Layout;

class Profile extends Component {
  render() {
    return (
      <Layout className="layout" style={{height:"100vh"}}>
        <Content style={{ padding: '25px 50px 0px 50px' }}>
          <Row>
            <Col span={6} />
            <Col span={12} style={{ minWidth: '600px' }}>
              <div style={{ background: '#fff', padding: 25 }}>
                <h3>My Profile</h3>
                <Divider />
                <UserInfoEditForm />
                <br />
                <UserPasswordEditForm />
              </div>
            </Col>
            <Col span={6} />
          </Row>
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          CTFZone Finals © 2018
        </Footer>
      </Layout>
    );
  }
}

export default Profile;
