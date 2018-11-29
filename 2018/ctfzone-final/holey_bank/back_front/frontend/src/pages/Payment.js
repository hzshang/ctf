import React, { Component } from 'react';
import { Layout, Divider, Avatar, Row, Col, Modal, Button, Table, Spin } from 'antd';
import { inject, observer } from 'mobx-react';
import { withRouter } from 'react-router-dom';

const { Footer, Content } = Layout;

const columns = [{
  title: 'Type',
  dataIndex: 'type',
  key: 'type',
  render: (type) => {
    let avatar;

    if ( type === 'c2c' )
      avatar = <Avatar style={{ backgroundColor: '#87d068' }}>C2C</Avatar>;
    else if ( type === 'a2a' )
      avatar = <Avatar style={{ backgroundColor: '#c068d0' }}>A2A</Avatar>;
    else if ( type === 'a2c' )
      avatar = <Avatar style={{ backgroundColor: '#cd8c66' }}>A2C</Avatar>;
    else if ( type === 'c2a' )
      avatar = <Avatar style={{ backgroundColor: '#7193c7' }}>C2A</Avatar>;
    else
      avatar = <Avatar>???</Avatar>;

    return (
      avatar
    )
  }
}, {
  title: 'Date',
  dataIndex: 'date',
  key: 'date',
}, {
  title: 'From',
  dataIndex: 'from',
  key: 'from',
}, {
  title: 'To',
  dataIndex: 'to',
  key: 'to',
}, {
  title: 'Sum',
  key: 'sum',
  dataIndex: 'sum',
  render: (sum) => (
    <div>
      ${ sum }
    </div>
  )
}];

class Payment extends Component {
  state = { visible: false };

  showModal = () => {
    this.setState({
      visible: true,
    });
  };

  handleOk = (e) => {
    this.setState({
      visible: false,
    });
  };

  handleCancel = (e) => {
    this.setState({
      visible: false,
    });
  };

  componentDidMount() {
    this.props.paymentStore.setPageLoadingStatus(false);
    this.props.paymentStore.getHistory();
  };

  render() {
    if (this.props.paymentStore.pageLoaded) {
      return (
        <Layout className="layout" style={{height: "100vh"}}>
          <Content className="center-horizontal" style={{ paddingTop: 25 }}>
            <div style={{background: '#fff', padding: 24, minHeight: 280}}>
              <a href="/api/report"><Button
                style={{float: 'right'}}
                type="primary"
                icon="download"
              >
                Download Statement
              </Button></a>
              <h3>Payments</h3>
              <Divider />
              <Table columns={columns} dataSource={ this.props.paymentStore.history } style={{ width: 1000, minWidth: 1000 }}/>
            </div>
          </Content>
          <Modal
            title="Creating of new payment"
            visible={this.state.visible}
            onOk={this.handleOk}
            onCancel={this.handleCancel}
          >
          </Modal>
        </Layout>
      );
    } else {
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

export default inject('paymentStore')(
  withRouter(observer(Payment))
);
