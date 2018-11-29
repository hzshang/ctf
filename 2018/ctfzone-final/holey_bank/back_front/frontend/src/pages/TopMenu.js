import React, { Component } from 'react';
import { NavLink, withRouter } from 'react-router-dom';
import '../index.css';
import { inject, observer } from 'mobx-react';
import { Redirect } from 'react-router-dom'

import { Menu, Icon } from 'antd';

const SubMenu = Menu.SubMenu;
const MenuItemGroup = Menu.ItemGroup;

class TopMenu extends Component {
  handleLogout = (e) => {
    this.props.commonStore.logout();
  };

  render() {
    if (!this.props.commonStore.isLogged) {
      return <Redirect to='/login' />
    }
    const { location } = this.props;
    return (
      <Menu
        onClick={this.handleClick}
        selectedKeys={[location.pathname]}
        mode="horizontal"
        defaultSelectedKeys={['2']}
        style={{ lineHeight: '64px' }}
      >
        <SubMenu
          style={{float: 'right'}}
          title={
            <span className="submenu-title-wrapper">
              <Icon type="user" />{ this.props.userStore.userInfo.full_name }
            </span>
          }
        >
          <MenuItemGroup>
            <Menu.Item key="setting:2" onClick={this.handleLogout}><Icon type="logout" />Logout</Menu.Item>
          </MenuItemGroup>
        </SubMenu>
        <Menu.Item key="/">
          <NavLink to="/" className="nav-text">
            <Icon type="bank" />Account
          </NavLink>
        </Menu.Item>
        <Menu.Item key="/payment">
          <NavLink to='/payment' className="nav-text">
            <Icon type="credit-card" />History
          </NavLink>
        </Menu.Item>
      </Menu>
    );
  }
}

export default inject('commonStore', 'userStore')(
  withRouter(observer(TopMenu))
);
