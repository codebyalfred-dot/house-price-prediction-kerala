import { NavLink } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { user, logout, isAuthenticated, isLoading } = useAuth();

  return (
    <header className="navbar">
      <NavLink className="brandmark" to="/">
        <span className="brandmark-badge">KH</span>
        <div>
          <p>Kerala House Price</p>
          <span>Prediction System</span>
        </div>
      </NavLink>

      <nav className="nav-links">
        <NavLink to="/">Home</NavLink>
        <NavLink to="/predict">Predict</NavLink>
        <NavLink to="/results">Results</NavLink>
      </nav>

      <div className="nav-actions">
        {isLoading ? <span className="status-pill">Checking session...</span> : null}
        {isAuthenticated && user ? (
          <>
            <span className="status-pill">Signed in as {user.full_name}</span>
            <button className="ghost-button" onClick={logout} type="button">
              Logout
            </button>
          </>
        ) : (
          <>
            <NavLink className="ghost-link" to="/login">
              Login
            </NavLink>
            <NavLink className="primary-link" to="/signup">
              Sign up
            </NavLink>
          </>
        )}
      </div>
    </header>
  );
}

export default Navbar;

