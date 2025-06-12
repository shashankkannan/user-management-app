import { useState } from 'react';
import { updateUser } from '../api/api';
import '../style.css';

export default function UserForm({ userId, onFinish }) {
  const [username, setUsername] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await updateUser(userId, { username });
    onFinish();
  };

  return (
    <form onSubmit={handleSubmit} className="container">
      <h2>Edit Username</h2>
      <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="New Username" required />
      <button type="submit">Update</button>
    </form>
  );
}
