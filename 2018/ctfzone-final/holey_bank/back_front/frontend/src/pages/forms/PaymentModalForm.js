import React, { Component } from 'react';
import { Form, Input, Select, InputNumber, Modal } from 'antd';
import { inject, observer } from 'mobx-react';
import { withRouter } from 'react-router-dom';

const FormItem = Form.Item;
const InputGroup = Input.Group;
const Option = Select.Option;

class PaymentModalForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      from: props.paymentData.from,
      fromType: props.paymentData.fromType,
      to: props.paymentData.to,
      toType: props.paymentData.toType,
    };
  }

  render() {
    const { visible, onCancel, onOk, form } = this.props;
    const { getFieldDecorator } = form;

    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 5 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 19 },
      },
    };

    let fromInput;
    if ( this.state.from && this.state.fromType )
      fromInput =
        <FormItem {...formItemLayout} label="From">
          <InputGroup compact>
            {getFieldDecorator('fromType',
              {
                initialValue: this.state.fromType,
                rules: [{
                  // ...
                }, {
                  required: true, message: 'Please input source type!',
                }],
              })(
              <Select disabled style={{ width: '25%' }}>
                <Option value="Card">Card</Option>
                <Option value="Account">Account</Option>
              </Select>
            )}
            {getFieldDecorator('from',
              {
                initialValue: this.state.from,
                rules: [{
                  // ...
                }, {
                  required: true, message: 'Please input source number!',
                }],
              })(
              <Input disabled style={{ width: '75%' }} />
            )}
          </InputGroup>
        </FormItem>;
    else
      fromInput =
        <FormItem {...formItemLayout} label="From">
          <InputGroup compact>
            {getFieldDecorator('fromType',
              {
                initialValue: 'Card',
                rules: [{
                  // ...
                }, {
                  required: true, message: 'Please input source type!',
                }],
              })(
              <Select style={{ width: '25%' }}>
                <Option value="Card">Card</Option>
                <Option value="Account">Account</Option>
              </Select>
            )}
            {getFieldDecorator('from',
              {
                rules: [{
                  // ...
                }, {
                  required: true, message: 'Please input source number!',
                }],
              })(
              <Input style={{ width: '75%' }} />
            )}
          </InputGroup>
        </FormItem>;

    let toInput;
    if ( this.state.to && this.state.toType )
      toInput =
        <FormItem {...formItemLayout} label="To">
          <InputGroup compact>
            {getFieldDecorator('toType',
              {
                initialValue: this.state.toType,
                rules: [{
                  // ...
                }, {
                  required: true, message: 'Please input source type!',
                }],
              })(
              <Select disabled style={{ width: '25%' }}>
                <Option value="Card">Card</Option>
                <Option value="Account">Account</Option>
              </Select>
            )}
            {getFieldDecorator('to',
              {
                initialValue: this.state.to,
                rules: [{
                  // ...
                }, {
                  required: true, message: 'Please input source number!',
                }],
              })(
              <Input disabled style={{ width: '75%' }} />
            )}
          </InputGroup>
        </FormItem>;
    else
      toInput =
        <FormItem {...formItemLayout} label="To">
          <InputGroup compact>
            {getFieldDecorator('toType',
              {
                initialValue: 'Card',
                rules: [{
                  // ...
                }, {
                  required: true, message: 'Please input source type!',
                }],
              })(
              <Select style={{ width: '25%' }}>
                <Option value="Card">Card</Option>
                <Option value="Account">Account</Option>
              </Select>
            )}
            {getFieldDecorator('to',
              {
                rules: [{
                  // ...
                }, {
                  required: true, message: 'Please input source number!',
                }],
              })(
              <Input style={{ width: '75%' }} />
            )}
          </InputGroup>
        </FormItem>;

    return (
      <Modal
        title="New Payment"
        visible={visible}
        onOk={onOk}
        onCancel={onCancel}
        okText="Approve"
        cancelText="Cancel"
      >
        <Form>
          {fromInput}
          {toInput}
          <FormItem {...formItemLayout} label="Comment">
            <InputGroup compact>
              {getFieldDecorator('comment',
                {
                  rules: [{
                    required: true
                  }]
                })(
                <Input
                  style={{width: '100%'}}
                />
              )}
            </InputGroup>
          </FormItem>
          <FormItem {...formItemLayout} label="Sum">
            <InputGroup compact>
              {getFieldDecorator('sum',
                {
                  rules: [{
                    required: true
                  }]
                })(
                <InputNumber
                  formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  style={{width: '100%'}}
                  min={0} max={100000} step={0.01}
                />
              )}
            </InputGroup>
          </FormItem>
        </Form>
      </Modal>
    );
  }
}

export default inject('commonStore')(
  withRouter(
    Form.create()(observer(PaymentModalForm))
  )
);
