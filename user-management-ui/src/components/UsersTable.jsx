import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUsers, deleteUser } from '../api/api';
import UserForm from './UserForm';
import '../style.css';

export default function UsersTable() {
  const [users, setUsers] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const userId = localStorage.getItem('user_id');
  const navigate = useNavigate();

  const fetchUsers = async () => {
    const res = await getUsers();
    setUsers(res.data);
  };

  const handleDelete = async (id) => {
    if (id.toString() !== userId) {
      alert('You can only delete your own account.');
      return;
    }

    try {
      await deleteUser(id);
      localStorage.removeItem('token');
      localStorage.removeItem('user_id');
      setTimeout(()=>{
        navigate('/');
      }, 100);
      
    } catch (error) {
      console.error('Error deleting user:', error);
      alert('Something went wrong while deleting the account.');
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/');
      return;
    }
    fetchUsers();
  }, []);

  return (
    <div className="table-container">
      <h2>All Users</h2>
      <button onClick={()=>{
        localStorage.clear();
        navigate('/');
      }}>Logout</button>
      <table>
        <thead>
          <tr>
            <th>ID</th><th>Username</th><th>Email</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.username}</td>
              <td>{u.email}</td>
              <td className="actions">
                {u.id.toString() === userId && (
                  <>
                    <button onClick={() => setEditingId(u.id)}>Edit</button>
                    <button onClick={() => handleDelete(u.id)}>Delete</button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {editingId && <UserForm userId={editingId} onFinish={() => { setEditingId(null); fetchUsers(); }} />}
    </div>
  );
}
