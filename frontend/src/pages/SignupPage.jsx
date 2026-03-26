import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

function SignupPage() {
  const navigate = useNavigate();
  const { signup } = useAuth();
  const [formData, setFormData] = useState({ full_name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;
    setFormData((current) => ({ ...current, [name]: value }));
  }

  function validateForm() {
    if (!formData.full_name.trim()) {
      return "Full name is required.";
    }

    if (!formData.email.trim()) {
      return "Email is required.";
    }

    if (!formData.password.trim()) {
      return "Password is required.";
    }

    if (formData.password.length < 8) {
      return "Password must be at least 8 characters.";
    }

    return "";
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);

    try {
      await signup(formData);
      navigate("/predict");
    } catch (err) {
      setError(err.message || "Unable to create the account.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="auth-shell panel">
      <div className="section-heading">
        <span className="eyebrow">Authentication</span>
        <h1>Create your account</h1>
      </div>

      <form className="auth-form" onSubmit={handleSubmit}>
        <label>
          <span>Full name</span>
          <input name="full_name" onChange={handleChange} type="text" value={formData.full_name} />
        </label>

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
          {loading ? "Creating account..." : "Sign up"}
        </button>
      </form>

      <p className="muted-copy">
        Already have an account?{" "}
        <Link className="inline-link" to="/login">
          Log in
        </Link>
      </p>
    </section>
  );
}

export default SignupPage;
