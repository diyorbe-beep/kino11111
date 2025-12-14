/**
 * Admin panel for movie CRUD operations
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { moviesAPI, genresAPI, actorsAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import './AdminPanel.css';

const AdminPanel = () => {
  const { user, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [movies, setMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [actors, setActors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingMovie, setEditingMovie] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    release_year: new Date().getFullYear(),
    poster: null,
    genre_ids: [],
    actor_ids: [],
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    if (!user) {
      // User login qilmagan, admin login sahifasiga yuborish
      navigate('/admin/login');
      return;
    }
    if (!isAdmin()) {
      // User login qilgan, lekin admin emas
      setError('You do not have admin privileges. Please login with an admin account.');
      navigate('/');
      return;
    }
    loadData();
  }, [user, isAdmin, navigate]);

  const loadData = async () => {
    try {
      const [moviesRes, genresRes, actorsRes] = await Promise.all([
        moviesAPI.list({ page_size: 100 }),
        genresAPI.list(),
        actorsAPI.list(),
      ]);
      // Handle CustomResponse format: { id, message, data, results, pagination }
      const moviesData = moviesRes.data?.results || moviesRes.data?.data?.results || moviesRes.data?.data || [];
      const genresData = genresRes.data?.data || genresRes.data || [];
      const actorsData = actorsRes.data?.data || actorsRes.data || [];
      
      setMovies(Array.isArray(moviesData) ? moviesData : []);
      setGenres(Array.isArray(genresData) ? genresData : []);
      setActors(Array.isArray(actorsData) ? actorsData : []);
    } catch (error) {
      console.error('Failed to load data:', error);
      setError('Failed to load data. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, files } = e.target;
    if (type === 'file') {
      setFormData({ ...formData, [name]: files[0] });
    } else if (type === 'checkbox') {
      const id = parseInt(value);
      const currentIds = formData[name];
      if (e.target.checked) {
        setFormData({ ...formData, [name]: [...currentIds, id] });
      } else {
        setFormData({
          ...formData,
          [name]: currentIds.filter((i) => i !== id),
        });
      }
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      if (editingMovie) {
        await moviesAPI.update(editingMovie.id, formData);
        setSuccess('Movie updated successfully!');
      } else {
        await moviesAPI.create(formData);
        setSuccess('Movie created successfully!');
      }
      resetForm();
      loadData();
    } catch (error) {
      // Handle CustomResponse error format: { id, message, errors }
      const errorMessage = error.response?.data?.message || 
                          error.response?.data?.detail ||
                          (error.response?.data?.errors ? JSON.stringify(error.response.data.errors) : null) ||
                          JSON.stringify(error.response?.data) ||
                          'Operation failed';
      setError(errorMessage);
    }
  };

  const handleEdit = (movie) => {
    setEditingMovie(movie);
    setFormData({
      title: movie.title,
      description: movie.description,
      release_year: movie.release_year,
      poster: null,
      genre_ids: movie.genres?.map((g) => g.id) || [],
      actor_ids: movie.actors?.map((a) => a.id) || [],
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this movie?')) {
      return;
    }

    try {
      await moviesAPI.delete(id);
      setSuccess('Movie deleted successfully!');
      loadData();
    } catch (error) {
      setError('Failed to delete movie');
    }
  };

  const resetForm = () => {
    setEditingMovie(null);
    setFormData({
      title: '',
      description: '',
      release_year: new Date().getFullYear(),
      poster: null,
      genre_ids: [],
      actor_ids: [],
    });
  };

  const handleCSVImport = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      await moviesAPI.importCSV(file);
      setSuccess('Movies imported successfully!');
      loadData();
    } catch (error) {
      setError('Failed to import CSV');
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="admin-panel">
      <h1>Admin Panel - Movie Management</h1>

      <div className="admin-actions">
        <label className="csv-import-button">
          Import CSV
          <input
            type="file"
            accept=".csv"
            onChange={handleCSVImport}
            style={{ display: 'none' }}
          />
        </label>
      </div>

      <form onSubmit={handleSubmit} className="admin-form">
        <h2>{editingMovie ? 'Edit Movie' : 'Create New Movie'}</h2>
        {error && <div className="form-error">{error}</div>}
        {success && <div className="form-success">{success}</div>}

        <div className="form-group">
          <label htmlFor="title">Title *</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description *</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            rows="4"
            required
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="release_year">Release Year *</label>
            <input
              type="number"
              id="release_year"
              name="release_year"
              value={formData.release_year}
              onChange={handleInputChange}
              min="1900"
              max="2030"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="poster">Poster Image</label>
            <input
              type="file"
              id="poster"
              name="poster"
              accept="image/*"
              onChange={handleInputChange}
            />
          </div>
        </div>

        <div className="form-group">
          <label>Genres</label>
          <div className="checkbox-group">
            {genres.map((genre) => (
              <label key={genre.id} className="checkbox-label">
                <input
                  type="checkbox"
                  name="genre_ids"
                  value={genre.id}
                  checked={formData.genre_ids.includes(genre.id)}
                  onChange={handleInputChange}
                />
                {genre.name}
              </label>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>Actors</label>
          <div className="checkbox-group">
            {actors.map((actor) => (
              <label key={actor.id} className="checkbox-label">
                <input
                  type="checkbox"
                  name="actor_ids"
                  value={actor.id}
                  checked={formData.actor_ids.includes(actor.id)}
                  onChange={handleInputChange}
                />
                {actor.name}
              </label>
            ))}
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="form-button">
            {editingMovie ? 'Update Movie' : 'Create Movie'}
          </button>
          {editingMovie && (
            <button
              type="button"
              onClick={resetForm}
              className="form-button-secondary"
            >
              Cancel
            </button>
          )}
        </div>
      </form>

      <div className="movies-list">
        <h2>All Movies ({movies.length})</h2>
        <div className="movies-table">
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Year</th>
                <th>Genres</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {movies.map((movie) => (
                <tr key={movie.id}>
                  <td>{movie.title}</td>
                  <td>{movie.release_year}</td>
                  <td>
                    {movie.genres?.map((g) => g.name).join(', ') || 'None'}
                  </td>
                  <td>
                    <button
                      onClick={() => handleEdit(movie)}
                      className="action-button edit"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(movie.id)}
                      className="action-button delete"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;








