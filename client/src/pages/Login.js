import { useState } from "react";
import axios from "axios";

export default function Login() {
  const [username, setUsername] = useState("root");
  const [password, setPassword] = useState("Rajeshj");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = (e) => {
    setLoading(true);
    setError(null);
    e.preventDefault();
    console.log(username, password);

    axios({
      url: "http://127.0.0.1:8000/auth/token/",
      method: "POST",
      data: {
        username,
        password,
      },
    })
      .then((res) => {
        setLoading(false);
        console.log(res.data);
      })
      .catch((err) => {
        err = JSON.parse(err.request.response);
        setLoading(false);
        console.log(err.detail);
        setError(err.detail);
      });
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error ? <p style={{ color: "red" }}>{error}</p> : null}

        <button disabled={loading} type="submit">
          Login
        </button>
      </form>
    </div>
  );
}
