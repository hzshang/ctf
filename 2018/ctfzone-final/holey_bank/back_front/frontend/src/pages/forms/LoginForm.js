import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Form, Icon, Input, Button, Checkbox, Divider, Spin, message } from 'antd';
import { Redirect } from 'react-router-dom'
import { inject, observer } from 'mobx-react';
import { withRouter } from 'react-router-dom';

const FormItem = Form.Item;

class LoginForm extends Component {

  handleSubmit = (e) => {
    e.preventDefault();
    const { getFieldValue } = this.props.form;
    this.props.form.validateFields((err, values) => {
      if (!err) {
        let username = getFieldValue('username');
        let password = getFieldValue('password');
        this.props.commonStore.login(username, password)
          .catch(error => {
            message.error(error);
            this.props.form.setFieldsValue({
             password: "",
             });
          });
      }
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;
    if (this.props.commonStore.isLogged) {
      return <Redirect to='/' />
    }

    let submitButton;
    if (this.props.commonStore.inProgress) {
      submitButton = (
        <Button disabled="disabled" type="primary" htmlType="submit" className="login-form-button">
          <Spin size="small" />
        </Button>)
    } else {
      submitButton = (
        <Button type="primary" htmlType="submit" className="login-form-button">
          Log in
        </Button>);
    }

    return (
      <Form onSubmit={this.handleSubmit} className="login-form">
        <FormItem>
          <Divider>Sign in</Divider>
        </FormItem>
        <FormItem>
          {getFieldDecorator('username', {
            rules: [{ required: true, message: 'Please input your username!' }],
          })(
            <Input
              prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
              placeholder="Username"
            />
          )}
        </FormItem>
        <FormItem>
          {getFieldDecorator('password', {
            rules: [{ required: true, message: 'Please input your Password!' }],
          })(
            <Input
              prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
              type="password"
              placeholder="Password"
            />
          )}
        </FormItem>
        <FormItem>
          {getFieldDecorator('remember', {
            valuePropName: 'checked',
            initialValue: true,
          })(
            <Checkbox>Remember me</Checkbox>
          )}
          <a className="login-form-forgot" href="">Forgot password</a>
          {submitButton}
          Or <Link to="/register">register now!</Link>
        </FormItem>
      </Form>
    );
  }
}

//export default Form.create()(LoginForm);
//export default LoginForm;
export default inject('commonStore')(
  withRouter(
    Form.create()(observer(LoginForm))
  )
);
