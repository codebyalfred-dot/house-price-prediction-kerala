import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;
    setFormData((current) => ({ ...current, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      await login(formData);
      navigate("/predict");
    } catch (err) {
      setError(err.message || "Unable to log in.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="auth-shell panel">
      <div className="section-heading">
        <span className="eyebrow">Authentication</span>
        <h1>Welcome back</h1>
      </div>

      <form className="auth-form" onSubmit={handleSubmit}>
        <label>
          <span>Email</span>
          <input name="email" onChange={handleChange} type="email" value={formData.email} />
        </label>

        <label>
          <span>Password</span>
          <input name="password" onChange={handleChange} type="password" value={formData.password} />
        </label>

        {error ? <div className="error-banner">{error}</div> : null}

        <button className="primary-button" disabled={loading} type="submit">
          {loading ? "Signing in..." : "Login"}
        </button>
      </form>

      <p className="muted-copy">
        New here?{" "}
        <Link className="inline-link" to="/signup">
          Create an account
        </Link>
      </p>
    </section>
  );
}

export default LoginPage;

