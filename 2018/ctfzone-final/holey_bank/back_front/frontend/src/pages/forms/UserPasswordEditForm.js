import React, { Component } from 'react';
import { Form, Input, Button, Row } from 'antd';
import { inject, observer } from 'mobx-react';
import { withRouter } from 'react-router-dom';

const FormItem = Form.Item;

class UserPasswordEditForm extends Component {
  render() {
    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 5 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 18 },
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
          <FormItem {...formItemLayout} label="Old Password">
            <Input type="password" />
          </FormItem>
          <FormItem {...formItemLayout} label="New Password">
            <Input type="password" />
          </FormItem>
        </Row>
        <Row>
          <FormItem {...tailFormItemLayout} style={{"margin-bottom": "0px"}}>
            <div style={{ textAlign: 'right' }}>
              <Button type="primary" htmlType="submit">Save</Button>
            </div>
          </FormItem>
        </Row>
      </Form>
    );
  }
}

export default inject('commonStore')(
  withRouter(
    Form.create()(observer(UserPasswordEditForm))
  )
);
