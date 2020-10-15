import React from 'react';

function SignUp() {


    

    return (
        <div className="ui card" style={{padding: '40px 10px', width: '400px', maxWidth: '80%'}}>
            <div className="content">
                <div className="header">Sign Up</div>
            </div>
            <div className="content">
                <form className="ui form">
                    <div className="field">
                        <label>Email</label>
                        <input type="text" name="first-name" placeholder="johndoe@email.com"/>
                    </div>
                    <div className="field">
                        <label>Twitter Username</label>
                        <input type="text" name="last-name" placeholder="johndoe"/>
                    </div>
                    <div className="field">
                        <label>Password</label>
                        <input type="password" name="password"/>
                    </div>
                    <div className="field">
                        <label>Repeat Password</label>
                        <input type="password" name="password"/>
                    </div>
                    <div className="field">
                        <div className="ui checkbox">
                            <input type="checkbox" tabindex="0" className="hidden"/>
                            <label>I agree to the Terms and Conditions</label>
                        </div>
                    </div>
                    <button className="ui button" type="submit">Submit</button>
                </form>
            </div>
        </div>
    );
}

export default SignUp;