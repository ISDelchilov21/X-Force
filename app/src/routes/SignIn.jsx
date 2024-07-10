import React from "react";
import Navbar from "../components/navbar/Navbar";
import "../styles/sign-in.css"
export default function SignIn() {
  return (
    <div className="page">
      <Navbar />
      <div className="form">
        <form className="form-container">
          
          <div>
          <label>Enter username</label>
            <input type="text" placeholder="Username"></input>
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
            <button type="submit">Submit</button>
          </div>
        </form>
      </div>
    </div>
  );
}
