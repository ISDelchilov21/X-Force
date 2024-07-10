import React from "react";
import Navbar from "../components/navbar/Navbar";
import "../styles/sign-up.css"

export default function SignUp() {
  return (
    <div className="page">
      <Navbar />
      SignUp
      <div className="form">
        <form className="form-container">
          <div>
            <label >Enter e - mail:</label>
            <input type="text" placeholder="Email"></input>
          </div>
          <div>
          <label>Enter username</label>
            <input type="text" placeholder="Username"></input>
          </div>
          <div>
          <label >Choose your role</label>

            <input type="text" placeholder="Role"></input>
          </div>
          <div>
          <label >Enter password</label>

            <input
              type="password"
              name="password"
              placeholder="Password"
            ></input>
          </div>
          <div>
          <label >Confirm password</label>

            <input
              type="password"
              name="password"
              placeholder="Password"
            ></input>
          </div>
          <div>
            <button type="submit">Submit</button>
          </div>
        </form>
      </div>
    </div>
  );
}
