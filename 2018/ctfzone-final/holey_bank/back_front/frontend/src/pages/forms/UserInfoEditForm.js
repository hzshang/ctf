import React, { Component } from 'react';
import { Form, Input, Button, Row } from 'antd';
import { inject, observer } from 'mobx-react';
import { withRouter } from 'react-router-dom';

const FormItem = Form.Item;

class UserInfoEditForm extends Component {
  render() {
    const { getFieldDecorator } = this.props.form;

    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 4 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 19 },
      },
    };
    const tailFormItemLayout = {
      wrapperCol: {
        xs: {
          span: 24,
          offset: 0,
        },
        sm: {
          span: 16,
          offset: 7,
        },
      },
    };
    return (
      <Form className="profile-form" onSubmit={this.handleUpdateUserInfo}>
        <Row gutter={24}>
          <FormItem {...formItemLayout} label="Name">
            {getFieldDecorator('first_name', {
              valuePropName: 'value',
              initialValue: this.props.userStore.userInfo['full_name'],
            })(
              <Input />
            )}
          </FormItem>
          <FormItem {...formItemLayout} label="Email">
            {getFieldDecorator('email', {
              valuePropName: 'value',
              initialValue: this.props.userStore.userInfo['email'],
            })(
              <Input />
            )}
          </FormItem>
          <FormItem {...formItemLayout} label="Phone">
            {getFieldDecorator('phone', {
              valuePropName: 'value',
              initialValue: this.props.userStore.userInfo['phone'],
            })(
              <Input />
            )}
          </FormItem>
        </Row>
        <Row>
          <FormItem {...tailFormItemLayout} style={{"margin-bottom": "0px"}}>
            <div style={{ textAlign: 'right' }}>
              <Button type="primary" htmlType="submit">Save</Button>
              <Button style={{ marginLeft: 8 }} onClick={this.handleReset}>Reset</Button>
            </div>
          </FormItem>
        </Row>
      </Form>
    );
  }
}

export default inject('userStore')(
  withRouter(
    Form.create()(observer(UserInfoEditForm))
  )
);
