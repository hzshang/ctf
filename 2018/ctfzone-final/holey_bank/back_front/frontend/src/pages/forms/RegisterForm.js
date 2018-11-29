import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Form, Icon, Input, Button, Divider, message } from 'antd';
import { Redirect } from 'react-router-dom'
import { inject, observer } from 'mobx-react';
import { withRouter } from 'react-router-dom';

const FormItem = Form.Item;

function* entries(obj) {
  for (let key of Object.keys(obj)) {
    yield [key, obj[key]];
  }
}

class RegisterForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      registerFinished: false
    };
  }

  handleSubmit = (e) => {
    e.preventDefault();
    const { getFieldValue } = this.props.form;
    this.props.form.validateFields((err, values) => {
      if (!err) {
        let username = getFieldValue('username');
        let password = getFieldValue('password');
        let firstname = getFieldValue('firstname');
        let lastname = getFieldValue('lastname');
        let passport = getFieldValue('passport');
        let residence = getFieldValue('residence');
        this.props.userStore.createNewUser(username, password, firstname, lastname, passport, residence)
          .then(() => {
            this.setState({
              registerFinished: true
            });
          })
          .catch(error => {
            if ( typeof error === "object" )
              for (let [key, value] of entries(error)) {
                message.error(`${key}: ${value}`);
              }
            else
              message.error(error);
          });
      }
    });
  };

  render() {
    if (this.state.registerFinished) {
      return <Redirect to='/login' />
    }

    const { getFieldDecorator } = this.props.form;
    return (
      <Form onSubmit={this.handleSubmit} className="login-form">
        <FormItem>
          <Divider>Registration</Divider>
        </FormItem>
        <FormItem>
          {getFieldDecorator('username', {
            rules: [{
              required: true,
              message: 'Please input your username!'
            }],
          })(
            <Input prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />} placeholder="Username" />
          )}
        </FormItem>
        <FormItem>
          {getFieldDecorator('firstname', {
            rules: [{
              required: true,
              message: 'Please input your first name!'
            }],
          })(
            <Input prefix={<Icon type="solution" style={{ color: 'rgba(0,0,0,.25)' }} />} placeholder="First Name" />
          )}
        </FormItem>
        <FormItem>
          {getFieldDecorator('lastname', {
            rules: [{
              required: true,
              message: 'Please input your last name!'
            }],
          })(
            <Input prefix={<Icon type="solution" style={{ color: 'rgba(0,0,0,.25)' }} />} placeholder="Last Name" />
          )}
        </FormItem>
        <FormItem>
          {getFieldDecorator('passport', {
            rules: [{
              required: true,
              pattern: new RegExp("^[0-9]*$"),
              message: 'Passport has contain only numeric symbols!'
            }],
          })(
            <Input prefix={<Icon type="solution" style={{ color: 'rgba(0,0,0,.25)' }} />} placeholder="Passport" />
          )}
        </FormItem>
        <FormItem>
          {getFieldDecorator('residence', {
            rules: [{
              required: true,
              message: 'Please input your last name!'
            }],
          })(
            <Input prefix={<Icon type="solution" style={{ color: 'rgba(0,0,0,.25)' }} />} placeholder="Residence" />
          )}
        </FormItem>
        <FormItem>
          {getFieldDecorator('password', {
            rules: [{
              required: true,
              message: 'Please input your Password!'
            }],
          })(
            <Input prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />} type="password" placeholder="Password" />
          )}
        </FormItem>
        <FormItem>
          <Button type="primary" htmlType="submit" className="login-form-button">
            Register
          </Button>
          Back <Link to="/login">to login!</Link>
        </FormItem>
      </Form>
    );
  }
}

//export default Form.create()(RegisterForm);
export default inject('userStore')(
  withRouter(
    Form.create()(observer(RegisterForm))
  )
);