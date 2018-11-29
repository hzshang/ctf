import React, { Component } from 'react';
import { Icon, Layout, Row, Col, Divider, Button, Spin, Modal, message } from 'antd';
import { inject, observer } from 'mobx-react';
import { withRouter } from 'react-router-dom';
import { Map, Marker, Popup, TileLayer } from 'react-leaflet'
import {Icon as MDIcon} from '@mdi/react'
import { mdiCreditCardPlus, mdiMapLegend } from '@mdi/js'

import CardsList from './CardsList'
import PaymentModalForm from './forms/PaymentModalForm'
import L from 'leaflet';

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

const { Footer, Content } = Layout;
const confirm = Modal.confirm;

class Account extends Component {

  state = {
    paymentModalVisible: false,
    confirmLoadingModalVisible: false,
    mapModalVisible: false,
    paymentData: {
      from: null,
      to: null,
      fromType: null,
      toType: null,
    },
    //markers: [[55.745, 37.605],[55.700, 37.605]]
  };

  showMapModal = () => {
    this.setState({
      mapModalVisible: true,
    });
  };

  handleCancelMapModal = () => {
    this.setState({
      mapModalVisible: false,
    });
  };

  showPaymentModal = (from, fromType, to, toType) => {
    this.state.paymentData = {
      from: from,
      fromType: fromType,
      to: to,
      toType: toType,
    };
    this.setState({
      paymentModalVisible: true,
    });
  };

  handleOkPaymentModal = () => {
    this.setState({
      confirmLoadingModalVisible: true,
    });

    const form = this.formRef;

    form.validateFields((err, values) => {
      if (err) {
        return;
      }

      this.props.paymentStore.createPayment(values.from, values.fromType, values.to,
                                            values.toType, values.comment, values.sum)
        .catch(error => {
          message.error(error);
        });

      this.setState({ paymentModalVisible: false });
    });
  };

  handleCancelPaymentModal = () => {
    this.setState({
      paymentModalVisible: false,
    });
  };

  showConfirm = () => {
    confirm({
      title: 'New Card',
      content: 'Do you want to create new bank card?',
      onOk: this.createNewCard,
      onCancel() {},
    });
  };

  createNewCard = () => {
    this.props.accountStore.createNewCard();
  };

  saveFormRef = (formRef) => {
    this.formRef = formRef;
  };

  componentDidMount() {
    this.props.accountStore.setPageLoadingStatus(false);
    this.props.accountStore.getMapMarkers();
    this.props.accountStore.getAccountInfo();
  };

  render() {
    console.log(this.state.markers);
    if (this.props.accountStore.pageLoaded) {
      return (
        <Layout className="layout" style={{height: "100vh"}}>
          <Content className="center-horizontal" style={{ paddingTop: 25 }}>
            { this.state.paymentModalVisible && (
              <PaymentModalForm
                wrappedComponentRef = { this.saveFormRef }
                paymentData = { this.state.paymentData }
                visible = { this.state.paymentModalVisible }
                onCancel = { this.handleCancelPaymentModal }
                onOk = { this.handleOkPaymentModal }
              />
            )}
            <Row>
              <Col span={6} />
              <Col span={12} style={{minWidth: '780px'}}>
                <div style={{background: '#fff', padding: 25, minHeight: 280, minWidth: 780, maxWidth: 780 }}>
                  <Button
                    style={{float: 'right'}}
                    type="primary"
                    onClick={this.showConfirm}>
                    <MDIcon path={mdiCreditCardPlus}
                            size={1}
                            color="white"
                            style={{paddingTop: 3}}/>
                </Button>
                  <Button
                    style={{float: 'right', marginRight: 8}}
                    type="primary"
                    onClick={this.showMapModal}>
                    <MDIcon path={mdiMapLegend}
                            size={1}
                            color="white"
                            style={{paddingTop: 3}}/>
                  </Button>
                  <h3>My Account</h3>
                  <Divider />
                  <div style={{float: 'right', paddingRight: 26, textAlign: 'center'}}>
                    <h3>${ this.props.accountStore.accountInfo.balance }</h3>
                  </div>
                  <h3>Account Information <Icon type="down"/></h3>
                  <div style={{paddingLeft: 20, paddingTop: 10,}}>
                    <Row>
                      <Col span={3}>
                        <div style={{float: 'right', paddingRight: 10}}>Client name</div>
                      </Col>
                      <Col span={21}>{ this.props.userStore.userInfo.full_name }</Col>
                    </Row>
                    <Row>
                      <Col span={3}>
                        <div style={{float: 'right', paddingRight: 10}}>Passport</div>
                      </Col>
                      <Col span={21}>{ this.props.userStore.userInfo.passport }</Col>
                    </Row>
                    <Row>
                      <Col span={3}>
                        <div style={{float: 'right', paddingRight: 10}}>Residence</div>
                      </Col>
                      <Col span={21}>{ this.props.userStore.userInfo.residence }</Col>
                    </Row>
                    <Row>
                      <Col span={3}>
                        <div style={{float: 'right', paddingRight: 10}}>Account ID</div>
                      </Col>
                      <Col span={21}>{ this.props.accountStore.accountInfo.id }</Col>
                    </Row>
                  </div>
                  <CardsList
                    wrappedComponentRef={ this.saveFormRef }
                    cards={ this.props.accountStore.cards }
                    holderName={ this.props.userStore.userInfo.full_name }
                    showPaymentModal={ this.showPaymentModal }
                    accountNumber={ this.props.accountStore.accountInfo.id }
                  />
                  <Modal
                    visible={this.state.mapModalVisible}
                    title="People nearby"
                    onCancel={this.handleCancelMapModal}
                    footer={null}
                    width={800}
                  >
                    <div>
                      <Map
                        center={[55.745, 37.605]}
                        zoom={10}
                      >
                          <TileLayer
                            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                            url='http://{s}.tile.osm.org/{z}/{x}/{y}.png'
                          />
                          {this.props.accountStore.mapMarkers.map((marker, idx) =>
                            <Marker key={`marker-${idx}`} position={[marker.x, marker.y]}>
                              <Popup>
                                <span>ID: {marker.id}<br/> Username: {marker.username}</span>
                              </Popup>
                            </Marker>
                          )}
                      </Map>
                    </div>
                  </Modal>
                </div>
              </Col>
              <Col span={6} />
            </Row>
          </Content>
        </Layout>
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

export default inject('userStore', 'accountStore', 'paymentStore')(
  withRouter(observer(Account))
);
