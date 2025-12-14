/**
 * Home page with movie list, search, and filters
 */
import { useState, useEffect } from 'react';
import { moviesAPI, genresAPI } from '../services/api';
import MovieCard from '../components/MovieCard';
import Pagination from '../components/Pagination';
import './Home.css';

const Home = () => {
  const [movies, setMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [filters, setFilters] = useState({
    search: '',
    genre: '',
    year: '',
    min_rating: '',
    max_rating: '',
    ordering: '-created_at',
  });

  useEffect(() => {
    loadGenres();
  }, []);

  useEffect(() => {
    loadMovies();
  }, [currentPage, filters]);

  const loadGenres = async () => {
    try {
      const response = await genresAPI.list();
      // Backend uses CustomResponse format: { id, message, data }
      const genresData = response.data?.data || response.data || [];
      setGenres(Array.isArray(genresData) ? genresData : []);
    } catch (error) {
      console.error('Failed to load genres:', error);
      setGenres([]); // Set empty array on error
    }
  };

  const loadMovies = async () => {
    setLoading(true);
    try {
      const params = {
        page: currentPage,
        ordering: filters.ordering,
      };

      if (filters.search) {
        params.search = filters.search;
      }
      if (filters.genre) {
        params.genres = filters.genre;
      }
      if (filters.year) {
        params.release_year = filters.year;
      }
      if (filters.min_rating) {
        params.min_rating = filters.min_rating;
      }
      if (filters.max_rating) {
        params.max_rating = filters.max_rating;
      }

      const response = await moviesAPI.list(params);
      // Backend uses CustomPageNumberPagination: { pagination: {...}, results: [...] }
      const moviesData = response.data?.results || response.data?.data?.results || [];
      const pagination = response.data?.pagination || {};
      setMovies(Array.isArray(moviesData) ? moviesData : []);
      setTotalPages(pagination.total_pages || Math.ceil((pagination.total_items || 0) / 20) || 1);
    } catch (error) {
      console.error('Failed to load movies:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters({ ...filters, [key]: value });
    setCurrentPage(1);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    loadMovies();
  };

  return (
    <div className="home">
      <div className="home-header">
        <h1>Movie Database</h1>
        <p>Discover and explore your favorite movies</p>
      </div>

      <div className="home-filters">
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            placeholder="Search movies, actors, descriptions..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="search-input"
          />
          <button type="submit" className="search-button">
            Search
          </button>
        </form>

        <div className="filters-row">
          <select
            value={filters.genre}
            onChange={(e) => handleFilterChange('genre', e.target.value)}
            className="filter-select"
          >
            <option value="">All Genres</option>
            {Array.isArray(genres) && genres.map((genre) => (
              <option key={genre.id} value={genre.id}>
                {genre.name}
              </option>
            ))}
          </select>

          <input
            type="number"
            placeholder="Year"
            value={filters.year}
            onChange={(e) => handleFilterChange('year', e.target.value)}
            className="filter-input"
            min="1900"
            max="2030"
          />

          <input
            type="number"
            placeholder="Min Rating"
            value={filters.min_rating}
            onChange={(e) => handleFilterChange('min_rating', e.target.value)}
            className="filter-input"
            min="1"
            max="10"
            step="0.1"
          />

          <input
            type="number"
            placeholder="Max Rating"
            value={filters.max_rating}
            onChange={(e) => handleFilterChange('max_rating', e.target.value)}
            className="filter-input"
            min="1"
            max="10"
            step="0.1"
          />

          <select
            value={filters.ordering}
            onChange={(e) => handleFilterChange('ordering', e.target.value)}
            className="filter-select"
          >
            <option value="-created_at">Newest First</option>
            <option value="created_at">Oldest First</option>
            <option value="title">Title A-Z</option>
            <option value="-title">Title Z-A</option>
            <option value="release_year">Year (Oldest)</option>
            <option value="-release_year">Year (Newest)</option>
            <option value="-average_rating">Highest Rated</option>
            <option value="average_rating">Lowest Rated</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="loading">Loading movies...</div>
      ) : movies.length === 0 ? (
        <div className="no-results">No movies found. Try adjusting your filters.</div>
      ) : (
        <>
          <div className="movies-grid">
            {movies.map((movie) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
          {totalPages > 1 && (
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
            />
          )}
        </>
      )}
    </div>
  );
};

export default Home;






