import React, { Component } from 'react'

function UserGreeting(props) {
    return <h1>Welcome back!</h1>
}

function GuestGreeting(props) {
    return <h1>please sign in</h1>
}

// 按登录条件问候
function Greeting(props) {
    const isLoggedIn = props.isLoggedIn;
    if (isLoggedIn) {
        return <UserGreeting/>
    } else {
        return <GuestGreeting/>
    }
}

function LoginButtion(props) {
    return (
        <button onClick={props.onclick} >登录</button>
    )
}

function LogoutButton(props) {
    return (
        <button onClick={props.onclick} ></button>
    )
}

class LoginControl extends Component {
    constructor(props) {
        super(props)
    }

    handleLoginClick() {
        this.setState({ isLoggedIn: true })
    }

    handleLogoutClick() {
        this.setState({ isLoggedIn: false })
    }

    render() {
        // 初始化是，当然是 false
        const isLoggedIn = this.state.isLoggedIn;

        let button = null;
        if (isLoggedIn) {
            button = (
                <LogoutButton onClick={this.handleLogoutClick}/>
            )
        } else {
            button = (
                <LoginButtion onClick={this.handleLoginClick}/>
            )
        }

        return (
            <div>
                <Greeting isLoggIn={ isLoggedIn } />
                {button}
            </div>
        )
    }
}

