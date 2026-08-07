import { useState } from "react";
import api from "./api";
import "./theme.css";
import "./Login.css";

function Login({ setLoggedIn }) {
  const [mode, setMode] = useState("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const isSignUp = mode === "signup";

  const switchMode = (nextMode) => {
    setMode(nextMode);
    setError("");
    setPassword("");
    setConfirmPassword("");
    setShowPassword(false);
  };

  const signIn = async () => {
    const response = await api.post("/api/auth/login", {
      email: email.trim().toLowerCase(),
      password,
    });
    localStorage.setItem("token", response.data.token);
    setLoggedIn(true);
  };

  const signUp = async () => {
    if (password.length < 6) {
      throw { customMessage: "Password must be at least 6 characters." };
    }
    if (password !== confirmPassword) {
      throw { customMessage: "Passwords do not match." };
    }

    await api.post("/api/auth/register", {
      email: email.trim().toLowerCase(),
      password,
    });
    await signIn();
  };

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      if (isSignUp) {
        await signUp();
      } else {
        await signIn();
      }
    } catch (err) {
      if (err?.customMessage) {
        setError(err.customMessage);
      } else if (err?.response?.status === 409) {
        setError("An account with that email already exists.");
      } else if (err?.response?.status === 401) {
        setError("Incorrect email or password. Please try again.");
      } else if (err?.response?.status === 429) {
        setError("Too many attempts. Please wait a moment and try again.");
      } else {
        setError(
          isSignUp
            ? "Could not create your account. Please try again."
            : "Incorrect email or password. Please try again."
        );
      }
    }

    setSubmitting(false);
  };

  return (
    <div className="login-stage">
      <form className="login-card" onSubmit={submit}>
        <span className="login-brand-name">ChatBot</span>

        <h1 className="login-title">
          {isSignUp ? "Create an account" : "Sign in"}
        </h1>
        <p className="login-subtitle">
          {isSignUp
            ? "Get started in a few seconds."
            : "Continue where you left off."}
        </p>

        <hr className="login-divider" />

        <label className="login-field">
          <span>Email</span>
          <input
            className="login-input"
            type="email"
            placeholder="you@example.com"
            value={email}
            required
            autoComplete="email"
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>

        <label className="login-field">
          <span>Password</span>
          <div className="login-password-row">
            <input
              className="login-input"
              type={showPassword ? "text" : "password"}
              placeholder="••••••••"
              value={password}
              required
              autoComplete={isSignUp ? "new-password" : "current-password"}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button
              type="button"
              className="login-password-toggle"
              onClick={() => setShowPassword((prev) => !prev)}
              aria-label={showPassword ? "Hide password" : "Show password"}
            >
              <span className="material-symbols-outlined">
                {showPassword ? "visibility_off" : "visibility"}
              </span>
            </button>
          </div>
        </label>

        {isSignUp && (
          <label className="login-field">
            <span>Confirm password</span>
            <div className="login-password-row">
              <input
                className="login-input"
                type={showPassword ? "text" : "password"}
                placeholder="••••••••"
                value={confirmPassword}
                required
                autoComplete="new-password"
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>
          </label>
        )}

        {error && <p className="login-error">{error}</p>}

        <button className="login-button" type="submit" disabled={submitting}>
          {submitting
            ? isSignUp
              ? "Creating account…"
              : "Signing in…"
            : isSignUp
              ? "Create account"
              : "Sign in"}
        </button>

        <hr className="login-divider login-divider-bottom" />

        <p className="login-switch">
          {isSignUp ? (
            <>
              Already have an account?{" "}
              <button type="button" onClick={() => switchMode("signin")}>
                Sign in
              </button>
            </>
          ) : (
            <>
              New here?{" "}
              <button type="button" onClick={() => switchMode("signup")}>
                Create an account
              </button>
            </>
          )}
        </p>
      </form>
    </div>
  );
}

export default Login;
