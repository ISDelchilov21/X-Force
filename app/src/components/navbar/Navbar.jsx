import React from "react";
import { Link } from "react-router-dom";
import "./navbar.css";
export default function Navbar() {
  return (
    <div>
      <ul className="navbar">
        <div className="left-side">
          <li>
            <Link to="/">X-Force</Link>
          </li>
        </div>

        <div className="right-side">
          <li>
            <Link to="/signin">SignIn</Link>
          </li>
          <li>
            <Link to="/signup">SignUp</Link>
          </li>
        </div>
      </ul>
    </div>
  );
}
